
from typing import Any

from polls.models import Question
from common.utils.constraints import get_unique_constraint_fields
from polls.services.answer_options import AnswerOptionServices


class QuestionServices:

    @staticmethod
    def bulk_create_questions(
        user,
        questions_data: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:

        if not questions_data:
            return []

        # 1. Prepare question objects from the normalized payload.
        question_objs = [
            Question(
                created_by=user,
                name=question_data['name'],
                description=question_data['description'],
            )
            for question_data in questions_data
        ]

        # 2. Bulk upsert questions.
        Question.objects.bulk_create(
            question_objs,
            update_conflicts=True,
            unique_fields=get_unique_constraint_fields(
                Question,
                'unique_question_per_user',
            ),
            update_fields=['description'],
        )

        # 3. Retrieve the saved questions.
        question_names = [
            question_data['name']
            for question_data in questions_data
        ]

        questions_qs = Question.objects.filter(
            created_by=user,
            name__in=question_names,
        )

        # CHANGED: Explicitly declare the model type for PyCharm.
        question_map: dict[str, Question] = {
            question.name: question
            for question in questions_qs
        }

        # 4. Build one payload containing options for all questions.
        options_payload: list[dict[str, Any]] = []

        for question_data in questions_data:
            question = question_map[question_data['name']]

            for option_data in question_data['options']:
                options_payload.append({
                    'question_id': question.pk,
                    'name': option_data['name'],
                    'order': option_data['order'],
                })

        # 5. Bulk-upsert all answer options in one service call.
        options_result = AnswerOptionServices.bulk_create_options(
            options_payload=options_payload,
        )

        # 6. Group answer options by their question ID.
        options_by_question: dict[int, list[dict[str, Any]]] = {}

        for option_result in options_result:
            question_id = option_result['question_id']

            options_by_question.setdefault(
                question_id, []
            ).append({
                'name': option_result['name'],
                'order': option_result['order'],
            })

        # 7. Return questions with their relevant answer options.
        created_questions: list[dict[str, Any]] = []

        for question_data in questions_data:
            question = question_map[question_data['name']]

            question_options = options_by_question.get(
                question.pk, []
            )

            question_options.sort(
                key=lambda option_data: option_data['order']
            )

            created_questions.append({
                'id': question.pk,
                'name': question.name,
                'description': question.description,
                'options': question_options,
            })

        return created_questions

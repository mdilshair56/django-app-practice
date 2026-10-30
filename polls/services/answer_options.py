
from polls.models import AnswerOption
from common.utils.constraints import get_unique_constraint_fields


class AnswerOptionServices:

    @staticmethod
    def bulk_create_options(options_payload=None):
        if not options_payload:
            return []

        # 1. Prepare all answer-option objects.
        option_objs = [
            AnswerOption(
                question_id=option_data['question_id'],
                name=option_data['name'],
                order=option_data['order'],
            )
            for option_data in options_payload
        ]

        # 2. Bulk upsert all options for all questions.
        AnswerOption.objects.bulk_create(
            option_objs,
            update_conflicts=True,
            unique_fields=get_unique_constraint_fields(
                AnswerOption,
                'unique_option_per_question',
            ),
            update_fields=['order'],
        )

        # 3. Retrieve only the requested question-option pairs.
        requested_pairs = {
            (option['question_id'], option['name'])
            for option in options_payload
        }

        question_ids = {
            option['question_id']
            for option in options_payload
        }

        option_names = {
            option['name']
            for option in options_payload
        }

        options_qs = AnswerOption.objects.filter(
            question_id__in=question_ids,
            name__in=option_names,
        ).values(
            'question_id',
            'name',
            'order',
        )

        return [
            option
            for option in options_qs
            if (
                option['question_id'],
                option['name'],
            ) in requested_pairs
        ]

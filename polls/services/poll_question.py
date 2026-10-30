from polls.models import PollQuestion, Question
from polls.services.question import QuestionServices


class PollQuestionServices:

    @staticmethod
    def bulk_upsert_poll_questions(poll_id, user, questions_data=None):

        if not questions_data:
            return PollQuestion.objects.none()

        # Create or update questions and their supplied options
        QuestionServices.bulk_create_questions(
            user=user,
            questions_data=questions_data,
        )

        # Retrieve questions belonging to this user
        names = list(dict.fromkeys(                     #Removes Duplicate names
            q_dict["name"].strip().lower()
            for q_dict in questions_data
            if (
                isinstance(q_dict, dict)
                and isinstance(q_dict.get("name"), str)
                and q_dict["name"].strip()
            )
        ))

        if not names:
            return PollQuestion.objects.none()

        questions_qs = Question.objects.filter(
            created_by=user,
            name__in=names,
        )

        question_ids = list(
            questions_qs.values_list("id", flat=True)
        )

        if not question_ids:
            return PollQuestion.objects.none()

        # Poll-Question relationships | List Comprehension
        poll_question_objs = [
            PollQuestion(
                poll_id=poll_id,
                question_id=question_id,
            )
            for question_id in question_ids
        ]

        PollQuestion.objects.bulk_create(
            poll_question_objs,
            ignore_conflicts=True,
        )

        return PollQuestion.objects.filter(
            poll_id=poll_id,
            question_id__in=question_ids,
        ).select_related("question")
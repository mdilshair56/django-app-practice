from django.db import transaction
from common.exceptions import APIValidationError
#from polls.utils.constraints import get_unique_constraint_fields
from polls.models import Vote, PollQuestion, AnswerOption


class VoteServices:

    @staticmethod
    @transaction.atomic
    def cast_vote(*, user, poll_question_id, answer_option_id):

        # 1. Get the question as it exists within a particular poll.
        try:
            poll_question = PollQuestion.objects.select_related(
                'poll', 'question'
            ).get(pk=poll_question_id)
        except PollQuestion.DoesNotExist:
            raise APIValidationError({
                'poll_question_id': 'This question does not exist in the poll.'
            })

        # 2. Get the selected answer option.
        try:
            answer_option = AnswerOption.objects.get(
                pk=answer_option_id
            )
        except AnswerOption.DoesNotExist:
            raise APIValidationError({
                'answer_option_id': 'This answer option does not exist.'
            })

        # 3. Ensure the answer belongs to this question.
        if answer_option.question_id != poll_question.question_id:
            raise APIValidationError({
                'answer_option_id': (
                    'This answer option does not belong to the selected question.'
                )
            })

        # 4. Update the existing vote or create a new one.
        vote, created = Vote.objects.update_or_create(
            user=user,
            poll_question=poll_question,
            defaults={
                'answer': answer_option,
            }
        )

        # Vote.objects.bulk_create(
        #     [
        #         Vote(
        #             user=user,
        #             poll_question=poll_question,
        #             answer=answer_option,
        #         )
        #     ],
        #     update_conflicts=True,
        #     unique_fields=get_unique_constraint_fields(
        #         Vote,
        #         "unique_user_vote_per_question"
        #     ),
        #     update_fields=['answer'],
        # )
        #
        # vote = Vote.objects.get(
        #     user=user,
        #     poll_question=poll_question,
        # )

        return vote, created

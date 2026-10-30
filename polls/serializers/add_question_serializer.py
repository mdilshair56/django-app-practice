from rest_framework import serializers
from django.db import transaction
from polls.models.question import Question
from polls.models.poll_question import PollQuestion
# from polls.services.question import QuestionServices
from polls.services.answer_options import AnswerOptionServices


class OptionInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    order = serializers.IntegerField()

class AddQuestionToPollSerializer(serializers.Serializer):
    question_name = serializers.CharField(max_length=255)
    order = serializers.IntegerField(help_text="Position of the question in this poll")
    options = OptionInputSerializer(many=True)

    @transaction.atomic
    def save(self, poll, user, questions_data=None):
        question = Question.objects.create(
            name=self.validated_data['question_name'],
            created_by=user
        )

        options_data = self.validated_data['options']
        if options_data:
            AnswerOptionServices.bulk_create_options(
                questions_data=questions_data, #UPDATED
                options_data=options_data
            )


        PollQuestion.objects.create(
            poll=poll,
            question=question,
            order=self.validated_data['order']
        )

        return question
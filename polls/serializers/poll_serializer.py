from rest_framework import serializers
from polls.models.poll import Poll
from polls.models.answer_option import AnswerOption
from polls.models.vote import Vote
from polls.models.poll_question import PollQuestion


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'name', 'order']


class PollQuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(source='question.answer_options', many=True, read_only=True)
    question_name = serializers.CharField(source='question.name', read_only=True)

    class Meta:
        model = PollQuestion
        fields = ['id', 'question', 'question_name', 'order', 'options']


class PollDetailSerializer(serializers.ModelSerializer):
    questions = PollQuestionSerializer(source='poll_questions', many=True, read_only=True)
    created_by = serializers.SerializerMethodField()

    # Formats timestamps into readable strings (e.g., "Oct 27, 2026, 02:00 PM")
    starts_at = serializers.DateTimeField(format="%b %d, %Y, %I:%M %p", required=False)
    ends_at = serializers.DateTimeField(format="%b %d, %Y, %I:%M %p", required=False)

    class Meta:
        model = Poll
        fields = [
            'id',
            'name',
            'description',
            'status',
            'result_visibility',
            'created_by',
            'starts_at',
            'ends_at',
            'questions'
        ]
        read_only_fields = ['created_by']

    @staticmethod
    def get_created_by(obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return None


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'poll_question', 'answer']

    def validate(self, attrs, *args, **kwargs):
        user = self.context['request'].user
        poll_question = attrs['poll_question']

        if Vote.objects.filter(user=user, poll_question=poll_question).exists():
            raise serializers.ValidationError("You have already voted on this question.")
        return attrs
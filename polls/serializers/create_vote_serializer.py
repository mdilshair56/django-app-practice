from rest_framework import serializers
from polls.models.vote import Vote

class CreateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['poll_question', 'answer']

    def validate(self, attrs):
        user = self.context['request'].user
        poll_question = attrs['poll_question']
        answer = attrs['answer']

        # Prevent duplicate voting
        if Vote.objects.filter(user=user, poll_question=poll_question).exists():
            raise serializers.ValidationError("You have already voted on this question.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return Vote.objects.create(user=user, **validated_data)
from django.db import models


class PollQuestion(models.Model):
    poll = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE,
        related_name='poll_questions'
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='poll_questions'
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['poll', 'question'],
                name='unique_poll_question'
            ),
        ]

    def __str__(self):
        p_id = self.poll.id if self.poll else "No Poll"
        q_id = self.question.id if self.question else "New"

        return f"Poll ID: {p_id} | Question ID: {q_id} (Order: {self.order})"
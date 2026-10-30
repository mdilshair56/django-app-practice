from django.contrib import admin
from polls.models.poll import Poll
from polls.models.question import Question
from polls.models.answer_option import AnswerOption
from polls.models.poll_question import PollQuestion
from polls.models.vote import Vote

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'result_visibility', 'created_by', 'starts_at', 'ends_at')
    list_filter = ('status', 'result_visibility')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name',)

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'question', 'order')
    list_filter = ('question',)
    search_fields = ('name',)
    ordering = ('question', 'order')

@admin.register(PollQuestion)
class PollQuestionAdmin(admin.ModelAdmin):
    list_display = ('poll', 'question', 'order')
    list_filter = ('poll',)
    ordering = ('poll', 'order')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'poll_question', 'answer', 'created_at')
    list_filter = ('poll_question__poll', 'created_at')
    search_fields = ('user__username', 'user__email')
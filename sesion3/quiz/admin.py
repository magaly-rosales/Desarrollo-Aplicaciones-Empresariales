from django.contrib import admin
from .models import Exam, Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    can_delete = False


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam', 'text_preview')
    list_filter = ('exam',)
    inlines = [ChoiceInline]

    def text_preview(self, obj):
        return obj.text[:80]
    text_preview.short_description = 'Question Text'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'text', 'is_correct')
    list_filter = ('is_correct', 'question__exam')
    search_fields = ('text', 'question__text')

    def question_text(self, obj):
        return obj.question.text[:60]
    question_text.short_description = 'Question'

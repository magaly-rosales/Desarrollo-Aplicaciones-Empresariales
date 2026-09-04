from django import forms
from django.forms import inlineformset_factory
from .models import Exam, Question, Choice


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']


ChoiceFormSet = inlineformset_factory(
    parent_model=Question,
    model=Choice,
    fields=['text', 'is_correct'],
    extra=3,
    can_delete=False,
)

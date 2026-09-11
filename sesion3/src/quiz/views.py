from django.shortcuts import render, get_object_or_404, redirect
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceFormSet


def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'quiz/exam_list.html', {'exams': exams})


def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    questions = exam.questions.all()
    return render(request, 'quiz/exam_detail.html', {
        'exam': exam,
        'questions': questions,
    })


def question_add(request, pk):
    exam = get_object_or_404(Exam, pk=pk)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)

        if question_form.is_valid() and choice_formset.is_valid():
            instances = choice_formset.save(commit=False)
            correct_count = sum(1 for i in instances if i.is_correct)

            if correct_count != 1:
                question_form.add_error(
                    None, 'Exactly one choice must be marked as correct.'
                )
            else:
                question = question_form.save(commit=False)
                question.exam = exam
                question.save()
                for instance in instances:
                    instance.question = question
                    instance.save()
                return redirect('quiz:exam_detail', pk=exam.pk)
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet()

    return render(request, 'quiz/question_add.html', {
        'exam': exam,
        'question_form': question_form,
        'choice_formset': choice_formset,
    })

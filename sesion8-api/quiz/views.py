from django.db.models import Count
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import filters, viewsets

from .models import Choice, Exam, Question
from .serializers import ChoiceDetailSerializer, ChoiceSerializer, ExamSerializer, QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceDetailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["text"]

    def get_queryset(self):
        return Choice.objects.select_related("question").order_by("id")


class ExamViewSet(viewsets.ModelViewSet):
    serializer_class = ExamSerializer
    queryset = Exam.objects.annotate(question_count=Count("questions")).order_by("id")


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("exam", int, description="Solo las preguntas de este examen."),
        ]
    )
)
class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["text"]

    def get_queryset(self):
        queryset = Question.objects.select_related("exam").prefetch_related("choices")
        exam = self.request.query_params.get("exam")
        if exam and exam.isdigit():
            queryset = queryset.filter(exam_id=int(exam))
        return queryset

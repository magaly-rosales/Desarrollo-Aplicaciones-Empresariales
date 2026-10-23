from django.db import transaction
from rest_framework import serializers

from .models import Choice, Exam, Question


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "text", "is_correct"]


class ChoiceDetailSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

    class Meta:
        model = Choice
        fields = ["id", "question", "text", "is_correct"]
        read_only_fields = ["id"]

    def validate(self, data):
        choice = data.get("is_correct", self.instance.is_correct if self.instance else False)
        question = data.get("question", self.instance.question if self.instance else None)
        if not question:
            return data
        if choice:
            existing_correct = Choice.objects.filter(question=question, is_correct=True).exclude(
                id=self.instance.id if self.instance else 0
            )
            if existing_correct.exists():
                raise serializers.ValidationError(
                    "Ya existe una opción correcta para esta pregunta. Al marcar esta como correcta, la anterior dejará de serlo."
                )
        return data


class ExamSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Exam
        fields = ["id", "title", "created_at", "question_count"]
        read_only_fields = ["created_at"]


class QuestionSerializer(serializers.ModelSerializer):
    # Choices travel nested inside the question; the exam travels as an identifier.
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "exam", "text", "choices", "created_at"]
        read_only_fields = ["created_at"]

    def validate_choices(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Una pregunta necesita al menos dos opciones.")
        if sum(1 for choice in value if choice.get("is_correct")) != 1:
            raise serializers.ValidationError("Debe haber exactamente una opción correcta.")
        return value

    def create(self, validated_data):
        choices = validated_data.pop("choices")
        with transaction.atomic():
            question = Question.objects.create(**validated_data)
            Choice.objects.bulk_create(Choice(question=question, **choice) for choice in choices)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop("choices", None)
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if choices is not None:  # sent choices replace the old ones
                instance.choices.all().delete()
                Choice.objects.bulk_create(Choice(question=instance, **choice) for choice in choices)
        return instance

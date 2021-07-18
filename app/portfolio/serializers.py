from django.contrib.auth import get_user_model

from rest_framework import serializers

from portfolio.models import Portfolio, Section, Category, Task, WorkItem
from user.serializers import UserSerializer


User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'duration',
            'completion_days',
            'created',
            'created_by',
            'archived',
        )
        read_only_fields = ('created', )

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        return task

    def to_representation(self, instance):
        data = super(TaskSerializer, self).to_representation(instance)
        data['created_by'] = UserSerializer(instance=instance.created_by).data
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'description',
            'created',
            'created_by',
            'archived',
        )
        read_only_fields = ('created', )

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

    def to_representation(self, instance):
        data = super(CategorySerializer, self).to_representation(instance)
        data['created_by'] = UserSerializer(instance=instance.created_by).data
        return data


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'section_id',
            'order',
            'portfolio',
            'category',
            'created',
            'created_by',
            'meta',
            'completed',
            'workitems',
        )
        read_only_fields = ('id', 'section_id', 'created', )

    def to_representation(self, instance):
        data = super(SectionSerializer, self).to_representation(instance)
        data['created_by'] = UserSerializer(instance=instance.created_by).data
        data['category'] = CategorySerializer(instance=instance.category).data
        return data


class WorkItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkItem
        fields = (
            'id',
            'workitem_id',
            'order',
            'section',
            'task',
            'created',
            'created_by',
            'meta',
            'completed',
            'assigned_to',
        )

        read_only_fields = ('id', 'workitem_id', 'created', )

    def to_representation(self, instance):
        data = super(WorkItemSerializer, self).to_representation(instance)
        data['created_by'] = UserSerializer(instance=instance.created_by).data
        data['assigned_to'] = UserSerializer(instance=instance.assigned_to).data
        data['task'] = TaskSerializer(instance=instance.task).data
        data['section'] = SectionSerializer(instance=instance.section).data
        return data


class PortfolioSerializer(serializers.ModelSerializer):
    """Serializer for portfolio objects"""
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'portfolio_id', 'reference', 'sections', 'created', 'created_by', 'meta', 'completed', ]
        read_only_fields = ['id', 'portfolio_id', 'created', ]

    def to_representation(self, instance):
        data = super(PortfolioSerializer, self).to_representation(instance)
        data['created_by'] = UserSerializer(instance=instance.created_by).data
        return data

    def create(self, validated_data):
        portfolio = Portfolio.objects.create(**validated_data)
        return portfolio

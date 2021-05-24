from rest_framework import serializers

from portfolio.models import Portfolio, Section, SectionCategory, Task, WorkItem
from user.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'duration',
            'created',
            'created_by',
            'archived',
        )
        read_only_fields = ('created', 'created_by')


class SectionCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SectionCategory
        fields = (
            'title',
            'description',
            'created',
            'created_by',
            'archived',
        )
        read_only_fields = ('created', 'created_by')


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = (
            'id',
            'section_id',
            'portfolio',
            'category',
            'created',
            'created_by',
            'meta',
            'completed',
            'workitems',
        )
        read_only_fields = ('id', 'section_id', 'created', 'created_by', )

    def to_representation(self, instance):
        data = super(SectionSerializer, self).to_representation(instance)
        data['created_by'] = UserSerializer(instance=instance.created_by).data
        return data


class WorkItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkItem
        fields = (
            'id',
            'workitem_id',
            'section',
            'task',
            'created',
            'created_by',
            'meta',
            'completed',
            'assigned_to',
        )

        read_only_fields = ('id', 'workitem_id', 'created', 'created_by', )

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
        read_only_fields = ['id', 'portfolio_id', 'created', 'created_by', ]

    def to_representation(self, instance):
        data = super(PortfolioSerializer, self).to_representation(instance)
        data['created_by'] = UserSerializer(instance=instance.created_by).data
        return data

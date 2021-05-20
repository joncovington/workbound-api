from rest_framework import serializers

from portfolio.models import Portfolio, Section
from user.serializers import UserSerializer


class SectionSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False)
    created = serializers.DateTimeField()
    completed = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Section
        fields = [
            'id',
            'section_id',
            'portfolio',
            'category',
            'created',
            'created_by',
            'meta',
            'completed',
        ]
        read_only_fields = ['id', 'section_id', 'created', 'created_by', ]


class PortfolioSerializer(serializers.ModelSerializer):
    """Serializer for portfolio objects"""
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'portfolio_id', 'reference', 'sections', 'created', 'created_by', 'meta', 'completed', ]
        read_only_fields = ['id', 'portfolio_id', 'created', 'created_by', ]

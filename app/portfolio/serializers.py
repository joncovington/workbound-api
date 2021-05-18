from rest_framework import serializers

from portfolio.models import Portfolio


class PortfolioSerializer(serializers.ModelSerializer):
    """Serializer for portfolio objects"""
    sections = serializers.StringRelatedField(many=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'reference', 'meta', 'sections']
        read_only_fields = ['id', ]

from rest_framework import serializers

from portfolio.models import Portfolio


class PortfolioSerializer(serializers.ModelSerializer):
    """Serializer for portfolio objects"""

    class Meta:
        model = Portfolio
        fields = ['id', 'reference', ]
        read_only_fields = ['id', ]

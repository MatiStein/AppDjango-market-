from market.models import Stock, IrregularStocksDates
from rest_framework import serializers


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = "__all__"


class IrregularStocksDatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = IrregularStocksDates
        fields = "__all__"

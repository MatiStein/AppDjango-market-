from market.models import Stock, IrregularStocksDates, StockList, UserStock
from rest_framework import serializers


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = "__all__"


class IrregularStocksDatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = IrregularStocksDates
        fields = "__all__"


class StockListSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockList
        fields = "__all__"


class UserStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStock
        fields = "__all__"


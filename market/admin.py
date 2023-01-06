from django.contrib import admin
from market.models import *

admin.site.register(Stock)
admin.site.register(IrregularStocksDates)
admin.site.register(StockList)
admin.site.register(UserStock)

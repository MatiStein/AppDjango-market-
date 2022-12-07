from django.db.models import Avg, F, RowRange, Window
from market.models import Stock
import numpy as np


def moving_ave():

    for vol in windows(60, 'time'):
        items = Stock.objects.annotate(
        avg=Window(
        expression=Avg('volume'),
        frame=RowRange(start=0, end=60)
    )
)


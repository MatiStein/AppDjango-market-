from django.db import models
from django.contrib.auth.models import User



# Data by 'ticker'

class Stock(models.Model):
    ticker = models.CharField(max_length=8)
    volume = models.DecimalField(max_digits=24 ,decimal_places=6)
    volume_weighted = models.DecimalField(max_digits=24 ,decimal_places=6)
    open_price = models.DecimalField(max_digits=16, decimal_places=6)
    close_price = models.DecimalField(max_digits=20, decimal_places=6)  
    highest_price = models.DecimalField(max_digits=16, decimal_places=6) 
    lowest_price = models.DecimalField(max_digits=16, decimal_places=6)
    time = models.DateTimeField() 
    num_transactions = models.IntegerField()

    class Meta:
        unique_together = [['ticker', 'time']]
    
    def __str__(self) -> str:
        return f"{self.ticker}, {self.open_price} To {self.close_price} & V {self.volume}"



# Data analyzed by 'ticker' of views.analyze_volume_data():

class IrregularStocksDates(models.Model): 
    ticker = models.CharField(max_length=24)
    volume = models.DecimalField(max_digits=24, decimal_places=6)
    avg_volume = models.DecimalField(max_digits=24, decimal_places=6)
    dev_volume = models.DecimalField(max_digits=15, decimal_places=6, null = True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null = True)
    time = models.DateTimeField(null=True)

    class Meta:
        unique_together = [['ticker', 'time']]

    def __str__(self) -> str:
        return f"{self.ticker} is {self.volume} & {self.rating} at {self.time}"



# List of all 'tickers' in the DB.

class StockList(models.Model):
    ticker = models.CharField(max_length=8)

    class Meta:
        unique_together = [['ticker']]

    def __str__(self) -> str:
        return f"{self.ticker}"




# List of 'tickers' associated with 'user'

class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(StockList, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['user','stock']]

    def __str__(self) -> str:
        return f"{self.user}, {self.stock}"

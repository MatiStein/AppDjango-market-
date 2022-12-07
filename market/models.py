from django.db import models

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
    
    def __str__(self):
        return f"{self.ticker}, {self.close_price}, {self.volume}"



class IrregularStocksDates(models.Model):
    ticker = models.CharField(max_length=24)
    volume = models.DecimalField(max_digits=24 ,decimal_places=6)
    avg_volume = models.DecimalField(max_digits=24,decimal_places=6)
    time = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.ticker} with {self.volume} at {self.time}"



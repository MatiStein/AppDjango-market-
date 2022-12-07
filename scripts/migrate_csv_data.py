import csv
import datetime
from market.models import Stock



with open('data\AAPL.csv') as file:
    csv_reader = csv.reader(file)
    for index,row in enumerate(csv_reader):

        if index != 0:
            
            print(datetime.datetime.fromtimestamp(int(row[7][0:10])))
            Stock.objects.create(
                ticker = file.name.split('.')[0],
                volume = row[1],
                volume_weighted = row [2],
                open_price = row[3],
                close_price = row [4],
                high_price = row [5],
                low_price = row [6],
                time = datetime.datetime.fromtimestamp(row[7]),
                num_transactions = row [8]
            )

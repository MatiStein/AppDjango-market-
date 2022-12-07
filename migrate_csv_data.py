import csv
import datetime
import os
import django
from market.models import Stock
from django.http import HttpRequest
from urllib import request
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'App.settings')
django.setup()


path_of_directory = 'data'
for ind, file_name in enumerate(os.listdir(path_of_directory)):
    print(file_name, ind)

    if (file_name.split('.')[1] == 'csv' and ind >= 28):
        with open('data\\' + file_name) as file:
            csv_reader = csv.reader(file)
            for index, row in enumerate(csv_reader):

                if index != 0:

                    print(datetime.datetime.fromtimestamp(int(row[7][0:10])))
                    print(file.name.replace('data\\', '').split('.')[0])
                    try:
                        Stock.objects.create(
                            ticker=file.name.replace(
                                'data\\', '').split('.')[0],
                            volume=row[1],
                            volume_weighted=row[2],
                            open_price=row[3],
                            close_price=row[4],
                            highest_price=row[5],
                            lowest_price=row[6],
                            time=datetime.datetime.fromtimestamp(
                                int(row[7][0:10])),
                            num_transactions=row[8]
                        )
                        print(file.name.replace(
                            'data\\', '').split('.')[0], 'Inserted')
                    except Exception as error:
                        print(f'Was an ${error}')

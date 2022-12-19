from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from market.models import (Stock, IrregularStocksDates)
from market.serializers import (StockSerializer, IrregularStocksDatesSerializer)
from datetime import (datetime, date, timedelta)
from django.db.models import Avg
from django.db.models.aggregates import StdDev
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


# View of data by 'ticker'
@api_view(['GET', 'POST'])
def stocks_list(requests):
    if requests.method == "GET":
        ticker = requests.GET.get('ticker', '')
        from_date = requests.GET.get('from_date', '01-01-1970')
        to_date = requests.GET.get('to_date', '01-01-2030')

        from_date_object = datetime.strptime(from_date, '%d-%m-%Y')
        to_date_object = datetime.strptime(to_date, '%d-%m-%Y')

        if from_date_object > to_date_object:
            return Response('The from date can not be bigger than to date', status=status.HTTP_400_BAD_REQUEST)

        if ticker == '' and from_date == '01-01-1970' and to_date == '01-01-2030':
            return Response('You can not query all data from data base, please select certain ticker or dates',
                            status=status.HTTP_400_BAD_REQUEST)

        filtered_stocks = Stock.objects.filter(
            ticker__icontains=ticker, time__gte=from_date_object, time__lte=to_date_object).order_by("-time")
        serializer = StockSerializer(filtered_stocks, many=True)
        return Response(serializer.data)


# View of analyzed by 'ticker'
@api_view(['GET', 'POST'])
def Stock_Analyze(requests):
    if requests.method == "GET":
        ticker = requests.GET.get('ticker', '')
        from_date = requests.GET.get('from_date', '01-01-1970')
        to_date = requests.GET.get('to_date', '01-01-2030')

        from_date_object = datetime.strptime(from_date, '%d-%m-%Y')
        to_date_object = datetime.strptime(to_date, '%d-%m-%Y')

        if from_date_object > to_date_object:
            return Response('The from date can not be bigger than to date', status=status.HTTP_400_BAD_REQUEST)

        if ticker == '' and from_date == '01-01-1970' and to_date == '01-01-2030':
            return Response('You can not query all data from data base, please select certain ticker or dates',
                            status=status.HTTP_400_BAD_REQUEST)

        analyzed_stocks = IrregularStocksDates.objects.filter(
            ticker=ticker, time__gte=from_date_object, time__lte=to_date_object).order_by("-time")
        serializer = IrregularStocksDatesSerializer(analyzed_stocks, many=True)
        return Response(serializer.data)


# Import new 'ticker' to system.
@api_view(["GET"])
def get_data(request):
    if request.method == "GET":
        ticker = request.GET.get('ticker', '')
        print(ticker)
        current_date = date.today()
        start_date = current_date - timedelta(days=729)

        current_date_string = current_date.strftime("%Y-%m-%d")
        start_date_string = start_date.strftime("%Y-%m-%d")

        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date_string}/{current_date_string}?adjusted=true&sort=asc&limit=500000&apiKey=nyd1QVoAqt4QVkHYYMqe_5kvFfN40G8D"
        response = requests.get(url)
        data = response.json()

        for data_row in data["results"]:
            print(data_row["t"])
            ticker_timestamp = str(data_row['t'])
            corrected_timestamp = ticker_timestamp[0:10]
            Stock.objects.create(
                ticker=data["ticker"],
                volume=data_row["v"],
                volume_weighted=data_row['vw'],
                open_price=data_row['o'],
                close_price=data_row['c'],
                highest_price=data_row['h'],
                lowest_price=data_row['l'],
                time=datetime.fromtimestamp(int(corrected_timestamp)),
                num_transactions=data_row['n']
            )
        return Response(f"A new ticker was collected {ticker} ")

# @api_view(['GET', 'POST'])
# def analyze_volume_by_request(request):
#   query  = requests.get('ticker', 'multiplier', 'start_date', 'end_date')
    # from_date = requests.get('start_date', '%d-%m-%Y', blank=Today())
    # to_date = requests.get('end_date', '%d-%m-%Y')
#     multiplier = default(2.3263)
#     ticker_unique = Stock.objects.order_by().values_list("ticker").distinct()

#     for ticker in ticker_unique:
#         ticker = ticker[0]
#         amount_of_rows_per_stock = Stock.objects.filter(ticker=ticker).count()

        #         for period in range(amount_of_rows_per_stock//40):
        #             offset = 40*period
        #             limit = 40*(period+1)
        #             print(f'From {offset} to {limit}')
#             filtered_ticker = Stock.objects.filter(
#                   ticker, from_date, to_date).order_by("-time")
#             avg_volume = filtered_ticker.aggregate(Avg("volume"))[
#                 "volume__avg"]
#             print("The Average is: ", avg_volume)
#             value_to_check = float(avg_volume) * float(multiplier)
#             data_to_response = Stock.objects.filter(
#                 volume__gte=value_to_check,ticker__icontains=ticker).order_by("-time")

#             for row in data_to_response:
#                 already_existed = IrregularStocksDates.objects.filter(ticker=ticker,time=row.time)
#                 if already_existed:
#                     continue
#                 IrregularStocksDates.objects.create(
#                     ticker=ticker,
#                     volume=row.volume,
#                     avg_volume=avg_volume,
#                     time=row.time
#                 )
#                 print("ADDED IRREGULAR ROW TO ", ticker)
#     return print("Done analyzing the data")


# Update 'Stock' by 'ticker', since last known entry in the DB.
def get_latest_data():
    current_date = datetime.now()
    print("Started getting latest data at ", current_date)
    ticker_unique = Stock.objects.order_by().values_list("ticker").distinct()
    for tick in ticker_unique:
        ticker = tick[0]
        stocks = Stock.objects.filter(
            time__lt=current_date, ticker=ticker).order_by("-time")
        the_latest_date = str(stocks.values_list("time", flat=True).first())
        year = the_latest_date[0:4]
        month = the_latest_date[5:7]
        date = the_latest_date[8:10]
        full_date = f"{year}-{month}-{date}"
        current_date_string = datetime.strftime(current_date, "%Y-%m-%d")
        print(full_date)
        print(current_date_string)

        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{full_date}/{current_date_string}?adjusted=true&sort=asc&limit=500000&apiKey=nyd1QVoAqt4QVkHYYMqe_5kvFfN40G8D"
        response = requests.get(url)
        data = response.json()
        print(data)
        if data["status"] == "ERROR":
            print("Going to sleep before more requests")
            time.sleep(61)
            url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{full_date}/{current_date_string}?adjusted=true&sort=asc&limit=500000&apiKey=nyd1QVoAqt4QVkHYYMqe_5kvFfN40G8D"

            response = requests.get(url)
            data = response.json()
        if data["resultsCount"] == 0:
            print("Skipped on ", ticker, " stock")
            continue

        for index, ticker_result in enumerate(data["results"]):
            print("RUN Once on ticker ", data["ticker"])
            ticker_timestamp = str(ticker_result['t'])
            corrected_timestamp = ticker_timestamp[0:10]
            already_exist = Stock.objects.filter(
                ticker=data["ticker"], time=datetime.fromtimestamp(int(corrected_timestamp))).count()
            if already_exist > 0:
                continue
            Stock.objects.create(
                ticker=data["ticker"],
                volume=ticker_result["v"],
                volume_weighted=ticker_result['vw'],
                open_price=ticker_result['o'],
                close_price=ticker_result['c'],
                highest_price=ticker_result['h'],
                lowest_price=ticker_result['l'],
                time=datetime.fromtimestamp(int(corrected_timestamp)),
                num_transactions=ticker_result['n']
            )
    data = ticker_unique.count()
    return print(f'Updated today {data} amount of stocks data')


# Analyze data by 'ticker' using methods 'Moving Average' and 'Standard deviation' of 30 trade days.
# Find those days higher then Average by 10times 'StdDev'.
def analyze_volume_data():
    multiplier = 5
    ticker_unique = Stock.objects.order_by().values_list("ticker").distinct()

    for ticker in ticker_unique:
        ticker = ticker[0]
        amount_of_rows_per_stock = Stock.objects.filter(ticker=ticker).count()

        for period in range(amount_of_rows_per_stock//30):
            offset = 30*period
            limit = 30*(period+1)
            print(f'From {offset} to {limit}')
            filtered_stocks = Stock.objects.filter(
                ticker=ticker).order_by("-time")[offset:limit]
            avg_volume = filtered_stocks.aggregate(Avg("volume"))[
                "volume__avg"]
            dev_volume = filtered_stocks.aggregate(StdDev("volume"))[
                "volume__stddev"]
            print("The Average is: ", avg_volume, "The Deviation is: ", dev_volume)
            value_to_check = float(dev_volume) * float(multiplier) + float(avg_volume)
            data_to_response = Stock.objects.filter(
                volume__gte=value_to_check, ticker=ticker).order_by("-time")[offset:limit]

            for row in data_to_response:
                already_existed = IrregularStocksDates.objects.filter(
                    ticker=ticker, time=row.time)
                if already_existed:
                    continue
                IrregularStocksDates.objects.create(
                    ticker=ticker,
                    volume=row.volume,
                    avg_volume=avg_volume,
                    dev_volume=dev_volume,
                    time=row.time
                )
                print("ADDED IRREGULAR ROW TO ", ticker)
    return print("Done analyzing the data")


# Triggers to run "def get_latest_data():" & "def analyze_volume_data():"
scheduler = BackgroundScheduler()
scheduler.add_job(get_latest_data, trigger=CronTrigger(hour=23, minute=50, day_of_week="mon,tue,wed,thu,fri"))
scheduler.add_job(analyze_volume_data,trigger=CronTrigger(day=20, hour=0, minute=33))
scheduler.start()

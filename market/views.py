from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes 
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from market.models import (Stock, IrregularStocksDates, StockList,UserStock)
from market.serializers import (StockSerializer, IrregularStocksDatesSerializer)
from datetime import (datetime, date, timedelta)
from django.db.models import Avg
from django.db.models.aggregates import StdDev
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.http import JsonResponse, HttpResponse


# View of list of all 'ticker' in Stock.Model
@api_view(['GET'])
def ticker_list(requests):
    if requests.method == "GET":
        # stocks_names = Stock.objects.values_list("ticker").distinct()
        # for stock in stocks_names:
        #     StockList.objects.create(ticker=stock[0])
        ticker_sym = list(Stock.objects.values_list('ticker').distinct())
        return JsonResponse(ticker_sym, safe=False)


# Save tickers to user in UserStock.Model
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_stock(requests):
    user = requests.user
    if requests.method == "POST":
        ticker = requests.data['ticker_id']
        stock = StockList.objects.get(id=ticker)
        user_new_stock = UserStock.objects.create(stock=stock, user=user)
        if user_new_stock:
            return Response(status=status.HTTP_201_CREATED)


# View of data by 'ticker'
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
            ticker=ticker, time__gte=from_date_object, time__lte=to_date_object).order_by("-time")
        serializer = StockSerializer(filtered_stocks, many=True)
        return Response(serializer.data)


# View of analyzed IrregularStocksDates.Model by 'ticker'
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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


# Import new 'ticker' into the app.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_data(request):
    if request.method == "GET":
        ticker = request.GET.get('ticker', '')
        test_already_exist = Stock.objects.filter(ticker=ticker).count()
        if test_already_exist > 0:
            return Response(f"{ticker} Already exist in database, query the database through /stock api endpoint",400)
        current_date = date.today()
        start_date = current_date - timedelta(days=728)
        current_date_string = current_date.strftime("%Y-%m-%d")
        start_date_string = start_date.strftime("%Y-%m-%d")

        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date_string}/{current_date_string}?adjusted=true&sort=asc&limit=500000&apiKey=nyd1QVoAqt4QVkHYYMqe_5kvFfN40G8D"
        response = requests.get(url)
        data = response.json()
        StockList.objects.create(ticker=data["ticker"])
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


# Query for analyzed date for a 'ticker' using method 'Average Volume' within a time frame.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analyze_volume_query(requests):
    if requests.method == "GET":
        ticker = requests.GET.get('ticker', '')
        multiplier = requests.GET.get('multi', 2.3263)
        from_date = requests.GET.get("from_date")
        to_date = requests.GET.get("to_date")
        try:
            from_date_object = datetime.strptime(from_date,"%d-%m-%Y")
            to_date_object = datetime.strptime(to_date,"%d-%m-%Y")
        except:
            return Response("From date or to date was not inserted correctly",400)

        average_volume_between_dates = Stock.objects.filter(ticker=ticker,time__lte=to_date_object,time__gte=from_date_object)
        avg_volume = average_volume_between_dates.aggregate(Avg("volume"))[
            "volume__avg"] 
        print("The Average is: ", avg_volume)
        if (avg_volume == None):
            return Response("No stocks's event was found")

        value_to_check = float(avg_volume) * float(multiplier)
        data_to_response = average_volume_between_dates.filter(
            volume__gte=value_to_check).order_by("-volume")
        
        serializer = StockSerializer(data_to_response,many=True)

        response_object = {
            "averageVolume":avg_volume,
            "stockDays":serializer.data,
            }
        return Response(response_object)


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
        print("Sleep for 15 seconds before getting next stock")
        time.sleep(15)
    data = ticker_unique.count()
    return print(f'Updated {data} amount of stocks data')


# Analyze data by 'ticker' using methods 'Moving Average' and 'Standard deviation' of 30 trade days window.
# Find the dates of volume higher then Average by 5 times 'StdDev'.
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
                volume = row.volume
                rating = (volume - avg_volume)//avg_volume
                IrregularStocksDates.objects.create(
                    ticker=ticker,
                    volume=row.volume,
                    avg_volume=avg_volume,
                    dev_volume=dev_volume,
                    rating = rating,
                    time=row.time
                )
                print("ADDED IRREGULAR ROW TO ", ticker)
    return print("Done analyzing the data")


# Triggers to run "def get_latest_data():" & "def analyze_volume_data():"
scheduler = BackgroundScheduler()
scheduler.add_job(get_latest_data, trigger=CronTrigger
    (timezone='UTC', hour=12, minute=1, day_of_week="mon,tue,wed,thu,fri,sat"))
scheduler.add_job(analyze_volume_data,trigger=CronTrigger
    (timezone='UTC', hour=1, minute=2, day_of_week="mon"))

# scheduler.add_job(get_latest_data,trigger=CronTrigger(hour=21,minute=28))
# scheduler.add_job(analyze_volume_data,trigger=CronTrigger(hour=9, minute=16))

scheduler.start()


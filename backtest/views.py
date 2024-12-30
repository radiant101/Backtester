from django.shortcuts import render
from django.http import HttpResponse
from .data_loader import load_ohlc_data
import pandas as pd

# Create your views here.
def index(request):
    return render(request,'backtest/index.html')

def results(request):
    return render(request,'backtest/results.html')

def load_data(): #helper function it can be changed
    file_path='path/to/your/data.parquet'
    return load_ohlc_data(file_path)
    
def strategy(request):
    if request.method == "POST":
        try:
            stratname = request.POST.get('stratname')
            symbol = request.POST.get('symbol')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            short_window = int(request.POST.get('short_window', 0))
            long_window = int(request.POST.get('long_window', 0))

            if not all([symbol, start_date, end_date]):
                return HttpResponse("Missing required parameters.", status=400)

            print(f"Symbol: {symbol}, Start Date: {start_date}, End Date: {end_date}")

            ohlc_data = load_ohlc_data(symbol, start_date, end_date)
            if ohlc_data is None:
                result = "Failed to load data."
                print(result)
                return HttpResponse(result)
            else:
                print(ohlc_data.head())
                return HttpResponse(ohlc_data.head().to_html())

        except ValueError:
            return HttpResponse("Invalid input for window sizes.", status=400)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return HttpResponse(f"An error occurred: {e}", status=500)

    return render(request, 'backtest/strategy.html')



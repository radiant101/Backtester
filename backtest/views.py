from django.shortcuts import render
from django.http import HttpResponse
from .data_loader import load_ohlc_data
from .utils import moving_average
import pandas as pd
from .metrics import calculate_sharpe
from django.shortcuts import redirect
from django.http import JsonResponse
import os
import plotly.express as px
import time
from .metrics import calculate_maxdrawdown
from scipy.stats import zscore
import numpy as np 


# Create your views here.
def index(request):
    return render(request,'backtest/index.html')

def results(request):
    return render(request,'backtest/results.html')

def news(request):
    return render(request,'backtest/news.html')

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

            print(f"Symbol: {symbol}, Start Date: {start_date}, End Date: {end_date}");

            ohlc_data = load_ohlc_data(symbol, start_date, end_date)
            if ohlc_data is None:
                result = "Failed to load data."
                print(result)
                return HttpResponse(result)
            ohlc_data = ohlc_data[np.abs(zscore(ohlc_data["close"])) < 3]
            print("Before moving_average:")
            resample_interval = '1h'
            ohlc_data=moving_average(ohlc_data,short_window,long_window,resample_interval)
            print("After moving_average:")
            csv_file_path = os.path.join(os.getcwd(), f"{symbol}_ohlc_data.csv")
            ohlc_data.to_csv(csv_file_path, index=False)
            return redirect(f"/results/?symbol={symbol}&short_window={short_window}&long_window={long_window}")

        except ValueError:
            return HttpResponse("Invalid input for window sizes.", status=400)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return HttpResponse(f"An error occurred: {e}", status=500)

    return render(request, 'backtest/strategy.html')
    
def results(request):
    symbol = request.GET.get('symbol')
    short_window = request.GET.get('short_window')
    long_window = request.GET.get('long_window')

    if not symbol:
        return HttpResponse("Missing symbol parameter.", status=400)

    # Log before loading CSV
    print("Loading CSV data.")
    start_time = time.time()  # Start timing

    # Load the processed CSV file
    csv_file_path = os.path.join(os.getcwd(), f"{symbol}_ohlc_data.csv")
    if not os.path.exists(csv_file_path):
        return HttpResponse("CSV file not found.", status=404)

    ohlc_data = pd.read_csv(csv_file_path)
    sharpe_val=calculate_sharpe(csv_file_path)
    max_drawdown=calculate_maxdrawdown(csv_file_path)
    # Ensure 'date' is parsed correctly and in datetime format
    ohlc_data['date'] = pd.to_datetime(ohlc_data['date'])

    # Log after loading CSV
    print(f"CSV loaded in {time.time() - start_time:.2f} seconds.")

    # Log before creating the Plotly chart
    print(f"Dataframe shape: {ohlc_data.shape}")

    # Create Plotly chart with the entire dataset
    fig = px.line(
        ohlc_data,
        x='date',
        y=['short_ma', 'long_ma', 'close'],
        title=f"Backtesting Results for {symbol} ({short_window}-{long_window})",
        labels={'value': 'Price', 'variable': 'Legend'},
        template='plotly_dark'  # Optional: Apply a template for better visuals
    )

    chart_json = fig.to_json()

    # Log after creating the chart
    print("Plotly chart created successfully.")

    # Render the template
    return render(request, 'backtest/results.html', {
    'chart_json': chart_json,
    'sharpe_val': sharpe_val,
    'max_drawdown': max_drawdown
})


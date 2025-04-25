import pandas as pd
import os
from datetime import datetime

"""def load_ohlc_data(file_path):
    try: 
        data=pd.read_parquet(file_path)
        return data
    except Exception as e:
        print(f"error due to:{e}")
        return None """

def load_ohlc_data(symbol, start_date, end_date):
    base_path = f"D:\\stock_data\\candles\\{symbol}"
    dflist = []

    try:
        available_dates = os.listdir(base_path)  # Get all date folders
        print(f"Available dates: {available_dates}")  # Debug output
    except FileNotFoundError:
        print(f"Directory for symbol '{symbol}' not found at {base_path}")
        return None

    # Parse start and end dates
    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

    for date in available_dates:
        print(f"Processing date: {date}")  # Debugging output
        try:
            date_dt = datetime.strptime(date, "%Y-%m-%d")

            # Process only if the date falls within the range
            if start_date_dt <= date_dt <= end_date_dt:
                date_folder_path = os.path.join(base_path, date)
                print(f"Checking folder: {date_folder_path}")  # Debugging output
                parquet_files = os.listdir(date_folder_path)

                print(f"Contents of {date_folder_path}: {parquet_files}")  # Debugging output
                if not parquet_files:
                    print(f"No parquet files found for {date_folder_path}")
                    continue

                for par in parquet_files:
                 if par.endswith('.parquet') or par.endswith('.parquet.gz'):
                  file_path = os.path.join(date_folder_path, par)
                  try:
                    print(f"Reading file: {file_path}")
                    df = pd.read_parquet(file_path)  # This will handle .parquet.gz automatically if you have the right libraries installed
                    dflist.append(df)
                  except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                else:
                 print(f"Skipping non-parquet file: {par}")
        except ValueError as ve:
            print(f"Skipping invalid date folder '{date}': {ve}")

    if not dflist:
        print(f"No data found for {symbol} between {start_date} and {end_date}")
        return None

    final_df = pd.concat(dflist, ignore_index=True)
    print(f"Total records loaded: {len(final_df)}")  # Check total records
    final_df['date']=pd.to_datetime(final_df['date'],format="%d-%m-%Y %H:%M",errors='coerce')
    final_df = final_df.sort_values('date').reset_index(drop=True)
    
    final_df=final_df[(final_df['date']>=start_date_dt)&(final_df['date']<=end_date_dt)]
    final_df = final_df.ffill().bfill()
    # Specify the CSV file path
    #csv_file_path = os.path.join(os.getcwd(), f"{symbol}_ohlc_data.csv")
    #final_df.to_csv(csv_file_path, index=False)

    print(df.columns)
    print(df['close'].isna().sum())  # Count NaN values
    print(df['close'].dtype)  # Check data type
    #print(f"Data saved to: {csv_file_path}")  # Output the CSV file path
    return final_df # Return the DataFrame and the CSV file path
    

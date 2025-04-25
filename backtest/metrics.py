import pandas as pd

def calculate_sharpe(csv_file_path,risk_free_return=1.00):
    df=pd.read_csv(csv_file_path)
    #ensure date coloumn is datetime
    df['date']=pd.to_datetime(df['date'])
    #calculate daily returns
    df['return']=df['close'].pct_change()
    # Convert risk-free rate to the daily rate assuming 252 trading days in a year
    daily_risk_free_rate = (1 + risk_free_return) ** (1/252) - 1
    # Calculate excess returns
    df['excess_returns'] = df['return'] - daily_risk_free_rate
    # Calculate the mean and standard deviation of excess returns
    mean_excess_return = df['excess_returns'].mean()
    std_excess_return = df['excess_returns'].std()
    # Calculate the Sharpe ratio
    sharpe_ratio = mean_excess_return / std_excess_return

    print(f"Sharpe Ratio: {sharpe_ratio}")
    
    return sharpe_ratio


def calculate_maxdrawdown(csv_file_path):
    df=pd.read_csv(csv_file_path)
    
    equity_curve=df['close']
    #cumulative sum calculate kela
    cumulative_maximum=equity_curve.cummax()
    #calculate drawdown kela
    drawdown=(equity_curve-cumulative_maximum)/cumulative_maximum
    #negative drawdown calculated
    max_drawdown = drawdown.min()
    return max_drawdown

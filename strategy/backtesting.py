import pandas as pd

def calculate_pnl(data):
    """
    Made Generic for Both Markets
    """
    trades = pd.DataFrame(data)

    def compute_pnl(row):
        if row['Direction'].lower() == 'long':
            return (row['Exit Price'] - row['Entry Price']) * row['Quantity']
        elif row['Direction'].lower() == 'short':
            return (row['Entry Price'] - row['Exit Price']) * row['Quantity']
        else:
            return 0
    
    trades['PnL'] = trades.apply(compute_pnl, axis=1)
    return trades




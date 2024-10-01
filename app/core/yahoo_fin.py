import logging
import yfinance as yf
import polars as pl
from app.core.base import DataProvider


logger = logging.getLogger(__name__)
class YahooFinance(DataProvider):

    def fetch_historic_data(self, symbol, start, end):
        logger.info(f"Get historical OHLC for ticker={symbol} from {start} to {end} from datasource(yf)")
        if symbol is not None and symbol.strip():
            ticker = yf.Ticker(symbol)
            name = ticker.info.get('shortName', 'Symbol not found')
            if name == 'Symbol not found':
                return None, None
            else:
                result = ticker.history(start=start, end=end)
                df = result.copy()
                # Convert into Polars DataFrame. Avoiding not modifying code from here for further method/function calls
                df.reset_index(inplace=True)  # Reset the index to turn the date index into a column
                df['ticker'] = symbol  # Add a ticker column filled with the symbol
                df['short_name'] = name
                df = df.rename(
                    columns={
                        'Date': 'date',
                        'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close',
                        'Dividends': 'dividends', 'Stock Splits': 'stock_splits'
                    }
                )
                df = df[
                    ['ticker', 'short_name', 'date', 'open', 'high', 'low', 'close', 'dividends', 'stock_splits']]
                df['date'] = df['date'].dt.date  # Convert datetime to date
                # Convert Pandas DataFrame to Polars DataFrame
                pl_df = pl.from_pandas(df)
                return pl_df, name
        else:
            return None, None

    def get_live_data(self, symbol, period=1):
        ticker = yf.Ticker(symbol)
        live_data = ticker.history(period="1d")
        # Fetch today's data
        return live_data.to_dict()

    def get_live_price(self, symbol: str):
        ticker = yf.Ticker(symbol)
        live_price = ticker.fast_info
        return live_price
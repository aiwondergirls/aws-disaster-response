import pandas as pd

def standard_date_format(some_date: str) -> str:
  """
  takes a date and formats it to the standard YYYY-MM-DD format
  """
  return pd.Timestamp(some_date).date().isoformat()

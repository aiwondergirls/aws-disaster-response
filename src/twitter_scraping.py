import pandas as pd
import twint

from src.utils import standard_date_format

class Twitter_agent:

    def __init__(self, keyword, location, start_date, end_date, min_n_tweets=None):
        self.search_word = keyword
        self.location = location
        self.min_n_tweets = min_n_tweets
        #"YYYY-MM-DD"
        self.start_date = standard_date_format(start_date)
        self.end_date = standard_date_format(end_date)

    def get_tweets(self) -> pd.DataFrame:
        c = twint.Config()
        c.Lang = "en"
        c.Search = self.search_word
        c.Near = self.location
        c.Since = self.start_date #"YYYY-MM-DD"
        c.Until = self.end_date   #"YYYY-MM-DD"
        # c.Hide_output = True
        if self.min_n_tweets:
          c.Limit = self.min_n_tweets
        # c.Store_csv = False
        # c.Output = "{}_{}.csv".format(self.location, self.search_word)
        c.Pandas = True
        twint.run.Search(c)

        df = twint.storage.panda.Tweets_df

        return df[['date', 'place', 'tweet', 'link']].rename(
            columns=dict(
                tweet='body',
                link='url',
                date = 'time'
            )
        )

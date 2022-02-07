import pandas as pd
import streamlit as st

from src.newspaper_scraping import Newspaper_agent
from src.twitter_scraping import Twitter_agent

country_codes = pd.read_csv("data_news/country_codes.csv")

class Query:
    def __init__(
        self,
        start_date,
        end_date,
        location,
        event_type,
        scraper_type,
        languages,
        number_of_articles,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.event_type = event_type
        self.scraper_type = scraper_type
        self.languages = languages
        self.number_of_articles = number_of_articles


class Scraper:
    def __init__(self, query: Query):
        self.query = query

    def scrape(self) -> pd.DataFrame:
        final_result = []
        if self.query.scraper_type.lower() == "newspaper":
            for name in self.query.location:
                country_code_final = country_codes[country_codes["Country"] == name][
                    "Alpha-2 code"
                ].values[0]
                
                language = 'English'
                language_code_final = "en"
                
                keyword_final = 'earthquake'
                            
                keywords = str(str(name) + " " + str(keyword_final))
                newspaper = Newspaper_agent(self.query,
                        keywords,
                        country_code_final,
                        language_code_final,
                        name,
                        language,
                    )
                news_results_list = newspaper.get_news_links()
                if news_results_list is not None and len(news_results_list) > 0:
                        final_result.append(news_results_list)
            return pd.concat(final_result) if len(final_result) > 0 else None

        
        elif self.query.scraper_type.lower() == "twitter":
            return pd.concat(
                [
                    Twitter_agent(
                        keyword=self.query.event_type.lower(),
                        location=location,
                        start_date=self.query.start_date,
                        end_date=self.query.end_date,
                        min_n_tweets=max(self.query.number_of_articles, 1000),
                        ).get_tweets()
                    for location in self.query.location
                ]
            )

        else:
            st.error("Scraper not supported")
            return

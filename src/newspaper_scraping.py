import nltk
nltk.download('punkt')
from newspaper import Article, Config
from pygooglenews import GoogleNews
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from pathlib import Path


class Newspaper_agent:
    TMP_DIRECTORY = Path("./tmp_data")
    if not TMP_DIRECTORY.exists():
        TMP_DIRECTORY.mkdir()

    def __init__(
        self,
        query,
        keywords,
        country_code_final,
        language_code_final,
        country,
        language,
    ):
        self.query = query
        self.keywords = keywords
        self.country_code_final = country_code_final
        self.language_code_final = language_code_final
        self.country = country
        self.language = language
        self.custom_tags = pd.read_csv("data_news/Custom_Websites_Tags.csv")

    def custom_scraper(self, url, title_tag, title_class, date_tag, date_class):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        article_title = soup.find(title_tag, class_=title_class)
        article_title = article_title.get_text() if article_title is not None else ""

        article_content = ""

        regex = re.compile(".*Paragraph")
        for each in soup.find_all("p"):
            article_content = article_content + each.get_text() + " "
        date_published = soup.find(date_tag, class_=date_class)
        if date_published is not None:
            date_published = date_published.get_text()
        return article_content, date_published

    # Get the sumary of the articles
    def get_article_content_display(self, article_url):
        # try block added
        try:
            news_article = Article(article_url)

            news_article.download()
            news_article.parse()
            news_article.nlp()

            # get a summary of article
            # st.write("**Summary:** %s" % news_article.summary)
        except:
            pass

        return

    def get_article_content(self, article_url):
        # get the date of posting the article
        news_content = ""
        date_published = ""
        try:
            news_article = Article(article_url)
            news_article.download()
            news_article.parse()
            news_article.nlp()
            news_content = news_article.text
            date_published = news_article.publish_date

        except:
            pass

        if len(news_content) == 0:
            domain = urlparse(article_url).netloc
            if domain in self.custom_tags["Newspaper website name"].tolist():
                title_tag = self.custom_tags[
                    self.custom_tags["Newspaper website name"] == domain
                ]["title_tag"].values[0]
                title_class = self.custom_tags[
                    self.custom_tags["Newspaper website name"] == domain
                ]["title_class"].values[0]
                date_tag = self.custom_tags[
                    self.custom_tags["Newspaper website name"] == domain
                ]["date_tag"].values[0]
                date_class = self.custom_tags[
                    self.custom_tags["Newspaper website name"] == domain
                ]["date_class"].values[0]
                news_content, date_published = self.custom_scraper(
                    article_url, title_tag, title_class, date_tag, date_class
                )

        # get the article text
        return (
            news_content,
            date_published,
            news_article.top_image,
            news_article.keywords,
        )

    def get_news_links(self):

        # to access through the firewall
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        config = Config()
        config.browser_user_agent = user_agent

        gn = GoogleNews(country=self.country_code_final, lang=self.language_code_final)
        article_num = []
        article_title = []
        article_link = []
        article_content = []
        publishing_date = []
        article_image = []
        article_keywords = []
        search = gn.search(
            query=self.keywords,
            helper=True,
            when=None,
            from_=self.query.start_date,
            to_=self.query.end_date,
            proxies=None,
            scraping_bee=None,
        )

        count = 0
        i = 0

        # loop over the first `number_of_articles` items in `search['entries']`
        for count, item in enumerate(
            search["entries"][: self.query.number_of_articles]
        ):
            # st.write('**Result no. %s:**' % int(i+1))
            article_num.append(count)

            ##Title
            article_title.append(item["title"])
            # st.write("**Title:** %s" % article_title[i])

            ##Link
            article_link.append(item["link"])
            # st.write("**Link:** %s" %article_link[i])

            ##Publishing Date
            article_stuff = self.get_article_content(item["link"])
            if item["published"] is None:
                publishing_date.append(article_stuff[1])
            else:
                publishing_date.append(item["published"])

            # st.write("**Published Date:** %s" % str(publishing_date[i]))

            ##Complete Content
            article_content.append(article_stuff[0])

            # ##Image
            # article_image.append(article_stuff[2])
            # try:
            #     image = Image.open(requests.get(article_image[i], stream=True).raw)
            #     res = requests.get(article_image[i])
            #     #res.raise_for_status()
            #     #st.image(image, width=500)

            # except UnidentifiedImageError:
            #     #st.write("**No Image Provided**")
            #     pass
            # except requests.exceptions.MissingSchema:
            #     pass
            #     #st.write("**No Image Provided**")

            # ##Summary of the article
            # self.get_article_content_display(item['link'])

            ##Keywords
            article_keywords.append(self.get_article_content(item["link"])[3])
            # st.write("**Keywords:** %s" % article_keywords[i])

            # st.write("-------------------------------------------------------------------------------------")
            # time.sleep(1)

        articles_dict = {
            "ID": article_num,
            "title": article_title,
            "time": publishing_date,
            "keywords": article_keywords,
            "data_source": "news_article",
            "category": self.query.event_type,
            "country": self.country,
            "source_URL": article_link,
            "body": article_content,
            "language": self.language,
        }

        print("scraping done")
        df = pd.DataFrame(articles_dict)
        df.drop_duplicates("title", inplace=True)

        filename = (
            Newspaper_agent.TMP_DIRECTORY / f"Scraped_news_articles_for_{self.keywords}.csv"
        )
        print("writing to file:", filename)
        with open(filename, "w") as f:
            df.to_csv(filename)
        print("`Newspaper_agent.get_links` is done")
        return df

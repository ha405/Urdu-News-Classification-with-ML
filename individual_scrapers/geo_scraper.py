import os
import json
import time
import random
import zipfile
import requests
import pandas as pd
import csv
import re
from bs4 import BeautifulSoup



class Geo_Scraper:
    def __init__(self,id_=0):
        self.id = id_

    def get_geo_articles(self, max_articles_per_category=60):
        geo_df = {
            "id": [],
            "title": [],
            "link": [],
            "content": [],
            "gold_label": [],
        }
        categories = {
            "sports": "https://urdu.geo.tv/category/sports",
            "science": "https://urdu.geo.tv/category/science-technology",
            "business": "https://urdu.geo.tv/category/business",
            "world": "https://urdu.geo.tv/category/world",
            "entertainment": "https://urdu.geo.tv/category/entertainment"
        }
        for category, url in categories.items():
            article_count = 0
            print(f"Scraping articles for category '{category}'...")
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("li", class_="border-box")
            if not articles:
                print(f"No articles found in category '{category}'")
                continue
            for article in articles:
                title_tag = article.find("a", class_="open-section")
                title = title_tag.get("title", "Title not found")
                link = title_tag["href"]
                if link.endswith('-'):
                    article_id = link.split('-')[-1] 
                    if len(article_id) <= 3:
                        next_two_digits = article_id[2:]  
                        link = link + next_two_digits
                    else:
                        link = link + article_id[:2]  
                article_response = requests.get(link)
                article_response.raise_for_status()
                article_soup = BeautifulSoup(article_response.text, "html.parser")
                content_div = article_soup.find("div", class_="content-area")
                paragraphs = content_div.find_all("p") if content_div else []
                content = " ".join(p.get_text(strip=True) for p in paragraphs)
                geo_df["id"].append(self.id)
                geo_df["title"].append(title)
                geo_df["link"].append(link)
                geo_df["content"].append(content)
                geo_df["gold_label"].append(category)
                self.id += 1
                article_count += 1
                print(f"\t--> Scraped article {article_count} in category '{category}'.")
                if article_count >= max_articles_per_category:
                    break
            print(f"Completed scraping {article_count} articles from category '{category}'.")
        df = pd.DataFrame(geo_df)
        return df
    
    def save_to_csv(self, df, filename="geo_articles.csv"):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(["ID", "Title", "Link", "Content", "Gold Label"])
            for _, row in df.iterrows():
                writer.writerow([row["id"], row["title"], row["link"], row["content"], row["gold_label"]])
        print(f"Articles saved to {filename}")


geo_scraper = Geo_Scraper()
df = geo_scraper.get_geo_articles(max_articles_per_category=60)
geo_scraper.save_to_csv(df, filename="geo_articles.csv")
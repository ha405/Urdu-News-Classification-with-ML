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

# list of categories
cats = ["World News", "Sports News", "Science & Technology News", "Business News", "Entertainment News"]
class Jang_Scraper:
    def __init__(self, id_=0):
        self.id = id_

    def get_category_links(self, base_url):
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        footer_links = {}
        footer_section = soup.find('section', class_='footer')

        if footer_section:
            footer_content = footer_section.find('div', class_='footer_content')
            if footer_content:
                first_row = footer_content.find('div', class_='first_footer')
                if first_row:
                    col = first_row.find('div', class_='col-lg-3 col-md-3 col-sm-6 col-xs-6 h_footer')
                    if col:
                        footer_list = col.find('ul', class_='footer-list')
                        if footer_list:
                            footer_quick1 = footer_list.find('div', class_='footer-quick1')

                            if footer_quick1:
                                for li in footer_quick1.find_all('li'):
                                    a_tag = li.find('a')
                                    if a_tag and 'href' in a_tag.attrs:
                                        category_url = a_tag['href']
                                        category_title = a_tag.get_text(strip=True)

                                        # check if the category title is in the `cats` list
                                        if category_title in cats:
                                            # extract the last part of the URL to use as the category label
                                            label = re.search(r'/([^/]+)$', category_url).group(1)
                                            footer_links[category_url] = label

        return footer_links

    def get_articles_from_category(self, category_url, label, max_pages=1):
        articles_data = {
            "id": [],
            "title": [],
            "link": [],
            "content": [],
            "gold_label": []
        }

        for page in range(1, max_pages + 1):
            page_url = f"{category_url}?page={page}" if page > 1 else category_url
            response = requests.get(page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            try:
                latest_page = soup.find('section', class_='latest_page')
                if latest_page:
                    latest_page_list = soup.find('section', class_='latest_page_list')
                    if latest_page_list:
                        container = latest_page_list.find('div', class_='container')
                        if container:
                            latest_page_right = container.find('div', class_='latest_page_right')
                            if latest_page_right:
                                scroll_pagination = latest_page_right.find('ul', class_='scrollPaginationNew__')
                                if scroll_pagination:
                                    for li in scroll_pagination.find_all('li'):
                                        main_heading = li.find('div', class_='main-heading')
                                        if main_heading:
                                            a_tag = main_heading.find('a')
                                            if a_tag and 'href' in a_tag.attrs:
                                                article_url = a_tag['href']
                                                full_url = f"{article_url}"
                                                article_response = requests.get(full_url)
                                                article_response.raise_for_status()
                                                content_soup = BeautifulSoup(article_response.text, "html.parser")

                                                # get article title
                                                title_div = content_soup.find('section', class_='detail-page')
                                                if title_div:
                                                    container = title_div.find('div', class_='container')
                                                    if container:
                                                        detail_right = container.find('div', class_='detail-right')
                                                        if detail_right:
                                                            detail_right_top = detail_right.find('div', class_='detail-right-top')
                                                            if detail_right_top:
                                                                title_tag = detail_right_top.find('h1')
                                                                if title_tag:
                                                                    title = title_tag.get_text(strip=True)
                                                                else:
                                                                    title = "No title found"
                                                            
                                                            # get the article count
                                                            detail_content = detail_right.find('div', class_='detail-content')
                                                            if detail_content:
                                                                description_area = detail_content.find('div', class_='description-area')
                                                                if description_area:
                                                                    detail_view_content = description_area.find('div', class_='detail_view_content')
                                                                    if detail_view_content:
                                                                        paragraphs = detail_view_content.find_all('p')
                                                                        article_content = " ".join([para.get_text(strip=True) for para in paragraphs])
                                                                    else:
                                                                        article_content = "No content found"
                                                            else:
                                                                article_content = "No content found"
                                                            
                                                            # add the data to articles_data
                                                            articles_data["id"].append(self.id)
                                                            articles_data["title"].append(title)
                                                            articles_data["link"].append(full_url)
                                                            articles_data["content"].append(article_content)
                                                            articles_data["gold_label"].append(label)  

                                                            # print statement after each article is added
                                                            print(f"Added article: {title}")

                                                            self.id += 1

            except AttributeError as e:
                pass

        return articles_data

    def get_all_articles(self, base_url, max_pages=1):
        category_links = self.get_category_links(base_url)

        all_articles = {
            "id": [],
            "title": [],
            "link": [],
            "content": [],
            "gold_label": []
        }

        for category_url, label in category_links.items():
            category_data = self.get_articles_from_category(category_url, label, max_pages)
            for key in all_articles:
                all_articles[key].extend(category_data[key])

        return pd.DataFrame(all_articles)
    
    
scraper = Jang_Scraper()
base_url = "https://jang.com.pk/"
articles_df = scraper.get_all_articles(base_url, max_pages=1)
articles_df.to_csv("jang_articles.csv", index=False)
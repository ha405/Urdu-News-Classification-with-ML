import requests
from bs4 import BeautifulSoup
import csv

class SamaaScraper:
    def __init__(self):
        self.base_url = "https://urdu.samaa.tv"  # Updated to Urdu URL
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        self.articles = []

    def fetch_category_articles(self, category_url, category_name):
        """
        Fetches up to 80 articles from a category page with pagination.
        """
        page = 1
        while len([a for a in self.articles if a['category'] == category_name]) < 150:
            url = f"{category_url}?page={page}"
            print(f"Fetching page: {url}")
            response = requests.get(url, headers=self.headers)  # Add headers here
            
            print("response: ", response)
            if response.status_code == 403:
                print(f"Access forbidden (403) for {url}. Check headers or other access restrictions.")
                break
            elif response.status_code != 200:
                print(f"Error fetching page {page} of {category_name}. Status code: {response.status_code}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles_in_category = []
            for article in soup.select('article.story-article'):
                title = article.h3.a.text.strip()
                link = article.h3.a['href']
                if not link.startswith("http"):
                    link = self.base_url + link
                full_content = self.fetch_article_content(link)
                articles_in_category.append({
                    'title': title,
                    'link': link,
                    'content': full_content,
                    'category': category_name,
                    'id': len(self.articles) + len(articles_in_category)
                })
                if len(articles_in_category) + len([a for a in self.articles if a['category'] == category_name]) >= 150:
                    break
            
            if not articles_in_category:
                break  # Exit if no more articles are found (end of pagination)
            
            self.articles.extend(articles_in_category)
            page += 1

    def fetch_article_content(self, url):
        """
        Fetches the full content of an article from its URL.
        """
        response = requests.get(url, headers=self.headers)  # Add headers here
        article_soup = BeautifulSoup(response.text, 'html.parser')
        content_div = article_soup.find('div', class_='article-content')
        
        if content_div:
            paragraphs = content_div.find_all('p')
            full_content = ' '.join(paragraph.text.strip() for paragraph in paragraphs)
            return full_content
        else:
            print(f"Warning: No content found for URL {url}")
            return ""

    def scrape(self, categories):
        """
        Main scraping function to fetch articles from multiple categories.
        """
        for category_name, category_url in categories.items():
            print(f"Scraping category: {category_name}")
            self.fetch_category_articles(category_url, category_name)
            print(f"Found {len([a for a in self.articles if a['category'] == category_name])} articles in {category_name}.")

    def save_to_csv(self, filename="articles.csv"):
        """
        Saves the scraped articles to a CSV file with quotes around text fields.
        """
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # Use quoting to handle commas
            writer.writerow(["ID", "Category", "Title", "Link", "Content"])
            for article in self.articles:
                writer.writerow([article['id'], article['category'], article['title'], article['link'], article['content']])
        print(f"Articles saved to {filename}")

# Define the categories to scrape with their URLs
categories = {
    "Business": "https://urdu.samaa.tv/money",
    "Science-Technology": "https://urdu.samaa.tv/tech",
    "International": "https://urdu.samaa.tv/global",
    "Sports": "https://urdu.samaa.tv/sports",
    "Entertainment": "https://urdu.samaa.tv/lifestyle",
}

# Initialize the scraper and start scraping
scraper = SamaaScraper()
scraper.scrape(categories)

# Save the articles to a CSV file
scraper.save_to_csv("samaa_articles.csv")

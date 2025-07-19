import time
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import redis
import json


load_dotenv()
r = redis.Redis()


def parser_habr():
    cashed = r.get('habr')
    if cashed:
        return cashed.decode('utf-8')
    url = "https://habr.com/ru/articles/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки
        
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.find_all("article", class_="tm-articles-list__item")  # Класс может меняться!
        
        res = ''

        for article in articles[:5]:  # Первые 5 статей
            title = article.find("h2").text.strip()
            link = article.find("a", class_="tm-title__link")["href"]
            full_link = f"https://habr.com{link}"
            res += f"📄 {title}\n🔗 {full_link}\n\n"
        r.setex('habr', 30, res)
        return res
    except Exception as e:
        return(f"Ошибка: {e}")
    

def parser_ria():
    cashed = r.get('ria')
    if cashed:
        return cashed.decode('utf-8')
    url = "https://ria.ru/politics/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки
        
        soup = BeautifulSoup(response.text, 'lxml')
        news = soup.find_all("div", class_="list-item")

        res = ''

        for new in news[:5]:  # Первые 5 статей
            title = new.find("a", class_="list-item__title color-font-hover-only").text.strip()
            link = new.find("a", class_="list-item__image")["href"]
            full_link = f"{link}"
            res += f"📄 {title}\n🔗 {full_link}\n\n"
        r.setex('ria', 30, res)
        return res
    except Exception as e:
        return(f"Ошибка: {e}")
    

def parser_vk():
    cashed = r.get('vk')
    if cashed:
        return json.loads(cashed.decode('utf-8'))
    access_token = os.getenv('API_VK')
    group_id = "rhymes"

    try:
        response = requests.get(
            "https://api.vk.com/method/wall.get",
            params={
                "domain": group_id,
                "count": 3,
                "access_token": access_token,
                "v": "5.131"
            }
        )
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()

        if 'error' in data:
            return f"Ошибка API: {data['error']['error_msg']}"

        posts = []
        for post in data.get("response", {}).get("items", []):
            post_data = {
                "text": post.get("text", ""),
                "photo": None
            }


            for attachment in post.get("attachments", []):
                if attachment.get("type") == "photo":
                    sizes = attachment["photo"].get("sizes", [])
                    if sizes:
                        largest = max(sizes, key=lambda x: x.get("width", 0))
                        post_data["photo"] = largest["url"]
                    break

            posts.append(post_data)
        r.setex('vk', 30, json.dumps(posts))
        return posts
    
    except Exception as e:
        return {"error": f"Ошибка: {str(e)}"}
    

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parser_wb():
    cashed = r.get('wb')
    if cashed:
        return cashed.decode('utf-8')
    service = EdgeService(r'D:\AAAAAAAAAAAAA\EdgeDrivers\msedgedriver.exe')

    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument("--headless=new")
    edge_options.add_argument("--disable-gpu")  # Отключение GPU (может улучшить стабильность)
    edge_options.add_argument("--window-size=1920,1080")  # Фиксированный размер окна
    edge_options.add_argument("--log-level=3")  # Минимальный уровень логов

    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option("useAutomationExtension", False)
    
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")

    driver = webdriver.Edge(service=service, options=edge_options)
    wait = WebDriverWait(driver, 15)
    
    driver.get("https://www.wildberries.ru/")

    open_search = wait.until(
        EC.element_to_be_clickable(('class name', "search-catalog__block")))
    open_search.click()

    item_search = driver.find_element('xpath', "//input[@id='searchInput']")
    item_search.send_keys('Штаны мужские' + Keys.ENTER)

    wait.until(
        EC.presence_of_all_elements_located(('xpath', "//article[contains(@class, 'product-card')]")))
    all_card = driver.find_elements('xpath', "//article[contains(@class, 'product-card')]")

    res = ''
    for card in all_card[:5]:
        try:
            url = card.find_element('xpath', ".//a[contains(@class, 'product-card__link')]").get_attribute('href')
            brand = card.find_element('xpath', ".//span[@class='product-card__brand']").text
            title = card.find_element('xpath', ".//span[@class='product-card__name']").text
            price = card.find_element('xpath', ".//ins[contains(@class, 'wallet-price')]").text
            res += f'🎴{brand} {title}\n<b>Цена:</b> {price} \n{url}' + '\n\n'
        except Exception as e:
            return (f"Ошибка: {e}")
    driver.quit()
    r.setex('wb', 30, res)
    return res

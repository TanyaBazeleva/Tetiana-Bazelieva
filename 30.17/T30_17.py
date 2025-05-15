import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_weather(city):
    url = f"https://sinoptik.ua/погода-{city}"
    page = requests.get(url)
    if page.status_code != 200:
        raise ValueError("Не вдалося отримати сторінку")
    soup = BeautifulSoup(page.text, "html.parser")
    data = []
    for i in range(1, 6):
        day = soup.find("div", {"id": f"bd{i}"})
        if not day:
            continue
        date = day.find("p", class_="date").text.strip()
        month = day.find("p", class_="month").text.strip()
        min_temp = day.find("div", class_="min").text.strip().replace("−", "-")
        max_temp = day.find("div", class_="max").text.strip().replace("−", "-")
        data.append({
            "Дата": f"{date} {month}",
            "Мінімальна температура": min_temp,
            "Максимальна температура": max_temp,
        })
    return data

def save_weather(data, file_name):
    df = pd.DataFrame(data)
    df["Збережено"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_excel(file_name, index=False)

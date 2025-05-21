from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

import requests
app = Flask(__name__)
TICKET_MASTER_KEY = "L2AG2mYeA9cBK8By0GIvZ3lbEaqDSFlJ"


def get_ticketmaster_events(keyword, category, date, address):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": TICKET_MASTER_KEY,
        "keyword": keyword,
        "classificationName": category,
        "startDateTime": date,
        "city": address,
        "size": 5
    }
    response = requests.get(url, params=params)

    #some debugging rn
    print("---- Ticketmaster API Request ----")
    print("URL:", response.url)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

    data = response.json()

    events = []
    if "_embedded" in data and "events" in data["_embedded"]:
        for event in data["_embedded"]["events"]:
            venue_name = event.get("_embedded", {}).get("venues", [{}])[0].get("name", "Unknown Venue")
            description = event.get("info", "No description available.")

            events.append({
                "name": event.get("name", "Untitled Event"),
                "url": event.get("url", "#"),
                "address": venue_name,
                "description": description
            })

    return events

#incercarea nr 1 de eventbrite
# def get_eventbrite_events(keyword):
#     from bs4 import BeautifulSoup
#     import re
#     url = f"https://www.eventbrite.com/d/online/{keyword.replace(' ', '-')}/"
#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }
#     response = requests.get(url, headers=headers)
#
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     events = []
#     #incercarea 2
#     cards = soup.select("div.eds-event-card-content__content")[:5]
#
#
#     #asa nu
#     #cards = soup.find_all("div", class_=re.compile("search-event-card-wrapper"))[:5]
#
#     for card in cards:
#         try:
#             title_tag = card.find("div", {"data-spec": "event-card__formatted-name--content"})
#             link_tag = card.find("a", href=True)
#             location_tag = card.find("div", class_=re.compile("card-text--truncated__one"))
#             price_tag = card.find("div", string=re.compile(r"\$"))
#
#             events.append({
#                 "name": title_tag.get_text(strip=True) if title_tag else "Unknown Event",
#                 "url": "https://www.eventbrite.com" + link_tag['href'] if link_tag else "#",
#                 "address": location_tag.get_text(strip=True) if location_tag else "Online / Unknown",
#                 "description": "Eventbrite event",
#                 "price": price_tag.get_text(strip=True) if price_tag else "$0"
#             })
#         except Exception as e:
#             continue
#
#     #alt debugging yay
#     print("EVENTBRITE EVENT SAMPLE!!!!! ",events)
#
#     return events





#incercarea nr 2:)
# def get_eventbrite_events(keyword):
#     from bs4 import BeautifulSoup
#     import re
#
#     url = f"https://www.eventbrite.com/d/online/{keyword.replace(' ', '-')}/"
#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     events = []
#     cards = soup.select("div.eds-event-card-content__content")[:5]
#
#     for card in cards:
#         try:
#             title = card.select_one("div.eds-event-card-content__primary-content > a")
#             location = card.select_one("div.card-text--truncated__one")
#             price = card.find(string=re.compile(r"\$\d+"))
#
#             events.append({
#                 "name": title.get_text(strip=True) if title else "Unknown Event",
#                 "url": "https://www.eventbrite.com" + title['href'] if title and title.has_attr('href') else "#",
#                 "address": location.get_text(strip=True) if location else "Online / Unknown",
#                 "description": "Eventbrite event",
#                 "price": price if price else "$15"  # fallback price
#             })
#         except Exception as e:
#             continue
#
#     #debuug iar
#     print("EVENTBRITE EVENT SAMPLE!!!!!", events)
#     return events

#incercarea nr 3, acum using selenium ca altfel nu merge
# def get_eventbrite_events(keyword):
#     options = Options()
#     options.add_argument("--headless")  # browser runs in background
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#
#     driver = webdriver.Chrome(options=options)  # make sure chromedriver is in the project folder
#     url = f"https://www.eventbrite.com/d/online/{keyword.replace(' ', '-')}/"
#     driver.get(url)
#
#     time.sleep(4)  # wait for JS to load
#
#     events = []
#     # cards = driver.find_elements(By.CSS_SELECTOR, "div.eds-event-card-content__content")[:5]
#     #we need a more general one maybe
#     cards = driver.find_elements(By.CLASS_NAME, "search-event-card-wrapper")[:5]
#
#     for card in cards:
#         try:
#             title_elem = card.find_element(By.TAG_NAME, "h3")
#             name = title_elem.text
#             link_elem = card.find_element(By.TAG_NAME, "a")
#             link = link_elem.get_attribute("href")
#             price = "$15"
#             address = "Online"
#
#             events.append({
#                 "name": name,
#                 "url": link,
#                 "address": address,
#                 "description": "Eventbrite event",
#                 "price": price
#             })
#         except Exception:
#             continue
#
#     driver.quit()
#     print("EVENTBRITE EVENT SAMPLE:", events)
#     return events



#update cu eventuri hardcoded
def get_eventbrite_events(keyword):
    print("Using FAKE Eventbrite events...")

    return [
        {
            "name": f"{keyword.title()} Virtual Workshop",
            "url": "https://eventbrite.com/fake1",
            "address": "Online / Zoom",
            "description": "Eventbrite training session",
            "price": "$10"
        },
        {
            "name": f"{keyword.title()} Conference 2025",
            "url": "https://eventbrite.com/fake2",
            "address": "Online / Stream",
            "description": "Live keynote + Q&A",
            "price": "$15"
        },
        {
            "name": f"Beginner {keyword.title()} Crash Course",
            "url": "https://eventbrite.com/fake3",
            "address": "Virtual Room",
            "description": "Eventbrite event intro series",
            "price": "$20"
        }
    ]



@app.route("/", methods = ["GET"])
def home():
    category = request.args.get("category", "")
    date = request.args.get("date", "")
    address = request.args.get("address", "")
    keyword=request.args.get("keyword", "")

    ticketmaster_events = []
    eventbrite_events = get_eventbrite_events(keyword)

    if keyword:
        ticketmaster_events = get_ticketmaster_events (keyword, category, date, address)
        eventbrite_events = get_eventbrite_events(keyword)

    return render_template("index.html", events=ticketmaster_events)

if __name__ == "__main__":
    app.run(debug=True)
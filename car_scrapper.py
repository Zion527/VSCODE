from pprint import pprint
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def find_last_page_number():
    base_url = "https://www.nzkoreapost.com/bbs/board.php?bo_table=market_car"
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        last_page_link = soup.find("i", class_="fa-angle-double-right").parent
        if last_page_link:
            last_page_url = last_page_link.get("href")
            last_page_number = int(last_page_url.split("=")[-1])
            return last_page_number
    return 20


def scrape_car_list(base_url, max_pages):
    result = []
    for page in range(1, max_pages + 1):
        url = f"{base_url}&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all tr elements where display is not 'none'
            car_items = soup.find_all(
                "tr", style=lambda value: value is None or "none" not in value.lower()
            )

            # Print the car information
            for car_item in car_items:
                if car_item.find("td", class_="notice"):
                    continue
                elif car_item.find("td", class_="premium"):
                    continue
                elif car_item.find("td", class_="special"):
                    continue
                elif car_item.find("td", class_="special"):
                    continue

                title_td = car_item.find("td", class_="list-subject")
                link_url = title_td.find("a").get("href")
                title_text = title_td.find("a").text.strip()
                posted_at = car_item.find(
                    "td", class_="text-center en"
                ).text.strip()  # 조회 247 | 댓글 2 2023.12.25 (월) 06:41
                image_td = car_item.find("td", class_="list-img")
                if image_td is None:
                    thumb_image_url = None
                    image_url = None
                else:
                    thumb_image_url = image_td.find("img").get("src")
                    image_url = thumb_image_url.replace("thumb-", "").replace(
                        "_50x50", ""
                    )
                data = {
                    "title": title_text,
                    "link": link_url,
                    "thumb_image": thumb_image_url,
                    "image": image_url,
                }
                result.append(data)
        else:
            print(
                f"Error: Unable to retrieve the page (Status Code: {response.status_code})"
            )

    return result


# Base URL for the car listings
base_url = "https://www.nzkoreapost.com/bbs/board.php?bo_table=market_car"

# Maximum number of pages to scrape
max_pages = (
    1  # You can adjust this based on the actual number of pages you want to scrape
)

# Run the scraper
max_pages = find_last_page_number()
res = scrape_car_list(base_url, max_pages)

# Save the results to a JSON file
with open("car_list.json", "w", encoding="utf-8") as f:
    json.dump(
        res,
        f,
        ensure_ascii=False,
    )
# pprint(res)
print("DONE")
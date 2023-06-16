from bs4 import BeautifulSoup
from time import sleep
import json
import requests


aesthetic_list_html = open("data/list.html", 'r')

soup = BeautifulSoup(aesthetic_list_html, "html.parser")

tags = soup.find_all(attrs={"class": "twocolumn"})

links = []

for category in tags:
    link_tags = category.ul.find_all('li')
    category_links = [tag.a.get('href')
                      for tag in link_tags
                      if tag.a is not None]
    links += category_links

root_url = "https://aesthetics.fandom.com"

graph = {
    "nodes": [],
    "links": []
}

for link in links:
    # print(link)
    try:
        with open(f"data/{link.split('/')[-1]}.html", "r") as html_file:
            # print("used cache")
            html = html_file.read()
    except FileNotFoundError:
        with open(f"data/{link.split('/')[-1]}.html", "w") as html_file:
            sleep(2)
            res = requests.get(f"{root_url}{link}")
            # print("wrote cache")
            html_file.write(res.text)
            html = res.text

    soup = BeautifulSoup(html, 'html.parser')
    related_aesthetics_div = soup.find(
        'div', attrs={"data-source": "related_aesthetics"})

    if related_aesthetics_div is None:
        continue

    related_aesthetics_links = related_aesthetics_div.find_all("a")
    related_aesthetics = [ra.get('href') for ra in related_aesthetics_links]

    graph["links"] += [{"source": link, "target": ra}
                       for ra in related_aesthetics]

    title = soup.find('meta', property="og:title")
    if title is not None:
        title = title.get("content")

    url = soup.find('meta', property="og:url")
    if url is not None:
        url = url.get("content")

    description = soup.find(
        'meta', property="og:description")
    if description is not None:
        description = description.get("content")

    image_url = soup.find('meta', property="og:image")
    if image_url is not None:
        image_url = image_url.get("content")

    graph["nodes"].append({
        "id": link,
        "name": title,
        "value": len(related_aesthetics),
        "url": url,
        "description": description,
        "image_url": image_url
    })

with open("graph.json", 'w') as out_file:
    out_file.write(json.dumps(graph))

import requests
from rss_parser import Parser
from dotenv import load_dotenv
import dataset
import os
import guessit
from guessit.jsonutils import GuessitEncoder
import json
import mal
import tqdm
import datetime

load_dotenv()

db = dataset.connect(os.environ.get("DATABASE_URL", 'sqlite:///database.db'))
table = db["entry"]

url = "https://nyaa.si/?page=rss&c=1_0&f=0"
resp = requests.get(url)

parser = Parser(resp.content)

feed = parser.parse()

for i in tqdm.tqdm(feed.feed):
    title = i.title
    link = i.link
    data = guessit.guessit(title)
    jikan_data = json.dumps(mal.search(data["title"]))
    table.upsert(
        dict(title=title,
             link=link,
             jikan=jikan_data,
             guessit=json.dumps(data, cls=GuessitEncoder),
             now=datetime.datetime.now()),
        [
            'title',
        ],
    )

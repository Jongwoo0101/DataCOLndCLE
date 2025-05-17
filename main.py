import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

base_url = "https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?page={}&land_id=0&ausrichtung=Sturm&spielerposition_id=alle&altersklasse=alle&jahrgang=0&kontinent_id=0&plus=1"
players = []

for page in range(1, 50):
    print(f"Fetching page {page}...")
    url = base_url.format(page)
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "lxml")

    rows = soup.select("table.items > tbody > tr")

    for row in rows:
        try:
            # 이름
            name_tag = row.select_one("td:nth-of-type(2) table tr td:nth-of-type(2) a")
            name = name_tag.text.strip() if name_tag else ""

            # 나이
            age = row.select_one("td:nth-of-type(3)").text.strip()

            # 국적 (img alt)
            nationality_tag = row.select_one("td:nth-of-type(4) img")
            nationality = nationality_tag["title"] if nationality_tag else ""

            # 소속클럽 (img alt)
            club_tag = row.select_one("td:nth-of-type(5) img")
            club = club_tag["alt"] if club_tag else ""

            # 시장가치
            value_tag = row.select_one("td:nth-of-type(6) a")
            value = value_tag.text.strip() if value_tag else ""

            # 경기수
            appearances = row.select_one("td:nth-of-type(7)").text.strip()

            # 골
            goals = row.select_one("td:nth-of-type(8)").text.strip()

            # 어시스트
            assists = row.select_one("td:nth-of-type(10)").text.strip()

            # 옐로카드
            yellow = row.select_one("td:nth-of-type(11)").text.strip()

            # 레드카드
            red = row.select_one("td:nth-of-type(13)").text.strip()
            
            # 교체 인
            sub_in = row.select_one("td:nth-of-type(14)").text.strip()
            
            # 교체 아웃
            sub_out = row.select_one("td:nth-of-type(15)").text.strip()


            players.append({
                "이름": name,
                "나이": age,
                "국적": nationality,
                "소속클럽": club,
                "선수가치": value,
                "경기수": appearances,
                "골": goals,
                "어시스트": assists,
                "옐로카드": yellow,
                "레드카드": red,
                "교체인": sub_in,
                "교체아웃": sub_out,
            })

        except Exception as e:
            print("Row error:", e)
            continue

    time.sleep(1.5)

# CSV 저장
df = pd.DataFrame(players)
df.to_csv("most_valuable_forwards_fixed.csv", index=False, encoding="utf-8-sig")
print("정상적으로 저장 완료!")

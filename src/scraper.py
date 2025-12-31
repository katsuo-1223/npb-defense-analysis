import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time

# game_ids.csvを読み込む
game_ids_df = pd.read_csv('game_ids.csv')
game_ids = game_ids_df['game_id']

# 手動で指定した試合IDのリスト
# game_ids = ['2021019720', '2021019721', '2021019888']  # ここに任意の試合IDを入力

# すべての試合情報を格納するリスト
all_games_data = []

# 各試合IDに対してスクレイピングを実行
for game_id in game_ids:
    # スクレイピングしたいURLを設定
    url = f'https://baseball.yahoo.co.jp/npb/game/{game_id}/text'
    response = requests.get(url)

    if response.status_code == 200:
        # BeautifulSoupでHTMLを解析
        soup = BeautifulSoup(response.content, 'html.parser')

        # 対戦カードと日付を取得（先ほどの例に従って）
        # この部分はページの構造に応じて適宜修正してください
        match_card_tag = soup.find('h2', class_='bb-head01__title')
        match_card = match_card_tag.get_text(strip=True) if match_card_tag else 'カード不明'
        date_tag = soup.find('li', class_='bb-gameRound--matchDate')
        match_date = date_tag.get_text(strip=True) if date_tag else '日付不明'

        # 内容を取得（先ほどの例に従って）
        # この部分はページの構造に応じて適宜修正してください
        elements = soup.find_all(['p', 'h1'], class_=['bb-liveText__inning', 'bb-liveText__summary', 'bb-liveText__summary--change'])
        current_inning = ""
        for element in elements:
            if 'bb-liveText__inning' in element.get('class', []):
                current_inning = element.get_text(strip=True)
            elif 'bb-liveText__summary' in element.get('class', []):
                event_text = element.get_text(strip=True)
                all_games_data.append({
                    '対戦カード': match_card,
                    '日付': match_date,
                    '試合ID': game_id,
                    '回': current_inning,
                    '内容': event_text
                })
    else:
        print(f'試合ID {game_id} のページ取得に失敗しました。ステータスコード: {response.status_code}')

    # リクエスト間に遅延を設ける
    time.sleep(1)  # 1秒間の遅延

# 全試合の情報をDataFrameに変換
all_games_df = pd.DataFrame(all_games_data)

# DataFrameをCSVに保存
all_games_df.to_csv('all_baseball_data.csv', index=False, encoding='utf-8-sig')

print('全試合情報の取得とCSVへの保存が完了しました。')

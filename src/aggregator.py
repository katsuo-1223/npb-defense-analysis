import pandas as pd

# CSVファイルの読み込む際に必要なカラムのみ指定
columns_to_load = ['試合ID', '回', 'ボールの行方', '守備交代・守備変更後のポジション']
# df = pd.read_csv('sample_baseball_data2.csv', usecols=columns_to_load)
df = pd.read_csv('fixed_baseball_data.csv', usecols=columns_to_load)

#特定のIDだけを抽出
# df = df.query('試合ID == "2021014379"')

# NaN値を空文字列で置換（守備交代・守備変更後のポジション）
df['守備交代・守備変更後のポジション'] = df['守備交代・守備変更後のポジション'].fillna('')

# 守備交代・守備変更後のポジションがnullでないデータ（守備変更データ）とnullのデータ（打撃方向のデータ）をそれぞれ抽出
df_def_change = df[df['守備交代・守備変更後のポジション'] != '']
df_batting_direction = df[df['守備交代・守備変更後のポジション'] == '']

# print(df_def_change)
# print(df_batting_direction)

# df_def_changeの '試合ID' と '回' の組み合わせを取得
def_change_pairs = df_def_change[['試合ID', '回']].drop_duplicates()

# print(def_change_pairs)

# df_batting_directionから、def_change_pairsに含まれる '試合ID' と '回' の組み合わせを除外
df_batting_direction_except_def_change_innings = pd.merge(df_batting_direction, def_change_pairs, on=['試合ID', '回'],
                                how='left', indicator=True)

df_batting_direction_except_def_change_innings = df_batting_direction_except_def_change_innings[df_batting_direction_except_def_change_innings['_merge'] == 'left_only'].drop(columns=['_merge'])

# 守備変更データと打撃方向のデータを試合IDと回をキーに結合
merged_df = pd.merge(df_def_change, df_batting_direction, on=['試合ID', '回'], suffixes=('_def_change', '_batting_dir'))

# 守備変更データと打撃方向のデータを試合IDと回をキーに結合する前に、
# 'ボールの行方' 列を文字列型に変換します。
df_def_change['ボールの行方'] = df_def_change['ボールの行方'].astype(str)
df_batting_direction['ボールの行方'] = df_batting_direction['ボールの行方'].astype(str)

# 結合されたデータフレームの 'ボールの行方' 列が文字列型であることを確認する
merged_df['ボールの行方_batting_dir'] = merged_df['ボールの行方_batting_dir'].astype(str)
merged_df['守備交代・守備変更後のポジション_def_change'] = merged_df['守備交代・守備変更後のポジション_def_change'].astype(str)

# 打撃方向のデータのボールの行方が守備交代・守備変更後のポジションに含まれる回数を集計
count = merged_df.apply(lambda x: x['ボールの行方_batting_dir'] in x['守備交代・守備変更後のポジション_def_change'], axis=1).sum()

# 結果の出力
print(f"ボールの行方が守備交代・守備変更後のポジションに含まれる回数: {count}")
# 結合されたデータフレームのレコード数を出力する
print(f"結合されたデータフレームのレコード数: {merged_df.shape[0]}")

# 各ポジションでボールの行方が何回含まれるかを集計する
positions = ['ファースト', 'セカンド', 'サード', 'ショート', 'レフト', 'センター', 'ライト']
position_counts_batting_dir = {position: df_batting_direction_except_def_change_innings['ボールの行方'].str.contains(position, na=False).sum() for position in positions}

# ポジションごとの集計結果を出力する
for position, count in position_counts_batting_dir.items():
    print(f"{position}: {count}回")

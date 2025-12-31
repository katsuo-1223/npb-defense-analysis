import pandas as pd
import os

# 現在のディレクトリを取得
current_directory = os.getcwd()
print("Current Directory:", current_directory)

# CSVファイルの読み込み
# df = pd.read_csv('test_data2.csv')
df = pd.read_csv('all_baseball_data.csv')

# フィルタリングするキーワードのリスト
keywords = ['守備変更', '守備交代', 'ファースト', 'セカンド', 'サード', 'ショート', 'レフト', 'センター', 'ライト', 'ゴロ', 'ヒット', 'フライ']

# キーワードを含む行のみを残す
df_filtered = df[df['内容'].apply(lambda x: any(keyword in x for keyword in keywords))]

# ボールの行方を抽出
positions = ['ファースト', 'セカンド', 'サード', 'ショート', 'レフト', 'センター', 'ライト']
df_filtered['ボールの行方'] = df_filtered['内容'].apply(
    lambda x: next((pos for pos in positions if pos in x), None)
)

# 守備交代・守備変更が含まれる場合、ボールの行方をnullに設定
df_filtered.loc[df_filtered['内容'].str.contains('守備変更|守備交代'), 'ボールの行方'] = None

# 守備交代・守備変更後のポジションを抽出
def extract_position_change(text):
    if '守備交代' in text or '守備変更' in text:
        return ', '.join(pos for pos in positions if pos in text)
    return None

df_filtered['守備交代・守備変更後のポジション'] = df_filtered['内容'].apply(extract_position_change)

# ボールの行方と守備交代・守備変更後のポジションが両方nullの行を削除
df_filtered = df_filtered[~((df_filtered['ボールの行方'].isnull()) & (df_filtered['守備交代・守備変更後のポジション'].isnull()))]

# 必要なカラムのみを選択
df_sample = df_filtered[['試合ID', '内容', '回', 'ボールの行方', '守備交代・守備変更後のポジション']]

# 新しいCSVファイルとして保存
# df_sample.to_csv('sample_baseball_data2.csv', index=False, encoding='utf-8-sig')
df_sample.to_csv('fixed_baseball_data.csv', index=False, encoding='utf-8-sig')

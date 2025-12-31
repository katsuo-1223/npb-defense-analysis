from scipy.stats import chisquare

# 観測値
observed = [1366, 4322]  # ボールが飛んでくる回数、飛んでこない回数

# ボールが飛んでくる確率（任意の値を設定可能）
probability_ball_comes = 0.07

# 守備が交代した合計回数
total_trials = sum(observed)

# 期待値の計算
expected_ball_comes = total_trials * probability_ball_comes
expected_ball_not_comes = total_trials * (1 - probability_ball_comes)
expected = [expected_ball_comes, expected_ball_not_comes]

# カイ二乗適合度検定の実行
chi2, p = chisquare(f_obs=observed, f_exp=expected)

# 結果の出力
print(f"カイ二乗統計量: {chi2}")
print(f"P値: {p}")

# 結果の解釈
if p < 0.05:
    print("観測された分布は期待される分布と異なります（帰無仮説を棄却）。")
else:
    print("観測された分布は期待される分布と有意な差がありません（帰無仮説を採択）。")

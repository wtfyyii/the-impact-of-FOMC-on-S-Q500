import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# 抓資料
sp500 = yf.download("^GSPC", start="2018-01-01", end="2025-05-28", auto_adjust=False)
sp500.reset_index(inplace=True)

# FOMC 日期
fomc_dates = [
    datetime(2018, 1, 31), datetime(2018, 3, 21), datetime(2018, 6, 13), datetime(2018, 9, 26), datetime(2018, 12, 19),
    datetime(2019, 1, 30), datetime(2019, 3, 20), datetime(2019, 6, 19), datetime(2019, 9, 18), datetime(2019, 12, 11),
    datetime(2020, 1, 29), datetime(2020, 3, 15), datetime(2020, 4, 29), datetime(2020, 6, 10), datetime(2020, 9, 16), datetime(2020, 12, 16),
    datetime(2021, 1, 27), datetime(2021, 3, 17), datetime(2021, 6, 16), datetime(2021, 9, 22), datetime(2021, 12, 15),
    datetime(2022, 1, 26), datetime(2022, 3, 16), datetime(2022, 6, 15), datetime(2022, 9, 21), datetime(2022, 12, 14),
    datetime(2023, 3, 22), datetime(2023, 6, 14), datetime(2023, 9, 20), datetime(2023, 12, 13),
    datetime(2024, 3, 20), datetime(2024, 6, 19), datetime(2024, 9, 18), datetime(2024, 12, 11),
    datetime(2025, 3, 19), datetime(2025, 6, 18)
]

event_data = []

for event_date in fomc_dates:
    window = sp500[(sp500['Date'] >= event_date - timedelta(days=3)) &
                   (sp500['Date'] <= event_date + timedelta(days=3))].copy()

    window['EventDate'] = event_date
    window['DaysFromEvent'] = (window['Date'] - event_date).dt.days
    window['Return'] = window['Close'].pct_change()
    event_data.append(window)

event_df = pd.concat(event_data, ignore_index=True)

# 確認欄位
print("✅ 欄位名稱：", event_df.columns.tolist())
print(event_df[['Date', 'DaysFromEvent', 'Return']].head())

# 如果欄位是 MultiIndex，就轉成單層欄位
if isinstance(event_df.columns, pd.MultiIndex):
    event_df.columns = ['_'.join(map(str, col)).strip() for col in event_df.columns]


# 儲存為 Excel 檔案
event_df.to_excel("d:/python/final/fomc_event_data.xlsx", index=False)

print("📁 成功儲存 Excel 檔案：fomc_event_data.xlsx")
print("🧾 欄位名稱為：", event_df.columns.tolist())

# 要畫的相對日期列表
target_days = [-2, -1, 0, 1, 2]
labels = {-2: "Day -2", -1: "Day -1", 0: "Day 0", 1: "Day 1", 2: "Day 2"}

# 畫圖
plt.figure(figsize=(10, 6))

for day in target_days:
    subset = event_df[event_df['DaysFromEvent_'] == day]['Return_'].dropna()
    sns.kdeplot(subset, label=labels[day], linewidth=2)

# 製圖美化
plt.axvline(x=0, color='black', linestyle='--', linewidth=1)
plt.title("S&P 500 Return Distribution (Day -2 to Day 2 around FOMC)")
plt.xlabel("Daily Return")
plt.ylabel("Density")
plt.legend(title="Days From Event")
plt.grid(True)
plt.tight_layout()
plt.show()
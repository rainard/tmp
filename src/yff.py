#coding: utf-8
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf

# 定义股票代码（ADATA 在台湾证券交易所的代码是 3260.TW）
ticker = "3260.TW"

# 获取股票数据
data = yf.download(ticker, start="2022-01-01", end="2023-01-01")


# 绘制蜡烛图
mpf.plot(data, type='candle', style='charles', title=f'{ticker} Candlestick Chart (2022)', ylabel='Price (TWD)', volume=True, figratio=(10, 6))


# 绘制股票价格图表
# plt.figure(figsize=(10, 6))
# plt.plot(data['Close'], label='ADATA Close Price', color='blue')
# plt.title(f'{ticker} Stock Price (2022)')
# plt.xlabel('Date')
# plt.ylabel('Price (TWD)')
# plt.legend()
# plt.grid()
# plt.show()


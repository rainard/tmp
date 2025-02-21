import adata
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 定义股票代码（300468 是 A 股中的股票代码）
ticker = '300468'
start_date = '2021-01-01'
save_file = "{}-{}-data.csv".format(ticker, start_date)
fig = plt.figure(dpi=150)

# 获取股票数据
# 假设 adata 的用法类似于 yfinance，具体方法请参考 adata 的文档
data =  pd.read_csv(save_file, index_col=0, parse_dates=True)
# 确保数据格式符合 mplfinance 的要求
# mplfinance 需要的数据列包括：Open, High, Low, Close, Volume
data = data[['open', 'high', 'low', 'close', 'volume']]
data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']  # 重命名列
data.index.name = 'Date'  # 确保索引是日期

# 创建子图
fig, axes = mpf.plot(data, type='candle', style='charles', title=f'{ticker} Candlestick Chart (2022)', ylabel='Price (CNY)', volume=True, figratio=(10, 6), returnfig=True)

# 添加十字线和提示功能
ax_main = axes[0]  # 主图区域
ax_volume = axes[2]  # 成交量区域

# 初始化十字线
vline = ax_main.axvline(color='gray', linestyle='--', alpha=0)  # 垂直线
hline = ax_main.axhline(color='gray', linestyle='--', alpha=0)  # 水平线
text = ax_main.text(0.01, 0.99, '', transform=ax_main.transAxes, verticalalignment='top', color='red')

# 鼠标移动事件处理函数
def on_mouse_move(event):
    if event.inaxes == ax_main:  # 检查鼠标是否在主图区域
        x = event.xdata  # 获取鼠标的 x 坐标（日期）
        y = event.ydata  # 获取鼠标的 y 坐标（价格）
        if x is not None and y is not None:
            # 找到最接近的日期
            date_index = int(round(x))
            if 0 <= date_index < len(data):
                date = data.index[date_index]
                price = data['Close'].iloc[date_index]
                # 更新十字线位置
                vline.set_xdata([x, x])
                hline.set_ydata([y, y])
                vline.set_alpha(1)
                hline.set_alpha(1)
                # 更新提示文本
                text.set_text(f'Date: {date.date()}\nClose: {price:.2f} CNY')
                fig.canvas.draw_idle()  # 更新图表
        else:
            # 鼠标离开主图区域时隐藏十字线和提示
            vline.set_alpha(0)
            hline.set_alpha(0)
            text.set_text('')
            fig.canvas.draw_idle()
    elif event.inaxes == ax_volume:  # 检查鼠标是否在成交量区域
        vline.set_alpha(0)
        hline.set_alpha(0)
        text.set_text('')
        fig.canvas.draw_idle()

# 绑定鼠标移动事件
fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

# 显示图表
plt.show()
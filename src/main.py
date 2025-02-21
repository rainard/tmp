#coding=utf-8
import adata
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from matplotlib.widgets import RectangleSelector
import tools 


# 设置代理,代理是全局设置,代理失效后可重新设置。参数:ip,proxy_url
#adata.proxy(is_proxy=True, ip='60.167.21.27:1133')

#获取所有的股票代码的函数
def all_code():
    res_df = adata.stock.info.all_code()
    print(res_df)

#获取股票的行情数据
def stock_quote(data,ticker):
    # dataframe生成k线图
    

    print(data) 
    
    # dataframe生成k线图
    fig, axes = mpf.plot(
        data, 
        type='candle', 
        style='yahoo', 
        title=f'{ticker} Candlestick Chart', 
        ylabel='Price', 
        volume=True, 
        # figratio=(10, 6),
        figratio=(10, 6),
        mav=(10, 20, 30),  # 整数，或包含整数的列表/元组
        show_nontrading=False,  # 显示非交易日的蜡烛图
         returnfig=True,
        # tight_layout=True,
        
    )
    
    ax_main = axes[0]  # 主图区域
    ax_volume = axes[2]  # 成交量区域

    # 保存初始的 x 轴和 y 轴范围
    initial_xlim = ax_main.get_xlim()
    initial_ylim = ax_main.get_ylim()

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
                    price = data['close'].iloc[date_index]
                    # 更新十字线位置
                    vline.set_xdata([x, x])
                    hline.set_ydata([y, y])
                    vline.set_alpha(1)
                    hline.set_alpha(1)
                    # 更新提示文本
                    text.set_text(f'Date: {date.date()}\nclose: {price:.2f} CNY')
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

    # 框选放大功能
    # 框选放大功能（仅放大缩小横轴）
    def on_select(eclick, erelease):
        x1, x2 = eclick.xdata, erelease.xdata  # 框选的 x 范围
        if x1 is not None and x2 is not None:
            ax_main.set_xlim(min(x1, x2), max(x1, x2))  # 仅设置 x 轴范围
            fig.canvas.draw_idle()  # 更新图表

    # 初始化 RectangleSelector
    rect_selector = RectangleSelector(
        ax_main,
        on_select,
        useblit=True,
        button=[1],  # 左键框选
        minspanx=5,  # 最小 x 方向跨度
        minspany=0,  # 不需要 y 方向跨度
        spancoords='pixels',
        interactive=True
    )


    # 按 ESC 键还原初始大小
    def on_key_press(event):
        if event.key == 'escape':  # 按下 ESC 键
            ax_main.set_xlim(initial_xlim)  # 还原 x 轴范围
            ax_main.set_ylim(initial_ylim)  # 还原 y 轴范围
            fig.canvas.draw_idle()  # 更新图表

    # 绑定事件
    #fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)  # 鼠标移动事件
    fig.canvas.mpl_connect('key_press_event', on_key_press)  # 按键事件
    plt.grid()
    plt.show()
    
    ##################### 绘制股票价格图表 ############
    #plt.figure(figsize=(10, 6))
    #plt.plot(data['close'], label='ADATA close Price', color='blue')
    #plt.title(f'{ticker} Stock Price (2022)')
    #plt.xlabel('Date')
    #plt.ylabel('Price (TWD)')
    #plt.legend()
    #plt.grid()
    #plt.show()


# QW1:=(HIGH+LOW+CLOSE*2)/4;
# QW3:=EMA(QW1,10);
# QW4:=STD(QW1,10);
# QW5:=(QW1-QW3)*100/QW4;
# QW6:=EMA(QW5,5);
# RK7:=EMA(QW6,10);
# 涨:EMA(QW6,10)+100/2-5

# 实现上方10行到16行的通达信公式




#main入口
if __name__ == '__main__':
    ticker = '300468'
    start_date = '2010-01-01'
    filter_date = '2014-03-01'
    save_file = "300468-data.csv".format(ticker, start_date)
    fig = plt.figure(dpi=150)
    # k_type: k线类型：1.日；2.周；3.月 默认：1 日k
    #data = adata.stock.market.get_market(stock_code=ticker, k_type=1, start_date=start_date)
    #data.set_index('trade_date', inplace=True)
    #data = data.set_index('trade_date')
    # 将设置好索引的 DataFrame 保存到 CSV 文件，这里因为 trade_date 已成为索引，所以 index 为 True 保存索引
    #data.to_csv(save_file, index=True)
    data =  pd.read_csv(save_file, index_col=0, parse_dates=True)
    
    #计算5,10日均线，并保存回去
    data['m5'] = data['close'].rolling(window=5).mean().round(2)
    data['m10'] = data['close'].rolling(window=10).mean().round(2)
    
    
    # 计算SuperWave指标
    CLOSE=data.close.values
    HIGH=data.high.values
    LOW=data.low.values
    data['wave']=tools.SuperWave(CLOSE,HIGH,LOW,10).round(2)
    
    data.to_csv(save_file, index=True)
    print(data)
    
    #过滤data数据
    #filtered_data = data[data.index >= filter_date]
    #stock_quote(filtered_data,ticker)

#coding:utf-8
from  MyTT import *            #myTT麦语言工具函数指标库  https://github.com/mpquant/MyTT


def SuperWave(CLOSE, HIGH, LOW, N=10):
    """
    计算SuperWave指标

    参数:
    CLOSE (numpy.ndarray): 收盘价数组
    HIGH (numpy.ndarray): 最高价数组
    LOW (numpy.ndarray): 最低价数组
    N (int, optional): 计算周期，默认为10

    返回:
    numpy.ndarray: SuperWave指标数组
    """
    # 计算QW1指标，即(HIGH + LOW + CLOSE * 2) / 4
    QW1 = ((HIGH + LOW + CLOSE * 2) / 4).round(2)
    print('QW1=',RET(QW1, 1))

    # 计算QW3指标，即QW1的N周期指数移动平均线
    QW3 = (EMA(QW1, N)).round(3)
    print('QW3=',RET(QW3, 1))

    # 计算QW4指标，即QW1的N周期标准差
    QW4 = (STD(QW1, N)).round(2)
    print('QW4=',RET(QW4, 1))

    # 计算QW5指标，即(QW1 - QW3) * 100 / QW4
    QW5 = ((QW1 - QW3) * 100 / QW4).round(2)
    print('QW5=',RET(QW5, 1))

    # 计算QW6指标，即QW5的5周期指数移动平均线
    QW6 = (EMA(QW5, 5)).round(2)
    print('QW6=',RET(QW6, 1))

    # 返回SuperWave指标，即QW6的10周期指数移动平均线 + 100 / 2 - 5
    return EMA(QW6, 10) + 45
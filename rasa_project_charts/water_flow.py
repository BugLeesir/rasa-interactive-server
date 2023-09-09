import pymysql
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

def get_water_flow_data(place:str):
    conn = pymysql.connect(host='43.142.246.112', port=3306, user='common', password='common666', db='hydrology',
                           charset='utf8')
    cur = conn.cursor(pymysql.cursors.DictCursor)  # 生成游标对象
    sql = f"select * from waterlevel where station_id in (select station_id from hydrometric_station where name='{place}' )"
    cur.execute(sql)
    w = cur.fetchall()

    stage = np.array([d["water_level"] for d in w])  # 提取水位值
    discharge = np.array([d["flow_rate"] for d in w])  # 提取流量值

    # 定义模型函数
    def model(x, a, b):
        return a * x + b

    # 拟合最小二乘法
    p0 = [1, 1]  # 初始参数值
    popt, pcov = opt.curve_fit(model, stage, discharge, p0)  # 使用curve_fit函数求解最优参数值
    a, b = popt  # 最优参数值

    # 绘制图像
    plt.plot(stage, discharge, "bo", label="actual")  # 绘制实际数据点，蓝色圆点
    plt.plot(stage, model(stage, a, b), "r-", label="fit")  # 绘制拟合曲线，红色实线
    plt.title("WaterLevelAndFlowRelationshipLine")  # 添加标题
    plt.xlabel("waterlevel（m）")  # 添加x轴标签
    plt.ylabel("flowrate（m^3 /s）")  # 添加y轴标签
    plt.legend()  # 添加图例
    plt.savefig(f'./water_flow_charts/{place}.png')

    cur.close()
    conn.close()

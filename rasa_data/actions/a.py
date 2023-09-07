import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import pymysql


conn = pymysql.connect(host='43.142.246.112', port=3306, user='common', password='common666', db='hydrology', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor) # 生成游标对象
sql=f"select water_level from waterlevel"
cur.execute(sql)
stage=cur.fetchall()
sql=f"select flow_rate from waterlevel"
cur.execute(sql)
discharge=cur.fetchall()


cur.close()
conn.close()

# 定义模型函数
def model(x, a, b, c):
    return a * x ** b + c # y = a * x ** b + c

# 拟合最小二乘法
p0 = [1, 1, 1] # 初始参数值
popt, pcov = opt.curve_fit(model, stage, discharge, p0) # 使用curve_fit函数求解最优参数值
a, b, c = popt # 最优参数值
print("最优参数值为：", a, b, c)

# 绘制图像
plt.plot(stage, discharge, "bo", label="实际数据") # 绘制实际数据点，蓝色圆点
plt.plot(stage, model(stage, a, b, c), "r-", label="拟合曲线") # 绘制拟合曲线，红色实线
plt.title("水位流量关系曲线") # 添加标题
plt.xlabel("水位（米）") # 添加x轴标签
plt.ylabel("流量（立方米/秒）") # 添加y轴标签
plt.legend() # 添加图例
plt.show() # 显示图像
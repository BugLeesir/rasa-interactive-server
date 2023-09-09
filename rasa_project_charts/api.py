from flask import Flask, jsonify, send_file, request
from knowledge_graph import graph_data
from water_flow import get_water_flow_data
import os
import time
app = Flask(__name__)


@app.route("/get_water_flow_data", methods=["post"])
def get_water_level_data():
    base_path="./water_flow_charts"
    place=request.json.get("place")
    img_path=f"{base_path}/{place}.png"

    if not os.path.exists(img_path):
        get_water_flow_data(place)

    return send_file(img_path,mimetype="image/png")


@app.route("/get_graph_data", methods=["POST"])
def get_graph_data():
    graph_data_dict = graph_data()
    return jsonify(graph_data_dict)


# 每隔半个小时就会删除water_flow_charts文件夹下的所有文件
def del_water_flow_charts():
    folder_path="./water_flow_charts"

    while True:
        try:
            for filename in os.listdir(folder_path):
                file_path=os.path.join(folder_path,filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"删除文件{file_path}时出错：{e}")

            time.sleep(60*30)
        except KeyboardInterrupt:
            # 如果按下Ctrl+C，退出循环
            break


if __name__ == "__main__":
    app.run(debug=True)

    del_water_flow_charts()
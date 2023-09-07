from flask import Flask, jsonify
import pandas as pd
from knowledge_graph import graph_data


app = Flask(__name__)

data = pd.DataFrame({
    "time": [1, 2, 3],
    "water_level": [10, 15, 12],
    "flow_rate": [5, 8, 6]
})


@app.route("/get_water_flow_data")
def get_water_level_data():
    return jsonify(data.to_dict(orient="records"))


@app.route("/get_graph_data", methods=["POST"])
def get_graph_data():
    graph_data_dict = graph_data()
    return jsonify(graph_data_dict)


if __name__ == "__main__":
    app.run(debug=True)

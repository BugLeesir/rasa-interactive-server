from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

data = pd.DataFrame({
    "time": [1, 2, 3],
    "water_level": [10, 15, 12],
    "flow_rate": [5, 8, 6]
})


@app.route("/get_water_flow_data")
def get_water_level_data():
    return jsonify(data.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)

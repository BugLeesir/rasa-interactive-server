# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# from typing import Any, Text, Dict, List

# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.forms import FormAction
# import requests

# class ActionWeatherAPI(Action):
#     def name(self) -> Text:
#         return "action_weather_api"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         location = tracker.get_slot('location')
#         api_key = "7a2f481009dc95e40c26d42351201246"
#         api_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric&lang=zh_cn"
#         response = requests.get(api_url)
#         response_json = response.json()
#         weather_description = response_json["weather"][0]["description"]
#         temperature = response_json["main"]["temp"]
#         weather_info = f"天气：{weather_description}，温度：{temperature}°C"
#         dispatcher.utter_message(template="utter_weather_info", weather_info=weather_info)
#         return []

import requests
import pymysql
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet


class WeatherAPIAction(Action):
    def name(self) -> Text:
        return "action_weather_api"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: DomainDict) -> List[Dict[Text, Any]]:
        location=tracker.get_slot("location")
        dispatcher.utter_message(f"你来自{location},现在程序正在开发中，请勿着急")
        return []
    
class ActionFillLocationByLatestMassage(Action):
    def name(self) -> Text:
        return "action_fill_location_by_latest_massage"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 获取用户位置

        location=tracker.latest_message.get('text') # 将用户回答的位置作为location
        # 将槽填充
        return [SlotSet('location',location)]


class ActionSearchHydrometricStationByName(Action):
    def name(self) -> Text:
        return "action_search_hydrometric_station_by_name"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        stationName=tracker.get_slot("stationName")

        # dispatcher.utter_message(f"名字是{stationName}")

        # 连接数据库
        conn = pymysql.connect(host='43.142.246.112', port=3306, user='common', password='common666', db='hydrology', charset='utf8')
        cur = conn.cursor(pymysql.cursors.DictCursor) # 生成游标对象
        sql=f"select * from hydrometric_station where name='{stationName}'"
        cur.execute(sql)
        data=cur.fetchall()
        cur.close()
        conn.close()
        if data :
            data_item = data[0]  # 获取列表中的第一个字典
            dispatcher.utter_message(f"已查询到河道站\n 河道站编号：{data_item['station_id']} 河道站名称：{data_item['name']} 河流名称：{data_item['river_name']} 水系名称：{data_item['hydrographic_net_name']} 建站名称：{data_item['esDate']} 站点位置:{data_item['location']}")
        else :
            dispatcher.utter_message("未查询到河道站,抱歉")    
        
        resetSlot="false"

        return[SlotSet('stationName', resetSlot)]

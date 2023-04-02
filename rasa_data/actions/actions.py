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
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

class WeatherAPIAction(Action):
    def name(self) -> Text:
        return "action_weather_api"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: DomainDict) -> List[Dict[Text, Any]]:
        api_key = "7a2f481009dc95e40c26d42351201246"
        location = tracker.latest_message['text']
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + location
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] != "404":
            weather = data["weather"][0]["description"]
            temperature = round(float(data["main"]["temp"]) - 273.15, 2)
            wind_speed = data["wind"]["speed"]
            dispatcher.utter_message(template="utter_weather_info", weather_description=weather, temperature=temperature, wind_speed=wind_speed)
        else:
            dispatcher.utter_message(template="utter_weather_error")
        return []
    
class ActionFillLocation(Action):
    def name(self) -> Text:
        return "action_fill_location"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 获取用户位置
        location=tracker.latest_message.get('text')
        # 将槽填充
        return [SlotSet('location',location)]
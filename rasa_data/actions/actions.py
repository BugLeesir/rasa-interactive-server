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
            dispatcher.utter_message(f"已查询到河道站")
            dispatcher.utter_message(f"河道站编号：{data_item['station_id']}")
            dispatcher.utter_message(f"河道站名称：{data_item['name']}")
            dispatcher.utter_message(f"河流名称：{data_item['river_name']}")
            dispatcher.utter_message(f"水系名称：{data_item['hydrographic_net_name']}")
            dispatcher.utter_message(f"建站名称：{data_item['esDate']}")
            dispatcher.utter_message(f"站点位置: {data_item['location']}")
        else :
            dispatcher.utter_message("未查询到河道站,抱歉")    
        
        resetSlot="false"

        return[SlotSet('stationName', resetSlot)]

class ActionFillHydrometricStationByLatestMassege(Action):
    def name(self) -> Text:
        return "action_fill_hydrometric_station_by_latest_massege"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        stationName=tracker.latest_message.get('text') 

        # 将槽填充
        return [SlotSet('stationName',stationName)]


class ActionFillWaveSpeedCoefByLatestMassaege(Action):
    def name(self) -> Text:
        return "action_fill_waveSpeedcoef_by_latest_massage"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        waveSpeedcoef=tracker.latest_message.get('text') # 将用户回答作为波速系数
        # 将槽填充
        return [SlotSet('waveSpeedcoef',waveSpeedcoef)]


class ActionFillUpStationByLatestMassage(Action):
    def name(self) -> Text:
        return "action_fill_up_station_by_latest_massage"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        upStation=tracker.latest_message.get('text') # 将用户回答作为上河道站

        # 将槽填充
        return [SlotSet('upStation',upStation)]

class ActionFillDownStationByLatestMassage(Action):
    def name(self) -> Text:
        return "action_fill_down_station_by_latest_massage"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        downStation=tracker.latest_message.get('text') # 将用户回答作为下河道站
        # 将槽填充
        return [SlotSet('downStation',downStation)]
    
class CalculateTheFloodTransmissionTime(Action):
    def name(self) -> Text:
        return "action_calculate_the_flood_transmission_time"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        waveSpeedcoef=tracker.get_slot("waveSpeedcoef")
        upStation=tracker.get_slot("upStation")
        downStation=tracker.get_slot("downStation")
        
        # 连接数据库
        conn = pymysql.connect(host='43.142.246.112', port=3306, user='common', password='common666', db='hydrology', charset='utf8')
        cur = conn.cursor(pymysql.cursors.DictCursor) # 生成游标对象
        sql=f"select * from hydrometric_station where name='{upStation}'"
        cur.execute(sql)
        upStationTemp=cur.fetchall()
        if len(upStationTemp)==0:
            dispatcher.utter_message("上河道站信息缺少抱歉,抱歉")
            return []
        upStationTempItem=upStationTemp[0]
        upStationID=upStationTempItem['station_id']
        sql=f"select * from waterlevel where station_id='{upStationID}'"
        cur.execute(sql)
        upStationData=cur.fetchall()
        if len(upStationData)==0:
            dispatcher.utter_message("上河道站缺少水位流量信息，抱歉")
            return []
        sql=f"select * from hydrometric_station where name='{downStation}'"
        cur.execute(sql)
        downStationTemp=cur.fetchall()
        if len(downStationTemp)==0:
            dispatcher.utter_message("下河道站信息缺少抱歉,抱歉")
            return []
        downStationTempItem=downStationTemp[0]
        downStationID=downStationTempItem['station_id']
        sql=f"select * from waterlevel where station_id='{downStationID}'"
        cur.execute(sql)
        downStationData=cur.fetchall()
        if len(downStationData)==0:
            dispatcher.utter_message("下河道站缺少水位流量信息，抱歉")
            return []
        cur.close()
        conn.close()

        # 计算洪水传播时间

        upStationDataItem=upStationData[0]
        downStationDataItem=downStationData[0]

        Q1=upStationDataItem['flow_rate']
        Q2=downStationDataItem['flow_rate']    # 获取两个站点的流量

        # Z1=upStationDataItem['water_level']
        # Z2=downStationDataItem['water_level']  # 获取两个站点的水位线（可能要判断是否达到警戒线？）

        

        L=10000                                # 假定两个站点之间距离10km

        V=(Q1+Q2)/2                            # 计算断面平均流量

        u=float(waveSpeedcoef)*V                      # 计算波速

        t=L/u                                  # 计算洪水传播时间

        format_time=round(t,2)                 # 保留两位小数

        dispatcher.utter_message(f"洪水传播时间：{format_time}s")

        return []
    
class ActionSearchPrecipitationByName(Action):
    def name(self) -> Text:
        return "action_search_precipitation_by_name"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        place=tracker.get_slot("place")

        # dispatcher.utter_message(f"{place}")
  
        # 连接数据库
        conn = pymysql.connect(host='43.142.246.112', port=3306, user='common', password='common666', db='hydrology', charset='utf8')
        cur = conn.cursor(pymysql.cursors.DictCursor) # 生成游标对象
        sql=f"select * from hydrometric_station where name='{place}'"
        cur.execute(sql)
        data=cur.fetchall()

        if data :
            data_item = data[0]  # 获取列表中的第一个字典
            station_id=data_item['station_id']
            sql=f"select * from waterlevel where station_id={station_id}"  
            cur.execute(sql)
            data=cur.fetchall()
            if data :
                data_item = data[0]
                dispatcher.utter_message(f"{place}的降水量是 {data_item['precipitation'] } mm")
            else :
                dispatcher.utter_message("未查询到该地的降水量，抱歉")
        else :
            dispatcher.utter_message("未查询到该地的降水量，抱歉")    
        
        cur.close()
        conn.close()
        
        resetSlot="false" # 将槽重置

        return[SlotSet('place', resetSlot)]


class ActionFillPlaceByLatestMassage(Action):
    def name(self) -> Text:
        return "action_fill_place_by_latest_massage"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
         
        place=tracker.latest_message.get('text') # 将用户回答作为用户的位置

        # 将槽填充
        return [SlotSet('place',place)]
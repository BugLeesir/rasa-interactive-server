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
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import pandas as pd
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet


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
        
        resetSlot=None # 将槽重置

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
    
class ActionGetKnowledgeGraph(Action):
    def name(self) -> Text:
        return "action_get_knowledge_graph"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        graph = Graph('bolt://43.142.246.112:7687',auth=('neo4j','common666'))
        cypher1 = "match (n:riverstation) return n.name as node"
        cypher2 = "match (n:riverstation)-[r]->(m:riverstation) return STARTNODE(r) as source,ENDNODE(r) as target,r.time as time"
        node_df = graph.run(cypher1).to_data_frame()
        edge_df = graph.run(cypher2).to_data_frame()
        dispatcher.utter_message(f"test")
        return []
    
class ActionGetFloodTime(Action):
    def name(self):
        return "action_get_flood_time"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        source_station = tracker.get_slot("source_station")
        destination_station = tracker.get_slot("destination_station")
        graph = Graph('bolt://43.142.246.112:7687', auth=('neo4j', 'common666'))
        cypher1 = "match (n:riverstation) return n.name as node"
        cypher2 = ("match (n:riverstation)-[r]->(m:riverstation) return STARTNODE(r) as source,ENDNODE(r) as target,"
                   "r.time as time")
        node_df = graph.run(cypher1).to_data_frame()
        edge_df = graph.run(cypher2).to_data_frame()
        # 数据处理
        node_list = node_df["node"].tolist()
        source_list = edge_df["source"].tolist()
        target_list = edge_df["target"].tolist()
        time_list = edge_df["time"].tolist()
        edge_list = list()
        for i in range(len(source_list)):
            edge_list.append([source_list[i]["name"], target_list[i]["name"], time_list[i]])
        # 构造邻接矩阵
        inf = 999999
        adj_matrix = [[inf for i in range(len(node_list))] for j in range(len(node_list))]
        for i in range(len(adj_matrix)):
            adj_matrix[i][i] = 0
        for relation in edge_list:
            x = node_list.index(relation[0])
            y = node_list.index(relation[1])
            adj_matrix[x][y] = relation[2]
        start = node_list.index(source_station)
        end = node_list.index(destination_station)
        # dijkstra算法
        passed = [start]
        nopass = [x for x in range(len(adj_matrix)) if x != start]
        dis = adj_matrix[start]

        while len(nopass):
            idx = nopass[0]
            for i in nopass:
                if dis[i] < dis[idx]: idx = i
            nopass.remove(idx)
            passed.append(idx)
            for i in nopass:
                if dis[idx] + adj_matrix[idx][i] < dis[i]: dis[i] = dis[idx] + adj_matrix[idx][i]
        dispatcher.utter_message(f"从{source_station}到{destination_station}的洪水传播时间为{dis[end]} h")
        return [SlotSet("source_station", None), SlotSet("destination_station", None)]
    

        


        
class ActionResetSourceStationSlot(Action):
    def name(self):
        return "action_reset_source_station_slot"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("source_station", None)]
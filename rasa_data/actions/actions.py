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
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

class ActionSearchHydrometricStationByName(Action):
    def name(self) -> Text:
        return "action_search_hydrometric_station_by_name"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        stationName=tracker.get_slot("stationName")

        # dispatcher.utter_message(f"名字是{stationName}")

        # 连接数据库
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='143323', db='hydrology', charset='utf8')
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

  
        # 连接数据库
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='143323', db='hydrology', charset='utf8')
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
    

class ActionDrawWaterLevelAndFlowRelationshipLine(Action):
    def name(self) -> Text:
        return "action_draw_water_level_and_flow_relationship_line_by_name"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        place=tracker.get_slot("water_line_place")

        conn = pymysql.connect(host='localhost', port=3306, user='root', password='143323', db='hydrology', charset='utf8')
        cur = conn.cursor(pymysql.cursors.DictCursor) # 生成游标对象
        sql=f"select * from waterlevel where station_id in (select station_id from hydrometric_station where name='{place}' )"
        cur.execute(sql)
        w=cur.fetchall()



        stage = np.array([d["water_level"] for d in w]) # 提取水位值
        discharge = np.array([d["flow_rate"] for d in w]) # 提取流量值

        # 定义模型函数
        def model(x, a, b):
            return a * x + b

        # 拟合最小二乘法
        p0 = [1, 1] # 初始参数值
        popt, pcov = opt.curve_fit(model, stage, discharge, p0) # 使用curve_fit函数求解最优参数值
        a, b = popt # 最优参数值

        # 绘制图像
        plt.plot(stage, discharge, "bo", label="actual") # 绘制实际数据点，蓝色圆点
        plt.plot(stage, model(stage, a, b), "r-", label="fit") # 绘制拟合曲线，红色实线
        plt.title("WaterLevelAndFlowRelationshipLine") # 添加标题
        plt.xlabel("waterlevel（m）") # 添加x轴标签
        plt.ylabel("flowrate（m^3 /s）") # 添加y轴标签
        plt.legend() # 添加图例
        plt.savefig('savefig_example.png')



        cur.close()
        conn.close()
        dispatcher.utter_message(f"已查询到{place}的水位流量关系曲线")
        return [SlotSet("water_line_place", None)]
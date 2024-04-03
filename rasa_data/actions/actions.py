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

        print(place)
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
    
    class ActionSearchLatestFlowRateByName(Action):
        def name(self) -> Text:
            return "action_search_latest_flow_rate_by_name"
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            place=tracker.get_slot("place")
            conn = pymysql.connect(host='localhost', port=3306, user='root', password='143323', db='hydrology', charset='utf8')
            cur = conn.cursor(pymysql.cursors.DictCursor)
            # 从waterlevel表中查询流量值,按照time降序排列，取第一个值
            sql=f"select * from waterlevel where station_id in (select station_id from hydrometric_station where name='{place}' ) order by time desc limit 1"
            cur.execute(sql)
            w=cur.fetchall()
            if w:
                data_item = w[0]
                dispatcher.utter_message(f"{place}的流量是{data_item['flow_rate']} m^3/s")
            else:
                dispatcher.utter_message("未查询到该地的流量，抱歉")
            cur.close()
            conn.close()
            return [SlotSet("place", None)]


    class ActionTellJoke(Action):
           def name(self):
               return "action_tell_joke"

           def run(self, dispatcher, tracker, domain):
               jokes = [
                   "第一个知道牛奶可以喝的家伙,你到底对牛做了什么",
                   "当金钱站出来说话时，所有“真理”都沉默了。",
                   "“特别能吃苦”这5个字，我想了想，我做到了前4 个……",
                   "像你这种人，在连续剧里,最多只能活2集。",
                   "泼出去的水，我连盆都不要。",
                   "早上起床我以为我一夜之间长高了，结果才发现是我 被子盖横了",
                   "永远不要和父母吵架，因为你吵不赢的时候只 有挨骂，当你吵得赢的时候只有挨打。",
                   "今天，哥去捞了QQ漂流瓶，捞了一个，结果一看崩溃 了！“再来一瓶”。",
                   "我画了一个棺材，里面躺着你和她。我多么的善良， 让你们死也在一起。",
                   "上帝想听歌了，带走了张国荣.上帝想看跳舞了，带走了MJ，上帝想用iPhone5了，带走了乔布斯。",
                   "官再大，钱再多，阎王照样往里拖。",
                   "每次考试我都好想在卷子上写满“百度一下，你就知道”，气死阅卷老师。",
                   "某理科生骂人：“你丫简直是X+2＞4的解集！”想了半天才想明白答案是“二到正无穷”……",
                   "像你这样的女孩就不能嫁人，就算嫁了也是嫁祸于人。",
                   "学校啊你虽然得到了我的肉体，可是你却得不到我的心><。",
                   "“我脸油不油?” “反光，看不清楚。”",
                   "“ 小时候，我最喜欢玩捉迷藏，等别人藏好了，我就回家吃饭。”",
                   "三个苹果改变了世界：一个诱惑了夏娃，一个砸醒了 牛顿，一个被乔布斯咬了一口。",
                   "月老，你是不是把我的红绳玩断了？",
                   "在十几年前的一个９月１号，我手舞足蹈眉开眼笑的 背上小书包，屁颠屁颠~的走进学校，从此踏上了一条 不归路。",
                   "等中国发达了。要老外来翻译文言文。",
                   "以前把生米煮成熟饭后那女的就是你的人了，现在你 就算是把生米煮成爆米花都不管用了。",
                   "如果考试用QB做奖励，那么国家马上就会富强的。",
                   "化学老师问：“家里煤气泄漏怎么办？”起身说道：“抽根烟冷静冷静。”",
                   "现在拨打110，还可以赢得看守所七日游，有精美手铐、时尚囚服赠送，还有警车免费接送，前10名免费剃头。",
                   "此次起床共用了5分钟，你已击败了全国88%学生，寝 室还有一位同学起床失败，正在重起，隔壁宿舍全部 死机！",
                   "考试作弊，同心协力。以抄为主，以蒙为弊。 抄蒙结合保护及格，谁敢告密，下课暴力。",
                   "某女；“你究竟看上我哪点了？我改还不行么”.某 男；“我就是喜欢你不喜欢我，你改啊~~~”",
                   "天天看穿越小说，看的马桶都像穿越的洞。",
                   "数学考试，三个老师监考。冒着生命危险，传纸条给 他：第三题会吗？过了好一会，纸条上面写着：我会！",
                   "如果你亲眼看着一棵棵大树变成一本本作业本时，你还忍 心写作业吗？为了保护大自然，我们不写作业~",
                   "雷锋少了，雷人多了，为人民服务的少了，为人民币服务 的多了，挽着奶奶过马路的少了，挽着二奶过马路多了。",
                   "今天胃疼，想吐。下午有考试，考到一半，憋不住吐 了。 老师走过来关切的说：”怎么，题出的太恶心了？”",
                   "老师问：一个鸡蛋去撞另一个鸡蛋，谁碎了？一个同 学说：心碎了！老师问：谁的心？同学：母鸡的心！",
                   "原来英文里面的救护车叫“ambulance” ----中文发 音是：俺不能死。我一下子就记住了！"
               ]
               joke = random.choice(jokes)
               dispatcher.utter_message(text=joke)
               return []
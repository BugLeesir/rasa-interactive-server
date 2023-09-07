def graph_data():
    # 假设您有一个DataFrame存储了站点和边的数据
    nodes = ['罗家庙', '邵阳', '冷水江', '新化', '柘溪', '桃江', '益阳', '城陵矶', '三门江', '新宁',
        '螺山', '汉口', '湘阴', '长沙', '湘潭', '株洲', '衡山', '衡阳', '归阳', '老埠头',
        '全州', '监利', '沙市', '枝城', '宜昌', '寸滩', '淋溪河', '江垭', '长潭河', '石门',
        '津市', '篢子头', '张家界', '桑植', '安乡', '石龟山', '南花', '沅江', '常德', '桃源',
        '五强溪', '浦市', '安江', '黔城', '锦屏']

    edges = data = [
    {'source': '罗家庙', 'target': '邵阳', 'time': 6},
    {'source': '邵阳', 'target': '冷水江', 'time': 6},
    {'source': '冷水江', 'target': '新化', 'time': 4},
    {'source': '新化', 'target': '柘溪', 'time': 15},
    {'source': '柘溪', 'target': '桃江', 'time': 16},
    {'source': '桃江', 'target': '益阳', 'time': 5},
    {'source': '益阳', 'target': '城陵矶', 'time': 52},
    {'source': '三门江', 'target': '罗家庙', 'time': 1},
    {'source': '新宁', 'target': '三门江', 'time': 13},
    {'source': '城陵矶', 'target': '螺山', 'time': 5},
    {'source': '螺山', 'target': '汉口', 'time': 24},
    {'source': '湘阴', 'target': '城陵矶', 'time': 13},
    {'source': '长沙', 'target': '湘阴', 'time': 13},
    {'source': '湘潭', 'target': '长沙', 'time': 6},
    {'source': '株洲', 'target': '湘潭', 'time': 6},
    {'source': '衡山', 'target': '株洲', 'time': 15},
    {'source': '衡阳', 'target': '衡山', 'time': 10},
    {'source': '归阳', 'target': '衡阳', 'time': 17},
    {'source': '老埠头', 'target': '归阳', 'time': 16},
    {'source': '全州', 'target': '老埠头', 'time': 12},
    {'source': '监利', 'target': '城陵矶', 'time': 22},
    {'source': '沙市', 'target': '监利', 'time': 24},
    {'source': '枝城', 'target': '沙市', 'time': 8},
    {'source': '宜昌', 'target': '枝城', 'time': 8},
    {'source': '寸滩', 'target': '宜昌', 'time': 24},
    {'source': '淋溪河', 'target': '湘阴', 'time': 3},
    {'source': '湘阴', 'target': '江垭', 'time': 2},
    {'source': '江垭', 'target': '长潭河', 'time': 4},
    {'source': '长潭河', 'target': '石门', 'time': 12},
    {'source': '石门', 'target': '津市', 'time': 9},
    {'source': '篢子头', 'target': '石门', 'time': 6},
    {'source': '张家界', 'target': '篢子头', 'time': 6},
    {'source': '桑植', 'target': '张家界', 'time': 5},
    {'source': '津市', 'target': '安乡', 'time': 16},
    {'source': '津市', 'target': '石龟山', 'time': 9},
    {'source': '安乡', 'target': '南花', 'time': 20},
    {'source': '石龟山', 'target': '南花', 'time': 12},
    {'source': '南花', 'target': '城陵矶', 'time': 48},
    {'source': '南花', 'target': '沅江', 'time': 8},
    {'source': '沅江', 'target': '城陵矶', 'time': 40},
    {'source': '常德', 'target': '南花', 'time': 22},
    {'source': '桃源', 'target': '常德', 'time': 7},
    {'source': '五强溪', 'target': '桃源', 'time': 8},
    {'source': '浦市', 'target': '五强溪', 'time': 3},
    {'source': '安江', 'target': '浦市', 'time': 12},
    {'source': '黔城', 'target': '安江', 'time': 6},
    {'source': '锦屏', 'target': '黔城', 'time': 14}
]

    nodes_with_name = [{"name": node} for node in nodes]

    graph_data_dict = {
        "nodes": nodes_with_name,
        "edges": edges
    }

    return graph_data_dict



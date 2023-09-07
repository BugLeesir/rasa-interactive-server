<template>
  <el-card class="box-card">
    <div id="waterFlowChart"></div>
  </el-card>
</template>

<script>
import axios from "axios";
import Highcharts from "highcharts";

export default {
  name: "WaterFlow",
  methods:{
        fetchData() {
      axios.get("/charts/get_water_flow_data")
          .then(response => {
            const data = response.data

            const waterLevelData = data.map(item => [item.time, item.water_level])
            const flowRateData = data.map(item => [item.time, item.flow_rate])

            Highcharts.chart("waterFlowChart", {
              title: {
                text: "水位流量关系线"
              },
              xAxis: {
                title: {
                  text: "Time"
                }
              },
              yAxis: {
                title: {
                  text: "Value"
                }
              },
              series: [{
                name: "Water Level",
                data: waterLevelData
              }, {
                name: "Flow Rate",
                data: flowRateData
              }]
            })
          })
          .catch(error => {
            console.log("获取数据失败：" + error)
          })
    }
  },
  mounted() {
    this.fetchData()
  }
}
</script>

<style scoped lang="less">
  .box-card{
    height: 80vh;
    div{
      font-size:18px;
      margin-top:20px;
    }
  }
</style>
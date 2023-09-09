<template>
  <div>
    <el-card class="box-card">
      <div class="chat-window">
        <div v-for="(message, index) in messages" :key="index" class="message" :class="{ 'user-message': message.from === 'user', 'rasa-message': message.from === 'rasa' }">
          <span class="prompt">{{message.prompt}}</span>
          {{ message.text }}
          <div v-if="index === messages.length - 1 && imgSrc">
            <img :src="imgSrc" alt="Water Flow Chart">
          </div>
        </div>
      </div>
      <div class="form-div">
        <el-input  @keyup.enter="onSubmit" placeholder="请输入您的问题..." v-model="questions" class="questions"></el-input>
        <el-button type="primary" @click="onSubmit">发送</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>

import axios from "axios"
export default {
  name: "Main",
  data(){
    return {
      questions:"",
      messages:[],
      imgSrc:null
    }
  },
  methods:{
    async onSubmit() {
      this.imgSrc=null
      this.messages.push({text:this.questions,from:"user",prompt:"您："})
      const response = await axios.post("http://localhost:5005/webhooks/rest/webhook", {
        message: this.questions
      }, {
        headers: {
          "Content-Type": "application/json"
        }
      })
      // 交互处理
      const data = response.data
      if(data.length===0){
        this.messages.push({text:"出现错误，请重试。",from:"rasa",prompt:""})
        return
      }
      for (let i = 0; i < data.length; i++) {
        this.messages.push({text:data[i].text,from:"rasa",prompt:"防洪减灾机器人："})
      }

      this.checkWaterFlow()
      this.imgSrc=null
      this.questions=""

    },
    checkWaterFlow(){
      const stationNames=["沙市","枝城","寸滩","桃源","桃江"]
      let matchedStation=null

      for (const station of stationNames){
        if(this.questions.includes(station)){
          matchedStation=station
          break
        }
      }
      if(matchedStation){
        axios.post("/charts/get_water_flow_data",{place:matchedStation},{responseType:"blob"})
            .then(response=>{
              this.messages.push({text:"水位流量关系线如下：",from:"rasa",prompt:"防洪减灾机器人："})

              const blob = new Blob([response.data],{type:"image/png"})
              const url=window.URL.createObjectURL(blob)
              this.imgSrc=url
            })
            .catch(error=>{
              console.log("获取水位流量关系线图片失败："+error)
            })
      }
    }
  }
}
</script>

<style scoped lang="less">
.box-card{
  height:80vh;
  position:relative;

  .chat-window{
    overflow-y: auto;
    height: 500px;

    .prompt{
      font-weight: bolder;
    }

    .message{
      height: 40px;
      line-height: 40px;
      font-size:16px;
    }
    .user-message{
      background-color: #F9F9F9;
    }
  }

  .form-div{
    position:absolute;
    bottom:10px;
    width: 1200px;

    display: flex;
    justify-content: space-around;

    .questions{
      margin-right: 40px;
    }
  }
}
</style>
<template>
  <div>
    <el-card class="box-card">
      <div class="chat-window">
        <div v-for="(message, index) in messages" :key="index" class="message" :class="{ 'user-message': message.from === 'user', 'rasa-message': message.from === 'rasa' }">
          <span class="prompt">{{message.prompt}}</span>
          {{ message.text }}
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
      messages:[]
    }
  },
  methods:{
    async onSubmit() {
      console.log("发送问题成功：" + this.questions)
      this.messages.push({text:this.questions,from:"user",prompt:"您："})
      const response = await axios.post("http://localhost:5005/webhooks/rest/webhook", {
        message: this.questions
      }, {
        headers: {
          "Content-Type": "application/json"
        }
      })
      this.questions=""
      // 交互处理
      const data = response.data
      if(data.length===0){
        this.messages.push({text:"出现错误，请重试。",from:"rasa",prompt:""})
        return
      }
      for (let i = 0; i < data.length; i++) {
        this.messages.push({text:data[i].text,from:"rasa",prompt:"防洪减灾机器人："})
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
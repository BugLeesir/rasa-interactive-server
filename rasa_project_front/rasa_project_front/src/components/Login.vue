<template>
  <div class="login-container">
    <el-card class="box-card">
      <div class="header">
        <span class="title">login</span>
      </div>
      <div class="content">
        <el-form ref="form" :model="form" class="login-form">
          <el-form-item>
            <el-input v-model="form.username" placeholder="username"></el-input>
          </el-form-item>
          <el-form-item>
            <el-input v-model="form.password" placeholder="password" show-password></el-input>
          </el-form-item>
          <el-form-item>
            <el-button @click="login" class="submit">登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
import {Message} from "element-ui";

export default {
  name: "Login",
  data(){
    return {
      form:{
        username:"",
        password:""
      }
    }
  },
  methods:{
    login(){
      if(this.form.username==="rasa" && this.form.password==="rasa"){
        localStorage.setItem("login","login")
        this.$router.push("/")
      }else{
        Message.info("用户名或密码错误")
        this.form.username=""
        this.form.password=""
      }
    }
  }
}
</script>

<style scoped lang="less">
  .login-container{
    background: url("@/assets/login.jpg") no-repeat center center fixed;
    background-size: cover;
    width: 100%;
    height:100vh;
    position:relative;

    .box-card{
      padding:0;
      background-color: rgba(255,255,255,0.2);
      width:600px;
      height:400px;
      position:absolute;
      top:20%;
      left:30%;
      border:0;
      opacity: 70%;

      .header{
        text-align: center;
        height: 60px;
        span{
          font-family: "Lobster",serif;
          font-size:40px;
          color:white;
        }
      }

      .content{
        height: 320px;
        margin-top:40px;
        .el-form-item{
          width:400px;
          height:40px;
          padding-left:80px;
        }
        .submit{
          width:400px;
        }
      }

    }
  }
</style>
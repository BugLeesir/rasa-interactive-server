<template>
<div>
  <span>防洪减灾问答机器人系统</span>

  <el-button type="info" @click="logout">退出</el-button>
</div>
</template>

<script>
export default {
  name: "Header",
  methods:{
    logout(){
      this.$router.push("/login")
      localStorage.removeItem("login")
    }
  }
}
</script>

<style scoped lang="less">
div{
  height: 100%;
  background-color: #373D40;
  display:flex;
  justify-content: space-between;
  padding-left:0px;
  align-items:center;

  span{
    padding-left:20px;
    color: #fff;
    font-size:22px;
  }
  .el-button{
    margin-right:20px;
  }
}
</style>
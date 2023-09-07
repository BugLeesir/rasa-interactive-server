<template>
  <div>
   <el-container class="home-container" v-if="$route.meta.keepalive">
     <el-header>
       <Header></Header>
     </el-header>
     <el-container>
       <el-aside width="200px"><Aside></Aside></el-aside>
       <el-main><router-view></router-view></el-main>
     </el-container>
   </el-container>
    <router-view v-if="!$route.meta.keepalive"></router-view>
  </div>
</template>

<script>


import Header from "@/components/Header.vue";
import Aside from "@/components/Aside.vue";
import Main from "@/components/Main.vue";

export default {
  name: 'App',
  components: {Main, Aside, Header}
}
</script>

<style lang="less">
*{
  padding:0;
  margin:0;
  border:0;
}
.home-container{
  height: 100vh;

  .el-header{
    padding:0;
  }
  .el-aside{
    background-color: #333744;
  }
  .el-main{
    background-color: #EAEDF1;
  }
}
</style>

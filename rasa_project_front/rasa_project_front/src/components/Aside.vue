<template>
  <el-col :span="24">
    <el-menu
        class="el-menu-vertical-demo"
        background-color="#333744"
        text-color="#fff"
        active-text-color="#ffd04b"
    >
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-location"></i>
          <span slot="title">
            <router-link to="/" class="router-link">问答专栏</router-link>
          </span>
        </template>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title">
            <i class="el-icon-document"></i>
            <span slot="title">
              <router-link to="/graph" class="router-link">知识图谱</router-link>
            </span>
        </template>
      </el-submenu>
    </el-menu>
  </el-col>
</template>

<script>
export default {
  name: "Aside"
}
</script>

<style scoped lang="less">
.el-col{
  height: 100%;

  .router-link {
    padding-left:16px;
    font-size:16px;
    color:rgb(255,255,255);
    text-decoration: none;
  }

  .el-menu-vertical-demo{
    ::v-deep .el-submenu__title {
      .el-icon-arrow-down {
        display: none;
      }
    }
  }

}
</style>
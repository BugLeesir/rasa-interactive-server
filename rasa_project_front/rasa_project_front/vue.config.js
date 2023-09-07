const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave:false,
  devServer:{
    proxy:{
      "/charts":{
        target:"http://127.0.0.1:5000",
        pathRewrite:{"^/charts":""},
        ws:true,
        changeOrigin:true
      }
    }
  }
})

const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000", // 本地后端服务
        changeOrigin: true,
        pathRewrite: { '^/api': '' },   
      }
    }
  }
});

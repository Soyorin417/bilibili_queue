<template>
  <div class="sidebar">
    <nav class="nav flex-column">
      <router-link class="nav-link" to="/">首页</router-link>

      <router-link class="nav-link" :to="{ name: 'queuedisplay' }">
        队列显示
      </router-link>

      <router-link class="nav-link" :to="{ name: 'queuestylegenerator' }">
        改变 CSS
      </router-link>

      <router-link class="nav-link" :to="{ name: 'keywordmanager' }">
        关键词管理
      </router-link>

      <router-link class="nav-link" to="/new">开发中</router-link>
    </nav>
  </div>
</template>

<script>
export default {
  name: "NavBar",
};
</script>

<style scoped>
/* 左侧侧栏布局 */
.sidebar {
  width: 200px;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  background: #f8f9fa;
  border-right: 1px solid #ddd;
  padding: 20px 10px;
}

/* 让 router-link 看起来像 bootstrap nav */
.nav-link {
  color: #333;
  padding: 10px 12px;
  border-radius: 6px;
  text-decoration: none;
  margin-bottom: 6px;
}

/* hover 效果 */
.nav-link:hover {
  background: #e8e8e8;
}

/* 当前路由高亮 */
.router-link-active {
  background: #42b983;
  color: #fff !important;
}
</style>

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import "bootstrap/dist/js/bootstrap";
import "bootstrap/dist/css/bootstrap.css";
createApp(App).use(store).use(store).use(router).use(router).mount('#app')

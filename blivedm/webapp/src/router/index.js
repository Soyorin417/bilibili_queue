import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import QueueDisplayView from '@/views/QueueDisplayView.vue'
import QueueStyleGeneratorView from '@/views/QueueStyleGeneratorView.vue'
import KeywordManagerView from '@/views/KeywordManagerView.vue'
import NewView from '@/views/NewView.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/queuedisplay',
    name: 'queuedisplay',
    component: QueueDisplayView
  },
  {
    path: '/queuestylegenerator',
    name: 'queuestylegenerator',
    component: QueueStyleGeneratorView
  },
  {
    path: '/keywordmanager',
    name: 'keywordmanager',
    component: KeywordManagerView
  },
  {
    path: '/new',
    name: 'new',
    component: NewView
  }

]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router

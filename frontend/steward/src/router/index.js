// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import create_user from '../components/create_user.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login,
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('walletname');
      if (token) {
        next(); // 已登录，允许访问
      } else {
        next('/'); // 未登录，跳转到登录页
      }
    },
  },
  {
    path: '/create_user',
    name: 'create_user',
    component: create_user,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('walletname');
      if (token) {
        next(); // 已登录，允许访问
      } else {
        next('/'); // 未登录，跳转到登录页
      }
    },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

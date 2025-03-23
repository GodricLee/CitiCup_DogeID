// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Home from '../components/Home.vue'
import create_did from '../components/create_did.vue'
import create_cred_req from '../components/create_cred_req.vue'
import store_credential from '../components/store_credential.vue'
import list_cred from '../components/list_cred.vue'
import create_proof from '../components/create_proof.vue'


const routes = [
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
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
        next(); 
      } else {
        next('/'); 
      }
    },
  },
  {
    path: '/create_did',
    name: 'create_did',
    component: create_did,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('walletname');
      if (token) {
        next(); 
      } else {
        next('/'); 
      }
    },
  },
  {
    path: '/create_cred_req',
    name: 'create_cred_req',
    component: create_cred_req,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('walletname');
      if (token) {
        next(); 
      } else {
        next('/'); 
      }
    },
  },
  {
    path: '/store_credential',
    name: 'store_credential',
    component: store_credential,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('walletname');
      if (token) {
        next(); 
      } else {
        next('/'); 
      }
    },
  },
  {
    path: '/list_cred',
    name: 'list_cred',
    component: list_cred,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('walletname');
      if (token) {
        next(); 
      } else {
        next('/'); 
      }
    },
  },
  {
    path: '/create_proof',
    name: 'create_proof',
    component: create_proof,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('walletname');
      if (token) {
        next(); 
      } else {
        next('/'); 
      }
    },
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

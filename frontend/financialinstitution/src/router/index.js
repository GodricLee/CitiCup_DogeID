// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Home from '../components/Home.vue'
import create_user from '../components/create_user.vue'
import create_did from '../components/create_did.vue'
//  <nav class="main-nav">
// <router-link to="/home" class="nav-link">Home</router-link>
// <router-link to="/create_did" class="nav-link">Create DID</router-link>
// <router-link to="/create_user" class="nav-link">Create User</router-link>
// <router-link to="/create_schema" class="nav-link">Create Schema</router-link>
// <router-link to="/create_cred_def" class="nav-link">Create Credential Definition</router-link>
// <router-link to="/create_cred_offer" class="nav-link">Create Credential Offer</router-link>
// <router-link to="/create_cred" class="nav-link">Create Credential</router-link>
// <router-link to="/verify_proof" class="nav-link">Verify Proof</router-link>
// </nav>
import create_schema from '../components/create_schema.vue'
import create_cred_def from '../components/create_cred_def.vue'
import create_cred_offer from '../components/create_cred_offer.vue'
import create_cred from '../components/create_cred.vue'
import verify_proof from '../components/verify_proof.vue'


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
    path: '/create_user',
    name: 'create_user',
    component: create_user,
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
    path: '/create_schema',
    name: 'create_schema',
    component: create_schema,
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
    path: '/create_cred_def',
    name: 'create_cred_def',
    component: create_cred_def,
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
    path: '/create_cred_offer',
    name: 'create_cred_offer',
    component: create_cred_offer,
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
    path: '/create_cred',
    name: 'create_cred',
    component: create_cred,
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
    path: '/verify_proof',
    name: 'verify_proof',
    component: verify_proof,
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('walletname');
      if (token) {
        next(); 
      } else {
        next('/'); 
      }
    },
  },

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

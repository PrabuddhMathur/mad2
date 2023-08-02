import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import SearchView from '../views/SearchView.vue'
import AdminDashboardView from '../views/AdminDashboardView.vue'
import ShowsView from '../views/ShowsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      // component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import('../views/AboutView.vue')
    },
    {
      path: '/admin_dashboard',
      name: 'adminDashboard',
      component: AdminDashboardView
    },
    {
      path: '/shows',
      name: 'showsView',
      component: ShowsView
    },
    {
      path: '/bookings',
      name: 'bookings'
    },
    {
      path: '/summary',
      name: 'summary'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    }
  ]
})

export default router

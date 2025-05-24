import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import authRoutes from '@/router/authRoutes.ts'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/appointments',
      name: 'appointments',
      component: import('../views/Appointment.vue'),
    },
    {
      path: '/chat',
      name: 'chat',
      component: import('../views/Chat.vue'),
    },
    {
      path: '/documentation',
      name: 'documentation',
      component: import('../views/Documentation.vue'),
    },
    ...authRoutes,
  ],
})

export default router

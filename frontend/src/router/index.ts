import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import authRoutes from '@/router/authRoutes.ts'

import guestGuard from '@/router/guards/guestGuard.ts'
import requiresAuthGuard from '@/router/guards/authenticatedGuard.ts'
import roleGuard from '@/router/guards/roleGuard.ts'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { guestOnly: true, authenticatedRedirect: '/documentation' },
    },
    {
      path: '/appointments',
      name: 'appointments',
      meta: { authOnly: true, allowedRoles: ['patient'] },
      component: import('../views/Appointment.vue'),
    },
    {
      path: '/chat',
      name: 'chat',
      meta: { authOnly: true, allowedRoles: ['patient'] },
      component: import('../views/Chat.vue'),
    },
    {
      path: '/documentation',
      name: 'documentation',
      component: import('../views/Documentation.vue'),
    },
    {
      path: '/documents',
      name: 'documents',
      component: import('../views/Documents.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      meta: { authOnly: true },
      component: import('../views/Profile.vue'),
    },
    ...authRoutes,
  ],
})

router.beforeEach(guestGuard)
router.beforeEach(requiresAuthGuard)
router.beforeEach(roleGuard)

export default router

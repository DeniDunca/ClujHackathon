import type { RouteRecordRaw } from 'vue-router'

const authRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    meta: { guestOnly: true },
    component: () => import('@/views/Auth/Login.vue'),
  },
  {
    path: '/register',
    name: 'register',
    meta: { guestOnly: true },
    component: () => import('@/views/Auth/Register.vue'),
  },
]

export default authRoutes

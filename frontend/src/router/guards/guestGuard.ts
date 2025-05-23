import { useAuthStore } from '@/stores/auth.ts'
import type {
  NavigationGuardNext,
  RouteLocationNormalizedGeneric,
  RouteLocationNormalizedLoaded,
} from 'vue-router'

const guestGuard = (
  to: RouteLocationNormalizedGeneric,
  from: RouteLocationNormalizedLoaded,
  next: NavigationGuardNext,
) => {
  const authStore = useAuthStore()

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    next({ name: 'home' })
  } else {
    next()
  }
}

export default guestGuard

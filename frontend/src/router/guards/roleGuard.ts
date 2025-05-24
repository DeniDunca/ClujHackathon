import { useAuthStore } from '@/stores/auth.ts'
import type {
  NavigationGuardNext,
  RouteLocationNormalizedGeneric,
  RouteLocationNormalizedLoaded,
} from 'vue-router'

const roleGuard = (
  to: RouteLocationNormalizedGeneric,
  from: RouteLocationNormalizedLoaded,
  next: NavigationGuardNext,
) => {
  const authStore = useAuthStore()
  const allowedRoles = to.meta.allowedRoles
  if (!allowedRoles || !Array.isArray(allowedRoles)) {
    next()
    return
  }

  if (!authStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }

  const userRole = authStore.role
  if (userRole && allowedRoles.includes(userRole)) {
    next()
  } else {
    next({ name: 'home' })
  }
}

export default roleGuard

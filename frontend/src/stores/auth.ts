import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'
import { useStorage, StorageSerializers } from '@vueuse/core'
import axios from 'axios'

interface LoginData {
  email: string
  password: string
}

interface RegisterData {
  email: string
  password: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = useStorage('user', null, localStorage, { serializer: StorageSerializers.object })
  const token = useStorage('token', null, localStorage, { serializer: StorageSerializers.object })
  const refreshToken = useStorage('refreshToken', null, localStorage, {
    serializer: StorageSerializers.object,
  })
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!user.value)
  const role = computed(() => user.value?.role || 'guest')

  watch(
    token,
    (newValue) => {
      if (!newValue) {
        axios.defaults.headers.common['Authorization'] = ''
      } else {
        axios.defaults.headers.common['Authorization'] = `Bearer ${newValue}`
      }
    },
    { immediate: true },
  )

  const login = async (data: LoginData) => {
    isLoading.value = true

    try {
      const response = await axios.post('/api/login', data)
      user.value = response.data.user
      token.value = response.data.token
      refreshToken.value = response.data.refreshToken
    } catch (e: Error | any) {
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  const register = async (data: RegisterData) => {
    isLoading.value = true

    try {
      const response = await axios.post('/api/register', data)
      user.value = response.data.user
      token.value = response.data.token
      refreshToken.value = response.data.refreshToken
    } catch (e: Error | any) {
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    user.value = null
    token.value = null
    refreshToken.value = null

    await axios.get('/api/logout')
  }

  const refreshAuthToken = async () => {
    if (!refreshToken.value) {
      console.error('No refresh token available')
      return
    }

    try {
      const response = await axios.post('/auth/refresh', { refreshToken: refreshToken.value })
      if (response.status === 200) {
        const { token: newToken, refreshToken: newRefreshToken } = response.data

        token.value = newToken
        refreshToken.value = newRefreshToken
      }
    } catch (err) {
      console.error('Failed to refresh token:', err)
      await logout()
    }
  }

  const initialize = async () => {
    if (!token.value) {
      token.value = null
      refreshToken.value = null
      user.value = null
    }

    try {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      const response = await axios.get('/auth/me')
      if (response.status === 200) {
        user.value = response.data
      }
    } catch (err) {
      await refreshAuthToken()
    }
  }

  return {
    user,
    token,
    refreshToken,
    isAuthenticated,
    role,
    isLoading,
    login,
    register,
    logout,
    refreshAuthToken,
    initialize,
  }
})

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
  first_name: string
  last_name: string
  role: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = useStorage('user', null, localStorage, { serializer: StorageSerializers.object })
  const token = useStorage('token', null, localStorage, { serializer: StorageSerializers.object })
  const tokenType = useStorage('tokenType', null, localStorage, {
    serializer: StorageSerializers.object,
  })
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
      const formData = new FormData()
      formData.append('username', data.email)
      formData.append('password', data.password)

      const response = await axios.post('/auth/token', formData)
      if (response.status !== 200) {
        throw new Error('Failed to login')
      }

      axios.defaults.headers.common['Authorization'] =
        `${tokenType.value} ${response.data['access_token']}`

      token.value = response.data['access_token']
      tokenType.value = response.data.token_type

      await initialize()
    } catch (e: Error | any) {
      isLoading.value = false
      console.error(e)
      return false
    } finally {
      isLoading.value = false
    }
    return true
  }

  const register = async (data: RegisterData) => {
    isLoading.value = true

    try {
      const registerResponse = await axios.post('/auth/register', data)
      if (registerResponse.status !== 201) {
        throw new Error('Failed to register')
      }

      const formData = new FormData()
      formData.append('username', data.email)
      formData.append('password', data.password)

      const response = await axios.post('auth/token', formData)
      token.value = response.data['access_token']
      tokenType.value = response.data['token_type']

      await initialize()
    } catch (e: Error | any) {
      console.error(e)
      isLoading.value = false
      return false
    } finally {
      isLoading.value = false
    }
    return true
  }

  const logout = async () => {
    user.value = null
    token.value = null
    refreshToken.value = null

    await axios.post('/auth/logout')
  }

  const refreshAuthToken = async () => {
    return
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
      await logout()
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

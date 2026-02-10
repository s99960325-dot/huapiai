import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import Cookies from 'js-cookie'
import { login as loginApi, checkAuth } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref<string | null>(Cookies.get('token') || null)
  const user = ref<any>(null)
  const loading = ref(false)

  // Getters
  const isLoggedIn = computed(() => !!token.value)

  // Actions
  async function login(password: string) {
    loading.value = true
    try {
      const res: any = await loginApi(password)
      if (res.token) {
        token.value = res.token
        Cookies.set('token', res.token, { expires: 7 })
        return true
      }
      return false
    } catch (error) {
      console.error('Login error:', error)
      return false
    } finally {
      loading.value = false
    }
  }

  async function check() {
    if (!token.value) return false
    try {
      const res: any = await checkAuth()
      return res.valid
    } catch (error) {
      logout()
      return false
    }
  }

  function logout() {
    token.value = null
    user.value = null
    Cookies.remove('token')
  }

  return {
    token,
    user,
    loading,
    isLoggedIn,
    login,
    check,
    logout
  }
})

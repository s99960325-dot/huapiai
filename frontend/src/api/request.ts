import axios, { type AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import Cookies from 'js-cookie'

// 创建axios实例
const request = axios.create({
  baseURL: '/backend-api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = Cookies.get('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data
  },
  (error) => {
    const { response } = error
    
    if (response?.status === 401) {
      ElMessage.error('登录已过期，请重新登录')
      Cookies.remove('token')
      window.location.href = '/login'
    } else {
      ElMessage.error(response?.data?.error || '请求失败')
    }
    
    return Promise.reject(error)
  }
)

export default request

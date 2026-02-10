import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
      meta: { public: true }
    },
    {
      path: '/',
      name: 'Layout',
      component: () => import('@/layouts/MainLayout.vue'),
      redirect: '/dashboard',
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: () => import('@/views/DashboardView.vue'),
          meta: { title: '仪表盘', icon: 'Odometer' }
        },
        {
          path: 'llm',
          name: 'LLM',
          component: () => import('@/views/LLMView.vue'),
          meta: { title: '大语言模型', icon: 'ChatDotRound' }
        },
        {
          path: 'im',
          name: 'IM',
          component: () => import('@/views/IMView.vue'),
          meta: { title: '消息平台', icon: 'Message' }
        },
        {
          path: 'workflows',
          name: 'Workflows',
          component: () => import('@/views/WorkflowView.vue'),
          meta: { title: '工作流', icon: 'Connection' }
        },
        {
          path: 'plugins',
          name: 'Plugins',
          component: () => import('@/views/PluginView.vue'),
          meta: { title: '插件管理', icon: 'Box' }
        },
        {
          path: 'system',
          name: 'System',
          component: () => import('@/views/SystemView.vue'),
          meta: { title: '系统设置', icon: 'Setting' }
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.public) {
    next()
    return
  }
  
  if (!authStore.token) {
    next('/login')
    return
  }
  
  next()
})

export default router

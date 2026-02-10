import request from './request'

// 获取所有插件
export function getPlugins() {
  return request.get('/api/plugin')
}

// 获取插件详情
export function getPlugin(pluginId: string) {
  return request.get(`/api/plugin/${pluginId}`)
}

// 安装插件
export function installPlugin(pluginId: string) {
  return request.post(`/api/plugin/${pluginId}/install`)
}

// 卸载插件
export function uninstallPlugin(pluginId: string) {
  return request.post(`/api/plugin/${pluginId}/uninstall`)
}

// 启用插件
export function enablePlugin(pluginId: string) {
  return request.post(`/api/plugin/${pluginId}/enable`)
}

// 禁用插件
export function disablePlugin(pluginId: string) {
  return request.post(`/api/plugin/${pluginId}/disable`)
}

// 从市场搜索插件
export function searchPlugins(query: string) {
  return request.get('/api/plugin/market/search', { params: { query } })
}

// 从本地安装插件
export function installPluginFromFile(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/api/plugin/install-from-file', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

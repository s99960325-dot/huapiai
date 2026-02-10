import request from './request'

// 获取IM适配器类型
export function getIMAdapterTypes() {
  return request.get('/api/im/types')
}

// 获取所有适配器
export function getAdapters() {
  return request.get('/api/im/adapters')
}

// 获取指定适配器
export function getAdapter(name: string) {
  return request.get(`/api/im/adapters/${name}`)
}

// 创建适配器
export function createAdapter(data: any) {
  return request.post('/api/im/adapters', data)
}

// 更新适配器
export function updateAdapter(name: string, data: any) {
  return request.put(`/api/im/adapters/${name}`, data)
}

// 删除适配器
export function deleteAdapter(name: string) {
  return request.delete(`/api/im/adapters/${name}`)
}

// 启动适配器
export function startAdapter(name: string) {
  return request.post(`/api/im/adapters/${name}/start`)
}

// 停止适配器
export function stopAdapter(name: string) {
  return request.post(`/api/im/adapters/${name}/stop`)
}

// 获取机器人资料
export function getBotProfile(adapterName: string) {
  return request.get(`/api/im/adapters/${adapterName}/profile`)
}

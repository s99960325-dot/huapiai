import request from './request'

// 获取LLM适配器类型
export function getLLMAdapterTypes() {
  return request.get('/api/llm/types')
}

// 获取所有后端
export function getBackends() {
  return request.get('/api/llm/backends')
}

// 获取指定后端
export function getBackend(name: string) {
  return request.get(`/api/llm/backends/${name}`)
}

// 创建后端
export function createBackend(data: any) {
  return request.post('/api/llm/backends', data)
}

// 更新后端
export function updateBackend(name: string, data: any) {
  return request.put(`/api/llm/backends/${name}`, data)
}

// 删除后端
export function deleteBackend(name: string) {
  return request.delete(`/api/llm/backends/${name}`)
}

// 自动检测模型
export function autoDetectModels(backendName: string) {
  return request.post(`/api/llm/backends/${backendName}/auto-detect`)
}

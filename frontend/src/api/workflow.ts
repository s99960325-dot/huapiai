import request from './request'

// 获取所有工作流
export function getWorkflows() {
  return request.get('/api/workflow')
}

// 获取指定工作流
export function getWorkflow(groupId: string, workflowId: string) {
  return request.get(`/api/workflow/${groupId}/${workflowId}`)
}

// 创建工作流
export function createWorkflow(data: any) {
  return request.post('/api/workflow', data)
}

// 更新工作流
export function updateWorkflow(groupId: string, workflowId: string, data: any) {
  return request.put(`/api/workflow/${groupId}/${workflowId}`, data)
}

// 删除工作流
export function deleteWorkflow(groupId: string, workflowId: string) {
  return request.delete(`/api/workflow/${groupId}/${workflowId}`)
}

// 获取所有Block类型
export function getBlockTypes() {
  return request.get('/api/block/types')
}

// 获取Block详情
export function getBlockType(typeName: string) {
  return request.get(`/api/block/types/${typeName}`)
}

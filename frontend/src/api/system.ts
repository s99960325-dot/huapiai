import request from './request'

// 获取系统配置
export function getSystemConfig() {
  return request.get('/api/system/config')
}

// 更新系统配置
export function updateSystemConfig(config: any) {
  return request.post('/api/system/config', config)
}

// 获取系统状态
export function getSystemStatus() {
  return request.get('/api/system/status')
}

// 获取版本信息
export function getVersion() {
  return request.get('/api/system/version')
}

// 检查更新
export function checkUpdate() {
  return request.get('/api/system/check-update')
}

// 重启系统
export function restartSystem() {
  return request.post('/api/system/restart')
}

// 获取日志
export function getLogs() {
  return request.get('/api/system/logs')
}

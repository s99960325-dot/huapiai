import request from './request'

export function login(password: string) {
  return request.post('/api/auth/login', { password })
}

export function checkAuth() {
  return request.get('/api/auth/check')
}

export function changePassword(oldPassword: string, newPassword: string) {
  return request.post('/api/auth/change-password', { old_password: oldPassword, new_password: newPassword })
}

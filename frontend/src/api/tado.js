import { api } from './client'

export const startAuth = () => api.post('/api/tado/auth/start')
export const completeAuth = () => api.post('/api/tado/auth/complete')
export const listZones = () => api.get('/api/tado/zones')

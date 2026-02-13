import { api } from './client'

export const getDashboard = () => api.get('/api/dashboard')
export const getHouseDashboard = (houseId) => api.get(`/api/dashboard/${houseId}`)

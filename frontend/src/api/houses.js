import { api } from './client'

export const listHouses = () => api.get('/api/houses')
export const getHouse = (id) => api.get(`/api/houses/${id}`)
export const createHouse = (data) => api.post('/api/houses', data)
export const updateHouse = (id, data) => api.put(`/api/houses/${id}`, data)
export const deleteHouse = (id) => api.del(`/api/houses/${id}`)

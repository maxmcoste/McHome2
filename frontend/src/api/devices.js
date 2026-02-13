import { api } from './client'

export const listDevices = (houseId) => api.get(`/api/houses/${houseId}/devices`)
export const createDevice = (houseId, data) => api.post(`/api/houses/${houseId}/devices`, data)
export const updateDevice = (deviceId, data) => api.put(`/api/devices/${deviceId}`, data)
export const deleteDevice = (deviceId) => api.del(`/api/devices/${deviceId}`)
export const getBoilerStatus = (houseId) => api.get(`/api/houses/${houseId}/boiler/status`)
export const overrideBoiler = (houseId, action) => api.post(`/api/houses/${houseId}/boiler/override`, { action })

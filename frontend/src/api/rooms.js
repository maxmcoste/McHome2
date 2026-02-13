import { api } from './client'

export const listRooms = (houseId) => api.get(`/api/houses/${houseId}/rooms`)
export const getRoom = (houseId, roomId) => api.get(`/api/houses/${houseId}/rooms/${roomId}`)
export const createRoom = (houseId, data) => api.post(`/api/houses/${houseId}/rooms`, data)
export const updateRoom = (houseId, roomId, data) => api.put(`/api/houses/${houseId}/rooms/${roomId}`, data)
export const deleteRoom = (houseId, roomId) => api.del(`/api/houses/${houseId}/rooms/${roomId}`)
export const getRoomCurrent = (houseId, roomId) => api.get(`/api/houses/${houseId}/rooms/${roomId}/current`)

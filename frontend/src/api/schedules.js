import { api } from './client'

export const listSchedules = (houseId, roomId) =>
  api.get(`/api/houses/${houseId}/rooms/${roomId}/schedules`)
export const createSchedule = (houseId, roomId, data) =>
  api.post(`/api/houses/${houseId}/rooms/${roomId}/schedules`, data)
export const deleteSchedule = (houseId, roomId, scheduleId) =>
  api.del(`/api/houses/${houseId}/rooms/${roomId}/schedules/${scheduleId}`)

import { api } from './client'

export const getSetupStatus = () => api.get('/api/setup/status')
export const checkDb = () => api.post('/api/setup/check-db')
export const runMigrate = () => api.post('/api/setup/migrate')

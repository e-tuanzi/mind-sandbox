import api from './api'
import type { WorldStatus } from '../types'

export const worldService = {
  async getStatus(): Promise<WorldStatus> {
    const response = await api.get('/world/status')
    return response.data
  },

  async tick(): Promise<{ message: string; time: string }> {
    const response = await api.post('/admin/world/tick', { ticks: 1 })
    return response.data
  }
}

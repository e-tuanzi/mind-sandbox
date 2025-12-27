import api from './api'
import type { InjectEventRequest } from '../types'

export const adminService = {
  async injectEvent(request: InjectEventRequest): Promise<{ message: string }> {
    const response = await api.post('/admin/inject-event', request)
    return response.data
  }
}

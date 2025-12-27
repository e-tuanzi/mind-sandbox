import api from './api'
import type { InjectEventRequest, Agent } from '../types'

export const adminService = {
  async injectEvent(request: InjectEventRequest): Promise<{ message: string }> {
    const response = await api.post('/admin/inject-event', request)
    return response.data
  },

  async createAgent(agentId: string, x: number, y: number): Promise<{ message: string; agent: Agent }> {
    const response = await api.post('/admin/agents/create', null, {
      params: { agent_id: agentId, x, y }
    })
    return response.data
  }
}

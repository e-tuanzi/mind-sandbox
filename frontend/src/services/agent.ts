import api from './api'
import type { Agent, Thought, AgentHistory } from '../types'

export const agentService = {
  async getAllAgents(): Promise<Agent[]> {
    const response = await api.get('/agents')
    return response.data
  },

  async getAgent(id: string): Promise<Agent> {
    const response = await api.get(`/agents/${id}`)
    return response.data
  },

  async getAgentThought(id: string): Promise<Thought> {
    const response = await api.get(`/agents/${id}/thought`)
    return response.data
  },

  async getAgentHistory(id: string): Promise<AgentHistory> {
    const response = await api.get(`/agents/${id}/history`)
    return response.data
  },

  async setAgentAction(id: string, action: string): Promise<{ message: string }> {
    const response = await api.post(`/agents/${id}/action`, { action })
    return response.data
  }
}

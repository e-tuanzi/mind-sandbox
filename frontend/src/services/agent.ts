import api from './api'
import type { Agent, Thought, AgentHistory } from '../types'

export const agentService = {
  async getAllAgents(language: string = 'zh'): Promise<Agent[]> {
    const response = await api.get('/agents', { params: { language } })
    return response.data
  },

  async getAgent(id: string, language: string = 'zh'): Promise<Agent> {
    const response = await api.get(`/agents/${id}`, { params: { language } })
    return response.data
  },

  async getAgentThought(id: string, language: string = 'zh'): Promise<Thought> {
    const response = await api.get(`/agents/${id}/thought`, { params: { language } })
    return response.data
  },

  async getAgentHistory(id: string, language: string = 'zh'): Promise<AgentHistory> {
    const response = await api.get(`/agents/${id}/history`, { params: { language } })
    return response.data
  },

  async setAgentAction(id: string, action: string, language: string = 'zh'): Promise<{ message: string }> {
    const response = await api.post(`/agents/${id}/action`, { action }, { params: { language } })
    return response.data
  }
}

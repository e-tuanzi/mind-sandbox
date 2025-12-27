import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { agentService } from '../services/agent'
import { useLocaleStore } from './locale'
import type { Agent, Thought, AgentHistory } from '../types'

export const useAgentStore = defineStore('agent', () => {
  const agents = ref<Map<string, Agent>>(new Map())
  const selectedAgentId = ref<string | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const localeStore = useLocaleStore()

  const selectedAgent = computed(() => {
    return selectedAgentId.value ? agents.value.get(selectedAgentId.value) : null
  })

  const agentList = computed(() => {
    return Array.from(agents.value.values())
  })

  async function fetchAllAgents() {
    isLoading.value = true
    error.value = null
    try {
      const data = await agentService.getAllAgents(localeStore.currentLanguage)
      agents.value.clear()
      data.forEach(agent => {
        agents.value.set(agent.id, agent)
      })
    } catch (e) {
      error.value = 'Failed to fetch agents'
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchAgent(id: string) {
    isLoading.value = true
    error.value = null
    try {
      const agent = await agentService.getAgent(id, localeStore.currentLanguage)
      agents.value.set(id, agent)
      return agent
    } catch (e) {
      error.value = `Failed to fetch agent ${id}`
      console.error(e)
      throw e
    } finally {
      isLoading.value = false
    }
  }

  async function fetchAgentThought(id: string): Promise<Thought> {
    try {
      return await agentService.getAgentThought(id, localeStore.currentLanguage)
    } catch (e) {
      console.error('Failed to fetch agent thought:', e)
      throw e
    }
  }

  async function fetchAgentHistory(id: string): Promise<AgentHistory> {
    try {
      return await agentService.getAgentHistory(id, localeStore.currentLanguage)
    } catch (e) {
      console.error('Failed to fetch agent history:', e)
      throw e
    }
  }

  function selectAgent(id: string | null) {
    selectedAgentId.value = id
  }

  function updateAgent(id: string, updates: Partial<Agent>) {
    const agent = agents.value.get(id)
    if (agent) {
      agents.value.set(id, { ...agent, ...updates })
    }
  }

  return {
    agents,
    selectedAgentId,
    selectedAgent,
    agentList,
    isLoading,
    error,
    fetchAllAgents,
    fetchAgent,
    fetchAgentThought,
    fetchAgentHistory,
    selectAgent,
    updateAgent
  }
})

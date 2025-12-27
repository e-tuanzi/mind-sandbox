import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  const showAdminPanel = ref(false)
  const showAgentPanel = ref(false)
  const showMemoryViewer = ref(false)
  const thoughtBubbles = ref<Map<string, { content: string; timestamp: number }>>(new Map())

  function toggleAdminPanel() {
    showAdminPanel.value = !showAdminPanel.value
  }

  function toggleAgentPanel() {
    showAgentPanel.value = !showAgentPanel.value
  }

  function toggleMemoryViewer() {
    showMemoryViewer.value = !showMemoryViewer.value
  }

  function addThoughtBubble(agentId: string, content: string) {
    thoughtBubbles.value.set(agentId, {
      content,
      timestamp: Date.now()
    })
  }

  function removeThoughtBubble(agentId: string) {
    thoughtBubbles.value.delete(agentId)
  }

  function clearExpiredBubbles(expiryMs: number = 5000) {
    const now = Date.now()
    for (const [id, bubble] of thoughtBubbles.value.entries()) {
      if (now - bubble.timestamp > expiryMs) {
        thoughtBubbles.value.delete(id)
      }
    }
  }

  return {
    showAdminPanel,
    showAgentPanel,
    showMemoryViewer,
    thoughtBubbles,
    toggleAdminPanel,
    toggleAgentPanel,
    toggleMemoryViewer,
    addThoughtBubble,
    removeThoughtBubble,
    clearExpiredBubbles
  }
})

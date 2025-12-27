<template>
  <div v-if="isOpen" class="memory-viewer-overlay">
    <div class="memory-viewer">
      <div class="panel-header">
        <h3>{{ t.agent.memory }} / Memory Viewer - {{ agent?.id }}</h3>
        <button @click="close" class="close-btn">&times;</button>
      </div>

      <div class="panel-content">
        <div class="search-section">
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="searchPlaceholder"
            class="search-input"
          />
          <button @click="searchMemories" class="btn btn-primary">{{ t.common.search }}</button>
        </div>

        <div v-if="isLoading" class="loading">
          {{ t.common.loading }}
        </div>

        <div v-else-if="history" class="history-section">
          <h4>{{ t.agent.activity }}</h4>
          <div class="memory-list">
            <div v-for="(item, index) in displayedHistory" :key="index" class="memory-item">
              <p class="memory-content">{{ item.content }}</p>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          {{ t.agent.noDescription }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useAgentStore } from '../../stores/agent'
import { useUIStore } from '../../stores/ui'
import { useLocaleStore } from '../../stores/locale'
import { getTranslation } from '../../locales'
import type { AgentHistory } from '../../types'

const agentStore = useAgentStore()
const uiStore = useUIStore()
const localeStore = useLocaleStore()

const isOpen = computed(() => uiStore.showMemoryViewer)
const agent = computed(() => agentStore.selectedAgent)

const t = computed(() => getTranslation(localeStore.currentLanguage))
const searchPlaceholder = computed(() => localeStore.currentLanguage === 'zh' ? '搜索记忆...' : 'Search memories...')

const searchQuery = ref('')
const isLoading = ref(false)
const history = ref<AgentHistory | null>(null)
const displayedHistory = ref<Array<{ content: string }>>([])

watch(isOpen, async (newVal) => {
  if (newVal && agent.value) {
    await loadHistory(agent.value.id)
  }
})

async function loadHistory(agentId: string) {
  isLoading.value = true
  try {
    history.value = await agentStore.fetchAgentHistory(agentId)
    displayedHistory.value = [...history.value.history]
  } catch (error) {
    console.error('Failed to load history:', error)
  } finally {
    isLoading.value = false
  }
}

function searchMemories() {
  if (!history.value) return

  const query = searchQuery.value.toLowerCase()
  if (!query) {
    displayedHistory.value = [...history.value.history]
  } else {
    displayedHistory.value = history.value.history.filter(item =>
      item.content.toLowerCase().includes(query)
    )
  }
}

function close() {
  uiStore.toggleMemoryViewer()
  searchQuery.value = ''
}
</script>

<style scoped>
.memory-viewer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.memory-viewer {
  width: 600px;
  max-height: 80vh;
  background: rgba(26, 26, 46, 0.98);
  border: 1px solid #4a4a6a;
  border-radius: 8px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.7);
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: rgba(74, 74, 106, 0.3);
  border-bottom: 1px solid #4a4a6a;
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
  color: #ffffff;
}

.close-btn {
  background: none;
  border: none;
  color: #aaa;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.close-btn:hover {
  color: #fff;
}

.panel-content {
  padding: 16px;
  overflow-y: auto;
  max-height: calc(80vh - 60px);
}

.search-section {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  background: #2a2a3a;
  border: 1px solid #4a4a6a;
  border-radius: 4px;
  color: #fff;
  font-size: 13px;
}

.search-input:focus {
  outline: none;
  border-color: #6a6a8a;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.btn-primary {
  background: #4a4a8a;
  color: #fff;
}

.btn-primary:hover {
  background: #5a5a9a;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #aaa;
}

.history-section h4 {
  margin: 0 0 12px;
  font-size: 14px;
  color: #aaa;
  border-bottom: 1px solid #4a4a6a;
  padding-bottom: 4px;
}

.memory-list {
  max-height: 400px;
  overflow-y: auto;
}

.memory-item {
  padding: 12px;
  background: rgba(42, 42, 58, 0.5);
  border-radius: 4px;
  margin-bottom: 8px;
}

.memory-content {
  margin: 0;
  font-size: 13px;
  color: #ddd;
  line-height: 1.5;
  white-space: pre-wrap;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #aaa;
}
</style>

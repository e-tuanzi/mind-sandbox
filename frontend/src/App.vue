<template>
  <div class="app">
    <header class="header">
      <div class="header-left">
        <h1 class="title">Digital Soul</h1>
        <span class="subtitle">数字生命模拟系统</span>
      </div>
      <div class="header-right">
        <div class="world-info">
          <span class="info-item">
            <span class="icon">🕐</span>
            <span>{{ worldStore.formattedTime }}</span>
          </span>
          <span class="info-item">
            <span class="icon">{{ weatherIcon }}</span>
            <span>{{ worldStore.weather }}</span>
          </span>
          <span class="info-item">
            <span class="icon">👥</span>
            <span>{{ agentStore.agentList.length }}</span>
          </span>
        </div>
        <button @click="toggleAdminPanel" class="btn-admin">🎮 上帝视角</button>
      </div>
    </header>

    <main class="main">
      <GameContainer ref="gameContainerRef" />
      <AgentStatusPanel v-if="agentStore.selectedAgent" />
      <MemoryViewer />
      <AdminPanel />
    </main>

    <footer class="footer">
      <span>Phase 4 - 前端可视化</span>
      <span>|</span>
      <span>点击 Agent 查看详情</span>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useWorldStore } from './stores/world'
import { useAgentStore } from './stores/agent'
import { useUIStore } from './stores/ui'
import GameContainer from './components/game/GameContainer.vue'
import AgentStatusPanel from './components/ui/AgentStatusPanel.vue'
import MemoryViewer from './components/ui/MemoryViewer.vue'
import AdminPanel from './components/admin/AdminPanel.vue'

const worldStore = useWorldStore()
const agentStore = useAgentStore()
const uiStore = useUIStore()

const gameContainerRef = ref()

const weatherIcon = computed(() => {
  const weather = worldStore.weather.toLowerCase()
  if (weather.includes('sunny')) return '☀️'
  if (weather.includes('rain')) return '🌧️'
  if (weather.includes('snow')) return '❄️'
  if (weather.includes('cloud')) return '☁️'
  return '🌤️'
})

function toggleAdminPanel() {
  uiStore.toggleAdminPanel()
}

onMounted(async () => {
  await worldStore.fetchWorldStatus()
  await agentStore.fetchAllAgents()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #0a0a1a;
  color: #ffffff;
  overflow: hidden;
}

.app {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background: rgba(26, 26, 46, 0.9);
  border-bottom: 1px solid #4a4a6a;
  z-index: 50;
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.title {
  font-size: 24px;
  font-weight: 700;
  color: #ffffff;
  background: linear-gradient(90deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 12px;
  color: #aaa;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.world-info {
  display: flex;
  gap: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #ccc;
}

.info-item .icon {
  font-size: 16px;
}

.btn-admin {
  padding: 8px 16px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  border-radius: 6px;
  color: #ffffff;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.btn-admin:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-admin:active {
  transform: translateY(0);
}

.main {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.footer {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  padding: 8px;
  background: rgba(26, 26, 46, 0.9);
  border-top: 1px solid #4a4a6a;
  font-size: 12px;
  color: #666;
  z-index: 50;
}
</style>

<template>
  <div v-if="agent" class="agent-status-panel">
    <div class="panel-header">
      <h3>Agent: {{ agent.id }}</h3>
      <button @click="close" class="close-btn">&times;</button>
    </div>

    <div class="panel-content">
      <div class="info-row">
        <span class="label">位置:</span>
        <span class="value">({{ agent.x }}, {{ agent.y }})</span>
      </div>

      <div class="info-row">
        <span class="label">状态:</span>
        <span class="value status-badge" :class="agent.current_action.toLowerCase()">
          {{ agent.current_action }}
        </span>
      </div>

      <div class="stats-section">
        <h4>属性数值</h4>
        <div class="stat-bar">
          <div class="stat-label">
            <span>Health</span>
            <span>{{ agent.stats.health.toFixed(0) }}/100</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill health" :style="{ width: agent.stats.health + '%' }"></div>
          </div>
        </div>

        <div class="stat-bar">
          <div class="stat-label">
            <span>Sanity</span>
            <span>{{ agent.stats.sanity.toFixed(0) }}/100</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill sanity" :style="{ width: agent.stats.sanity + '%' }"></div>
          </div>
        </div>

        <div class="stat-bar">
          <div class="stat-label">
            <span>Wealth</span>
            <span>${{ agent.stats.wealth.toFixed(0) }}</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill wealth" :style="{ width: Math.min(agent.stats.wealth / 10, 100) + '%' }"></div>
          </div>
        </div>

        <div class="stat-bar">
          <div class="stat-label">
            <span>Energy</span>
            <span>{{ agent.stats.energy.toFixed(0) }}/100</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill energy" :style="{ width: agent.stats.energy + '%' }"></div>
          </div>
        </div>
      </div>

      <div class="values-section">
        <h4>价值观</h4>
        <p class="values-text">{{ agent.values || '尚未形成明确价值观' }}</p>
      </div>

      <div class="actions-section">
        <button @click="showMemory" class="btn btn-secondary">查看记忆</button>
        <button @click="refreshAgent" class="btn btn-primary">刷新状态</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAgentStore } from '../../stores/agent'
import { useUIStore } from '../../stores/ui'

const agentStore = useAgentStore()
const uiStore = useUIStore()

const agent = computed(() => agentStore.selectedAgent)

function close() {
  agentStore.selectAgent(null)
}

function showMemory() {
  uiStore.toggleMemoryViewer()
}

async function refreshAgent() {
  if (agent.value) {
    await agentStore.fetchAgent(agent.value.id)
  }
}
</script>

<style scoped>
.agent-status-panel {
  position: fixed;
  right: 20px;
  top: 80px;
  width: 320px;
  background: rgba(26, 26, 46, 0.95);
  border: 1px solid #4a4a6a;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  z-index: 100;
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
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.label {
  color: #aaa;
}

.value {
  color: #fff;
  font-weight: 500;
}

.status-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  text-transform: uppercase;
}

.status-badge.idle {
  background: #666;
}

.status-badge.working {
  background: #aa4444;
}

.status-badge.moving {
  background: #44aa44;
}

.status-badge.sleeping {
  background: #4444aa;
}

.stats-section {
  margin: 16px 0;
}

.stats-section h4 {
  margin: 0 0 12px;
  font-size: 14px;
  color: #aaa;
  border-bottom: 1px solid #4a4a6a;
  padding-bottom: 4px;
}

.stat-bar {
  margin-bottom: 12px;
}

.stat-label {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #ccc;
  margin-bottom: 4px;
}

.progress-bar {
  height: 8px;
  background: #2a2a3a;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.progress-fill.health {
  background: linear-gradient(90deg, #ff4444, #ff6666);
}

.progress-fill.sanity {
  background: linear-gradient(90deg, #4488ff, #66aaff);
}

.progress-fill.wealth {
  background: linear-gradient(90deg, #ffaa00, #ffcc44);
}

.progress-fill.energy {
  background: linear-gradient(90deg, #44aa44, #66cc66);
}

.values-section {
  margin: 16px 0;
}

.values-section h4 {
  margin: 0 0 8px;
  font-size: 14px;
  color: #aaa;
  border-bottom: 1px solid #4a4a6a;
  padding-bottom: 4px;
}

.values-text {
  margin: 0;
  font-size: 13px;
  color: #ddd;
  line-height: 1.5;
  font-style: italic;
}

.actions-section {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

.btn {
  flex: 1;
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

.btn-secondary {
  background: #3a3a5a;
  color: #ccc;
}

.btn-secondary:hover {
  background: #4a4a6a;
}
</style>

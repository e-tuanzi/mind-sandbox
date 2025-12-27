<template>
  <div v-if="isOpen" class="admin-panel">
    <div class="panel-header">
      <h3>上帝视角控制台</h3>
      <button @click="close" class="close-btn">&times;</button>
    </div>

    <div class="panel-content">
      <div class="world-status">
        <h4>世界状态</h4>
        <div class="status-grid">
          <div class="status-item">
            <span class="label">时间:</span>
            <span class="value">{{ worldStore.formattedTime }}</span>
          </div>
          <div class="status-item">
            <span class="label">天气:</span>
            <span class="value">{{ worldStore.weather }}</span>
          </div>
          <div class="status-item">
            <span class="label">活跃 Agent:</span>
            <span class="value">{{ worldStore.activeAgentsCount }}</span>
          </div>
          <div class="status-item">
            <span class="label">状态:</span>
            <span class="value" :class="{ night: worldStore.isNight }">
              {{ worldStore.isNight ? '夜晚' : '白天' }}
            </span>
          </div>
        </div>
      </div>

      <div class="time-control">
        <h4>时间控制</h4>
        <div class="control-buttons">
          <button @click="tickWorld" :disabled="isTicking" class="btn btn-primary">
            {{ isTicking ? '推进中...' : '推进 1 小时' }}
          </button>
          <button @click="toggleAutoTick" class="btn" :class="autoTick ? 'btn-danger' : 'btn-secondary'">
            {{ autoTick ? '停止自动推进' : '开启自动推进' }}
          </button>
        </div>
      </div>

      <div class="event-injection">
        <h4>事件注入</h4>
        <div class="event-form">
          <select v-model="selectedEventType" class="event-select">
            <option value="GlobalCrisis">全球危机</option>
            <option value="WeatherChange">天气变化</option>
            <option value="EconomicEvent">经济事件</option>
          </select>
          <textarea
            v-model="eventDescription"
            placeholder="输入事件描述..."
            class="event-textarea"
          ></textarea>
          <button @click="injectEvent" :disabled="isInjecting" class="btn btn-primary">
            {{ isInjecting ? '注入中...' : '注入事件' }}
          </button>
        </div>
      </div>

      <div class="agent-list">
        <div class="section-header">
          <h4>Agent 列表</h4>
          <button @click="showCreateAgent = !showCreateAgent" class="btn-small">
            {{ showCreateAgent ? '关闭' : '新建' }}
          </button>
        </div>
        <div v-if="showCreateAgent" class="create-agent-form">
          <input
            v-model="newAgentId"
            placeholder="Agent ID"
            class="input-field"
          />
          <input
            v-model.number="newAgentX"
            type="number"
            placeholder="X 坐标"
            class="input-field"
          />
          <input
            v-model.number="newAgentY"
            type="number"
            placeholder="Y 坐标"
            class="input-field"
          />
          <button @click="createAgent" :disabled="isCreating" class="btn btn-primary btn-small">
            {{ isCreating ? '创建中...' : '创建' }}
          </button>
        </div>
        <div class="agent-scroll">
          <div
            v-for="agent in agentStore.agentList"
            :key="agent.id"
            @click="selectAgent(agent.id)"
            class="agent-item"
            :class="{ selected: agent.id === agentStore.selectedAgentId }"
          >
            <span class="agent-id">{{ agent.id }}</span>
            <span class="agent-action">{{ agent.current_action }}</span>
            <span class="agent-pos">({{ agent.x }}, {{ agent.y }})</span>
          </div>
        </div>
      </div>

      <div class="log-console">
        <h4>日志控制台</h4>
        <div class="log-scroll" ref="logContainer">
          <div v-for="(log, index) in logs" :key="index" class="log-entry" :class="log.type">
            <span class="log-time">{{ log.time }}</span>
            <span class="log-message">{{ log.message }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useWorldStore } from '../../stores/world'
import { useAgentStore } from '../../stores/agent'
import { useUIStore } from '../../stores/ui'
import { adminService } from '../../services/admin'
import type { LogEntry } from '../../types'

const worldStore = useWorldStore()
const agentStore = useAgentStore()
const uiStore = useUIStore()

const isOpen = computed(() => uiStore.showAdminPanel)
const isTicking = ref(false)
const isInjecting = ref(false)
const autoTick = ref(false)
const autoTickInterval = ref<number | null>(null)

const selectedEventType = ref('GlobalCrisis')
const eventDescription = ref('')

const showCreateAgent = ref(false)
const newAgentId = ref('')
const newAgentX = ref(10)
const newAgentY = ref(10)
const isCreating = ref(false)

const logs = ref<LogEntry[]>([])
const logContainer = ref<HTMLElement | null>(null)

onMounted(async () => {
  await worldStore.fetchWorldStatus()
  await agentStore.fetchAllAgents()
  addLog('info', '上帝视角控制台已启动')
})

onUnmounted(() => {
  if (autoTickInterval.value) {
    clearInterval(autoTickInterval.value)
  }
})

async function tickWorld() {
  isTicking.value = true
  try {
    // 推进 1 小时（每个 tick = 1 分钟，所以需要 60 个 ticks）
    const result = await worldStore.tickWorld(60)
    await agentStore.fetchAllAgents()
    const timeStr = result.current_time || result.time
    addLog('success', `时间推进到 ${timeStr}`)
  } catch (error) {
    addLog('error', '时间推进失败')
    console.error(error)
  } finally {
    isTicking.value = false
  }
}

function toggleAutoTick() {
  if (autoTick.value) {
    if (autoTickInterval.value) {
      clearInterval(autoTickInterval.value)
      autoTickInterval.value = null
    }
    autoTick.value = false
    addLog('info', '自动推进已停止')
  } else {
    autoTick.value = true
    addLog('info', '自动推进已开启 (每秒推进 1 次)')
    autoTickInterval.value = window.setInterval(() => {
      tickWorld()
    }, 1000)
  }
}

async function injectEvent() {
  if (!eventDescription.value.trim()) {
    addLog('warning', '请输入事件描述')
    return
  }

  isInjecting.value = true
  try {
    await adminService.injectEvent({
      type: selectedEventType.value,
      description: eventDescription.value
    })
    addLog('success', `事件已注入: ${selectedEventType.value}`)
    eventDescription.value = ''
  } catch (error) {
    addLog('error', '事件注入失败')
    console.error(error)
  } finally {
    isInjecting.value = false
  }
}

function selectAgent(id: string) {
  agentStore.selectAgent(id)
  addLog('info', `已选择 Agent: ${id}`)
}

async function createAgent() {
  if (!newAgentId.value.trim()) {
    addLog('warning', '请输入 Agent ID')
    return
  }

  isCreating.value = true
  try {
    await adminService.createAgent(newAgentId.value, newAgentX.value, newAgentY.value)
    await agentStore.fetchAllAgents()
    addLog('success', `Agent ${newAgentId.value} 创建成功`)
    newAgentId.value = ''
    showCreateAgent.value = false
  } catch (error) {
    addLog('error', 'Agent 创建失败')
    console.error(error)
  } finally {
    isCreating.value = false
  }
}

function addLog(type: 'info' | 'success' | 'warning' | 'error', message: string) {
  const now = new Date()
  const time = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
  logs.value.push({ type, message, time })
  
  nextTick(() => {
    if (logContainer.value) {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }
  })
}

function close() {
  uiStore.toggleAdminPanel()
}
</script>

<style scoped>
.admin-panel {
  position: fixed;
  left: 20px;
  top: 80px;
  width: 380px;
  max-height: calc(100vh - 100px);
  background: rgba(26, 26, 46, 0.98);
  border: 1px solid #4a4a6a;
  border-radius: 8px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.7);
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
  overflow-y: auto;
  max-height: calc(100vh - 160px);
}

.world-status,
.time-control,
.event-injection,
.agent-list,
.log-console {
  margin-bottom: 20px;
}

.world-status h4,
.time-control h4,
.event-injection h4,
.agent-list h4,
.log-console h4 {
  margin: 0 0 12px;
  font-size: 14px;
  color: #aaa;
  border-bottom: 1px solid #4a4a6a;
  padding-bottom: 4px;
}

.status-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  padding: 8px;
  background: rgba(42, 42, 58, 0.5);
  border-radius: 4px;
}

.label {
  color: #aaa;
  font-size: 12px;
}

.value {
  color: #fff;
  font-size: 12px;
  font-weight: 500;
}

.value.night {
  color: #8888ff;
}

.control-buttons {
  display: flex;
  gap: 8px;
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

.btn-primary:hover:not(:disabled) {
  background: #5a5a9a;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #3a3a5a;
  color: #ccc;
}

.btn-secondary:hover {
  background: #4a4a6a;
}

.btn-danger {
  background: #8a4a4a;
  color: #fff;
}

.btn-danger:hover {
  background: #9a5a5a;
}

.event-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.event-select {
  padding: 8px;
  background: #2a2a3a;
  border: 1px solid #4a4a6a;
  border-radius: 4px;
  color: #fff;
  font-size: 13px;
}

.event-select:focus {
  outline: none;
  border-color: #6a6a8a;
}

.event-textarea {
  padding: 8px;
  background: #2a2a3a;
  border: 1px solid #4a4a6a;
  border-radius: 4px;
  color: #fff;
  font-size: 13px;
  min-height: 60px;
  resize: vertical;
}

.event-textarea:focus {
  outline: none;
  border-color: #6a6a8a;
}

.agent-scroll {
  max-height: 150px;
  overflow-y: auto;
}

.agent-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  background: rgba(42, 42, 58, 0.5);
  border-radius: 4px;
  margin-bottom: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.agent-item:hover {
  background: rgba(58, 58, 74, 0.8);
}

.agent-item.selected {
  background: rgba(74, 74, 138, 0.8);
  border: 1px solid #6a6aaa;
}

.agent-id {
  color: #fff;
  font-size: 13px;
  font-weight: 500;
}

.agent-action {
  color: #aaa;
  font-size: 12px;
}

.agent-pos {
  color: #666;
  font-size: 11px;
}

.log-scroll {
  max-height: 200px;
  overflow-y: auto;
  background: #1a1a2a;
  border-radius: 4px;
  padding: 8px;
}

.log-entry {
  display: flex;
  gap: 8px;
  padding: 4px 0;
  font-size: 11px;
  line-height: 1.4;
}

.log-time {
  color: #666;
  min-width: 60px;
}

.log-message {
  color: #ccc;
}

.log-entry.info .log-message {
  color: #88ccff;
}

.log-entry.success .log-message {
  color: #66cc66;
}

.log-entry.warning .log-message {
  color: #ffcc66;
}

.log-entry.error .log-message {
  color: #ff6666;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-header h4 {
  margin: 0;
  font-size: 14px;
  color: #aaa;
  border-bottom: 1px solid #4a4a6a;
  padding-bottom: 4px;
  flex: 1;
}

.btn-small {
  padding: 4px 10px;
  font-size: 12px;
  background: #3a3a5a;
  color: #ccc;
  border: 1px solid #4a4a6a;
  border-radius: 4px;
  cursor: pointer;
}

.btn-small:hover {
  background: #4a4a6a;
  color: #fff;
}

.create-agent-form {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
  padding: 10px;
  background: rgba(42, 42, 58, 0.5);
  border-radius: 4px;
}

.input-field {
  flex: 1;
  min-width: 80px;
  padding: 6px 8px;
  background: #2a2a3a;
  border: 1px solid #4a4a6a;
  border-radius: 4px;
  color: #fff;
  font-size: 12px;
}

.input-field:focus {
  outline: none;
  border-color: #6a6a8a;
}
</style>

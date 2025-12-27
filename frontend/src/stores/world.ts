import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { worldService } from '../services/world'
import type { WorldStatus, GameTime } from '../types'

export const useWorldStore = defineStore('world', () => {
  const time = ref<GameTime>({ hour: 8, minute: 0 })
  const weather = ref('Sunny')
  const activeAgentsCount = ref(0)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const formattedTime = computed(() => {
    return `${time.value.hour.toString().padStart(2, '0')}:${time.value.minute.toString().padStart(2, '0')}`
  })

  const isNight = computed(() => {
    return time.value.hour >= 22 || time.value.hour < 6
  })

  async function fetchWorldStatus() {
    isLoading.value = true
    error.value = null
    try {
      const status = await worldService.getStatus()
      const [hour, minute] = status.time.split(':').map(Number)
      time.value = { hour, minute }
      weather.value = status.weather
      activeAgentsCount.value = status.active_agents
    } catch (e) {
      error.value = 'Failed to fetch world status'
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  async function tickWorld() {
    try {
      const result = await worldService.tick()
      const [hour, minute] = result.time.split(':').map(Number)
      time.value = { hour, minute }
      return result
    } catch (e) {
      error.value = 'Failed to tick world'
      console.error(e)
      throw e
    }
  }

  function updateTime(hour: number, minute: number) {
    time.value = { hour, minute }
  }

  return {
    time,
    weather,
    activeAgentsCount,
    isLoading,
    error,
    formattedTime,
    isNight,
    fetchWorldStatus,
    tickWorld,
    updateTime
  }
})

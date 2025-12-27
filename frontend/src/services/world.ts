import api from './api'
import type { WorldStatus } from '../types'

export const worldService = {
  async getStatus(language: string = 'zh'): Promise<WorldStatus> {
    const response = await api.get('/world/status', { params: { language } })
    return response.data
  },

  /**
   * 推进世界时间
   * @param ticks 要推进的 tick 数量，每个 tick 对应配置中的 MINUTES_PER_TICK 分钟
   */
  async tick(ticks: number = 1): Promise<{ message: string; time: string; current_time: string; is_night: boolean; active_agents: number }> {
    const response = await api.post('/admin/world/tick', { ticks })
    return response.data
  }
}

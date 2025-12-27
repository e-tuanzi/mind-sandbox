export interface AgentStats {
  health: number
  sanity: number
  wealth: number
  energy: number
}

export type ActionType = 
  | 'IDLE' 
  | 'MOVING' 
  | 'WORKING' 
  | 'EATING' 
  | 'SLEEPING' 
  | 'RESTING'

export interface Agent {
  id: string
  x: number
  y: number
  type: string
  stats: AgentStats
  current_action: ActionType
  is_active: boolean
  is_sleeping: boolean
  values: string
}

export interface Thought {
  content: string
  timestamp: string
  action: string
}

export interface GameTime {
  hour: number
  minute: number
}

export interface WorldStatus {
  time: string
  weather: string
  active_agents: number
}

export interface AgentHistory {
  agent_id: string
  history: Array<{ content: string }>
  values: string
}

export interface InjectEventRequest {
  type: string
  description: string
  target_agents?: string[]
}

export type LogType = 'info' | 'success' | 'warning' | 'error'

export interface LogEntry {
  type: LogType
  message: string
  time: string
}

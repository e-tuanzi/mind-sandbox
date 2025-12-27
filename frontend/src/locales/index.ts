import type { Language } from '../stores/locale'

export interface Translations {
  common: {
    loading: string
    error: string
    close: string
    create: string
    save: string
    cancel: string
    delete: string
    search: string
    refresh: string
  }
  world: {
    title: string
    time: string
    weather: string
    agents: string
    status: string
  }
  admin: {
    title: string
    worldControl: string
    eventInjection: string
    agentList: string
    eventDescription: string
    eventPlaceholder: string
    injectEvent: string
    injecting: string
    advanceHour: string
    advancing: string
    autoTickStart: string
    autoTickStop: string
    newAgent: string
    close: string
    agentId: string
    xCoordinate: string
    yCoordinate: string
    logs: string
  }
  logs: {
    adminStarted: string
    autoTickStopped: string
    autoTickStarted: string
    eventInjected: string
    eventInjectFailed: string
    agentSelected: string
    agentCreated: string
    agentCreateFailed: string
    enterAgentId: string
    enterEventDescription: string
    timeAdvanced: string
    timeAdvanceFailed: string
    agentCreateSuccess: string
  }
  agent: {
    id: string
    position: string
    activity: string
    state: string
    health: string
    memory: string
    noDescription: string
  }
  weather: {
    sunny: string
    rainy: string
    cloudy: string
    stormy: string
    snowy: string
  }
}

const translations: Record<Language, Translations> = {
  zh: {
    common: {
      loading: '加载中...',
      error: '错误',
      close: '关闭',
      create: '创建',
      save: '保存',
      cancel: '取消',
      delete: '删除',
      search: '搜索',
      refresh: '刷新'
    },
    world: {
      title: '数字灵魂',
      time: '时间',
      weather: '天气',
      agents: '活跃 Agent',
      status: '状态'
    },
    admin: {
      title: '管理面板',
      worldControl: '世界控制',
      eventInjection: '事件注入',
      agentList: 'Agent 列表',
      eventDescription: '事件描述',
      eventPlaceholder: '输入事件描述...',
      injectEvent: '注入事件',
      injecting: '注入中...',
      advanceHour: '推进 1 小时',
      advancing: '推进中...',
      autoTickStart: '开启自动推进',
      autoTickStop: '停止自动推进',
      newAgent: '新建',
      close: '关闭',
      agentId: 'Agent ID',
      xCoordinate: 'X 坐标',
      yCoordinate: 'Y 坐标',
      logs: '操作日志'
    },
    logs: {
      adminStarted: '上帝视角控制台已启动',
      autoTickStopped: '自动推进已停止',
      autoTickStarted: '自动推进已开启 (每秒推进 1 次)',
      eventInjected: '事件已注入: {eventType}',
      eventInjectFailed: '事件注入失败',
      agentSelected: '已选择 Agent: {agentId}',
      agentCreated: 'Agent {agentId} 创建成功',
      agentCreateFailed: 'Agent 创建失败',
      enterAgentId: '请输入 Agent ID',
      enterEventDescription: '请输入事件描述',
      timeAdvanced: '时间推进到 {time}',
      timeAdvanceFailed: '时间推进失败'
    },
    agent: {
      id: 'ID',
      position: '位置',
      activity: '活动',
      state: '状态',
      health: '健康',
      memory: '记忆',
      noDescription: '暂无描述'
    },
    weather: {
      sunny: '晴朗',
      rainy: '雨天',
      cloudy: '多云',
      stormy: '暴风雨',
      snowy: '下雪'
    }
  },
  en: {
    common: {
      loading: 'Loading...',
      error: 'Error',
      close: 'Close',
      create: 'Create',
      save: 'Save',
      cancel: 'Cancel',
      delete: 'Delete',
      search: 'Search',
      refresh: 'Refresh'
    },
    world: {
      title: 'Digital Soul',
      time: 'Time',
      weather: 'Weather',
      agents: 'Active Agents',
      status: 'Status'
    },
    admin: {
      title: 'Admin Panel',
      worldControl: 'World Control',
      eventInjection: 'Event Injection',
      agentList: 'Agent List',
      eventDescription: 'Event Description',
      eventPlaceholder: 'Enter event description...',
      injectEvent: 'Inject Event',
      injecting: 'Injecting...',
      advanceHour: 'Advance 1 Hour',
      advancing: 'Advancing...',
      autoTickStart: 'Start Auto Tick',
      autoTickStop: 'Stop Auto Tick',
      newAgent: 'Create New',
      close: 'Close',
      agentId: 'Agent ID',
      xCoordinate: 'X Coordinate',
      yCoordinate: 'Y Coordinate',
      logs: 'Operation Logs'
    },
    logs: {
      adminStarted: 'God view console started',
      autoTickStopped: 'Auto tick stopped',
      autoTickStarted: 'Auto tick started (1 tick per second)',
      eventInjected: 'Event injected: {eventType}',
      eventInjectFailed: 'Event injection failed',
      agentSelected: 'Agent selected: {agentId}',
      agentCreated: 'Agent {agentId} created successfully',
      agentCreateFailed: 'Agent creation failed',
      enterAgentId: 'Please enter Agent ID',
      enterEventDescription: 'Please enter event description',
      timeAdvanced: 'Time advanced to {time}',
      timeAdvanceFailed: 'Time advance failed'
    },
    agent: {
      id: 'ID',
      position: 'Position',
      activity: 'Activity',
      state: 'State',
      health: 'Health',
      memory: 'Memory',
      noDescription: 'No description'
    },
    weather: {
      sunny: 'Sunny',
      rainy: 'Rainy',
      cloudy: 'Cloudy',
      stormy: 'Stormy',
      snowy: 'Snowy'
    }
  }
}

/**
 * 获取指定语言的翻译
 */
export function getTranslation(lang: Language): Translations {
  return translations[lang]
}

/**
 * 获取天气翻译
 */
export function getWeatherTranslation(weather: string, lang: Language): string {
  const weatherKey = weather.toLowerCase() as keyof Translations['weather']
  const t = translations[lang].weather
  return t[weatherKey] || weather
}

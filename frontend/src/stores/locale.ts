import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { useAgentStore } from './agent'

export type Language = 'zh' | 'en'

export const useLocaleStore = defineStore('locale', () => {
  const currentLanguage = ref<Language>('zh')

  function setLanguage(lang: Language) {
    currentLanguage.value = lang
  }

  function toggleLanguage() {
    currentLanguage.value = currentLanguage.value === 'zh' ? 'en' : 'zh'
  }

  // 监听语言变化，自动刷新 Agent 数据
  watch(currentLanguage, () => {
    const agentStore = useAgentStore()
    if (agentStore.agentList.length > 0) {
      agentStore.fetchAllAgents()
    }
  })

  return {
    currentLanguage,
    setLanguage,
    toggleLanguage
  }
})

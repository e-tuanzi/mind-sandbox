<template>
  <div ref="gameContainer" class="game-container"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import Phaser from 'phaser'
import { GameScene } from './GameScene'
import { useAgentStore } from '../../stores/agent'
import { useWorldStore } from '../../stores/world'
import { agentService } from '../../services/agent'

const gameContainer = ref<HTMLDivElement>()
let game: Phaser.Game | null = null
let gameScene: GameScene | null = null
let pollInterval: number | null = null

const agentStore = useAgentStore()
const worldStore = useWorldStore()

onMounted(async () => {
  await agentStore.fetchAllAgents()
  await worldStore.fetchWorldStatus()

  initGame()
  startPolling()
})

onUnmounted(() => {
  if (game) {
    game.destroy(true)
    game = null
  }
  if (pollInterval) {
    clearInterval(pollInterval)
  }
})

function initGame() {
  if (!gameContainer.value) return

  const config: Phaser.Types.Core.GameConfig = {
    type: Phaser.AUTO,
    parent: gameContainer.value,
    width: gameContainer.value.clientWidth,
    height: gameContainer.value.clientHeight,
    backgroundColor: '#1a1a2e',
    scene: [GameScene]
  }

  game = new Phaser.Game(config)

  game.events.once('ready', () => {
    if (game && game.scene.getScene('GameScene')) {
      gameScene = game.scene.getScene('GameScene') as GameScene
    }
  })
}

function startPolling() {
  pollInterval = window.setInterval(async () => {
    await pollAgentThoughts()
    await agentStore.fetchAllAgents()
    await worldStore.fetchWorldStatus()
  }, 2000)
}

async function pollAgentThoughts() {
  for (const agent of agentStore.agentList) {
    try {
      const thought = await agentService.getAgentThought(agent.id)
      if (gameScene) {
        gameScene.updateThoughtBubble(agent.id, thought.content)
      }
    } catch (error) {
      console.error(`Failed to fetch thought for agent ${agent.id}:`, error)
    }
  }
}

watch(() => agentStore.selectedAgentId, (newId) => {
  if (gameScene && newId) {
    gameScene.centerOnAgent(newId)
  }
})

defineExpose({ game, gameScene })
</script>

<style scoped>
.game-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>

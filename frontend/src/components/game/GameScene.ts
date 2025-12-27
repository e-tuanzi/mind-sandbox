import Phaser from 'phaser'
import { useAgentStore } from '../../stores/agent'
import { useUIStore } from '../../stores/ui'
import type { Agent } from '../../types'

const TILE_SIZE = 32

export type TerrainType = 'WALL' | 'FLOOR' | 'RESIDENTIAL' | 'WORKPLACE_996' | 'WORKPLACE_965' | 'COMMERCIAL' | 'PARK'

export interface MapData {
  width: number
  height: number
  tiles: TerrainType[][]
}

export class GameScene extends Phaser.Scene {
  private agentSprites: Map<string, Phaser.GameObjects.Sprite> = new Map()
  private thoughtTexts: Map<string, Phaser.GameObjects.Text> = new Map()
  private tileGraphics!: Phaser.GameObjects.Graphics
  private mapData: MapData | null = null

  constructor() {
    super({ key: 'GameScene' })
  }

  preload() {
    this.createPlaceholderAssets()
  }

  create() {
    this.createMap()
    this.setupEvents()
  }

  update() {
    this.updateAgentPositions()
    this.updateThoughtBubbles()
  }

  private createPlaceholderAssets() {
    const graphics = this.make.graphics({ x: 0, y: 0, add: false })

    graphics.fillStyle(0x404040)
    graphics.fillRect(0, 0, TILE_SIZE, TILE_SIZE)
    graphics.generateTexture('tile_wall', TILE_SIZE, TILE_SIZE)

    graphics.clear()
    graphics.fillStyle(0x808080)
    graphics.fillRect(0, 0, TILE_SIZE, TILE_SIZE)
    graphics.generateTexture('tile_floor', TILE_SIZE, TILE_SIZE)

    graphics.clear()
    graphics.fillStyle(0x666688)
    graphics.fillRect(4, 4, TILE_SIZE - 8, TILE_SIZE - 8)
    graphics.generateTexture('tile_residential', TILE_SIZE, TILE_SIZE)

    graphics.clear()
    graphics.fillStyle(0xaa4444)
    graphics.fillRect(4, 4, TILE_SIZE - 8, TILE_SIZE - 8)
    graphics.generateTexture('tile_work996', TILE_SIZE, TILE_SIZE)

    graphics.clear()
    graphics.fillStyle(0x44aa44)
    graphics.fillRect(4, 4, TILE_SIZE - 8, TILE_SIZE - 8)
    graphics.generateTexture('tile_work965', TILE_SIZE, TILE_SIZE)

    graphics.clear()
    graphics.fillStyle(0xaaaa44)
    graphics.fillRect(4, 4, TILE_SIZE - 8, TILE_SIZE - 8)
    graphics.generateTexture('tile_commercial', TILE_SIZE, TILE_SIZE)

    graphics.clear()
    graphics.fillStyle(0x44aa66)
    graphics.fillRect(4, 4, TILE_SIZE - 8, TILE_SIZE - 8)
    graphics.generateTexture('tile_park', TILE_SIZE, TILE_SIZE)

    graphics.clear()

    const agentGraphics = this.make.graphics({ x: 0, y: 0, add: false })
    agentGraphics.fillStyle(0x00aaff)
    agentGraphics.fillCircle(TILE_SIZE / 2, TILE_SIZE / 2, TILE_SIZE / 3)
    agentGraphics.generateTexture('agent_idle', TILE_SIZE, TILE_SIZE)

    agentGraphics.clear()
    agentGraphics.fillStyle(0xffaa00)
    agentGraphics.fillCircle(TILE_SIZE / 2, TILE_SIZE / 2, TILE_SIZE / 3)
    agentGraphics.generateTexture('agent_working', TILE_SIZE, TILE_SIZE)

    agentGraphics.clear()
    agentGraphics.fillStyle(0x888888)
    agentGraphics.fillCircle(TILE_SIZE / 2, TILE_SIZE / 2, TILE_SIZE / 3)
    agentGraphics.generateTexture('agent_sleeping', TILE_SIZE, TILE_SIZE)
  }

  private createMap() {
    this.tileGraphics = this.add.graphics()
    
    this.cameras.main.setBackgroundColor('#1a1a2e')
    this.cameras.main.setZoom(1.5)
    this.cameras.main.centerOn(10 * TILE_SIZE, 10 * TILE_SIZE)

    this.drawDefaultMap()
  }

  private drawDefaultMap() {
    const width = 20
    const height = 20
    const tiles: TerrainType[][] = []

    for (let y = 0; y < height; y++) {
      tiles[y] = []
      for (let x = 0; x < width; x++) {
        if (x === 0 || x === width - 1 || y === 0 || y === height - 1) {
          tiles[y][x] = 'WALL'
        } else if (x < 5 && y < 5) {
          tiles[y][x] = 'RESIDENTIAL'
        } else if (x >= 5 && x < 10 && y < 5) {
          tiles[y][x] = 'WORKPLACE_996'
        } else if (x >= 10 && x < 15 && y < 5) {
          tiles[y][x] = 'WORKPLACE_965'
        } else if (x >= 15 && y < 5) {
          tiles[y][x] = 'PARK'
        } else if (x >= 5 && x < 15 && y >= 5 && y < 10) {
          tiles[y][x] = 'COMMERCIAL'
        } else {
          tiles[y][x] = 'FLOOR'
        }
      }
    }

    this.mapData = { width, height, tiles }
    this.renderMap()
  }

  private renderMap() {
    if (!this.mapData) return

    this.tileGraphics.clear()

    for (let y = 0; y < this.mapData.height; y++) {
      for (let x = 0; x < this.mapData.width; x++) {
        const tile = this.mapData.tiles[y][x]
        const color = this.getTerrainColor(tile)
        this.tileGraphics.fillStyle(color)
        this.tileGraphics.fillRect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1)
      }
    }
  }

  private getTerrainColor(terrain: TerrainType): number {
    const colors: Record<TerrainType, number> = {
      'WALL': 0x404040,
      'FLOOR': 0x808080,
      'RESIDENTIAL': 0x666688,
      'WORKPLACE_996': 0xaa4444,
      'WORKPLACE_965': 0x44aa44,
      'COMMERCIAL': 0xaaaa44,
      'PARK': 0x44aa66
    }
    return colors[terrain]
  }

  private setupEvents() {
    this.input.on('pointerdown', (pointer: Phaser.Input.Pointer) => {
      const worldPoint = this.cameras.main.getWorldPoint(pointer.x, pointer.y)
      const tileX = Math.floor(worldPoint.x / TILE_SIZE)
      const tileY = Math.floor(worldPoint.y / TILE_SIZE)

      this.handleTileClick(tileX, tileY)
    })
  }

  private handleTileClick(x: number, y: number) {
    const agentStore = useAgentStore()
    const clickedAgent = agentStore.agentList.find(a => a.x === x && a.y === y)

    if (clickedAgent) {
      agentStore.selectAgent(clickedAgent.id)
    } else {
      agentStore.selectAgent(null)
    }
  }

  updateAgents(agents: Agent[]) {
    agents.forEach(agent => {
      if (!this.agentSprites.has(agent.id)) {
        this.createAgentSprite(agent)
      }
      this.updateAgentSprite(agent)
    })

    const currentIds = new Set(agents.map(a => a.id))
    for (const id of this.agentSprites.keys()) {
      if (!currentIds.has(id)) {
        this.removeAgent(id)
      }
    }
  }

  private createAgentSprite(agent: Agent) {
    const sprite = this.add.sprite(
      agent.x * TILE_SIZE + TILE_SIZE / 2,
      agent.y * TILE_SIZE + TILE_SIZE / 2,
      'agent_idle'
    )
    sprite.setDisplaySize(TILE_SIZE * 0.8, TILE_SIZE * 0.8)
    this.agentSprites.set(agent.id, sprite)

    const thoughtText = this.add.text(0, 0, '', {
      fontSize: '10px',
      backgroundColor: '#ffffff',
      color: '#000000',
      padding: { x: 4, y: 2 },
      wordWrap: { width: 120 }
    })
    thoughtText.setOrigin(0.5, 1)
    thoughtText.setVisible(false)
    this.thoughtTexts.set(agent.id, thoughtText)
  }

  private updateAgentSprite(agent: Agent) {
    const sprite = this.agentSprites.get(agent.id)
    if (!sprite) return

    const targetX = agent.x * TILE_SIZE + TILE_SIZE / 2
    const targetY = agent.y * TILE_SIZE + TILE_SIZE / 2

    sprite.x = Phaser.Math.Linear(sprite.x, targetX, 0.1)
    sprite.y = Phaser.Math.Linear(sprite.y, targetY, 0.1)

    let textureKey = 'agent_idle'
    if (agent.is_sleeping) {
      textureKey = 'agent_sleeping'
    } else if (agent.current_action === 'WORKING') {
      textureKey = 'agent_working'
    }
    sprite.setTexture(textureKey)
  }

  private updateAgentPositions() {
    const agentStore = useAgentStore()
    this.updateAgents(agentStore.agentList)
  }

  updateThoughtBubble(agentId: string, content: string) {
    const uiStore = useUIStore()
    const sprite = this.agentSprites.get(agentId)
    const text = this.thoughtTexts.get(agentId)

    if (sprite && text) {
      if (content && content !== 'No thought recorded yet.') {
        text.setText(content)
        text.setPosition(sprite.x, sprite.y - TILE_SIZE / 2)
        text.setVisible(true)
        uiStore.addThoughtBubble(agentId, content)
      } else {
        text.setVisible(false)
      }
    }
  }

  private updateThoughtBubbles() {
    const uiStore = useUIStore()
    uiStore.clearExpiredBubbles(5000)

    for (const [id, bubble] of uiStore.thoughtBubbles.entries()) {
      const text = this.thoughtTexts.get(id)
      const sprite = this.agentSprites.get(id)
      if (text && sprite) {
        text.setPosition(sprite.x, sprite.y - TILE_SIZE / 2)
        if (Date.now() - bubble.timestamp > 5000) {
          text.setVisible(false)
          uiStore.removeThoughtBubble(id)
        }
      }
    }
  }

  private removeAgent(id: string) {
    const sprite = this.agentSprites.get(id)
    const text = this.thoughtTexts.get(id)

    if (sprite) sprite.destroy()
    if (text) text.destroy()

    this.agentSprites.delete(id)
    this.thoughtTexts.delete(id)
  }

  centerOnAgent(agentId: string) {
    const sprite = this.agentSprites.get(agentId)
    if (sprite) {
      this.cameras.main.pan(sprite.x, sprite.y, 500)
    }
  }
}

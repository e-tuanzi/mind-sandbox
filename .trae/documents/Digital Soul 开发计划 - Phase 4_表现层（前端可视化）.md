## Digital Soul 开发计划 - Phase 4: 表现层（前端可视化）

### 阶段概述

本阶段将构建前端表现层，实现 2D 像素风格的模拟世界可视化，让观察者能够直观地看到 Agent 的行为、状态和思维活动。

### 1. 项目初始化

**目标**：创建标准化的前端项目结构，配置开发环境。

**实现内容**：
- 创建 `frontend/` 目录结构
  ```
  frontend/
  ├── public/              # 静态资源
  │   └── assets/          # 像素图块、角色精灵图
  ├── src/
  │   ├── components/      # Vue 组件
  │   │   ├── game/        # 游戏渲染相关
  │   │   ├── ui/          # UI 组件
  │   │   └── admin/       # 管理员界面
  │   ├── stores/          # Pinia 状态管理
  │   ├── services/        # API 服务
  │   ├── types/           # TypeScript 类型定义
  │   └── main.ts          # 入口文件
  ├── package.json
  ├── vite.config.ts
  └── tsconfig.json
  ```
- 初始化 Vue 3 + TypeScript 项目
- 配置 Vite 构建工具
- 安装核心依赖：
  - `vue@^3.3`
  - `pinia`（状态管理）
  - `phaser@^3.60`（2D 游戏引擎）
  - `axios`（HTTP 请求）
  - `@types/phaser`

### 2. 渲染引擎（Game Engine）

**目标**：将后端的世界数据渲染为 2D 像素画面。

#### 2.1 游戏场景架构

**实现内容**：
- `GameScene.ts`：主游戏场景类
  - `preload()`：加载图块资源（地形、建筑物、角色精灵）
  - `create()`：初始化游戏世界，建立与后端的 WebSocket 连接
  - `update()`：每帧更新逻辑，处理平滑移动插值

#### 2.2 地图渲染

**实现内容**：
- 读取 `/api/v1/world/status` 获取地图数据
- 根据 `TerrainType` 渲染不同图块：
  - `RESIDENTIAL` → 住宅区图块（灰色建筑）
  - `WORKPLACE_996` → 996 企业图块（红色高耸建筑）
  - `WORKPLACE_965` → 965 企业图块（绿色低层建筑）
  - `COMMERCIAL` → 商业区图块（黄色店铺）
  - `PARK` → 公园图块（绿色树木）
  - `WALL` → 墙壁（黑色障碍）
- 使用 Phaser 的 `Tilemap` 系统管理网格世界

#### 2.3 Agent 实体渲染

**实现内容**：
- 为每个 Agent 创建 Phaser `Sprite` 实体
- 根据 Agent 状态显示不同姿态：
  - `IDLE` → 站立动画
  - `WORKING` → 工作动画
  - `MOVING` → 行走动画
  - `SLEEPING` → 躺卧动画
  - `EATING` → 进食动画
- 实现平滑移动插值（Lerp）：
  ```typescript
  // 将后端离散坐标转换为平滑移动
  targetX = agent.x * TILE_SIZE
  sprite.x = Phaser.Math.Linear(sprite.x, targetX, 0.1)
  ```

### 3. 数据监视器（Data Monitor）

**目标**：可视化 Agent 的心理活动，提供上帝视角观察能力。

#### 3.1 思维气泡（Thought Bubble）

**实现内容**：
- 创建 `ThoughtBubble.ts` 组件
- 轮询 `/api/v1/agents/{id}/thought` 或使用 WebSocket 推送
- 在 Agent 头顶显示思维内容：
  ```typescript
  // 使用 Phaser Text 显示气泡
  this.add.text(agentX, agentY - 20, thought, {
    fontSize: '12px',
    backgroundColor: '#ffffff',
    padding: { x: 4, y: 2 }
  })
  ```
- 气泡淡出效果：5 秒后自动消失

#### 3.2 状态面板（Status Panel）

**实现内容**：
- 创建 `AgentStatusPanel.vue` 组件
- 点击 Agent 时显示详细信息：
  - 四维状态数值条：
    - Health（红色进度条）
    - Sanity（蓝色进度条）
    - Wealth（金色进度条）
    - Energy（绿色进度条）
  - 当前动作标签
  - 价值观摘要
  - 位置坐标

#### 3.3 记忆查看器（Memory Viewer）

**实现内容**：
- 创建 `MemoryViewer.vue` 组件
- 调用 `/api/v1/agents/{id}/history` 获取历史记录
- 显示内容：
  - 每日日记列表
  - 长期记忆片段（向量检索结果）
  - 搜索框：支持语义搜索 Agent 记忆

#### 3.4 上帝视角工具（God View Admin）

**实现内容**：
- 创建 `AdminPanel.vue` 组件
- 功能：
  - **时间控制**：手动推进世界时间片（调用 `POST /api/v1/world/tick`）
  - **事件注入**：触发全局事件（调用 `POST /api/v1/admin/inject-event`）
  - **Agent 列表**：显示所有 Agent，支持点击切换观察对象
  - **全局状态**：显示世界时间、天气、活跃 Agent 数量
  - **日志控制台**：实时显示后端事件日志

### 4. 状态管理（Pinia Store）

**目标**：管理前端状态与后端数据同步。

**实现内容**：
- `stores/world.ts`：世界状态
  ```typescript
  export const useWorldStore = defineStore('world', {
    state: () => ({
      gameTime: { hour: 8, minute: 0 },
      weather: 'Sunny',
      agents: [] as Agent[]
    }),
    actions: {
      async fetchWorldStatus() { /* 调用 API */ },
      async tickWorld() { /* 推进时间 */ }
    }
  })
  ```
- `stores/agent.ts`：Agent 状态
  ```typescript
  export const useAgentStore = defineStore('agent', {
    state: () => ({
      selectedAgentId: null,
      agents: {} as Record<string, Agent>
    }),
    actions: {
      async fetchAgent(id: string) { /* 调用 API */ },
      async fetchAgentThought(id: string) { /* 调用 API */ }
    }
  })
  ```

### 5. API 服务层

**目标**：封装后端 API 调用。

**实现内容**：
- `services/api.ts`：Axios 实例配置
  ```typescript
  const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1'
  })
  ```
- `services/world.ts`：世界相关 API
- `services/agent.ts`：Agent 相关 API
- `services/admin.ts`：管理员相关 API

### 6. 集成与测试

**目标**：验证前后端联调效果。

#### 6.1 联调测试

| 测试项 | 验证点 |
|--------|--------|
| 地图渲染 | 地形图块正确显示，网格对齐 |
| Agent 移动 | Agent 平滑移动到目标位置 |
| 状态同步 | 四维数值实时更新 |
| 思维气泡 | 显示 Agent 最新思维内容 |
| 手动 Tick | 推进时间后世界状态变化 |
| 事件注入 | 注入事件后 Agent 产生反应 |

#### 6.2 性能优化

- 减少 API 轮询频率（使用 WebSocket 推送替代）
- 使用对象池管理 Sprite（避免频繁创建/销毁）
- 限制同时显示的思维气泡数量

### 7. 部署与配置

**目标**：实现前后端分离部署。

**实现内容**：
- 配置 CORS（后端已支持）
- 构建前端静态资源：`npm run build`
- 配置 Nginx 反向代理：
  ```nginx
  location /api/ {
    proxy_pass http://localhost:8000;
  }
  location / {
    root /var/www/digital-soul/frontend/dist;
  }
  ```

---

### Phase 4 完成标志

- ✅ 前端项目可独立运行（`npm run dev`）
- ✅ 游戏场景正确渲染地图和 Agent
- ✅ 点击 Agent 可查看状态面板和记忆
- ✅ 思维气泡实时显示 Agent 思考内容
- ✅ 管理员面板可注入事件和推进时间
- ✅ 前后端联调通过，完整展示 Agent 一天的生活
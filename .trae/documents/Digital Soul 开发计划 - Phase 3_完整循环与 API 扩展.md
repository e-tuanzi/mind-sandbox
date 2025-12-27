## Digital Soul 开发计划 - Phase 3: 完整循环与 API 扩展

### 1. Agent 模型完善与整合

**目标**：将分散的意识层模块整合到 Agent 实体中，使其成为具备完整决策能力的智能体。

**实现内容**：
- 完善 `Agent` 模型，关联 `MemorySystem` 和 `AgentBrain` 实例
- 添加 `current_action`、`action_queue` 属性，支持行动队列管理
- 实现 `Agent.decide_and_act()` 方法，封装完整决策循环
  1. **感知**：通过 `PerceptionFilter` 生成环境描述
  2. **检索**：从记忆库检索相关经验
  3. **思考**：调用 `AgentBrain` 生成决策
  4. **行动**：将决策转换为物理指令并执行
  5. **记录**：将行动和思考存入短期记忆

### 2. API 接口扩展

**目标**：实现完整的 Agent 交互接口，支持前端实时监控和控制。

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/v1/agents` | GET | 获取所有 Agent 列表 |
| `/api/v1/agents/{id}` | GET | 获取指定 Agent 的详细状态 |
| `/api/v1/agents/{id}/thought` | GET | 获取 Agent 的最新思维内容（用于思维气泡） |
| `/api/v1/agents/{id}/history` | GET | 获取 Agent 的历史日记记录 |
| `/api/v1/world/tick` | POST | 手动推进世界时间片（用于测试） |
| `/api/v1/admin/inject-event` | POST | 管理员接口，注入全局事件 |

### 3. 模拟循环引擎

**目标**：实现完整的游戏循环，驱动多个 Agent 并发决策。

**实现内容**：
- 在 `WorldEngine` 中添加 `run_agent_loop()` 方法
- 每个时间片：
  1. 推进时间 (`TimeSystem.tick()`)
  2. 对每个活跃 Agent 调用 `decide_and_act()`
  3. 应用行动效果 (`StateDynamics`)
  4. 检查夜间条件，触发反思机制

### 4. 夜间反思机制

**目标**：实现 Agent 的每日反思，更新价值观。

**实现内容**：
- 在 `WorldEngine` 中检测 `is_night()` 且 Agent 进入睡眠状态
- 调用 `AgentBrain.reflect(daily_log)` 生成反思
- 调用 `MemorySystem.consolidate_daily()` 归档记忆
- 更新 Agent 的 `values` 字段

### 5. 集成测试场景

**目标**：验证完整系统在复杂场景下的表现。

**测试用例**：

| ID | 场景 | 验证点 |
|----|------|--------|
| SCN-01 | **完整的一天** | Agent 从早晨到入睡的完整决策链，包含工作、消费、反思 |
| SCN-02 | **突发道德测试** | 注入"丢失钱包"事件，观察 Agent 的道德决策和次日反思 |

### 6. 测试清单更新

- `test_agent_integration.py`：测试 Agent 完整决策循环
- `test_api_agents.py`：测试 Agent 相关 API 接口
- `test_simulation_scenarios.py`：实现 SCN-01 和 SCN-02 场景测试

---

## Digital Soul 开发计划 - Phase 4: 表现层（前端可视化）

### 1. 技术栈初始化

- 初始化 `frontend/` 目录结构
- 配置 `package.json`，引入 **Vue 3 + TypeScript + Phaser 3**

### 2. 渲染引擎

**目标**：将后端的世界数据渲染为 2D 像素画面。

**实现内容**：
- 初始化 Phaser 场景，连接 `/api/v1/world/status`
- 实现地图网格渲染（根据 `TerrainType` 显示不同图块）
- 实现 Agent 实体渲染（根据状态显示不同姿态）
- 实现平滑移动插值

### 3. 数据监视器

**目标**：可视化 Agent 的心理活动。

**实现内容**：
- **思维气泡**：实时订阅 `/api/v1/agents/{id}/thought`，在 Agent 头顶显示
- **状态面板**：点击 Agent 显示 Health/Sanity/Wealth/Energy 数值条
- **记忆查看器**：展示 Agent 的日记摘要和记忆碎片
- **上帝视角工具**：管理员界面，支持注入事件和推进时间

---

### 总结

当前项目已完成：
- ✅ **Phase 1**：环境层（时间、地图、状态动力学）
- ✅ **Phase 2（部分）**：意识层（记忆、感知、决策引擎）
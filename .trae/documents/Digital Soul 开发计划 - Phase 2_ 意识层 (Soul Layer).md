**Phase 2: 意识层 (Soul Layer) 开发**

本阶段将构建 Agent 的“大脑”，使其具备感知、记忆和基于 LLM 的决策能力。

## 1. 依赖与配置 (Dependencies)
- 更新 `requirements.txt`: 引入 `langchain`, `langchain-openai`, `chromadb`, `tiktoken`。
- 更新 `.env` 配置: 添加 `OPENAI_API_KEY` 及模型配置。

## 2. 核心模块实现 (Core Modules)

### A. 感知系统 (Perception System)
- **目标**: 将环境数据转化为自然语言。
- **实现**:
    - 定义 `EnvironmentSnapshot` 数据模型（包含自身状态、周围环境、可视实体）。
    - 实现 `PerceptionFilter` 类，将快照格式化为 "You are at [Location]. You see [Entities]..."。

### B. 记忆系统 (Memory System)
- **目标**: 管理短期对话流与长期经验。
- **实现**:
    - `MemorySystem` 类。
    - **Short-term**: 基于 `deque` 的即时记忆缓冲区。
    - **Long-term**: 集成 `ChromaDB` (本地模式)，实现 `recall()` (向量检索) 和 `consolidate()` (归档)。

### C. 决策引擎 (Brain / Reasoning Engine)
- **目标**: 驱动 Agent 思考与行动。
- **实现**:
    - `AgentBrain` 类。
    - 封装 LLM 调用接口 (支持 `MockLLM` 用于无 Key 测试，与 `OpenAILLM` 用于实际运行)。
    - 实现 `decide_next_action()`: 组装 Prompt (System Prompt + Memory + Perception) -> JSON Output (`ActionDecision`)。

## 3. 集成与测试 (Integration & Testing)
- 更新 `Agent` 模型，关联 `MemorySystem` 和 `AgentBrain`。
- **测试用例**:
    - `SOUL-001`: 记忆检索相关性测试 (Mocked)。
    - `SOUL-002`: 决策一致性测试 (Mocked)。

---
*注意：为了保证在没有 API Key 的情况下也能验证系统逻辑，我将优先实现一个 `MockLLM`，它会根据规则返回预设的动作，同时保留接入真实 OpenAI API 的能力。*
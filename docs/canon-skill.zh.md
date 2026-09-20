# Canon Skill 0.1.0 — 实验版

Canon Skill 是面向固定主体的通用 Canon-aware 图像生成/编辑执行契约，并提供确定性的辅助代码。它不是图像模型、内置 Subject Pack、视觉识别服务或某家供应商的生成客户端。

## 边界与使用

Subject Project 负责“主体是什么”：书面 Canon、invariant groups、视觉参考、calibration、专属 validators、hooks 与 delivery。Canon Skill 负责“如何尊重这些 authority”。执行面负责真实工具、资产读取、视觉检查与授权。

通过本仓库现有安装脚本安装 `skills/canon-skill`，并携带可用 Subject Pack 调用：

```text
$canon-skill 使用这个 Subject Pack 编译三个镜头，保持 canonical identity，外部参考图只用于 pose 和 lighting；暂时不要生图。
```

Prompt Mode 只编译书面意图，不读取 canonical generation inventory 或传输其中的图片。Gen Mode 单独解析 route、image roles、外部 reference scope、最小 canonical evidence、执行能力和 gates，再冻结并执行一个 Packet。前置条件缺失时直接阻塞，不退化为更弱的流程。

## 实现位置

薄入口 [SKILL.md](../skills/canon-skill/SKILL.md) 路由至 begin、Prompt Mode 和 Gen Mode。按需契约位于 `references/`。六份 JSON Schema 分别描述 Subject Pack、references、calibration、runtime state、generation packet 与 result。`scripts/contract_runtime.py` 提供 route/role resolution、最小覆盖、Packet 不可变性、作用域绑定 gates、分类、recovery、hook invocation、transport checks 与 continuity/import 的确定性基础函数。

辅助代码仅依赖 Python 标准库；schema 与 fixture 测试在 CI 中使用固定的 jsonschema 和 PyYAML。`schemas.canon-skill.invalid` 下的 schema id 是本地注册表标识，不是在线服务地址；验证时在本地注册全部六份 schema。

可选 exact-cover helper 最多处理 24 个已经按任务相关性筛选的候选资产。更大 inventory 需要先缩小候选集合，或由执行面提供等价 planner。Helper 不执行图像模型推理，不自动识别人，也不会把调用方提供的 evidence 当成天然可信证明。

## 验证

仓库包含 63 项可执行通用契约测试，其中包括明确标为模拟的 Human/Pet/Virtual 三条端到端流程，并覆盖成功路径和负向边界。原有 Markdown trigger/runtime/validation 场景仍是前向测试规范，不被计为已执行的视觉测试。

```bash
python -m pip install 'jsonschema==4.26.0' 'PyYAML==6.0.3'
python -m unittest discover -s tests -p 'test_*.py' -v
./scripts/validate-skills.py
npm ci --ignore-scripts --no-audit --no-fund
npm run check
npx playwright install chromium
npm run test:browser
```

CI 还会使用固定的 Agent Skills `skills-ref` 和官方上游 skill-creator quick validator 检查全部 skills，测试安装器的检查、首次安装、重复安装和冲突拒绝，验证完整中文镜像及版本化网站资产，并运行 Chromium smoke tests。

合成字节、模拟 receipts、测试提供的 PASS 报告和 fixture manifest，均不能证明真实生图或视觉保真。执行面必须实际取得参考图并检查真实 candidate，才能验收。

## 版本门槛

| 阶段 | 必需证据 | 当前分发状态 |
| --- | --- | --- |
| 0.1.0 实验版 | 通用契约、三类主体、Prompt/Gen、routing、evidence、Packet、validation/recovery、continuity 与 hooks | 已实现，并有可执行契约验证 |
| 0.2.0 | 真实 consumer pack、完整 source-bound legacy parity、校准/Hook 行为及生成语义保持 | 保留门槛；私有 consumer 开发和有范围的 Shadow 检查不等于完整切换证据 |
| 1.0.0 | 至少两个不同真实 Subject Project 成功消费 runtime | 匿名 fixtures 或单一 consumer 的 metadata 测试不能证明 |

私有 consumer 的身份事实和资产不进入公共 Skill。不得仅因 CI 通过就宣称生产可用、执行 cutover，或把 fixture 算成已接入项目。接入冲突、未支持能力、真实视觉 QA 与 Principal approvals 应记录在各自 Subject Project 内。

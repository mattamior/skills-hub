# Canon Skill 开发与验收

[English](README.en.md)

## 已交付的核心

Canon Skill 是实验性的 Agent 指令运行时，附带确定性契约工具；它不是内置图像模型或视觉身份检测器。Subject Pack 与 generation backend 由调用方拥有。

Day 1–4 覆盖主体无关契约、证据 authority、六种 route、角色隔离、最小证据选择、临时状态、冻结 packet、三层 validator、五种结果分类、有界重试、来源记录、Prompt/Gen 交接、分阶段 hooks 与传输抽象。指令配有 JSON Schemas，以及匿名 Human/Pet/Virtual 的可执行声明级测试。

安装 jsonschema 与 PyYAML 后运行 `python -m unittest discover -s tests/canon-skill -v`。原有 Markdown 场景表仍属于人工 forward-test；画廊和安装器 CI 不等于 runtime 或视觉验收。新增 Canon workflow 执行真实单元测试及固定版本的上游 skill-creator 校验。

## Consumer 迁移

先把旧行为分为 GENERIC、SUBJECT_SPECIFIC 和 INFRASTRUCTURE，不改变生产路由。在主体自己的项目中构建 Subject Pack，以不可变 revision 固定 Canon Skill，并对源 metadata 做漂移检查。比较独立规范化的 legacy 结果与 pack 驱动的执行计划；同一个 mapper 调用两次不算独立回归。

检查 anchor ID 及顺序、条件支持、外部角色、edit/preview 行为、gates、retry、continuity、calibration、固定细节 finalization 与 delivery 来源边界。旧规则之间的矛盾必须作为明确 cutover 阻塞项保留，不能通过静默改变通用契约消除。

只有语义回归、实际图片传输、可信 hook 执行与必要的真实验收证据全部通过，才能切换。保留可回退的 legacy 入口。不得为了测试迁移而重新生成已经批准的 Canon/calibration 资产。

## 版本门槛

v0.1.0 要求通用契约覆盖三类主体，所有 runtime/interface 模型均已定义并验证。源码候选不自动等于已发布版本。

v0.2.0 还要求真实 consumer 的 Subject Pack、完整 legacy-versus-Canon 回归、生成语义保留、calibration 映射验证和主体自有的细节 hooks。声明级 shadow 测试不能证明生产图片行为一致，也不能授权切换。

v1.0.0 还要求至少两个不同真实 Subject Project 成功实际消费。匿名 fixture 不计入。合成的 PASS、自报的传输收据和没有执行过的视觉检查表都不能满足这些门槛。

## 保留的边界

具体 consumer 的事实、reference 文件名和 calibration 编号不得进入可复用实现。缺少必需图片、validator、hook 或 gate 时保持 BLOCKED。Construction precheck 不能成为完整验收，calibration 可以禁止自动重试，delivery derivative 永远不能回流到 identity 或 continuity。

# 吸收原意与语义复核

整合允许改变技能发现入口、文件位置和内部调用方式。原技能的目标、适用范围、前置条件、必需步骤及顺序、默认行为、约束、输出结构和完成标准应保留。相似能力不是相同流程，不能用合并或简化的名义替换。

## 本次修正

对照整合前仓库版本，恢复了被缩写的实现、项目配置和流程导航正文；恢复 TDD 原有的阶段划分；恢复 code-review 的双轴并行审查、完整 smell baseline 和分轴报告规则。补回先前调用替换中误删的限定语，包括实现流程的预先约定测试 seam，以及 wayfinder 的研究分支、上下文指针和目的说明。

code-review 与 review-work 分别保留为内部流程。两种 handoff 也分别保留，避免以相似性推定可互换。通用整合规则不再把原来的必需步骤改成可选。

`sources.json` 的 `semantic_baseline` 指向整合前的原文件与确切仓库版本，记录原正文哈希、允许的结构适配和本次恢复后的目标哈希。这是初次整合的可追溯基线；后续吸收有独立的语义核对记录。哈希证明具体文本身份，不证明自然语言的语义等价。

## 冲突与限制

- 原 TDD 流程把重构放到审查阶段，native verification 还包含 red-green-refactor 模式。两者保持独立，按选定流程执行；不得悄悄重写其中一方。
- 原 code-review 要求 Standards/Spec 独立并行审查、分轴报告；review-work 要求按严重程度排序。保留两个输出契约，入口明确区分。
- 原流程规定的工具、tracker、并行执行或发布步骤，若受环境或更高优先级指令限制，应说明未完成的步骤。不得以低配替代后仍声称等价完成。
- 发布、发消息、提交、推送等授权边界继续受用户请求和更高优先级指令约束。保留原流程的交付意图，不会因读取某章就自动获得额外授权。
- pstack 从最初就是部分实践来源，不应声称已完整保留整个上游技能。

## 逐来源记录

| 来源 | 当前正文 | 核对范围 |
| --- | --- | --- |
| `clarify-plan` | [GUIDE.md](references/workflows/clarify-plan/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `handoff` | [GUIDE.md](references/workflows/handoff/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--ask-matt` | [GUIDE.md](references/workflows/ask-matt/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--code-review` | [GUIDE.md](references/workflows/code-review/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--codebase-design` | [GUIDE.md](references/workflows/codebase-design/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--diagnosing-bugs` | [GUIDE.md](references/workflows/diagnosing-bugs/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--domain-modeling` | [GUIDE.md](references/workflows/domain-modeling/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--grill-with-docs` | [GUIDE.md](references/workflows/grill-with-docs/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--implement` | [GUIDE.md](references/workflows/implement/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--implement-spec` | [GUIDE.md](references/workflows/implement-spec/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--improve-codebase-architecture` | [GUIDE.md](references/workflows/improve-codebase-architecture/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--prototype` | [GUIDE.md](references/workflows/prototype-patterns/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--research` | [GUIDE.md](references/workflows/research/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--retro` | [GUIDE.md](references/workflows/retro/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--setup-matt-pocock-skills` | [GUIDE.md](references/workflows/setup-matt-pocock-skills/GUIDE.md) | 原正文保留；仅调整入口、调用与路径，安装检查改为内部流程可用性检查 |
| `mattpocock--engineering--tdd` | [GUIDE.md](references/workflows/tdd/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--to-spec` | [GUIDE.md](references/workflows/to-spec/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--to-tickets` | [GUIDE.md](references/workflows/to-tickets/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--triage` | [GUIDE.md](references/workflows/triage/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--wayfinder` | [GUIDE.md](references/workflows/wayfinder/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--engineering--wizard` | [GUIDE.md](references/workflows/wizard/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `mattpocock--productivity--handoff` | [GUIDE.md](references/workflows/handoff-compact/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `prototype` | [GUIDE.md](references/workflows/prototype/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `refactoring` | [08-refactoring.md](references/08-refactoring.md) | 原正文保留；仅调整入口、调用与路径 |
| `review-work` | [09-code-review.md](references/09-code-review.md) | 原正文保留；仅调整入口、调用与路径 |
| `slice-plan` | [GUIDE.md](references/workflows/slice-plan/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `technical-doc-writing` | [GUIDE.md](references/workflows/technical-doc-writing/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `vercel-composition-patterns` | [GUIDE.md](references/workflows/vercel-composition-patterns/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `vercel-react-best-practices` | [GUIDE.md](references/workflows/vercel-react-best-practices/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `web-design-guidelines` | [GUIDE.md](references/workflows/web-design-guidelines/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |
| `web-shader-extractor` | [GUIDE.md](references/workflows/web-shader-extractor/GUIDE.md) | 原正文保留；仅调整入口、调用与路径 |

## 后续吸收

每次候选都必须核对六个维度：目标与范围、前置条件、必需步骤与顺序、默认行为与约束、输出与完成标准、跨流程冲突。`semantic-review.json` 要求逐项保留结论及依据；记录确认后绑定当前候选内容，应用时检查记录仍然匹配。文本无冲突不能代替语义核对。

这道门槛能阻止遗漏核对或核对后又改候选，但不能自动判断复核依据是否正确。执行吸收的 agent 必须实际对照原文，遇到确实无法兼容的规则时应公开冲突，不得填表掩盖语义变化。

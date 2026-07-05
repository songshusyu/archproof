# ArchProof 架构证据审计 Skill

ArchProof 是一个面向 Codex/Agent 的可复用 Skill，用来审计“架构报告里的说法”是否真的能追溯到源码、配置、数据库约束、Redis Key、MQ 队列、自动化测试、日志和可复现部署证据。

它最初来自一个 Web 后端课程项目中的反复检查流程，但已经抽象成通用工具：课程项目只是第一个使用场景，不是绑定场景。

## 它解决什么问题

很多项目会写：

> 使用了网关、Redis、MQ、WebSocket/SSE、LLM、Docker Compose、生产高可用方案。

真正影响评分或评审质量的是：

> 每个亮点能不能对应到代码、接口、表、Key、队列、测试和运行证据？

ArchProof 的工作方式是把架构声明拆成证据链，输出：

- 需求到证据的追踪矩阵；
- 缺陷清单、影响范围与修复建议；
- 核心链路“证据护照”；
- 测试与故障注入计划；
- 已实现、已测试、仅设计、与代码矛盾、缺失的分级结论。

## 安装

```powershell
git clone git@github.com:songshusyu/archproof.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\archproof\skills\archproof-audit" "$env:USERPROFILE\.codex\skills\archproof-audit"
```

如果你的 Agent 支持项目级 Skill，也可以放在项目目录：

```text
.agents/skills/archproof-audit/
```

## 验证

```powershell
python C:\Users\xuhes\.codex\skills\.system\skill-creator\scripts\quick_validate.py `
  skills\archproof-audit

python skills\archproof-audit\scripts\test_collect_architecture_evidence.py
```

## 使用示例

可以直接让 Agent 执行：

> 使用 ArchProof 检查这个后端项目的架构报告是否有代码、Redis/MQ、数据库约束、测试和运行证据支撑，并输出追踪矩阵与缺陷清单。

## 边界

ArchProof 不会替你编造 QPS、准确率或生产部署结果。它的价值恰恰在于把“已验证”和“仅设计”分开，把复杂系统说清楚。

## 许可证

Apache License 2.0，见 [LICENSE](LICENSE)。

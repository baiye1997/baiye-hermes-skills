# Baiye Hermes Skills

一套基于 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 的 Skill 集合，主打 **AI + Obsidian 生活管理系统**。

> 🔍 配套 iOS 基金管理工具：[花花日记](https://github.com/baiye1997)

---

## 📦 Skills 一览

### 📰 信息流

| Skill | 说明 | 定时 | 依赖 |
|-------|------|------|------|
| [shan-shui-di-bao](skills/shan-shui-di-bao/) | 山水邸报 — 每日早晚报，整合天气/A股/财经新闻/板块热点 | 工作日 08:00 / 20:00 | [东财 API](#可选依赖)（可选） |
| [weekly-must-read](skills/weekly-must-read/) | 本周必读 — 从山水邸报提取 🔥 必读文章，按周汇总 | 每周日 10:00 | 依赖山水邸报 |

### 💰 投资（可选）

| Skill | 说明 | 定时 | 依赖 |
|-------|------|------|------|
| [investment-weekly](skills/investment-weekly/) | 投资周报 — 汇总花花日记持仓+山水邸报市场信息，生成周度复盘 | 每周日 10:15 | [花花日记](#花花日记) |

### 📝 笔记

| Skill | 说明 | 触发 |
|-------|------|------|
| [daily-recap](skills/daily-recap/) | 每日对话回顾 — 自动总结对话，生成个人日记 | 每天 23:00 |
| [idea-capture](skills/idea-capture/) | 灵感捕捉 — 快速记录想法，自动分类打标签 | 手动 |
| [reading-tracker](skills/reading-tracker/) | 阅读追踪 — 管理阅读清单和进度 | 手动 |
| [obsidian-auto-tags](skills/obsidian-auto-tags/) | 智能标签 — 自动扫描笔记提取关键词 | 手动/批量 |
| [knowledge-graph](skills/knowledge-graph/) | 知识图谱 — 分析笔记关联关系 | 手动/每月 |

### 📚 学习

| Skill | 说明 | 定时 |
|-------|------|------|
| [daily-english](skills/daily-english/) | 每日一学 — 每天一个英语单词/短语 | 每天 07:30 |

### 🚗 生活

| Skill | 说明 | 定时 |
|-------|------|------|
| [commute-reminder](skills/commute-reminder/) | 通勤提醒 — 天气+路况+今日事项 | 工作日 08:00 / 17:30 |

### 🎬 创作

| Skill | 说明 | 触发 |
|-------|------|------|
| [social-media-video-scripts](skills/social-media-video-scripts/) | 视频脚本 — 适配抖音/B站/小红书 | 手动 |

---

## 🚀 快速开始

### 前置要求

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) 已安装
- [Obsidian](https://obsidian.md/) + [Obsidian Headless CLI](https://github.com/nicholasgasior/obsidian-headless)（可选，用于同步）

### 安装

```bash
# 克隆仓库
git clone https://github.com/baiye1997/baiye-hermes-skills.git

# 复制你需要的 skill 到 Hermes skills 目录
cp -r baiye-hermes-skills/skills/daily-english ~/.hermes/skills/
cp -r baiye-hermes-skills/skills/daily-recap ~/.hermes/skills/
# ... 按需复制
```

### Obsidian Vault 模板

```bash
# 使用预设的 vault 目录结构
cp -r baiye-hermes-skills/templates/obsidian-vault ~/obsidian-vault
```

---

## 📁 Vault 目录结构

```
~/obsidian-vault/
├── 🏔️ 山水邸报/        # 每日早晚报
├── 💰 金精铜钱/        # 投资周报
├── 📖 本周必读/        # 每周精选文章
├── 📒 学海无涯/        # 每日英语
├── 🍺 二掌柜的酒铺/    # 日记/杂记
├── 💡 灵感捕捉/        # 想法记录
├── 📚 阅读清单/        # 阅读管理
├── README.md           # 主索引
└── graph.md            # 知识图谱
```

---

## ⚙️ 配置说明

### 通用配置

所有 skill 默认使用 `~/obsidian-vault` 作为 vault 路径。如果你的 vault 在其他位置，修改 SKILL.md 中的路径即可。

### 山水邸报配置

需要配置以下环境变量：

```bash
# 东方财富 API（用于财经新闻和市场数据）
export EM_API_KEY="your_api_key"
```

### 通勤提醒配置

修改 SKILL.md 中的地址信息：

```yaml
起点：{YOUR_HOME_ADDRESS}
终点：{YOUR_OFFICE_ADDRESS}
城市：{CITY}
```

---

## 🔧 可选依赖

部分 skill 需要额外的 API 或服务支持：

### 东方财富妙想 API（财经新闻/市场数据）

用于 `shan-shui-di-bao` 的财经新闻板块。

1. 注册：https://ai.eastmoney.com/mxClaw
2. 获取 API Key
3. 配置：`export EM_API_KEY="your_key"`
4. 安装东财 skill：[em-finance-search](https://github.com/anthropic/...), [em-market-hotspot](https://github.com/anthropic/...)
> 💡 不配置也能使用山水邸报，只是缺少财经新闻板块。

### 花花日记（持仓数据）

用于 `investment-weekly` 的持仓收益数据和 `shan-shui-di-bao` 的收益展示。

iOS 基金管理工具，通过 MCP 接口提供持仓数据。详情见 [花花日记](https://github.com/baiye1997)。

> 💡 不配置也能使用其他所有 skill。

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License

---

> Built with ❤️ by [baiye](https://github.com/baiye1997)

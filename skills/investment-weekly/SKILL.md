---
name: investment-weekly
description: 投资周报 — 每周日自动汇总本周山水邸报+基金持仓数据，生成投资周报写入 Obsidian
tags: [obsidian, finance, weekly, investment]
---

# 投资周报

每周日自动生成投资周报，整合基金持仓数据和山水邸报市场信息。

> ⚠️ 此 skill 为**可选功能**，需要基金追踪 API 支持。不配置也能使用其他所有 skill。

## 可选依赖

### 基金追踪 API

需要配置基金追踪服务，设置环境变量：

```bash
export FUND_API="your_fund_api_endpoint"
```

API 需支持以下接口：
- `GET /summary` — 持仓总览
- `GET /records` — 持仓明细
- `GET /overview` — 大盘指数
- `GET /daily-rank` — 涨跌榜
- `GET /fund-timeline?code=xxx&days=7` — 基金历史净值

## 数据来源

### 基金追踪 API — 主要数据源
```bash
# 持仓总览（总市值、累计收益、今日收益等）
# Requires: fund-tracking MCP server
curl -s $FUND_API/summary

# 持仓明细（每只基金的收益、收益率、持仓）
# Requires: fund-tracking MCP server
curl -s $FUND_API/records

# 大盘指数（上证、深证、创业板、恒生、纳指等）
# Requires: fund-tracking MCP server
curl -s $FUND_API/overview

# 涨跌榜
# Requires: fund-tracking MCP server
curl -s $FUND_API/daily-rank

# 指定基金历史净值（用于计算周涨幅）
# Requires: fund-tracking MCP server
curl -s $FUND_API/fund-timeline '{"code":"基金代码","days":7}'
```

### 山水邸报 — 仅用于市场事件补充
- 读取本周五篇晚报，提取关键市场事件
- 不用于收益数据（收益全部来自花花日记 API）

## 执行流程

1. **拉取基金数据**：get_summary + get_records + get_overview
2. **计算周度收益**：对比本周与上周的 summary 数据（需保存上周快照）
3. **扫描本周邸报**：仅提取大事记事件
4. **汇总分析**：板块轮动、持仓表现、市场热点
5. **生成周报**：写入 Obsidian + 同步到博客

## 输出格式

```markdown
---
date: {YYYY} 第{W}周 ({M.D}-{M.D})
type: 投资周报
tags: [投资周报, {板块标签}]
---

# 💰 投资周报 · 第{W}周

> **{起始日期} — {结束日期}**

---

## 📊 本周收益

| 项目 | 金额 |
|------|------|
| 💵 本周收益 | {周收益} |
| 📈 累计收益 | {累计收益} |
| 🏦 总市值 | {总市值} |
| 📊 收益率 | {收益率} |

### 收益曲线

```
周一  {+/-¥XXX}
周二  {+/-¥XXX}
周三  {+/-¥XXX}
周四  {+/-¥XXX}
周五  {+/-¥XXX}
─────────────
本周  {合计}
```

---

## 📈 持仓明细

| 基金 | 本周收益 | 收益率 | 趋势 |
|------|---------|--------|------|
| {基金名} | {收益} | {涨跌幅} | {↑/↓/→} |
| ... | ... | ... | ... |

---

## �板块轮动

### 本周涨幅板块 TOP5
1. {板块} +{X}%
2. {板块} +{X}%
3. ...

### 本周跌幅板块 TOP5
1. {板块} -{X}%
2. ...

### 板块与持仓关联
- {哪只基金受益于哪个板块}
- {哪只基金受哪个板块拖累}

---

## 📰 本周大事记

> 从山水邸报中提取的关键事件

| 日期 | 事件 | 影响 |
|------|------|------|
| 周一 | {事件} | {对市场/持仓的影响} |
| 周二 | {事件} | ... |
| ... | ... | ... |

---

## 🔮 下周展望

**宏观关注：**
- {下周重要经济数据/政策}

**板块预判：**
- {看好的板块及理由}
- {风险板块及理由}

**持仓建议：**
- {是否需要调仓，或"维持现有配置"}

---

*🌿 由 Hermes 自动生成 · 每周日 10:15*
```

## 文件命名

```
~/obsidian-vault/💰 金精铜钱/{YYYY}-第{W}周-投资周报.md
```

## 定时任务

每周日 10:15（在本周必读之后）

```
schedule: "15 10 * * 0"
```

## 注意事项

- 非交易日（节假日）跳过对应天数的数据
- 如果某天没有邸报，标注"无数据"
- **周收益计算**：每次运行时保存 summary 快照到 `/tmp/weekly_snapshot.json`，下周运行时对比计算周收益
- 处理完成后执行 `cd ~/obsidian-vault && ob sync`
- 更新主索引：更新 `~/obsidian-vault/README.md`（金精铜钱篇数）和 `graph.md`
- ⚠️ 金精铜钱不同步博客，仅存 Obsidian

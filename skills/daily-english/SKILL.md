---
name: daily-english
description: 每日一学 — 每天早上推送一个英语单词/短语，包含音标、释义、例句、记忆技巧
tags: [english, daily, learning]
---

# 每日一学

每天早上推送一个英语单词或短语，碎片时间学习。

## 推送内容

```markdown
📖 每日一学 · {日期}

🔤 **{word}** /{音标}/

📝 释义：
- {中文释义1}
- {中文释义2}

💬 例句：
> {英文例句}
> {中文翻译}

🧠 记忆技巧：
- {词根词缀/联想/谐音等}

💡 拓展：
- {相关词汇/常用搭配/文化背景}
```

## 选词策略

### 难度分级
- 周一/三/五：日常词汇（CET-4/6 水平）
- 周二/四：商务/金融词汇（与投资相关）
- 周六：编程/技术词汇（与开发相关）
- 周日：趣味词汇（生僻但有趣的词）

### 与用户兴趣结合
- 金融词汇优先：bull, bear, dividend, portfolio, hedge...
- 科技词汇：algorithm, API, deploy, refactor...
- 生活词汇：实用口语、俚语

## Obsidian 归档

每次推送后，将当日单词写入 Obsidian vault：

```
VAULT=~/obsidian-vault
FILE="$VAULT/📒 学海无涯/YYYY-MM-DD-{word}.md"
```

文件内容使用与推送相同的 markdown 格式，frontmatter 加上：

```yaml
---
tags: [english, 每日一学]
date: YYYY-MM-DD
word: xxx
---
```

归档后执行同步：

```bash
cd ~/obsidian-vault
ob sync          # 同步到 Obsidian 云端
git add "📒 学海无涯/" && git commit -m "feat: 每日一学 $(date +%Y-%m-%d) {word}" && git push  # 推送到博客
```

博客通过 git 仓库拉取笔记，仅 `ob sync` 不会同步到博客，需执行 `git push`。

## 定时任务

每天早上 7:30 推送（通勤前）

```
schedule: "30 7 * * *"
```

## 推送方式

发送到 Telegram（当前对话），同时归档到 Obsidian `📒 学海无涯` 文件夹。

## 注意事项

- 每天只推 1 个词，不贪多
- 例句要贴近生活，不要太学术
- 记忆技巧要实用，帮助真正记住
- Obsidian 文件名格式：`YYYY-MM-DD-英文单词.md`，方便按日期浏览

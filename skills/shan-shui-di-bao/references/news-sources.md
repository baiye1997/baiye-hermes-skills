# 新闻源抓取参考

每个新闻源的可靠抓取方式，基于 2026-05-15 实测验证。

## ✅ 可靠来源

### 36氪 — RSS Feed
- **URL**: `https://36kr.com/feed`
- **格式**: XML (RSS 2.0)
- **解析**: `xml.etree.ElementTree` → `<item>` → `<title>`, `<link>`, `<description>`
- **注意**: description 含 HTML 实体 (`&amp;nbsp;`)，需清理
- **产出**: 30 篇/天，覆盖科技、财经、创投

```python
from xml.etree import ElementTree as ET
html = re.sub(r'&(?!amp;|lt;|gt;|apos;|quot;|#)', '&amp;', html)
root = ET.fromstring(html)
for item in root.findall('.//item'):
    title = item.find('title').text
    link = item.find('link').text
    desc = re.sub(r'<[^>]+>', '', item.find('description').text)[:150]
```

### IT之家 — lapin 链接提取 + 促销过滤
- **URL**: `https://www.ithome.com/`
- **模式**: 首页文章使用 `https://lapin.ithome.com/html/digi/NNNNN.htm` 格式
- **⚠️ 不支持 `<a title="...">` 模式**：首页无 title 属性的 article 链接
- **可靠方案**: 提取 `<a href="https://lapin.ithome.com/html/digi/NNNNN.htm">TEXT</a>` 格式
- **注意**: lapin 链接多为产品推荐/促销，非深度科技新闻；作为补充源使用
- **过滤**: 跳过标题含 `华为`/`鸿蒙智行`/`鸿蒙` 的文章
- **产出**: 10-20 篇/天，以产品推荐为主
- **⚠️ 促销过滤（实战验证 2026-05-18）**：IT之家首页有 300+ 条 lapin 链接，其中大部分是促销。用以下 regex 过滤：
```python
# 促销关键词黑名单（标题含任一关键词则跳过）
promo_keywords = ['元', '元发车', '开袋即食', '送自己', '到手价', '优惠', '自营', '京东', '天猫', '拼多多', '直降', '秒杀']
is_promo = any(kw in title for kw in promo_keywords)
```
- **更好的方案**：直接从 `www.ithome.com/0/NNNN/NNNN.htm` 格式提取（真正的科技新闻），而非 lapin 链接

```python
# IT之家首页文章提取（lapin 模式）
for m in re.finditer(r'<a[^>]*href="(https://lapin\.ithome\.com/html/digi/\d+\.htm)"[^>]*>(.*?)</a>', html, re.DOTALL):
    link = m.group(1)
    title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    if title and len(title) > 4:
        items.append({'title': title, 'link': link})
```

### 爱范儿 — h2/h3 标签
- **URL**: `https://www.ifanr.com/`
- **模式**: `<h2>`/`<h3>` 标签内含标题文本，关联 `<a href="https://www.ifanr.com/NNNNNN">`
- **注意**: `<a>` 标签的文本内容为空，标题在兄弟或父级 `<h2>`/`<h3>` 中
- **产出**: 20+ 篇/天，科技消费为主

```python
titles = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', html, re.DOTALL)
clean = [re.sub(r'<[^>]+>', '', t).strip() for t in titles]
# 链接单独提取
links = re.findall(r'href="(https?://www\.ifanr\.com/\d+)"', html)
```

### GitHub Trending — 正则提取
- **URL**: `https://github.com/trending?since=daily`
- **模式**: 提取所有 `href="/user/repo"` 链接，过滤非 repo 路径
- **过滤**: 排除 `login/signup/features/topics/collections/events/sponsors/enterprise/trending/explore/pricing/security/team/pulls/issues/wiki/apps` 等。⚠️ **必须排除 `apps`**（如 `apps/github-actions` 不是真正仓库）

```python
repos = re.findall(r'href="/([a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+)"', html)
exclude = {'login', 'signup', 'features', 'topics', 'collections', 'events', 'sponsors', 'enterprise', 'trending', 'explore', 'pricing', 'security', 'team', 'pulls', 'issues', 'wiki', 'apps'}
filtered = [r for r in repos if len(r.split('/')) == 2 and '?' not in r and '%2F' not in r and not any(p in exclude for p in r.split('/'))]
```

### 联合早报 — h2/h3 标题 + 附近链接匹配
- **URL**: `https://www.zaobao.com.sg/realtime/china` 和 `/realtime/world`
- **模式**: 列表页 `<h2>`/`<h3>` 标签包含文章标题，附近有文章链接
- **✅ 不需要逐篇抓取文章页**：列表页的 h2/h3 + 附近链接已足够

**可靠方案（单步）：**
```python
# 提取 h2/h3 标题
h_tags = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', html, re.DOTALL)
# 在标题位置附近搜索链接
for th in h_tags:
    title = re.sub(r'<[^>]+>', '', th).strip()
    idx = html.find(title[:20])
    if idx > 0:
        link_match = re.search(r'href="(/news/(?:china|world)/story[^"]*)"', html[max(0,idx-500):idx+500])
        if link_match:
            link = f'https://www.zaobao.com.sg{link_match.group(1)}'
```

- **产出**: 10-15 篇/天，中国+国际新闻

### 量子位 — 需 User-Agent
- **URL**: `https://www.qbitai.com/`
- **模式**: `<h2>`/`<h3>` 标签提取标题
- **注意**: 必须加 User-Agent，否则返回 0 字节
- **产出**: 4-6 篇/天，AI 领域深度文章

## ⚠️ 不可靠来源（SPA，跳过）

| 来源 | 问题 | 替代方案 |
|------|------|---------|
| 虎嗅 (huxiu.com) | WAF 拦截，返回验证页面 | 36氪 RSS |
| 少数派 (sspai.com) | SPA，仅返回 meta description | 无直接替代 |
| 果壳 (guokr.com) | SPA，仅 1 个链接 | 知乎热榜 |
| 知乎热榜 (zhihu.com/hot) | 403 Forbidden，需登录 | 36氪 RSS、爱范儿 |
| 小众软件 | 未验证 | 无 |
| 机器之心 (jiqizhixin.com) | 已停更，重定向到落地页 | 量子位 |

## 东财财经新闻 API

⚠️ `EM_API_KEY` 当前环境未配置（空值），调用会报 "EM API KEY REQUIRED" 错误。无密钥时跳过东财数据源，用 36氪 RSS + 联合早报替代财经新闻。

```bash
cd ~/.hermes/eastmoney-skills/mx-finance-search/mx-finance-search
EM_API_KEY=$EM_API_KEY /usr/bin/python3 scripts/get_data.py "搜索关键词"
```

返回 JSON，关键字段: `data[].title`, `data[].content`, `data[].source`, `data[].jumpUrl`

### 推荐搜索词
- 早报: "今日A股市场重要公告和政策 央行货币政策"
- 晚报: "今日A股收盘后重要公告 晚间财经要闻"

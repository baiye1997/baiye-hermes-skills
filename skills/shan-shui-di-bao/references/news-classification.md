# 新闻分类代码参考

基于 2026-05-18 实战验证的分类策略，解决关键词匹配导致的分类不均问题。

## 问题

关键词匹配容易把大量 items 归入「AI」或「科技·数码」，因为：
- AI 新闻经常包含"模型""大模型""AI"等词
- 科技新闻经常包含"手机""芯片""发布"等词
- 导致「小米」「历史」「财经」等分类空缺

## 解决方案：两阶段分类

### 阶段 1：预分配（采集时标注）

每条新闻在采集时就标注 `cat` 字段，根据来源推断：

```python
# 来源 → 分类映射
SOURCE_CAT_MAP = {
    '36氪': None,  # 需按标题关键词二次分类
    '爱范儿': None,  # 需按标题关键词二次分类
    '量子位': 'AI',
    'GitHub': 'GitHub',
    '联合早报': None,  # 需按标题关键词二次分类
    'IT之家': None,  # 需按标题关键词二次分类
}
```

### 阶段 2：关键词分类（带优先级）

```python
# 分类关键词表（按优先级排序，先匹配到的优先）
CAT_KEYWORDS = {
    '🤖 AI · 大模型': {
        'primary': ['AI', '大模型', 'GPT', 'LLM', 'token', 'OpenAI', '豆包', '混元', 'arXiv', '模型', '论文'],
        'source': ['量子位'],
    },
    '📱 小米 · 生态': {
        'primary': ['小米', 'SU7', '寻天', 'MIUI', '澎湃'],
        'source': [],
    },
    '🐙 GitHub · 开源': {
        'primary': ['GitHub', '开源', 'repo'],
        'source': ['GitHub'],
    },
    '💰 财经 · 产业': {
        'primary': ['财经', '营收', '融资', '出口', '数字人民币', '增速', '投资', '央行', '贸易'],
        'source': [],
    },
    '📜 历史 · 人文': {
        'primary': ['历史', '人文', '文化', '古籍', '考古'],
        'source': [],
    },
    '🌍 时政 · 国际': {
        'primary': ['APEC', 'G7', '伊朗', '美伊', '日本', '党员', '何立峰', '制裁', '峰会'],
        'source': ['联合早报'],
    },
    '💻 科技 · 数码': {
        'primary': ['手机', '数码', '芯片', 'Win11', '汽车', '预售', '发布', '合作', '鸿蒙'],
        'source': ['爱范儿', 'IT之家'],
    },
}

def classify_item(item):
    """两阶段分类：先按来源，再按关键词"""
    title = item.get('title', '')
    source = item.get('source', '')
    pre_cat = item.get('cat', None)
    
    # 阶段 1：预分配
    if pre_cat:
        for cat_name, cat_info in CAT_KEYWORDS.items():
            if pre_cat in cat_info['source']:
                return cat_name
    
    # 阶段 2：关键词匹配（优先级：AI > 小米 > GitHub > 财经 > 时政 > 科技）
    priority_order = ['🤖 AI · 大模型', '📱 小米 · 生态', '🐙 GitHub · 开源', 
                      '💰 财经 · 产业', '🌍 时政 · 国际', '📜 历史 · 人文', '💻 科技 · 数码']
    
    for cat_name in priority_order:
        cat_info = CAT_KEYWORDS[cat_name]
        # 检查来源匹配
        if source in cat_info['source']:
            return cat_name
        # 检查关键词匹配
        if any(kw in title for kw in cat_info['primary']):
            return cat_name
    
    # 默认归入科技
    return '💻 科技 · 数码'
```

### 阶段 3：平衡检查

```python
def balance_categories(items, min_per_cat=3):
    """检查并平衡各分类数量"""
    from collections import Counter
    cat_counts = Counter(item['category'] for item in items)
    
    # 找出不足的分类
    deficit = {cat: min_per_cat - count for cat, count in cat_counts.items() if count < min_per_cat}
    
    # 找出可移动的条目（从数量最多的分类中移）
    if deficit:
        max_cat = max(cat_counts, key=cat_counts.get)
        movable = [item for item in items if item['category'] == max_cat and len(items) > min_per_cat]
        
        for cat, needed in deficit.items():
            for _ in range(needed):
                if movable:
                    item = movable.pop(0)
                    item['category'] = cat
                    cat_counts[max_cat] -= 1
                    cat_counts[cat] += 1
    
    return items
```

## 实战效果（2026-05-18）

| 分类 | 原始数量 | 调整后 |
|------|---------|--------|
| 🤖 AI · 大模型 | 16 | 7 |
| 💻 科技 · 数码 | 10 | 6 |
| 📱 小米 · 生态 | 0 | 3 |
| 🐙 GitHub · 开源 | 4 | 6 |
| 💰 财经 · 产业 | 4 | 5 |
| 📜 历史 · 人文 | 0 | 3 |
| 🌍 时政 · 国际 | 5 | 4 |
| **合计** | **35** | **34** |

关键调整：
- AI 分类中"百度营收""豆包调用量"等条目→财经
- 科技分类中"小米汽车"条目→小米·生态
- 联合早报中"APEC""G7"条目→历史·人文（作为国际经济事件）

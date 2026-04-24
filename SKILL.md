---
name: lunar-birthday
description: 中国农历与新历（公历）日期互查工具，以及农历生日管家。当用户需要查询农历对应的新历日期、新历对应的农历日期、管理家人的农历生日、检查即将到来的农历生日时，使用此技能。触发关键词：农历、新历、公历、阴历、阳历、生日提醒、生日管家、lunar、solar calendar。
---

# 农历生日管家 (Lunar Birthday Manager)

## 概述

此技能提供两大核心功能：
1. **农历/新历日期互查** — 精确转换公历和农历日期，支持闰月
2. **农历生日管家** — 记录家人的农历生日，自动计算当年新历日期，检查即将到来的生日

## 依赖

- Python 3.6+
- `lunar_python` 库（如未安装，执行 `pip install lunar_python --break-system-packages`）

## 脚本位置

- 日期转换脚本：`scripts/convert.py`
- 生日管家脚本：`scripts/birthday.py`
- 生日数据文件：`birthdays.json`（自动创建）

---

## 功能一：农历/新历日期互查

### 新历 → 农历

```bash
python3 scripts/convert.py solar_to_lunar <年> <月> <日>
```

示例：
```bash
python3 scripts/convert.py solar_to_lunar 2025 5 29
```

返回 JSON 包含：农历年月日、是否闰月、中文表示、天干地支、生肖、星期

### 农历 → 新历

```bash
python3 scripts/convert.py lunar_to_solar <农历年> <农历月> <农历日> [leap]
```

- `leap` 参数表示闰月（可选）
- 示例（正常月）：`python3 scripts/convert.py lunar_to_solar 2025 4 2`
- 示例（闰月）：`python3 scripts/convert.py lunar_to_solar 2023 2 11 leap`

### 查询某年农历信息

```bash
python3 scripts/convert.py year_info <年>
```

返回该年是否有闰月、各月初一对应的新历日期

---

## 功能二：农历生日管家

### 添加生日

```bash
python3 scripts/birthday.py add <名字/称呼> <农历月> <农历日> [leap] [备注]
```

示例：
```bash
python3 scripts/birthday.py add 爷爷 3 8
python3 scripts/birthday.py add 奶奶 9 15
python3 scripts/birthday.py add 外婆 2 11 leap 闰二月出生
python3 scripts/birthday.py add 张三 12 20 好朋友
```

**注意**：
- 名字/称呼支持任意中文或英文，如"爷爷"、"奶奶"、"妈妈"、"老爸"等
- `leap` 参数表示该生日在闰月（如闰二月）
- 备注为可选参数

### 删除生日

```bash
python3 scripts/birthday.py remove <名字/称呼>
```

### 列出所有生日

```bash
python3 scripts/birthday.py list
```

返回所有已记录的生日，包含：
- 农历日期（中文）
- 今年对应的新历日期
- 距今天数
- 按距离天数升序排列

### 检查即将到来的生日

```bash
python3 scripts/birthday.py check [天数]
```

- 默认检查未来 7 天
- 可自定义天数，如 `python3 scripts/birthday.py check 14` 检查未来 14 天

---

## Agent 使用指南

### 当用户说"查生日"、"有没有生日"等：

1. 运行 `python3 scripts/birthday.py check` 检查未来 7 天
2. 如果有即将到来的生日，用友好的方式提醒用户，包含：
   - 谁的生日
   - 新历日期是哪天（星期几）
   - 还有几天
   - 农历日期
3. 如果没有，告知用户近期没有生日

### 当用户说"列出所有生日"、"都有谁过生日"等：

1. 运行 `python3 scripts/birthday.py list`
2. 以清晰的表格或列表形式展示所有生日信息

### 当用户说"添加生日"、"记录生日"等：

1. 确认以下信息：
   - 名字/称呼（如"爷爷"）
   - 农历月份和日期
   - 是否是闰月（如果用户提到闰月）
   - 备注（可选）
2. 运行添加命令
3. 确认添加成功

### 当用户说"农历几月几号是新历几号"等日期转换问题：

1. 运行对应的转换命令
2. 用清晰的格式展示结果

### 当用户说"删除生日"、"移除生日"等：

1. 确认要删除的名字
2. 运行删除命令
3. 确认删除成功

## 重要注意事项

1. **闰月处理**：如果长辈的生日在闰月，添加时务必加上 `leap` 参数
2. **日期验证**：农历日期不一定每月都有 30 天，某些月只有 29 天，脚本会自动处理
3. **跨年处理**：如果今年农历生日已过，list 命令会自动计算明年的新历日期
4. **数据持久化**：生日数据保存在 `birthdays.json` 中，跨会话保留
5. **首次使用**：如果用户还没有添加任何生日，主动引导用户添加

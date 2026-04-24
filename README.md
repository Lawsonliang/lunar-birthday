# 农历生日管家 (Lunar Birthday Manager)

中国农历与新历（公历）日期互查工具，以及农历生日管家。

---

## 安装 Skill

### Trae IDE

1. 克隆仓库：
   ```bash
   git clone https://github.com/Lawsonliang/lunar-birthday.git
   ```
2. 在 Trae IDE 中打开项目目录
3. 安装依赖：
   ```bash
   pip install lunar_python --break-system-packages
   ```

### Claude Code / Codeq / Cursor / OpenClaw 等通用 AI 助手

1. 克隆仓库：
   ```bash
   git clone https://github.com/Lawsonliang/lunar-birthday.git
   cd lunar-birthday
   ```
2. 安装依赖：
   ```bash
   pip install lunar_python --break-system-packages
   ```
3. 将 `SKILL.md` 中的内容添加到你的 AI 助手的 skill 配置中

---

## 功能

- **日期互查** — 新历 ↔ 农历精确转换，支持闰月
- **生日管理** — 记录家人农历生日，自动计算当年新历日期
- **生日提醒** — 检查即将到来的农历生日

## 使用

### 日期转换

```bash
# 新历 → 农历
python3 scripts/convert.py solar_to_lunar 2025 5 29

# 农历 → 新历（正常月）
python3 scripts/convert.py lunar_to_solar 2025 4 2

# 农历 → 新历（闰月）
python3 scripts/convert.py lunar_to_solar 2023 2 11 leap

# 查询某年农历信息
python3 scripts/convert.py year_info 2025
```

### 生日管理

```bash
# 添加生日
python3 scripts/birthday.py add 爷爷 3 8
python3 scripts/birthday.py add 奶奶 9 15
python3 scripts/birthday.py add 外婆 2 11 leap  # 闰月

# 列出所有生日
python3 scripts/birthday.py list

# 检查即将到来的生日（默认7天）
python3 scripts/birthday.py check
python3 scripts/birthday.py check 14  # 自定义天数

# 删除生日
python3 scripts/birthday.py remove 爷爷
```

## 依赖

- Python 3.6+
- [lunar_python](https://github.com/3Shain/lunar_python)

## 数据存储

生日数据保存在本地 `birthdays.json` 文件中（不会提交到 Git）。
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
农历生日管家 - 管理农历生日并检查即将到来的生日
依赖：lunar_python (pip install lunar_python)
"""

import sys
import json
import os
from datetime import datetime, timedelta
from lunar_python import Solar, Lunar

# 中文数字映射
CN_NUMBERS = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十', 11: '十一', 12: '十二'}
CN_DAYS = {1: '初一', 2: '初二', 3: '初三', 4: '初四', 5: '初五', 6: '初六', 7: '初七', 8: '初八', 9: '初九', 10: '初十',
           11: '十一', 12: '十二', 13: '十三', 14: '十四', 15: '十五', 16: '十六', 17: '十七', 18: '十八', 19: '十九', 20: '二十',
           21: '廿一', 22: '廿二', 23: '廿三', 24: '廿四', 25: '廿五', 26: '廿六', 27: '廿七', 28: '廿八', 29: '廿九', 30: '三十'}

# 默认生日数据文件路径
DEFAULT_DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "birthdays.json")


def load_birthdays(data_file=None):
    """加载生日数据"""
    path = data_file or DEFAULT_DATA_FILE
    if not os.path.exists(path):
        return {"success": True, "data": [], "message": "暂无生日记录"}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": f"读取生日数据失败: {str(e)}"}


def save_birthdays(birthdays, data_file=None):
    """保存生日数据"""
    path = data_file or DEFAULT_DATA_FILE
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(birthdays, f, ensure_ascii=False, indent=2)
        return {"success": True, "message": f"已保存 {len(birthdays)} 条生日记录"}
    except Exception as e:
        return {"success": False, "error": f"保存生日数据失败: {str(e)}"}


def add_birthday(name, lunar_month, lunar_day, is_leap_month=False, note="", data_file=None):
    """添加一条农历生日记录"""
    # 验证月份和日期
    if not (1 <= lunar_month <= 12):
        return {"success": False, "error": "农历月份必须在 1-12 之间"}
    if not (1 <= lunar_day <= 30):
        return {"success": False, "error": "农历日期必须在 1-30 之间"}

    result = load_birthdays(data_file)
    if not result["success"]:
        return result

    birthdays = result["data"]

    # 检查是否已存在同名记录
    for b in birthdays:
        if b["name"] == name:
            return {"success": False, "error": f"已存在名为「{name}」的生日记录，请先删除再添加，或使用 update 命令修改"}

    entry = {
        "name": name,
        "lunar_month": lunar_month,
        "lunar_day": lunar_day,
        "is_leap_month": is_leap_month,
        "note": note,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    birthdays.append(entry)

    save_result = save_birthdays(birthdays, data_file)
    if not save_result["success"]:
        return save_result

    return {
        "success": True,
        "message": f"已添加「{name}」的农历生日：{'闰' if is_leap_month else ''}{CN_NUMBERS.get(lunar_month, str(lunar_month))}月{CN_DAYS.get(lunar_day, str(lunar_day))}",
        "entry": entry
    }


def remove_birthday(name, data_file=None):
    """删除一条生日记录"""
    result = load_birthdays(data_file)
    if not result["success"]:
        return result

    birthdays = result["data"]
    original_count = len(birthdays)
    birthdays = [b for b in birthdays if b["name"] != name]

    if len(birthdays) == original_count:
        return {"success": False, "error": f"未找到名为「{name}」的生日记录"}

    save_result = save_birthdays(birthdays, data_file)
    if not save_result["success"]:
        return save_result

    return {"success": True, "message": f"已删除「{name}」的生日记录"}


def list_birthdays(data_file=None):
    """列出所有生日记录"""
    result = load_birthdays(data_file)
    if not result["success"]:
        return result

    birthdays = result["data"]
    if not birthdays:
        return {"success": True, "data": [], "message": "暂无生日记录，请使用 add 命令添加"}

    # 计算每个生日在今年的新历日期
    today = datetime.now()
    current_year = today.year
    enriched = []

    for b in birthdays:
        lunar_month = b["lunar_month"]
        lunar_day = b["lunar_day"]
        is_leap = b.get("is_leap_month", False)

        # 尝试计算今年对应的新历日期
        solar_date = None
        try:
            actual_month = -lunar_month if is_leap else lunar_month
            lunar = Lunar.fromYmd(current_year, actual_month, lunar_day)
            solar = lunar.getSolar()
            solar_date = f"{solar.getYear()}-{solar.getMonth():02d}-{solar.getDay():02d}"
            solar_dt = datetime(solar.getYear(), solar.getMonth(), solar.getDay())

            # 计算距离今天的天数
            diff = (solar_dt.date() - today.date()).days
            if diff < 0:
                # 今年的生日已过，计算明年的
                try:
                    lunar_next = Lunar.fromYmd(current_year + 1, actual_month, lunar_day)
                    solar_next = lunar_next.getSolar()
                    solar_date_next = f"{solar_next.getYear()}-{solar_next.getMonth():02d}-{solar_next.getDay():02d}"
                    solar_dt_next = datetime(solar_next.getYear(), solar_next.getMonth(), solar_next.getDay())
                    diff_next = (solar_dt_next.date() - today.date()).days
                    days_until = diff_next
                    next_solar = solar_date_next
                except:
                    days_until = None
                    next_solar = None
            else:
                days_until = diff
                next_solar = solar_date
        except Exception as e:
            solar_date = None
            days_until = None
            next_solar = None

        enriched.append({
            "name": b["name"],
            "lunar_month": lunar_month,
            "lunar_day": lunar_day,
            "is_leap_month": is_leap,
            "lunar_cn": ("闰" if is_leap else "") + CN_NUMBERS.get(lunar_month, str(lunar_month)) + "月" + CN_DAYS.get(lunar_day, str(lunar_day)),
            "this_year_solar": solar_date,
            "next_solar": next_solar,
            "days_until": days_until,
            "note": b.get("note", "")
        })

    # 按距离天数排序
    enriched.sort(key=lambda x: (x["days_until"] if x["days_until"] is not None else 9999))

    return {"success": True, "data": enriched, "total": len(enriched)}


def check_upcoming(days=7, data_file=None):
    """检查未来 N 天内是否有生日"""
    result = list_birthdays(data_file)
    if not result["success"]:
        return result

    all_birthdays = result["data"]
    today = datetime.now()

    upcoming = []
    for b in all_birthdays:
        if b["days_until"] is not None and 0 <= b["days_until"] <= days:
            upcoming.append(b)

    if not upcoming:
        return {
            "success": True,
            "has_upcoming": False,
            "message": f"未来 {days} 天内没有生日 🎉",
            "today": today.strftime("%Y-%m-%d"),
            "check_range": f"{days} 天"
        }

    return {
        "success": True,
        "has_upcoming": True,
        "today": today.strftime("%Y-%m-%d"),
        "check_range": f"{days} 天",
        "upcoming": upcoming,
        "summary": f"⚠️ 未来 {days} 天内有 {len(upcoming)} 个生日！"
    }


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "请指定操作类型",
            "usage": {
                "add": "python birthday.py add <名字> <农历月> <农历日> [leap] [备注]",
                "remove": "python birthday.py remove <名字>",
                "list": "python birthday.py list",
                "check": "python birthday.py check [天数，默认7]"
            }
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    action = sys.argv[1]

    if action == "add":
        if len(sys.argv) < 5:
            print(json.dumps({"success": False, "error": "add 命令需要参数: 名字 农历月 农历日 [leap] [备注]"}, ensure_ascii=False))
            sys.exit(1)
        name = sys.argv[2]
        lunar_month = int(sys.argv[3])
        lunar_day = int(sys.argv[4])
        is_leap = len(sys.argv) >= 6 and sys.argv[5] == "leap"
        note = " ".join(sys.argv[6:]) if len(sys.argv) >= 7 else ""
        result = add_birthday(name, lunar_month, lunar_day, is_leap, note)

    elif action == "remove":
        if len(sys.argv) < 3:
            print(json.dumps({"success": False, "error": "remove 命令需要参数: 名字"}, ensure_ascii=False))
            sys.exit(1)
        result = remove_birthday(sys.argv[2])

    elif action == "list":
        result = list_birthdays()

    elif action == "check":
        days = int(sys.argv[2]) if len(sys.argv) >= 3 else 7
        result = check_upcoming(days)

    else:
        result = {"success": False, "error": f"未知操作: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

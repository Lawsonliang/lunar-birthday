#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
节假日管家 - 管理全年节假日并检查即将到来的节日
支持：法定假日、传统节日、西方节日、二十四节气、纪念日
"""

import sys
import json
import os
from datetime import datetime, timedelta

# 默认节假日数据文件路径
DEFAULT_DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "holidays.json")

# 2026年完整节假日数据
DEFAULT_HOLIDAYS_2026 = [
    # 法定放假日
    {"name": "劳动节", "date": "2026-05-01", "type": "法定假日", "days": 5, "note": "5月1日-5日放假，5月9日（周六）上班"},
    {"name": "端午节", "date": "2026-06-19", "type": "法定假日", "days": 3, "note": "6月19日-21日放假，不调休"},
    {"name": "中秋节", "date": "2026-09-25", "type": "法定假日", "days": 3, "note": "9月25日-27日放假，不调休"},
    {"name": "国庆节", "date": "2026-10-01", "type": "法定假日", "days": 7, "note": "10月1日-7日放假，10月10日（周六）上班"},
    
    # 中国传统节日（农历）
    {"name": "七夕节", "date": "2026-08-19", "type": "传统节日", "lunar": "七月初七", "note": "中国情人节"},
    {"name": "中元节", "date": "2026-08-27", "type": "传统节日", "lunar": "七月十五", "note": "鬼节/盂兰盆节"},
    {"name": "重阳节", "date": "2026-10-18", "type": "传统节日", "lunar": "九月初九", "note": "敬老节，登高赏菊"},
    {"name": "腊八节", "date": "2027-01-17", "type": "传统节日", "lunar": "腊月初八", "note": "喝腊八粥，过了腊八就是年"},
    
    # 家庭/亲情节日
    {"name": "母亲节", "date": "2026-05-10", "type": "家庭节日", "note": "5月第二个周日"},
    {"name": "儿童节", "date": "2026-06-01", "type": "家庭节日", "note": "14岁以下儿童放假1天"},
    {"name": "父亲节", "date": "2026-06-21", "type": "家庭节日", "note": "6月第三个周日"},
    {"name": "教师节", "date": "2026-09-10", "type": "家庭节日", "note": "感谢老师"},
    
    # 情侣/爱情节日
    {"name": "520网络情人节", "date": "2026-05-20", "type": "网络节日", "note": "我爱你"},
    
    # 其他重要日子
    {"name": "青年节", "date": "2026-05-04", "type": "纪念日", "note": "青年放假半天"},
    {"name": "护士节", "date": "2026-05-12", "type": "纪念日", "note": "国际护士节"},
    {"name": "万圣节", "date": "2026-10-31", "type": "西方节日", "note": "Halloween"},
    {"name": "平安夜", "date": "2026-12-24", "type": "西方节日", "note": "Christmas Eve"},
    {"name": "圣诞节", "date": "2026-12-25", "type": "西方节日", "note": "Christmas"},
    {"name": "元旦", "date": "2027-01-01", "type": "法定假日", "note": "新年第一天"},
    
    # 二十四节气（剩余）
    {"name": "立夏", "date": "2026-05-05", "type": "节气", "note": "夏季开始"},
    {"name": "小满", "date": "2026-05-21", "type": "节气", "note": "麦粒渐满"},
    {"name": "芒种", "date": "2026-06-05", "type": "节气", "note": "有芒之谷可播种"},
    {"name": "夏至", "date": "2026-06-21", "type": "节气", "note": "白昼最长"},
    {"name": "小暑", "date": "2026-07-07", "type": "节气", "note": "初伏前后"},
    {"name": "大暑", "date": "2026-07-23", "type": "节气", "note": "一年最热"},
    {"name": "立秋", "date": "2026-08-07", "type": "节气", "note": "秋季开始"},
    {"name": "处暑", "date": "2026-08-23", "type": "节气", "note": "暑气结束"},
    {"name": "白露", "date": "2026-09-07", "type": "节气", "note": "天气转凉，露水凝结"},
    {"name": "秋分", "date": "2026-09-23", "type": "节气", "note": "昼夜平分"},
    {"name": "寒露", "date": "2026-10-08", "type": "节气", "note": "露水变寒"},
    {"name": "霜降", "date": "2026-10-23", "type": "节气", "note": "初霜出现"},
    {"name": "立冬", "date": "2026-11-07", "type": "节气", "note": "冬季开始"},
    {"name": "小雪", "date": "2026-11-22", "type": "节气", "note": "开始降雪"},
    {"name": "大雪", "date": "2026-12-07", "type": "节气", "note": "雪量增多"},
    {"name": "冬至", "date": "2026-12-22", "type": "节气", "note": "白昼最短，吃饺子/汤圆"},
    {"name": "小寒", "date": "2027-01-05", "type": "节气", "note": "气候变冷"},
    {"name": "大寒", "date": "2027-01-20", "type": "节气", "note": "一年最冷"},
]


def load_holidays(data_file=None):
    """加载节假日数据"""
    path = data_file or DEFAULT_DATA_FILE
    if not os.path.exists(path):
        # 首次使用，创建默认数据
        save_holidays(DEFAULT_HOLIDAYS_2026, data_file)
        return {"success": True, "data": DEFAULT_HOLIDAYS_2026, "message": "已创建2026年默认节假日数据"}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": f"读取节假日数据失败: {str(e)}"}


def save_holidays(holidays, data_file=None):
    """保存节假日数据"""
    path = data_file or DEFAULT_DATA_FILE
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(holidays, f, ensure_ascii=False, indent=2)
        return {"success": True, "message": f"已保存 {len(holidays)} 条节假日记录"}
    except Exception as e:
        return {"success": False, "error": f"保存节假日数据失败: {str(e)}"}


def list_holidays(data_file=None):
    """列出所有节假日"""
    result = load_holidays(data_file)
    if not result["success"]:
        return result

    holidays = result["data"]
    today = datetime.now()
    
    enriched = []
    for h in holidays:
        try:
            holiday_date = datetime.strptime(h["date"], "%Y-%m-%d")
            diff = (holiday_date.date() - today.date()).days
            
            weekday = holiday_date.strftime("%a")
            weekday_cn = {"Mon": "一", "Tue": "二", "Wed": "三", "Thu": "四", "Fri": "五", "Sat": "六", "Sun": "日"}.get(weekday, weekday)
            
            enriched.append({
                "name": h["name"],
                "date": h["date"],
                "weekday": f"周{weekday_cn}",
                "type": h.get("type", "其他"),
                "days_until": diff,
                "lunar": h.get("lunar", ""),
                "note": h.get("note", "")
            })
        except:
            continue
    
    # 按距离天数排序
    enriched.sort(key=lambda x: x["days_until"])
    
    return {"success": True, "data": enriched, "total": len(enriched)}


def check_upcoming(days=7, data_file=None):
    """检查未来 N 天内是否有节假日"""
    result = list_holidays(data_file)
    if not result["success"]:
        return result

    all_holidays = result["data"]
    today = datetime.now()

    upcoming = [h for h in all_holidays if 0 <= h["days_until"] <= days]

    if not upcoming:
        return {
            "success": True,
            "has_upcoming": False,
            "message": f"未来 {days} 天内没有节假日 🎉",
            "today": today.strftime("%Y-%m-%d"),
            "check_range": f"{days} 天"
        }

    return {
        "success": True,
        "has_upcoming": True,
        "today": today.strftime("%Y-%m-%d"),
        "check_range": f"{days} 天",
        "upcoming": upcoming,
        "summary": f"📅 未来 {days} 天内有 {len(upcoming)} 个节日！"
    }


def filter_by_type(holiday_type, data_file=None):
    """按类型筛选节假日"""
    result = list_holidays(data_file)
    if not result["success"]:
        return result
    
    filtered = [h for h in result["data"] if h["type"] == holiday_type and h["days_until"] >= 0]
    return {"success": True, "data": filtered, "type": holiday_type, "total": len(filtered)}


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "请指定操作类型",
            "usage": {
                "list": "python holidays.py list",
                "check": "python holidays.py check [天数，默认7]",
                "filter": "python holidays.py filter <类型>"
            },
            "可用类型": ["法定假日", "传统节日", "家庭节日", "网络节日", "西方节日", "节气", "纪念日"]
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    action = sys.argv[1]

    if action == "list":
        result = list_holidays()

    elif action == "check":
        days = int(sys.argv[2]) if len(sys.argv) >= 3 else 7
        result = check_upcoming(days)

    elif action == "filter":
        if len(sys.argv) < 3:
            print(json.dumps({"success": False, "error": "filter 命令需要参数: 类型"}, ensure_ascii=False))
            sys.exit(1)
        result = filter_by_type(sys.argv[2])

    else:
        result = {"success": False, "error": f"未知操作: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

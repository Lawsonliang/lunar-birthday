#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
农历/新历（公历）日期转换工具
支持：新历→农历、农历→新历、闰月处理
依赖：lunar_python (pip install lunar_python)
"""

import sys
import json
from lunar_python import Solar, Lunar

# 中文数字映射
CN_NUMBERS = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十', 11: '十一', 12: '十二'}
CN_DAYS = {1: '初一', 2: '初二', 3: '初三', 4: '初四', 5: '初五', 6: '初六', 7: '初七', 8: '初八', 9: '初九', 10: '初十',
           11: '十一', 12: '十二', 13: '十三', 14: '十四', 15: '十五', 16: '十六', 17: '十七', 18: '十八', 19: '十九', 20: '二十',
           21: '廿一', 22: '廿二', 23: '廿三', 24: '廿四', 25: '廿五', 26: '廿六', 27: '廿七', 28: '廿八', 29: '廿九', 30: '三十'}


def solar_to_lunar(year, month, day):
    """新历转农历"""
    try:
        solar = Solar.fromYmd(year, month, day)
        lunar = solar.getLunar()
        lunar_month = abs(lunar.getMonth())
        is_leap = lunar.getMonth() < 0
        lunar_day = lunar.getDay()

        result = {
            "solar": {"year": year, "month": month, "day": day},
            "lunar": {
                "year": lunar.getYear(),
                "month": lunar_month,
                "day": lunar_day,
                "is_leap_month": is_leap,
                "year_cn": lunar.getYearInChinese() + "年",
                "month_cn": ("闰" if is_leap else "") + CN_NUMBERS.get(lunar_month, str(lunar_month)) + "月",
                "day_cn": CN_DAYS.get(lunar_day, str(lunar_day)),
                "full_cn": lunar.getYearInChinese() + "年" + ("闰" if is_leap else "") + CN_NUMBERS.get(lunar_month, str(lunar_month)) + "月" + CN_DAYS.get(lunar_day, str(lunar_day))
            },
            "extra": {
                "gan_zhi_year": lunar.getYearInGanZhi(),
                "sheng_xiao": lunar.getYearShengXiao(),
                "week_cn": solar.getWeekInChinese()
            }
        }
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def lunar_to_solar(year, month, day, is_leap_month=False):
    """农历转新历"""
    try:
        # lunar_python 中闰月用负数表示
        actual_month = -month if is_leap_month else month
        lunar = Lunar.fromYmd(year, actual_month, day)
        solar = lunar.getSolar()

        result = {
            "lunar": {
                "year": year,
                "month": month,
                "day": day,
                "is_leap_month": is_leap_month,
                "full_cn": Lunar.fromYmd(year, 1, 1).getYearInChinese() + "年" + ("闰" if is_leap_month else "") + CN_NUMBERS.get(month, str(month)) + "月" + CN_DAYS.get(day, str(day))
            },
            "solar": {
                "year": solar.getYear(),
                "month": solar.getMonth(),
                "day": solar.getDay(),
                "full": f"{solar.getYear()}-{solar.getMonth():02d}-{solar.getDay():02d}",
                "week_cn": solar.getWeekInChinese()
            }
        }
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_lunar_info_for_year(year):
    """获取某年农历信息，包括闰月"""
    try:
        # 通过遍历查找闰月
        leap_month = None
        for m in range(1, 13):
            try:
                lunar = Lunar.fromYmd(year, -m, 1)
                solar = lunar.getSolar()
                # 如果转换成功，说明该月有闰月
                leap_month = m
                break
            except:
                continue

        # 获取该年农历各月初一对应的新历日期
        months_info = []
        for m in range(1, 13):
            try:
                lunar = Lunar.fromYmd(year, m, 1)
                solar = lunar.getSolar()
                months_info.append({
                    "month": m,
                    "month_cn": CN_NUMBERS.get(m, str(m)) + "月",
                    "first_day_solar": f"{solar.getYear()}-{solar.getMonth():02d}-{solar.getDay():02d}"
                })
            except:
                break

        result = {
            "year": year,
            "leap_month": leap_month,
            "leap_month_cn": ("闰" + CN_NUMBERS.get(leap_month, str(leap_month)) + "月") if leap_month else None,
            "months": months_info
        }
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "请指定操作类型: solar_to_lunar / lunar_to_solar / year_info",
            "usage": {
                "solar_to_lunar": "python convert.py solar_to_lunar 2025 5 29",
                "lunar_to_solar": "python convert.py lunar_to_solar 2025 4 2 [leap]",
                "year_info": "python convert.py year_info 2025"
            }
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    action = sys.argv[1]

    if action == "solar_to_lunar":
        if len(sys.argv) < 5:
            print(json.dumps({"success": False, "error": "需要参数: 年 月 日"}, ensure_ascii=False))
            sys.exit(1)
        result = solar_to_lunar(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))

    elif action == "lunar_to_solar":
        if len(sys.argv) < 5:
            print(json.dumps({"success": False, "error": "需要参数: 年 月 日 [leap]"}, ensure_ascii=False))
            sys.exit(1)
        is_leap = len(sys.argv) >= 6 and sys.argv[5] == "leap"
        result = lunar_to_solar(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), is_leap)

    elif action == "year_info":
        if len(sys.argv) < 3:
            print(json.dumps({"success": False, "error": "需要参数: 年份"}, ensure_ascii=False))
            sys.exit(1)
        result = get_lunar_info_for_year(int(sys.argv[2]))

    else:
        result = {"success": False, "error": f"未知操作: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

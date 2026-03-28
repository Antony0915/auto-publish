#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
希腊华人每日简报 - 实用资讯版
简洁明了，每天不同内容
"""

import subprocess
import json
from datetime import datetime, timedelta
import sys
import os
import random

sys.path.insert(0, os.path.expanduser("~/.qclaw/workspace/scripts"))
from send_email import send_email

RECIPIENT_EMAIL = "25932437@qq.com"

def get_weather():
    """天气"""
    month = datetime.now().month
    seasons = {
        3: "🌸 雅典 12-18°C 春季转暖",
        4: "🌸 雅典 15-22°C 阳光明媚",
        5: "☀️ 雅典 18-26°C 初夏舒适",
        6: "☀️ 雅典 22-30°C 注意防晒",
        7: "☀️ 雅典 25-35°C 盛夏炎热",
        8: "☀️ 雅典 25-34°C 多喝水",
        9: "🍂 雅典 20-28°C 初秋宜人",
        10: "🍂 雅典 15-24°C 渐凉添衣",
        11: "🍂 雅典 10-18°C 深秋保暖",
        12: "❄️ 雅典 8-15°C 冬季潮湿",
        1: "❄️ 雅典 6-13°C 湿冷",
        2: "❄️ 雅典 7-14°C 多雨"
    }
    return seasons.get(month, "🌤️ 雅典 气温适中")

def get_greek_phrase():
    """每日希腊语"""
    phrases = [
        ("Καλημέρα", "卡利梅拉", "早上好"),
        ("Ευχαριστώ", "埃夫哈里斯托", "谢谢"),
        ("Παρακαλώ", "帕拉卡洛", "请/不客气"),
        ("Γεια σου", "耶亚苏", "你好"),
        ("Πόσο;", "波索", "多少钱？"),
        ("Δεν καταλαβαίνω", "卡塔拉文诺", "我不懂"),
        ("Ναι / Όχι", "奈 / 奥希", "是/不是"),
        ("Συγγνώμη", "辛戈诺米", "对不起"),
        ("Βοήθεια", "维西亚", "救命"),
        ("Πού είναι;", "普埃尼", "在哪里？"),
        ("Το λογαριασμό", "洛加里阿莫", "买单"),
        ("Νερό", "内罗", "水"),
    ]
    day = datetime.now().timetuple().tm_yday
    return phrases[day % len(phrases)]

def get_daily_news():
    """每天不同的资讯组合"""
    day_of_year = datetime.now().timetuple().tm_yday
    weekday = datetime.now().weekday()
    
    # 所有资讯库
    life_tips = [
        "周日超市大多关门，周六下午也早关",
        "14:00-17:00午休，很多店关门别跑空",
        "上车前在站台买公交票，车上不售票",
        "环岛内车优先，进环岛要让行",
        "自来水可直接喝，很多人买瓶装水",
        "绿色十字是药店，非处方药可直接买",
        "租房押金1-2个月，签合同前仔细看",
        "居留提前预约，准备好材料复印件",
        "垃圾分类不严，玻璃瓶要单独放",
        "夏天蚊子多，药店超市有驱蚊水",
        "海滩躺椅遮阳伞需要租，大部分免费",
        "公交车票90分钟内有效，可换乘",
    ]
    
    culture_tips = [
        "希腊人贴面礼问候（左右各一下）",
        "希腊人摇头表示是，点头表示不是",
        "希腊人约会迟到15-30分钟很正常",
        "午餐14:00后，晚餐21:00后开始",
        "喝咖啡可以坐一下午，一杯配一杯水",
        "希腊人家庭观念重，周末常聚餐",
        "小费不是必须的，凑整零钱就行",
        "砍价在跳蚤市场可以，百货商店不行",
    ]
    
    foods = [
        "Moussaka慕萨卡：茄子肉酱焗土豆，国菜",
        "Souvlaki苏布拉基：烤肉串配饼快餐",
        "Gyros吉罗斯：旋转烤肉卷午餐首选",
        "Tzatziki塔扎基：酸奶黄瓜酱配面包",
        "Greek Salad希腊沙拉：番茄黄瓜羊奶酪",
        "Dolmades多尔玛德斯：葡萄叶包米饭",
        "Pastitsio帕斯蒂修：希腊版千层面",
        "Spanakopita菠菜派：酥皮菠菜点心",
        "Loukoumades：蜂蜜小油球甜点",
        "Koulouri库劳里：芝麻圈路边零食",
        "Bougatsa布加察：奶油酥皮早餐",
        "Saganaki萨嘎纳基：煎羊奶酪前菜",
    ]
    
    warnings = [
        "复活节约4月20日，提前备好物资",
        "圣诞期间12.24-26日商店关门多",
        "新年1月1日大部分服务暂停",
        "8月暑假很多小店铺主度假关门",
        "暴风雪天尽量避免开车出行",
    ]
    
    # 华人关心的本地资讯
    chinese_news = [
        "居留卡续签建议提前2个月预约，避免过期",
        "雅典中国城（地铁Agios Dimitrios站）超市周末也开",
        "华人快递：顺丰、DHL在雅典有代理点",
        "中希航班：国航雅典-北京每周多班，提前订票便宜",
        "希腊买房移民政策：25万欧元起，可带家属",
        "华人微信群：搜索「雅典华人互助」加群",
        "换汇提醒：找正规渠道，谨防被骗",
        "孩子上学：公立学校免费，国际学校学费约8000-15000欧/年",
        "医疗保险：建议买私人保险，公立排队久",
        "考驾照：中国驾照可换希腊驾照，需翻译公证",
        "开店注意：需申请营业执照，税务较复杂",
        "租房旺季：9月开学季房源紧张，提前找",
        "华人餐厅：新时代、新华东、京品等可送餐",
        "快递回国：EMS约7-15天，DHL约3-5天",
        "签证申请：申根签需提前1-2个月预约",
    ]
    
    # 根据日期选择不同的组合
    selected = []
    
    # 第1条：华人资讯（每天必有一条）
    selected.append(("🇨🇳 华人", chinese_news[day_of_year % len(chinese_news)]))
    
    # 第2条：轮换类型
    types = ["出行", "经济", "居住", "通讯", "生活"]
    type_idx = day_of_year % 5
    if type_idx == 0:
        selected.append(("🚌 出行", random.choice(["雅典地铁票90分钟有效", "机场快线提前90分钟到", "打车用Beat APP较便宜", "停车标志牌要看清楚颜色"])))
    elif type_idx == 1:
        selected.append(("💰 经济", random.choice(["1欧元≈7.8人民币", "银行周末不开，周五下午也早", "有些店只收现金", "支付宝微信部分地方可用"])))
    elif type_idx == 2:
        selected.append(("🏠 居住", random.choice(["签租约前要检查房屋状况", "物业费有时另算", "押金退还需要拍照留证", "水电费单月一付"])))
    elif type_idx == 3:
        selected.append(("📱 通讯", random.choice(["手机卡用COSMOTE信号较好", "公共图书馆有免费WiFi", "漫游建议开通欧盟套餐", "网络运营商：Cosmote/Vodafone/Wind"])))
    else:
        selected.append(("🛒 生活", life_tips[day_of_year % len(life_tips)]))
    
    # 第3条：文化
    selected.append(("🇬🇷 文化", culture_tips[day_of_year % len(culture_tips)]))
    
    # 第4条：美食
    selected.append(("🍽️ 美食", foods[day_of_year % len(foods)]))
    
    # 第5条：节日提醒
    selected.append(("📅 提醒", warnings[day_of_year % len(warnings)]))
    
    return selected

def send_newsletter():
    """发送简报"""
    print("="*50)
    print(f"希腊华人每日简报 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    athens_now = datetime.now() + timedelta(hours=6)
    date_str = athens_now.strftime("%Y年%m月%d日")
    weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][athens_now.weekday()]
    
    weather = get_weather()
    greek = get_greek_phrase()
    news = get_daily_news()
    
    subject = f"📋 希腊简报 {date_str} {weekday_cn}"
    
    content = f"""📋 希腊华人每日简报
{datetime.now().strftime('%Y年%m月%d日')} {weekday_cn}

🌤️ {weather}

📰 今日资讯

"""
    for cat, text in news:
        content += f"{cat} {text}\n\n"
    
    content += f"""📚 每日希腊语

{greek[0]}（{greek[1]}）
{greek[2]}

📍 实用电话

🏥 急救 166 | 报警 100 | 火警 199 | 欧盟通用 112

📍 编辑：希腊华人简报
"""
    
    print(f"\n📅 {date_str} {weekday_cn}")
    print(f"🌤️ {weather}")
    print("\n📰 今日资讯：")
    for cat, text in news:
        print(f"   {cat} {text}")
    
    print("\n📧 发送邮件...")
    success, message = send_email(RECIPIENT_EMAIL, subject, content)
    
    if success:
        print(f"✅ 发送成功 → {RECIPIENT_EMAIL}")
        return True
    else:
        print(f"❌ 发送失败: {message}")
        return False

if __name__ == "__main__":
    try:
        success = send_newsletter()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)

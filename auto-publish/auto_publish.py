#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动发布脚本 - 万金油暖心大叔 & 上海爷叔安东尼
目标：中年男人，走心共情共鸣，涨粉、增阅读

发布时间：7:30 / 19:30 / 23:30
平台：小红书 + 头条号

内容策略：
- 早7:30：积极生活篇 - 自律成长、健康管理（走心正能量）
- 晚19:30：人生智慧篇 - 过来人经验、生活感悟（共情实用）
- 晚23:30：温暖陪伴篇 - 治愈系、生活小确幸（共鸣治愈）
"""

import os
import json
import subprocess
import re
from datetime import datetime

# 配置 - 从环境变量读取，本地开发用默认值
YIXIAOER_API_KEY = os.environ.get("YIXIAOER_API_KEY", "2DtnDBGb4f90RB89IknpO")
DOUBAO_API_KEY = os.environ.get("DOUBAO_API_KEY", "40917d42-b88d-4e86-97df-368bb4aeba4f")
DOUBAO_MODEL = "doubao-seed-1-8-251228"

# GitHub Actions 使用相对路径
WORKSPACE = os.environ.get("GITHUB_WORKSPACE", os.path.expanduser("~/.qclaw/workspace"))
LOG_FILE = os.path.join(WORKSPACE, "auto-publish/publish.log")
IMAGE_USED_FILE = os.path.join(WORKSPACE, "auto-publish/images_used.json")
HISTORY_FILE = os.path.join(WORKSPACE, "auto-publish/title_history.json")

# 账号配置
ACCOUNTS = {
    "xiaohongshu": {
        "platform": "小红书",
        "account_id": "694c788c22f9fa4f9cfa4fa2",
        "account_name": "万金油暖心大叔抗衰（ESTJ 事业篇）"
    },
    "toutiao": {
        "platform": "头条号",
        "account_id": "692438d83b864e9db2b7b61a",
        "account_name": "上海爷叔安东尼"
    }
}

# 时间段配置 - 走心共情话题
TIME_SLOTS = {
    "morning": {
        "time": "7:30",
        "title": "积极生活篇",
        "style": "自律成长",
        "theme": "中年人的自我提升",
        "topics": [
            "坚持跑步一年后的变化",
            "每天早起一小时做什么",
            "中年人如何保持精力充沛",
            "戒掉熬夜30天的感受",
            "开始健身来得及吗",
            "养成早睡早起的小技巧",
            "每天读书半小时的收获",
            "中年人如何管理时间",
            "被人说显年轻那天我做了什么",
            "真实的男人可以有多年轻",
            "中年男人的逆龄秘诀不是护肤品",
            "同龄人老了，我却越活越年轻"
        ]
    },
    "evening": {
        "time": "19:30",
        "title": "人生智慧篇",
        "style": "经验干货",
        "theme": "过来人的真心话",
        "topics": [
            "中年以后才明白的10件事",
            "人到中年最重要的不是钱",
            "和老婆相处20年的心得",
            "教育孩子我走过哪些弯路",
            "真正的朋友越来越少是正常的",
            "中年人的体面是什么",
            "什么才是真正的安全感",
            "那些后悔没早点知道的事",
            "男人越活越年轻的底层逻辑",
            "让我看起来比实际年龄小的习惯",
            "中年男人的状态比年龄更重要",
            "同龄人都在老，我却在变年轻"
        ]
    },
    "night": {
        "time": "23:30",
        "title": "温暖陪伴篇",
        "style": "治愈走心",
        "theme": "生活中的小确幸",
        "topics": [
            "回家路上看到的一幕让我笑了",
            "孩子突然说了一句暖心的话",
            "和老婆牵手散步的日常",
            "周末陪父母吃饭的时光",
            "一个人的小确幸时刻",
            "收到老友信息的感动",
            "做一顿饭给家人的满足",
            "平凡日子里的幸福瞬间",
            "被年轻人说'大叔你好年轻'那一刻",
            "活出了年轻时的状态",
            "中年男人最好的样子是什么",
            "让自己越来越年轻的生活方式"
        ]
    }
}

def log_msg(msg):
    print(msg)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

def curl_post(url, headers, data):
    cmd = ['curl', '-s', '-X', 'POST', url]
    for key, value in headers.items():
        cmd.extend(['-H', f'{key}: {value}'])
    cmd.extend(['-d', json.dumps(data, ensure_ascii=False)])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout) if result.stdout else {}

def curl_get(url, headers):
    cmd = ['curl', '-s', '-X', 'GET', url]
    for key, value in headers.items():
        cmd.extend(['-H', f'{key}: {value}'])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout) if result.stdout else {}

def get_materials():
    try:
        response = curl_get(
            "https://www.yixiaoer.cn/api/material?page=1&size=50",
            {"Authorization": YIXIAOER_API_KEY, "Content-Type": "application/json"}
        )
        if response.get("statusCode") == 0:
            return response.get("data", {}).get("data", [])
    except Exception as e:
        log_msg(f"❌ 获取素材失败: {e}")
    return []

def get_next_image():
    """获取下一张未使用的图片"""
    materials = get_materials()
    if not materials:
        log_msg("❌ 素材库为空")
        return None
    
    used_images = []
    if os.path.exists(IMAGE_USED_FILE):
        try:
            with open(IMAGE_USED_FILE, 'r') as f:
                used_images = json.load(f)
        except:
            pass
    
    log_msg(f"   📷 素材库共 {len(materials)} 张，已用 {len(used_images)} 张")
    
    for m in materials:
        if m.get("id") not in used_images:
            used_images.append(m.get("id"))
            with open(IMAGE_USED_FILE, 'w') as f:
                json.dump(used_images, f)
            log_msg(f"   ✅ 新图片: {m.get('fileName')}")
            return m
    
    # 循环使用
    used_images = [materials[0].get("id")]
    with open(IMAGE_USED_FILE, 'w') as f:
        json.dump(used_images, f)
    return materials[0]

def get_time_slot():
    hour = datetime.now().hour
    if hour < 15:
        return "morning"
    elif hour < 22:
        return "evening"
    else:
        return "night"

def load_title_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return []

def save_title(title):
    history = load_title_history()
    history.append(title)
    history = history[-30:]
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def get_topic_for_slot(time_slot):
    """根据时间段和历史记录，轮换选择话题"""
    config = TIME_SLOTS[time_slot]
    topics = config["topics"]
    
    # 读取话题使用记录
    topic_file = os.path.expanduser("~/.qclaw/workspace/auto-publish/topic_history.json")
    topic_history = {}
    if os.path.exists(topic_file):
        try:
            with open(topic_file, 'r') as f:
                topic_history = json.load(f)
        except:
            pass
    
    used = topic_history.get(time_slot, [])
    
    # 找未用过的话题
    for t in topics:
        if t not in used:
            used.append(t)
            topic_history[time_slot] = used
            with open(topic_file, 'w') as f:
                json.dump(topic_history, f, ensure_ascii=False)
            return t
    
    # 全部用过，重新开始
    topic_history[time_slot] = [topics[0]]
    with open(topic_file, 'w') as f:
        json.dump(topic_history, f, ensure_ascii=False)
    return topics[0]

def generate_content(time_slot):
    """生成内容 - 走心共情版"""
    url = "https://ark.cn-beijing.volces.com/api/v3/responses"
    
    config = TIME_SLOTS[time_slot]
    topic = get_topic_for_slot(time_slot)
    history = load_title_history()
    history_str = ""
    if history:
        history_str = "\n最近用过的标题（不要重复）：\n" + "\n".join([f"- {t}" for t in history[-8:]])
    
    # 根据时间段定制不同的prompt - 走心共情版
    if time_slot == "morning":
        prompt = f"""你是"万金油暖心大叔"，一个经历过人生起伏的中年男人。你用行动证明中年人也可以自律成长，越活越年轻。你的文字走心、真实，让人产生共鸣。

【今日话题】{topic}
【内容结构】
① 开头：分享一个改变后的小成就/变化（让人眼前一亮，有画面感）
② 中间：具体做了什么+真实感受（真实细节，有代入感，走心）
③ 转折：遇到的困难怎么克服的（接地气，不说教）
④ 结尾：给人信心，觉得"我也可以试试"（正能量但不鸡汤，温暖）
{history_str}

【标题要求 - 必须吸引眼球！】
- 15-25字，有冲击力，让人忍不住想点进来
- 用数字、对比、反差来吸引：
  * 数字型：被误认成舅舅，健身后的真实变化
  * 对比型：同龄人老了，我却越活越年轻
  * 反差型：那天接娃被问"你是他哥哥吗"
  * 疑问型：中年男人为什么看起来比实际年龄小10岁？
- ❌ 禁止出现"50岁"、"40岁"等具体年龄数字
- ✅ 可以用"中年"、"大叔"、"过来人"等模糊表述
- ✅ 标题要有故事感、有细节、有代入感

【标签策略 - 必须8个】
成长（3个）：#中年成长 #自我提升 #自律生活 中选3个
逆龄（2个）：#抗衰逆龄 #越活越年轻 #状态比年龄重要 中选2个
热门（3个）：#中年人生 #正能量 #积极生活 中选3个

【❌禁止】
- 禁止"标题："、"正文："、"标签："等标记词
- 禁止"首先、其次、最后、总之"
- 禁止空洞的"加油你可以的"
- 禁止提及体检异常、裁员、病痛等负面话题
- 禁止出现"50岁"、"40岁"、"30岁"等具体年龄数字

【输出格式 - 直接输出，第一行标题，第二行标签，第三行起正文】
（标题，15-25字，不出现具体年龄）
（8个标签，#开头空格分隔）
（正文，300-400字，走心真实分享，共情共鸣）"""

    elif time_slot == "evening":
        prompt = f"""你是"万金油暖心大叔"，一个经历过人生起落的中年男人，用过来人的智慧分享真心话。你越活越年轻，心态比很多年轻人都好。你的文字走心、有共鸣，让人看完觉得"说的就是我"。

【今日话题】{topic}
【内容结构】
① 开头：一个颠覆认知或引发思考的观点（让人停下来想，戳心）
② 中间：真实故事+具体感悟（1-2个故事，走心共情）
③ 转折：如果重来，我会怎么做（过来人的教训，不说教）
④ 结尾：让人觉得有收获，值得收藏（实用但不说教，温暖）
{history_str}

【标题要求 - 必须吸引眼球！】
- 15-25字，有智慧感+好奇心，让人想收藏
- 用洞察、反常识、过来人视角来吸引：
  * 洞察型：中年以后才明白，最贵的不是房子
  * 反常识型：那些活得年轻的中年男人，都有一个共同点
  * 过来人型：到了中年才发现，这几件事越早懂越好
  * 收藏型：男人越活越年轻的10个习惯，第5条很多人不知道
- ❌ 禁止出现"50岁"、"40岁"等具体年龄数字
- ✅ 可以用"中年"、"大叔"、"过来人"等模糊表述
- ✅ 标题要有洞察力，让人觉得"说的就是我"

【标签策略 - 必须8个】
智慧（3个）：#人生感悟 #中年智慧 #生活哲学 中选3个
逆龄（2个）：#抗衰秘诀 #心态年轻 #越活越年轻 中选2个
热门（3个）：#中年人生 #人生的意义 #中年人必看 中选3个

【❌禁止】
- 禁止"标题："、"正文："、"标签："等标记词
- 禁止"首先、其次、最后、总之"
- 禁止空洞的大道理，要有具体故事
- 禁止提及裁员、病痛等负面话题
- 禁止出现"50岁"、"40岁"、"30岁"等具体年龄数字

【输出格式 - 直接输出，第一行标题，第二行标签，第三行起正文】
（标题，15-25字，不出现具体年龄）
（8个标签，#开头空格分隔）
（正文，300-400字，有故事有感悟，走心共情）"""

    else:  # night
        prompt = f"""你是"万金油暖心大叔"，一个擅长发现生活中小确幸的中年男人，温暖治愈系。你说自己年轻别人都信，因为心态真的很好。你的文字温暖、治愈，让人产生共鸣。

【今日话题】{topic}
【内容结构】
① 开头：一个温馨的生活画面/小细节（让人会心一笑，有画面感）
② 中间：细节描写+内心感受（温馨有画面感，走心）
③ 转折：原来幸福就这么简单（升华，不说教）
④ 结尾：温暖治愈，让人对生活充满期待（轻柔的正能量，共鸣）
{history_str}

【标题要求 - 必须吸引眼球！】
- 15-25字，有温暖感+治愈感，让人看完心情好
- 用细节、场景、共鸣来吸引：
  * 细节型：孩子突然跑过来抱住我说"爸爸辛苦了"
  * 场景型：晚上和老婆牵手散步，邻居说我们像情侣
  * 治愈型：被叫"哥"而不是"叔"的那一刻，中年男人都懂
  * 确幸型：下班路上那20分钟，是我一天中最放松的时刻
- ❌ 禁止出现"50岁"、"40岁"等具体年龄数字
- ✅ 可以用"中年"、"大叔"、"过来人"等模糊表述
- ✅ 标题要有画面感，让人脑海里浮现那个场景

【标签策略 - 必须8个】
温暖（3个）：#生活的小确幸 #温暖治愈 #幸福很简单 中选3个
逆龄（2个）：#心态年轻 #抗衰生活 #越活越年轻 中选2个
热门（3个）：#平凡生活 #治愈系 #中年人的幸福 中选3个

【❌禁止】
- 禁止"标题："、"正文："、"标签："等标记词
- 禁止"首先、其次、最后、总之"
- 禁止强行正能量，要润物细无声
- 禁止提及孤独、失眠、崩溃等负面话题
- 禁止出现"50岁"、"40岁"、"30岁"等具体年龄数字

【输出格式 - 直接输出，第一行标题，第二行标签，第三行起正文】
（标题，15-25字，不出现具体年龄）
（8个标签，#开头空格分隔）
（正文，300-400字，温馨治愈风格，走心共鸣）"""

    payload = {
        "model": DOUBAO_MODEL,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": prompt}]}]
    }
    
    try:
        response = curl_post(
            url,
            {"Authorization": f"Bearer {DOUBAO_API_KEY}", "Content-Type": "application/json"},
            payload
        )
        output = response.get("output", [])
        for item in output:
            if item.get("type") == "message":
                for c in item.get("content", []):
                    if c.get("type") == "output_text":
                        return c.get("text", ""), topic
        return None, topic
    except Exception as e:
        log_msg(f"❌ 豆包API异常: {e}")
        return None, topic

def parse_content(text):
    """智能解析 - 不管AI输出什么格式都能提取"""
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    
    result = {
        "title": "",
        "tags": "",
        "body": ""
    }
    
    if not lines:
        return result
    
    # 第一行：标题（短句，不含#）
    for i, line in enumerate(lines):
        if not line.startswith('#') and len(line) < 40:
            result["title"] = line
            break
    
    # 收集所有标签
    all_tags = []
    for line in lines:
        if '#' in line:
            tags = re.findall(r'#[\w\u4e00-\u9fff]+', line)
            all_tags.extend(tags)
    
    # 去重，保留8个
    seen = set()
    unique_tags = []
    for t in all_tags:
        if t not in seen and len(unique_tags) < 8:
            seen.add(t)
            unique_tags.append(t)
    
    # 补充默认标签
    defaults = ["#中年危机", "#中年人生", "#职场焦虑", "#家庭压力", 
                "#情感共鸣", "#不敢喊累的中年人", "#上有老下有小", "#深夜情绪树洞"]
    for d in defaults:
        if d not in seen and len(unique_tags) < 8:
            unique_tags.append(d)
    
    result["tags"] = " ".join(unique_tags[:8])
    
    # 正文：排除标题行和标签行
    body_lines = []
    for line in lines:
        # 跳过标题行
        if line == result["title"]:
            continue
        # 跳过纯标签行
        if line.startswith('#') and all(c == '#' or c.isalnum() or c == ' ' or '\u4e00' <= c <= '\u9fff' for c in line.replace(' ', '')):
            continue
        # 收集正文
        body_lines.append(line)
    
    result["body"] = "\n\n".join(body_lines)
    
    # 如果正文太短，用整个文本（排除标题标签）
    if len(result["body"]) < 100:
        result["body"] = text.replace(result["title"], "").replace(result["tags"], "").strip()
    
    return result

def build_image_form(material):
    return {
        "width": material.get("width", 1080),
        "height": material.get("height", 1920),
        "size": material.get("size", 100000),
        "path": material.get("filePath", ""),
        "key": material.get("fileKey", ""),
        "format": material.get("fileFormat", "jpg")
    }

def publish_xiaohongshu(title, body, tags, image, account):
    """发布到小红书"""
    url = "https://www.yixiaoer.cn/api/taskSets/v2"
    
    body_with_tags = f"{body}\n\n{tags}"
    
    payload = {
        "platforms": ["小红书"],
        "publishType": "imageText",
        "isDraft": False,
        "publishChannel": "cloud",
        "coverKey": image.get("fileKey", ""),
        "desc": title,
        "publishArgs": {
            "accountForms": [{
                "platformAccountId": account["account_id"],
                "coverKey": image.get("fileKey", ""),
                "images": [build_image_form(image)],
                "contentPublishForm": {
                    "title": title,
                    "description": body_with_tags,
                    "text": body_with_tags,
                    "location": ""
                }
            }],
            "content": body_with_tags
        }
    }
    
    try:
        response = curl_post(url, {"Authorization": YIXIAOER_API_KEY, "Content-Type": "application/json"}, payload)
        return response.get("statusCode") == 0, response
    except Exception as e:
        return False, str(e)

def publish_toutiao(title, body, tags, image, account):
    """发布到头条号"""
    url = "https://www.yixiaoer.cn/api/taskSets/v2"
    
    body_with_tags = f"{body}\n\n{tags}"
    
    payload = {
        "platforms": ["头条号"],
        "publishType": "imageText",
        "isDraft": False,
        "publishChannel": "cloud",
        "coverKey": image.get("fileKey", ""),
        "desc": title,
        "publishArgs": {
            "accountForms": [{
                "platformAccountId": account["account_id"],
                "coverKey": image.get("fileKey", ""),
                "images": [build_image_form(image)],
                "contentPublishForm": {
                    "title": title,
                    "description": body_with_tags,
                    "text": body_with_tags,
                    "images": [build_image_form(image)],
                    "pubType": 1,
                    "declaration": 1
                }
            }],
            "content": body_with_tags
        }
    }
    
    try:
        response = curl_post(url, {"Authorization": YIXIAOER_API_KEY, "Content-Type": "application/json"}, payload)
        return response.get("statusCode") == 0, response
    except Exception as e:
        return False, str(e)

def main():
    log_msg("\n" + "="*60)
    log_msg(f"🎯 万金油大叔 & 爷叔安东尼 - 走心共情版")
    log_msg(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_msg("="*60)
    
    # 1. 时间段
    time_slot = get_time_slot()
    config = TIME_SLOTS[time_slot]
    log_msg(f"\n📌 {config['title']}（{config['style']}）")
    
    # 2. 图片
    log_msg("\n🖼️ 获取图片...")
    image = get_next_image()
    if not image:
        log_msg("❌ 无图片，终止")
        return False
    
    # 3. 生成内容
    log_msg(f"\n📝 生成内容...")
    result = generate_content(time_slot)
    if isinstance(result, tuple):
        raw, topic = result
    else:
        raw = result
        topic = "未知"
    
    if not raw:
        log_msg("❌ 生成失败，终止")
        return False
    
    log_msg(f"   ✅ 生成成功（话题：{topic}）")
    log_msg(f"\n{'='*60}\n【生成内容】\n{raw}\n{'='*60}")
    
    # 4. 解析
    content = parse_content(raw)
    
    # 保存标题
    if content["title"]:
        save_title(content["title"])
    
    # 检查
    log_msg(f"\n📊 内容检查:")
    log_msg(f"   标题: {content['title']} ({len(content['title'])}字)")
    log_msg(f"   正文: {len(content['body'])}字 {'✅' if len(content['body']) >= 200 else '⚠️'}")
    log_msg(f"   标签: {content['tags']}")
    
    # 如果解析失败，用原始文本
    if not content["title"]:
        content["title"] = "中年男人的心里话"
    if not content["body"] or len(content["body"]) < 50:
        content["body"] = raw
    
    # 5. 发布到小红书和头条号
    results = {}
    
    log_msg(f"\n📤 小红书...")
    ok, res = publish_xiaohongshu(content["title"], content["body"], content["tags"], image, ACCOUNTS["xiaohongshu"])
    results["小红书"] = ok
    log_msg(f"   {'✅ 成功' if ok else f'❌ 失败: {res}'}")
    
    log_msg(f"\n📤 头条号...")
    ok, res = publish_toutiao(content["title"], content["body"], content["tags"], image, ACCOUNTS["toutiao"])
    results["头条号"] = ok
    log_msg(f"   {'✅ 成功' if ok else f'❌ 失败: {res}'}")
    
    # 汇总
    log_msg(f"\n{'='*60}")
    log_msg("📊 发布汇总:")
    for p, ok in results.items():
        log_msg(f"   {p}: {'✅' if ok else '❌'}")
    log_msg(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 完成")
    log_msg("="*60 + "\n")
    
    return all(results.values())

if __name__ == "__main__":
    ok = main()
    exit(0 if ok else 1)

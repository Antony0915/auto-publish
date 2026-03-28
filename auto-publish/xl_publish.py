#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动发布脚本 - 中年心理疗愈账号
7:30: 心理疗愈/情绪管理（温暖治愈）
12:30: 职场压力/心理健康（理性建议）
22:30: 家庭婚姻情感（深夜情感）
"""

import os
import json
import subprocess
from datetime import datetime

# 配置 - 从环境变量读取，本地开发用默认值
YIXIAOER_API_KEY = os.environ.get("YIXIAOER_API_KEY", "2DtnDBGb4f90RB89IknpO")
DOUBAO_API_KEY = os.environ.get("DOUBAO_API_KEY", "40917d42-b88d-4e86-97df-368bb4aeba4f")
DOUBAO_MODEL = "doubao-seed-1-8-251228"

# GitHub Actions 使用相对路径
WORKSPACE = os.environ.get("GITHUB_WORKSPACE", os.path.expanduser("~/.qclaw/workspace"))
LOG_FILE = os.path.join(WORKSPACE, "auto-publish/xl-publish.log")
IMAGE_USED_FILE = os.path.join(WORKSPACE, "auto-publish/xl-images_used.json")
HISTORY_FILE = os.path.join(WORKSPACE, "auto-publish/xl-title_history.json")

# 账号配置
ACCOUNT = {
    "platform": "小红书",
    "account_id": "6974153887081539fad69f8b",
    "account_name": "万金油暖心大蜀中年心理疗愈"
}

# 时间段配置
TIME_SLOTS = {
    "morning": {
        "hour": 7,
        "slot_name": "7:30",
        "title": "心理疗愈/情绪管理",
        "style": "温暖治愈",
        "style_desc": "温暖治愈：像一杯热茶，抚慰人心，让人看完感觉被理解、被治愈，适合早晨的正能量",
        "theme": "中年心理疗愈、情绪管理、心理健康建议"
    },
    "noon": {
        "hour": 12,
        "slot_name": "12:30",
        "title": "职场压力/心理健康",
        "style": "理性建议",
        "style_desc": "理性建议：像老朋友分享经验，给出实用的心理健康和职场减压建议，让人觉得有收获",
        "theme": "职场压力、心理健康建议、情绪管理"
    },
    "night": {
        "hour": 22,
        "slot_name": "22:30",
        "title": "家庭婚姻情感",
        "style": "深夜情感",
        "style_desc": "深夜情感：写实又深情，写出中年婚姻、家庭关系的真实困境和温暖，让人产生强烈共鸣",
        "theme": "家庭婚姻情感、中年夫妻关系、家庭责任"
    }
}

def log_msg(msg):
    print(msg)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

def curl_get(url, headers):
    cmd = ['curl', '-s', '-X', 'GET', url]
    for key, value in headers.items():
        cmd.extend(['-H', f'{key}: {value}'])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout) if result.stdout else {}

def curl_post(url, headers, data):
    cmd = ['curl', '-s', '-X', 'POST', url]
    for key, value in headers.items():
        cmd.extend(['-H', f'{key}: {value}'])
    cmd.extend(['-d', json.dumps(data, ensure_ascii=False)])
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
    materials = get_materials()
    if not materials:
        return None
    
    used_images = []
    if os.path.exists(IMAGE_USED_FILE):
        try:
            with open(IMAGE_USED_FILE, 'r') as f:
                used_images = json.load(f)
        except:
            pass
    
    for m in materials:
        if m.get("id") not in used_images:
            used_images.append(m.get("id"))
            with open(IMAGE_USED_FILE, 'w') as f:
                json.dump(used_images, f)
            return m
    
    used_images = [materials[0].get("id")]
    with open(IMAGE_USED_FILE, 'w') as f:
        json.dump(used_images, f)
    return materials[0]

def get_time_slot():
    hour = datetime.now().hour
    if hour < 12:
        return "morning"
    elif hour < 20:
        return "noon"
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
    history = history[-20:]
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def generate_content(time_slot):
    url = "https://ark.cn-beijing.volces.com/api/v3/responses"
    config = TIME_SLOTS[time_slot]
    history = load_title_history()
    history_str = ""
    if history:
        history_str = "\n\n以下是最近用过的标题，不要重复：\n" + "\n".join([f"- {t}" for t in history[-5:]])
    
    # 根据时间段选择不同的标题模板和写作风格
    if time_slot == "morning":
        title_examples = """【温暖治愈风格 - 早晨7:30】
- 你不是不够努力，是真的累了
- 那些没说出口的话，才是中年人最深的孤独
- 有时候崩溃不需要理由，只需要一个人懂
- 你以为的坚强，其实是在强颜欢笑
- 40岁后，我终于学会了和孤独和解
- 别再对自己说"忍忍就过去了"，情绪需要出口
- 中年人的崩溃，都是从"我应该坚强"开始的
- 为什么你总是很累？暖心大叔帮你找原因"""
        writing_focus = "温暖治愈，给读者力量，让他们觉得被理解、被陪伴"
    elif time_slot == "noon":
        title_examples = """【理性建议风格 - 中午12:30】
- 40岁被裁员那天，我在车里坐了2小时
- 为什么你越努力越焦虑？暖心大叔想对你说这3句话
- 中年抑郁的5个信号，中2个以上就要重视了
- 从月薪5000到年薪50万，我失去了什么
- 别人40岁升职，我40岁被裁员，但我不后悔
- 20年职场生涯，最后一次被裁员才让我明白什么叫真正的自由
- 40岁前我拼命赚钱，40岁后才明白这3样东西钱买不到
- 总忍不住发脾气？可能是这3种情绪在消耗你"""
        writing_focus = "理性建议，像老朋友分享经验，给出实用的心理健康和职场减压建议"
    else:  # night
        title_examples = """【深夜情感风格 - 晚上22:30】
- 凌晨两点摸黑灌凉啤酒，连开瓶声都压到最低
- 老婆说"你变了"，我才发现自己已经不会笑了
- 孩子问我"爸爸你为什么总是在生气"，我哭了
- 那天我在车里坐了2小时，才明白中年人的崩溃是无声的
- 你有多久没有好好睡过一觉了？
- 你还记得上次真心笑是什么时候吗？
- 40岁才明白：人生不是马拉松，是散步
- 上有老下有小的无奈，只有中年人懂"""
        writing_focus = "深夜情感，写实又深情，写出中年婚姻、家庭关系的真实困境和温暖"

    prompt = f"""你是一位50岁的暖心大叔，经历过人生的起起落落，有过迷茫、崩溃、也有过温暖和治愈。你现在想用文字陪伴那些正在经历中年困境的朋友们。你的文字从不讲大道理，只是说出大家心里的感受，让人看完觉得"原来不止我一个人这样"。

请为以下主题创作一篇小红书文案：

主题：{config['title']}
风格：{config['style']}
写作重点：{writing_focus}
目标读者：40-55岁的中年人，上有老下有小，默默扛着一切{history_str}

【参考这些爆款标题的感觉 - 标题要让人忍不住点进来】
{title_examples}

【❌ 绝对禁止】
- 标题和正文中不能出现任何时间数字（如7:30、12:30、早上、中午、晚上、凌晨、深夜等）
- 不能用"首先、其次、最后、总之"这种AI式结构
- 不能用"让我们一起、希望你能"这种说教口吻
- 不能用"第一、第二、第三"这种列表式表达
- 不能用"这个故事告诉我们"这种总结式结尾
- 不能用"首先...然后...最后"这种流程式表达
- 不能写得太文艺、太鸡汤，要接地气
- 不能用"记住、记住这3点、请记住"这种命令式口吻

【✅ 必须做到 - 严格检查】
1. 标题要戳心：15-25字，让人一看就忍不住点进来，感觉"这说的不就是我吗"
2. 开头3秒抓人：第一句话就要让人停下来，用具体场景、数字、或反问
3. 场景要具体：写真实的生活细节，比如"刚把热好的饭端上桌，孩子说不想吃"
4. 情感要真诚：像跟老朋友深夜聊天，不装、不端着
5. 中间要有共鸣：写出中年人不敢说出口的那些委屈、无奈、心酸
6. 结尾要有温度：不一定要给答案，但要让读者觉得被理解、被安慰
7. 标签要8个：必须8个标签！混合热门大标签+垂直细分+长尾搜索标签
8. 字数要300-450字：内容要饱满，有细节，有感情，不能少于300字

【标签策略 - 必须8个】
热门大标签（2-3个）：#中年危机 #40岁人生 #职场焦虑 #家庭压力
垂直细分（2-3个）：#情感共鸣 #心理疗愈 #中年感悟 #人生哲学
长尾搜索（2-3个）：#不敢喊累的中年人 #上有老下有小 #深夜情绪树洞 #40岁男人的深夜独白 #中年人的崩溃不敢声张

【正文结构要求】
- 开头（20-30字）：具体场景抓人，比如"那天在车里坐了2小时，一根烟接一根烟"
- 场景细节（80-100字）：写真实困境，具体到时间、地点、动作、心理
- 情感共鸣（80-100字）：写出"不敢说"的真实感受，戳中痛点
- 转折启发（40-60字）：真实的改变，不说"我们应该"，说"我后来"
- 温暖结尾（30-50字）：给读者被理解的感觉，不一定要答案

【输出格式】
【小红书版】
标题：（戳心的标题，15-25字，不含任何时间）
标签：（必须8个标签，#开头，空格分隔）
（正文，300-450字，自然段落，不要列表，不要分点，要真实走心）

【重要】字数检查：正文必须在300-450字之间，标签必须8个！

现在开始写："""

    payload = {
        "model": DOUBAO_MODEL,
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": prompt}]
            }
        ]
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
                content_list = item.get("content", [])
                for c in content_list:
                    if c.get("type") == "output_text":
                        return c.get("text", "")
        log_msg(f"❌ 豆包API调用失败: {response}")
        return None
    except Exception as e:
        log_msg(f"❌ 调用豆包API异常: {e}")
        return None

def parse_content(content_text):
    lines = content_text.strip().split("\n")
    
    result = {
        "title": "",
        "tags": "",
        "body": ""
    }
    
    in_tags = False
    in_body = False
    body_lines = []
    all_tags = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 跳过格式标记行
        if line.startswith("【") and line.endswith("】"):
            if "小红书版" in line or "标题" in line:
                continue
        
        # 提取标题
        if line.startswith("标题：") or line.startswith("标题:"):
            result["title"] = line.replace("标题：", "").replace("标题:", "").strip()
            in_tags = False
            in_body = False
            continue
        
        # 提取标签行
        if line.startswith("标签：") or line.startswith("标签:"):
            tags_part = line.replace("标签：", "").replace("标签:", "").strip()
            # 解析标签
            tag_parts = [t.strip() for t in tags_part.split() if t.strip().startswith("#")]
            all_tags.extend(tag_parts)
            in_tags = True
            in_body = False
            continue
        
        # 收集单独的标签行
        if line.startswith("#") and in_tags:
            tag_parts = [t.strip() for t in line.split() if t.strip().startswith("#")]
            all_tags.extend(tag_parts)
            continue
        
        # 检测到非标签行，结束标签收集
        if in_tags and not line.startswith("#"):
            in_tags = False
        
        # 收集正文（排除格式标记和空行）
        if not line.startswith("【") and not line.startswith("标签") and not line.startswith("标题"):
            # 如果这行全是标签，单独处理
            if line.startswith("#") and all(c == '#' or c.isalnum() or c in '中文_' for c in line.replace(' ', '').replace('#', '')):
                tag_parts = [t.strip() for t in line.split() if t.strip().startswith("#")]
                if tag_parts:
                    all_tags.extend(tag_parts)
                    continue
            
            # 正文内容
            if len(line) > 3:  # 过滤掉太短的行
                body_lines.append(line)
    
    # 去重并限制8个标签
    seen = set()
    unique_tags = []
    for t in all_tags:
        if t not in seen and len(unique_tags) < 8:
            seen.add(t)
            unique_tags.append(t)
    
    # 如果标签不足8个，补充默认标签
    default_tags = [
        "#中年危机", "#40岁人生", "#职场焦虑", "#家庭压力",
        "#情感共鸣", "#不敢喊累的中年人", "#上有老下有小", "#深夜情绪树洞"
    ]
    for dt in default_tags:
        if dt not in seen and len(unique_tags) < 8:
            unique_tags.append(dt)
    
    result["tags"] = " ".join(unique_tags[:8])
    result["body"] = "\n\n".join(body_lines)
    
    # 如果没有标题，用正文第一句
    if not result["title"] and body_lines:
        result["title"] = body_lines[0][:30]
    
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

def get_xiaohongshu_topics(account_id):
    """获取小红书热门话题"""
    try:
        # 获取活动分类
        response = curl_get(
            "https://www.yixiaoer.cn/api/activity/list",
            {"Authorization": YIXIAOER_API_KEY, "Content-Type": "application/json"}
        )
        if response.get("statusCode") == 0:
            activities = response.get("data", {}).get("data", [])
            # 筛选热门活动
            hot_topics = [a for a in activities if a.get("hot", 0) > 0][:3]
            return hot_topics
    except Exception as e:
        log_msg(f"⚠️ 获取热门话题失败: {e}")
    return []

def publish_xiaohongshu(content, image, account):
    url = "https://www.yixiaoer.cn/api/taskSets/v2"
    
    body_text = content.get("body", "")
    tags_text = content.get("tags", "").strip()
    
    # 确保8个标签
    tag_list = [t.strip() for t in tags_text.split() if t.strip().startswith("#")]
    log_msg(f"   解析到标签数: {len(tag_list)}")
    if len(tag_list) < 8:
        log_msg(f"   ⚠️ 标签不足8个（仅{len(tag_list)}个），补充默认标签")
        default_tags = [
            "#中年危机", "#40岁人生", "#职场焦虑", "#家庭压力",
            "#情感共鸣", "#不敢喊累的中年人", "#上有老下有小", "#深夜情绪树洞"
        ]
        existing = set(tag_list)
        for dt in default_tags:
            if dt not in existing:
                tag_list.append(dt)
            if len(tag_list) >= 8:
                break
    tag_list = tag_list[:8]  # 最多8个
    tags_text = " ".join(tag_list)
    log_msg(f"   最终标签（{len(tag_list)}个）: {tags_text}")
    
    body_with_tags = f"{body_text}\n\n{tags_text}"
    
    # 获取热门话题
    log_msg(f"\n📋 获取小红书热门话题...")
    hot_topics = get_xiaohongshu_topics(account["account_id"])
    topic_str = ""
    if hot_topics:
        for t in hot_topics:
            topic_name = t.get("name", "")
            if topic_name:
                topic_str += f"#{topic_name} "
        log_msg(f"   热门话题: {topic_str.strip()}")
        body_with_tags = f"{body_with_tags}\n\n{topic_str.strip()}"
    
    payload = {
        "platforms": ["小红书"],
        "publishType": "imageText",
        "isDraft": False,
        "publishChannel": "cloud",
        "coverKey": image.get("fileKey", ""),
        "desc": content.get("title", ""),
        "publishArgs": {
            "accountForms": [
                {
                    "platformAccountId": account["account_id"],
                    "coverKey": image.get("fileKey", ""),
                    "images": [build_image_form(image)],
                    "contentPublishForm": {
                        "title": content.get("title", ""),
                        "description": body_with_tags,
                        "text": body_with_tags,
                        "location": "",
                        # 添加热门话题标签
                        "topics": hot_topics[0].get("id") if hot_topics else None
                    }
                }
            ],
            "content": body_with_tags
        }
    }
    
    try:
        response = curl_post(
            url,
            {"Authorization": YIXIAOER_API_KEY, "Content-Type": "application/json"},
            payload
        )
        if response.get("statusCode") == 0:
            return True, response
        return False, response
    except Exception as e:
        return False, str(e)

def main():
    log_msg("\n" + "="*50)
    log_msg(f"中年心理疗愈账号发布任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_msg("="*50)
    
    time_slot = get_time_slot()
    config = TIME_SLOTS[time_slot]
    log_msg(f"\n⏰ 时间段: {config['slot_name']} ({config['style']})")
    
    log_msg(f"\n🖼️ 获取素材图片...")
    image = get_next_image()
    if not image:
        log_msg("❌ 获取图片失败")
        return
    
    log_msg(f"   使用图片: {image.get('fileName')} (ID: {image.get('id')})")
    
    log_msg(f"\n📝 调用豆包生成{config['style']}风格文案...")
    raw_content = generate_content(time_slot)
    if not raw_content:
        log_msg("❌ 生成内容失败")
        return
    
    log_msg("   ✅ 内容生成成功")
    log_msg(f"\n【生成内容预览】")
    log_msg("=" * 40)
    log_msg(raw_content)
    log_msg("=" * 40 + "\n")
    
    content = parse_content(raw_content)
    
    if content.get("title"):
        save_title(content["title"])
    
    log_msg(f"   标题: {content.get('title', '')} ({len(content.get('title', ''))}字)")
    log_msg(f"   标签: {content.get('tags', '')} ({len(content.get('tags', '').split())}个)")
    body_text = content.get('body', '')
    body_len = len(body_text)
    log_msg(f"   正文: {body_len} 字")
    if body_len < 300:
        log_msg(f"   ⚠️ 警告: 正文不足300字，可能需要重新生成")
    
    log_msg(f"\n📤 发布到 {ACCOUNT['account_name']}...")
    success, result = publish_xiaohongshu(content, image, ACCOUNT)
    if success:
        log_msg(f"   ✅ 小红书发布成功!")
    else:
        log_msg(f"   ❌ 小红书发布失败: {result}")
    
    log_msg("\n" + "="*50)
    log_msg(f"发布任务完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_msg("="*50 + "\n")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

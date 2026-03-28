#!/usr/bin/env python3
"""
蚁小二视频号自动发布脚本
每天发布3条不同文案的正装男士内容
"""

import json
import requests
import random
import os
from datetime import datetime

# ============ 配置区域 ============
# 请替换为你的蚁小二 API Key
YIXIAOER_API_KEY = "YOUR_API_KEY_HERE"

# 视频号账号ID（从蚁小二后台获取）
VIDEO_ACCOUNT_ID = "YOUR_VIDEO_ACCOUNT_ID"

# 图片目录
IMAGE_DIR = "/Users/wangantony/.qclaw/workspace/images/suits"

# 蚁小二 API 基础地址
BASE_URL = "https://www.yixiaoer.cn/api"

# 文案库
SCRIPTS = [
    # 商务精英风
    {
        "title": "西装是男人的铠甲",
        "content": "西装是男人的铠甲，细节决定成败。\n一套合身的正装，让你在职场中气场全开。\n#正装 #商务穿搭 #男士西装 #职场穿搭"
    },
    {
        "title": "每个男人都需要一套好西装",
        "content": "不是每个场合都需要西装，\n但每个男人都需要一套好西装。\n关键时刻，它能替你说话。\n#西装 #正装男 #商务风 #穿搭技巧"
    },
    {
        "title": "正装穿搭是一门艺术",
        "content": "从面料到剪裁，从领带到袖扣，\n正装穿搭是一门艺术。\n你穿的不是衣服，是态度。\n#男士正装 #西装搭配 #品质生活 #穿搭分享"
    },
    # 生活品味风
    {
        "title": "周末也要精致",
        "content": "周末也要精致，正装不只是为了上班。\n懂得生活的男人，从不会对自己敷衍。\n#正装生活 #品质男装 #穿搭日常 #男士风格"
    },
    {
        "title": "正装可以很帅",
        "content": "有人说西装太正式，\n我说那是你没找到合适的穿法。\n正装可以很帅，也可以很松弛。\n#西装穿搭 #正装不无聊 #男士时尚 #穿搭灵感"
    },
    {
        "title": "投资一套好西装",
        "content": "投资一套好西装，就像投资自己。\n它陪你见客户、赴约会、参加重要场合。\n每一次出场，都是最好的状态。\n#正装投资 #男士穿搭 #西装推荐 #品质穿搭"
    },
    # 励志成长风
    {
        "title": "20岁穿款式，30岁穿品质",
        "content": "20岁穿的是款式，30岁穿的是品质。\n男人的衣柜里，总该有一套拿得出手的正装。\n#成长穿搭 #正装进阶 #男士成熟 #穿搭升级"
    },
    {
        "title": "自信从西装开始",
        "content": "穿上正装的那一刻，\n你会明白什么叫"人靠衣装"。\n自信，从一套好西装开始。\n#自信穿搭 #正装魅力 #男士形象 #穿搭改变"
    },
    {
        "title": "西装见证成长",
        "content": "从职场新人到业务骨干，\n我的西装见证了我的成长。\n你的第一套正装，是什么牌子？\n#职场成长 #正装故事 #男士穿搭 #西装记忆"
    }
]

def get_headers():
    """获取请求头"""
    return {
        "Authorization": YIXIAOER_API_KEY,
        "Content-Type": "application/json"
    }

def check_vip():
    """检查是否为VIP用户"""
    url = f"{BASE_URL}/team/info"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        data = response.json()
        if data.get("code") == 200:
            team = data.get("data", {})
            is_vip = team.get("isVip", False)
            print(f"✅ 团队: {team.get('name', 'Unknown')}")
            print(f"{'✅' if is_vip else '❌'} VIP状态: {'已开通' if is_vip else '未开通'}")
            return is_vip
        else:
            print(f"❌ 获取团队信息失败: {data.get('message')}")
            return False
    except Exception as e:
        print(f"❌ 检查VIP状态出错: {e}")
        return False

def get_image_files():
    """获取图片文件列表"""
    files = []
    for f in os.listdir(IMAGE_DIR):
        if f.endswith(('.jpg', '.jpeg', '.png')):
            files.append(os.path.join(IMAGE_DIR, f))
    return files

def select_daily_scripts():
    """随机选择3条不同的文案"""
    return random.sample(SCRIPTS, 3)

def create_publish_task(script, image_path, task_index):
    """
    创建发布任务
    注意：这里需要根据蚁小二实际API调整字段
    """
    # 视频号发布表单结构（参考蚁小二文档）
    task = {
        "title": script["title"],
        "content": script["content"],
        "type": "image",  # 图文类型
        "platform": "video_channel",  # 视频号
        "accountId": VIDEO_ACCOUNT_ID,
        "publishChannel": "cloud",  # 云发布
        "images": [image_path],  # 图片路径
        "publishTime": None,  # 立即发布
    }
    return task

def publish_content(tasks):
    """
    调用蚁小二API发布内容
    接口：POST /api/v2/tasks/batch
    """
    url = f"{BASE_URL}/v2/tasks/batch"
    
    payload = {
        "tasks": tasks,
        "publishChannel": "cloud"
    }
    
    try:
        response = requests.post(
            url, 
            headers=get_headers(), 
            json=payload,
            timeout=30
        )
        data = response.json()
        
        if data.get("code") == 200:
            print(f"✅ 发布成功！任务ID: {data.get('data', {}).get('taskId', 'N/A')}")
            return True
        else:
            print(f"❌ 发布失败: {data.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ 发布请求出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print(f"🤵 正装男士视频号自动发布")
    print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. 检查VIP状态
    if not check_vip():
        print("❌ 当前团队未开通VIP，无法使用蚁小二插件功能")
        return
    
    # 2. 获取图片
    images = get_image_files()
    if len(images) < 3:
        print(f"❌ 图片数量不足，当前只有 {len(images)} 张，需要至少3张")
        return
    
    print(f"✅ 找到 {len(images)} 张图片")
    
    # 3. 选择文案
    scripts = select_daily_scripts()
    print(f"✅ 已选择 {len(scripts)} 条文案")
    
    # 4. 创建发布任务
    tasks = []
    for i, script in enumerate(scripts):
        print(f"\n📋 任务 {i+1}:")
        print(f"   标题: {script['title']}")
        print(f"   图片: {os.path.basename(images[i])}")
        task = create_publish_task(script, images[i], i)
        tasks.append(task)
    
    # 5. 发布
    print(f"\n🚀 开始发布...")
    success = publish_content(tasks)
    
    if success:
        print("\n✅ 今日3条内容全部发布完成！")
    else:
        print("\n❌ 发布过程中出现错误")

if __name__ == "__main__":
    main()

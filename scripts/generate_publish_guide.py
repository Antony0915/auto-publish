#!/usr/bin/env python3
"""
蚁小二视频号发布方案 - 使用小龙虾插件
由于小龙虾插件主要通过客户端操作，这里提供手动发布指南和自动化建议
"""

import json
import os
from datetime import datetime

# 配置
CONFIG_FILE = "/Users/wangantony/.qclaw/workspace/config/yixiaoer_config.json"
IMAGE_DIR = "/Users/wangantony/.qclaw/workspace/images/real_suit"
SCRIPTS_FILE = "/Users/wangantony/.qclaw/workspace/content/suit_video_scripts_real.md"
LOG_DIR = "/Users/wangantony/.qclaw/workspace/logs"

# 文案库
SCRIPTS = [
    # 上班族日常
    {
        "title": "今天开会穿了这身",
        "content": "今天开会穿了这身\n同事说我看起来很靠谱\n其实我就是不想太随意\n#日常穿搭 #上班穿什么"
    },
    {
        "title": "周末约了客户",
        "content": "周末约了客户\n还是正装放心\n虽然有点热\n但气质到位了\n#正装日常 #打工人穿搭"
    },
    {
        "title": "这套买了两年了",
        "content": "这套买了两年了\n还是很好穿\n经典款就是不会过时\n#西装推荐 #日常穿搭分享"
    },
    # 生活碎片
    {
        "title": "路过公司楼下的咖啡店",
        "content": "路过公司楼下的咖啡店\n随手拍了一张\n今天的光线不错\n#日常记录 #正装"
    },
    {
        "title": "下班去吃了个饭",
        "content": "下班去吃了个饭\n朋友说我穿得太正式\n其实这是我最休闲的一套了\n#打工人的日常 #穿搭分享"
    },
    {
        "title": "家里拍的",
        "content": "家里拍的\n光线一般\n但这件衬衫我真的喜欢\n#日常穿搭 #衬衫推荐"
    },
    # 朋友视角
    {
        "title": "帮朋友拍的工作照",
        "content": "帮朋友拍的工作照\n他最近在相亲\n让我给他参谋一下穿搭\n#正装穿搭 #男生穿搭"
    },
    {
        "title": "我哥们今天面试",
        "content": "我哥们今天面试\n穿了我推荐这套\n他说感觉信心满满\n希望他能拿到offer\n#面试穿搭 #正装"
    },
    {
        "title": "和朋友出去吃饭",
        "content": "和朋友出去吃饭\n非让我帮他拍几张\n他最近迷上正装了\n#男生正装 #朋友穿搭"
    },
    # 简约风格
    {
        "title": "不说了",
        "content": "不说了\n今天穿这样\n#OOTD #正装"
    },
    {
        "title": "简单一身",
        "content": "简单一身\n出门办事\n#日常穿搭 #正装男"
    },
    {
        "title": "灰西装+白衬衫",
        "content": "灰西装+白衬衫\n永远不会出错\n#西装搭配 #男士穿搭"
    }
]

def get_images():
    """获取图片列表"""
    images = []
    if os.path.exists(IMAGE_DIR):
        for f in sorted(os.listdir(IMAGE_DIR)):
            if f.endswith(('.jpg', '.jpeg', '.png')):
                images.append(os.path.join(IMAGE_DIR, f))
    return images

def select_daily_scripts(count=3):
    """随机选择每日文案"""
    import random
    return random.sample(SCRIPTS, min(count, len(SCRIPTS)))

def generate_publish_guide():
    """生成发布指南"""
    images = get_images()
    scripts = select_daily_scripts()
    
    guide = f"""
# 蚁小二视频号发布指南 - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📋 今日发布内容

### 发布1️⃣
**文案：** {scripts[0]['title']}
```
{scripts[0]['content']}
```
**图片：** {os.path.basename(images[0]) if images else '无'}

---

### 发布2️⃣
**文案：** {scripts[1]['title']}
```
{scripts[1]['content']}
```
**图片：** {os.path.basename(images[1]) if len(images) > 1 else '无'}

---

### 发布3️⃣
**文案：** {scripts[2]['title']}
```
{scripts[2]['content']}
```
**图片：** {os.path.basename(images[2]) if len(images) > 2 else '无'}

---

## 🚀 发布步骤（蚁小二客户端）

1. 打开蚁小二客户端
2. 左侧菜单 → "发布" 或 "内容管理"
3. 点击"新建发布任务"
4. 选择平台：**微信视频号**
5. 选择账号：**你的视频号**
6. 上传图片：从 `{IMAGE_DIR}` 选择
7. 粘贴文案（上面的内容）
8. 点击"发布"或"定时发布"

## ⏰ 定时发布

- **发布1**：09:00
- **发布2**：12:00  
- **发布3**：18:00

## 📝 注意事项

- 文案已优化为真实日常风格
- 图片来自 Pexels（免费商用）
- 每条文案都包含相关话题标签
- 建议间隔3小时以上发布

---

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return guide

def main():
    """主函数"""
    print("=" * 60)
    print("🤵 蚁小二视频号发布指南生成器")
    print("=" * 60)
    
    # 生成指南
    guide = generate_publish_guide()
    
    # 保存到文件
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, f"publish_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print(guide)
    print(f"\n✅ 发布指南已保存到：{log_file}")

if __name__ == "__main__":
    main()

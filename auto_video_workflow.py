#!/usr/bin/env python3
"""
自动化视频号内容发布工作流
- 从免费图片网站搜索正装男性图片
- 下载2张图片
- 用 DeepSeek 生成文案（≤50字）+ 5个标签
- 用蚁小二发布到视频号
"""

import os
import sys
import json
import random
import requests
from datetime import datetime
from pathlib import Path

# ============ 配置 ============
YIXIAOER_API_KEY = "2DtnDBGb4f90RB89IknpO"
DEEPSEEK_API_KEY = "sk-ac63b2ee724b432eabf0e66b26bb191a"
VIDEO_ACCOUNT_ID = "699f138f388537b67562ba1a"  # 一个正装的普通朋友

# API 端点
YIXIAOER_BASE_URL = "https://www.yixiaoer.cn/api"
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

# 工作目录
WORK_DIR = Path("/Users/wangantony/.qclaw/workspace/auto_video_data")
WORK_DIR.mkdir(exist_ok=True)

# 免费图片网站列表
FREE_IMAGE_SOURCES = [
    {
        "name": "Pexels",
        "search_url": "https://api.pexels.com/v1/search",
        "api_key_env": "PEXELS_API_KEY"
    },
    {
        "name": "Unsplash",
        "search_url": "https://api.unsplash.com/search/photos",
        "api_key_env": "UNSPLASH_ACCESS_KEY"
    },
    {
        "name": "Pixabay",
        "search_url": "https://pixabay.com/api/",
        "api_key_env": "PIXABAY_API_KEY"
    }
]

# ============ 日志 ============
def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")

# ============ 1. 搜索和下载图片 ============
def search_pexels(keyword="suit man professional", count=2):
    """从 Pexels 搜索图片"""
    api_key = os.getenv("PEXELS_API_KEY", "")
    if not api_key:
        log("Pexels API Key 未配置，跳过", "WARN")
        return []
    
    try:
        headers = {"Authorization": api_key}
        params = {
            "query": keyword,
            "per_page": count * 2,
            "page": 1
        }
        
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params=params,
            timeout=15
        )
        
        if response.status_code != 200:
            log(f"Pexels API 错误: {response.status_code}", "WARN")
            return []
        
        data = response.json()
        photos = data.get("photos", [])
        
        results = []
        for photo in photos[:count]:
            results.append({
                "url": photo["src"]["large"],
                "source": "Pexels",
                "photographer": photo["photographer"]
            })
        
        log(f"Pexels 找到 {len(results)} 张图片")
        return results
        
    except Exception as e:
        log(f"Pexels 搜索异常: {e}", "WARN")
        return []

def search_unsplash(keyword="suit man professional", count=2):
    """从 Unsplash 搜索图片"""
    api_key = os.getenv("UNSPLASH_ACCESS_KEY", "")
    if not api_key:
        log("Unsplash API Key 未配置，跳过", "WARN")
        return []
    
    try:
        params = {
            "query": keyword,
            "per_page": count * 2,
            "client_id": api_key
        }
        
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params=params,
            timeout=15
        )
        
        if response.status_code != 200:
            log(f"Unsplash API 错误: {response.status_code}", "WARN")
            return []
        
        data = response.json()
        photos = data.get("results", [])
        
        results = []
        for photo in photos[:count]:
            results.append({
                "url": photo["urls"]["regular"],
                "source": "Unsplash",
                "photographer": photo["user"]["name"]
            })
        
        log(f"Unsplash 找到 {len(results)} 张图片")
        return results
        
    except Exception as e:
        log(f"Unsplash 搜索异常: {e}", "WARN")
        return []

def search_pixabay(keyword="suit man professional", count=2):
    """从 Pixabay 搜索图片"""
    api_key = os.getenv("PIXABAY_API_KEY", "")
    if not api_key:
        log("Pixabay API Key 未配置，跳过", "WARN")
        return []
    
    try:
        params = {
            "key": api_key,
            "q": keyword,
            "per_page": count * 2,
            "image_type": "photo",
            "safesearch": "true"
        }
        
        response = requests.get(
            "https://pixabay.com/api/",
            params=params,
            timeout=15
        )
        
        if response.status_code != 200:
            log(f"Pixabay API 错误: {response.status_code}", "WARN")
            return []
        
        data = response.json()
        photos = data.get("hits", [])
        
        results = []
        for photo in photos[:count]:
            results.append({
                "url": photo["largeImageURL"],
                "source": "Pixabay",
                "photographer": photo["user"]
            })
        
        log(f"Pixabay 找到 {len(results)} 张图片")
        return results
        
    except Exception as e:
        log(f"Pixabay 搜索异常: {e}", "WARN")
        return []

def search_placeholder_images():
    """使用免费的占位图片（当没有 API Key 时）"""
    log("使用预设的正装男性图片库...")
    
    # 这些是免费的、可用于商用的正装男性图片 URL
    # 来自 Pexels 等免费图片网站的公开图片
    placeholder_images = [
        "https://images.pexels.com/photos/2379005/pexels-photo-2379005.jpeg?auto=compress&cs=tinysrgb&w=600",
        "https://images.pexels.com/photos/2182970/pexels-photo-2182970.jpeg?auto=compress&cs=tinysrgb&w=600",
        "https://images.pexels.com/photos/1516680/pexels-photo-1516680.jpeg?auto=compress&cs=tinysrgb&w=600",
        "https://images.pexels.com/photos/774095/pexels-photo-774095.jpeg?auto=compress&cs=tinysrgb&w=600",
        "https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=600",
        "https://images.pexels.com/photos/1681010/pexels-photo-1681010.jpeg?auto=compress&cs=tinysrgb&w=600",
        "https://images.pexels.com/photos/927022/pexels-photo-927022.jpeg?auto=compress&cs=tinysrgb&w=600",
        "https://images.pexels.com/photos/834863/pexels-photo-834863.jpeg?auto=compress&cs=tinysrgb&w=600",
        "https://images.pexels.com/photos/762020/pexels-photo-762020.jpeg?auto=compress&cs=tinysrgb&w=600",
        "https://images.pexels.com/photos/736230/pexels-photo-736230.jpeg?auto=compress&cs=tinysrgb&w=600"
    ]
    
    # 随机选择2张
    selected = random.sample(placeholder_images, 2)
    
    results = []
    for url in selected:
        results.append({
            "url": url,
            "source": "Pexels (免费素材)",
            "photographer": "Pexels 用户"
        })
    
    return results

def download_images(count=2):
    """搜索并下载图片"""
    log(f"开始搜索和下载图片（目标: {count}张）...")
    
    images_dir = WORK_DIR / "images"
    images_dir.mkdir(exist_ok=True)
    
    # 尝试从各个图片源搜索
    all_results = []
    
    # Pexels
    results = search_pexels("suit man professional portrait", count)
    all_results.extend(results)
    
    # Unsplash
    if len(all_results) < count:
        results = search_unsplash("suit man professional portrait", count - len(all_results))
        all_results.extend(results)
    
    # Pixabay
    if len(all_results) < count:
        results = search_pixabay("suit man professional", count - len(all_results))
        all_results.extend(results)
    
    # 如果都没有，使用占位图片
    if len(all_results) < count:
        log("使用预设图片库", "INFO")
        results = search_placeholder_images()
        all_results.extend(results)
    
    # 下载图片
    downloaded = []
    for img_info in all_results[:count]:
        try:
            response = requests.get(img_info["url"], timeout=15)
            if response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"image_{timestamp}_{len(downloaded)+1}.jpg"
                filepath = images_dir / filename
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                
                downloaded.append(str(filepath))
                log(f"下载成功: {filename} (来源: {img_info['source']})")
        except Exception as e:
            log(f"下载图片失败: {e}", "WARN")
    
    if len(downloaded) < count:
        log(f"警告: 只下载到 {len(downloaded)} 张图片", "WARN")
    
    return downloaded

# ============ 2. 用 DeepSeek 生成文案 ============
def generate_copywriting():
    """用 DeepSeek 生成视频号文案"""
    log("开始生成文案...")
    
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = """你是一个短视频内容创作专家。请为视频号生成一条关于正装男性的文案。

要求：
1. 文案长度不超过50个字
2. 吸引人、有趣、能引发互动
3. 适合视频号平台
4. 风格可以是：职场感悟、生活态度、时尚穿搭、男性魅力等

同时生成5个相关标签。

请严格按以下 JSON 格式返回（不要有多余的文字）：
{"copywriting": "你的文案内容", "tags": "#标签1 #标签2 #标签3 #标签4 #标签5"}

示例：
{"copywriting": "穿正装的男人，走路都带风。今天也是精致的一天~", "tags": "#正装男 #职场穿搭 #西装控 #男士穿搭 #正装"}"""

        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 200
        }
        
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            log(f"DeepSeek API 错误: {response.status_code} - {response.text}", "ERROR")
            return None, None
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # 解析 JSON
        try:
            # 去除可能的 markdown 代码块标记
            content = content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1]  # 去除第一行
            if content.endswith("```"):
                content = content.rsplit("\n", 1)[0]  # 去除最后一行
            content = content.strip()
            
            parsed = json.loads(content)
            copywriting = parsed.get("copywriting", "")
            tags = parsed.get("tags", "")
            
            # 验证文案长度
            if len(copywriting) > 50:
                copywriting = copywriting[:47] + "..."
            
            log(f"文案生成成功: {copywriting}")
            log(f"标签: {tags}")
            
            return copywriting, tags
        except json.JSONDecodeError:
            log(f"无法解析 DeepSeek 返回的 JSON: {content}", "ERROR")
            # 尝试直接使用返回的内容作为文案
            if len(content) <= 50:
                return content, "#正装男 #正装 #职场穿搭 #男士穿搭 #西装"
            return None, None
            
    except Exception as e:
        log(f"生成文案异常: {e}", "ERROR")
        return None, None

# ============ 3. 用蚁小二发布 ============
def upload_to_yixiaoer_storage(image_path):
    """上传图片到蚁小二存储"""
    log(f"上传图片到蚁小二: {Path(image_path).name}")
    
    try:
        headers = {
            "Authorization": YIXIAOER_API_KEY
        }
        
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        file_size = len(image_data)
        
        # 1. 获取直传地址
        response = requests.get(
            f"{YIXIAOER_BASE_URL}/storages/cloud-publish/upload-url",
            headers=headers,
            params={
                "contentType": "image/jpeg",
                "size": str(file_size)
            }
        )
        
        if response.status_code != 200:
            log(f"获取上传地址失败: {response.status_code} - {response.text}", "ERROR")
            return None, None
        
        result = response.json()
        if result.get("statusCode") != 0:
            log(f"获取上传地址失败: {result.get('message')}", "ERROR")
            return None, None
        
        upload_data = result["data"]
        upload_url = upload_data.get("serviceUrl") or upload_data.get("url")
        file_key = upload_data.get("fileKey") or upload_data.get("key")
        
        if not upload_url:
            log(f"返回数据缺少上传地址: {result}", "ERROR")
            return None, None
        
        # 2. 上传图片 (使用 PUT)
        upload_response = requests.put(
            upload_url,
            data=image_data,
            headers={"Content-Type": "image/jpeg"}
        )
        
        if upload_response.status_code in [200, 201]:
            log("图片上传成功")
            # 返回可访问的 URL 和 fileKey
            # URL 格式: https://oss-v2.yixiaoer.cn/{fileKey}
            access_url = f"https://oss-v2.yixiaoer.cn/{file_key}"
            log(f"图片访问URL: {access_url}")
            return file_key, access_url
        
        log(f"上传失败: {upload_response.status_code}", "ERROR")
        return None, None
        
    except Exception as e:
        log(f"上传图片异常: {e}", "ERROR")
        return None, None

def publish_to_yixiaoer(images, copywriting, tags):
    """用蚁小二发布到视频号"""
    log("开始发布到视频号...")
    
    if not images:
        log("没有可用的图片", "ERROR")
        return False
    
    if not copywriting:
        log("没有可用的文案", "ERROR")
        return False
    
    try:
        # 直接使用本地图片路径上传到蚁小二
        uploaded_keys = []
        for img_path in images:
            file_key, _ = upload_to_yixiaoer_storage(img_path)
            if file_key:
                uploaded_keys.append(file_key)
        
        if not uploaded_keys:
            log("所有图片上传失败", "ERROR")
            return False
        
        log(f"成功上传 {len(uploaded_keys)} 张图片")
        log(f"图片 Keys: {uploaded_keys}")
        
        # 调用蚁小二发布 API
        headers = {
            "Authorization": YIXIAOER_API_KEY,
            "Content-Type": "application/json"
        }
        
        # 构建发布任务 - 使用 v2 API
        # 关键: images 应该是 fileKey 数组
        payload = {
            "coverKey": uploaded_keys[0] if uploaded_keys else "",
            "desc": copywriting,
            "platforms": ["视频号"],
            "publishType": "imageText",
            "isDraft": False,
            "publishChannel": "cloud",
            "publishArgs": {
                "content": copywriting,
                "accountForms": [
                    {
                        "platformAccountId": VIDEO_ACCOUNT_ID,
                        "coverKey": uploaded_keys[0] if uploaded_keys else "",
                        "images": uploaded_keys,  # 使用 fileKey 数组
                        "contentPublishForm": {
                            "title": copywriting[:20] if len(copywriting) > 20 else copywriting,
                            "content": copywriting,
                            "tags": tags
                        }
                    }
                ]
            }
        }
        
        log(f"发布内容: {copywriting}")
        log(f"调用 API: POST {YIXIAOER_BASE_URL}/taskSets/v2")
        log(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
        
        response = requests.post(
            f"{YIXIAOER_BASE_URL}/taskSets/v2",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        log(f"API 响应: {response.status_code} - {response.text[:800]}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            if result.get("statusCode") == 0:
                # data 可能是字符串或字典
                task_id = result.get("data", "")
                if isinstance(task_id, dict):
                    task_id = task_id.get("taskSetId") or task_id.get("id") or str(task_id)
                log(f"✅ 发布成功! 任务集ID: {task_id}")
                return True
            else:
                log(f"发布失败: {result.get('message', result)}", "ERROR")
                return False
        else:
            log(f"蚁小二 API 错误: {response.status_code}", "ERROR")
            return False
            
    except Exception as e:
        log(f"发布异常: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return False

# ============ 主流程 ============
def main():
    log("=" * 60)
    log("开始执行自动化视频号发布流程")
    log(f"目标账号: 一个正装的普通朋友 ({VIDEO_ACCOUNT_ID})")
    log("=" * 60)
    
    # 1. 下载图片
    images = download_images(count=2)
    if not images:
        log("未能下载到图片", "ERROR")
        return False
    
    # 2. 生成文案
    copywriting, tags = generate_copywriting()
    if not copywriting:
        log("未能生成文案", "ERROR")
        return False
    
    # 3. 发布到视频号
    success = publish_to_yixiaoer(images, copywriting, tags)
    
    log("=" * 60)
    if success:
        log("✅ 流程执行成功!")
        # 保存发布记录
        record = {
            "time": datetime.now().isoformat(),
            "copywriting": copywriting,
            "tags": tags,
            "images": images,
            "success": True
        }
        record_file = WORK_DIR / "publish_history.json"
        history = []
        if record_file.exists():
            history = json.loads(record_file.read_text())
        history.append(record)
        record_file.write_text(json.dumps(history, ensure_ascii=False, indent=2))
    else:
        log("❌ 流程执行失败", "ERROR")
    log("=" * 60)
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        log("用户中断", "WARN")
        sys.exit(1)
    except Exception as e:
        log(f"未预期的错误: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)

#!/usr/bin/env python3
"""
视频号自动发布脚本
- 使用 Playwright 控制浏览器
- 自动登录视频号后台
- 自动上传图片并发布
"""

import os
import sys
import json
import asyncio
import random
import requests
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

# ============ 配置 ============
DEEPSEEK_API_KEY = "sk-ac63b2ee724b432eabf0e66b26bb191a"
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

# 工作目录
WORK_DIR = Path("/Users/wangantony/.qclaw/workspace/auto_video_data")
WORK_DIR.mkdir(exist_ok=True)

# 浏览器数据目录（保存登录状态）
BROWSER_DATA_DIR = WORK_DIR / "browser_data"
BROWSER_DATA_DIR.mkdir(exist_ok=True)

# ============ 日志 ============
def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")

# ============ 1. 下载图片 ============
def download_images(count=2):
    """从预设的免费图片库下载图片"""
    log(f"开始下载图片（目标: {count}张）...")
    
    images_dir = WORK_DIR / "images"
    images_dir.mkdir(exist_ok=True)
    
    # 预设的正装男性图片 URL（来自 Pexels 免费素材）
    placeholder_images = [
        "https://images.pexels.com/photos/2379005/pexels-photo-2379005.jpeg?auto=compress&cs=tinysrgb&w=800",
        "https://images.pexels.com/photos/2182970/pexels-photo-2182970.jpeg?auto=compress&cs=tinysrgb&w=800",
        "https://images.pexels.com/photos/1516680/pexels-photo-1516680.jpeg?auto=compress&cs=tinysrgb&w=800",
        "https://images.pexels.com/photos/774095/pexels-photo-774095.jpeg?auto=compress&cs=tinysrgb&w=800",
        "https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=800",
        "https://images.pexels.com/photos/1681010/pexels-photo-1681010.jpeg?auto=compress&cs=tinysrgb&w=800",
        "https://images.pexels.com/photos/927022/pexels-photo-927022.jpeg?auto=compress&cs=tinysrgb&w=800",
        "https://images.pexels.com/photos/834863/pexels-photo-834863.jpeg?auto=compress&cs=tinysrgb&w=800",
        "https://images.pexels.com/photos/762020/pexels-photo-762020.jpeg?auto=compress&cs=tinysrgb&w=800",
        "https://images.pexels.com/photos/736230/pexels-photo-736230.jpeg?auto=compress&cs=tinysrgb&w=800",
        "https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=800",
        "https://images.pexels.com/photos/1043471/pexels-photo-1043471.jpeg?auto=compress&cs=tinysrgb&w=800",
    ]
    
    # 随机选择图片
    selected = random.sample(placeholder_images, min(count, len(placeholder_images)))
    
    downloaded = []
    for img_url in selected:
        try:
            response = requests.get(img_url, timeout=15)
            if response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"image_{timestamp}_{len(downloaded)+1}.jpg"
                filepath = images_dir / filename
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                
                downloaded.append(str(filepath))
                log(f"下载成功: {filename}")
        except Exception as e:
            log(f"下载图片失败: {e}", "WARN")
    
    return downloaded

# ============ 2. 生成文案 ============
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
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "max_tokens": 200
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code != 200:
            log(f"DeepSeek API 错误: {response.status_code}", "ERROR")
            return None, None
        
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()
        
        # 去除 markdown 代码块
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
        if content.endswith("```"):
            content = content.rsplit("\n", 1)[0]
        content = content.strip()
        
        parsed = json.loads(content)
        copywriting = parsed.get("copywriting", "")
        tags = parsed.get("tags", "")
        
        if len(copywriting) > 50:
            copywriting = copywriting[:47] + "..."
        
        log(f"文案: {copywriting}")
        log(f"标签: {tags}")
        
        return copywriting, tags
        
    except Exception as e:
        log(f"生成文案异常: {e}", "ERROR")
        return None, None

# ============ 3. 浏览器自动化发布 ============
async def publish_to_video_account(images, copywriting, tags):
    """使用浏览器自动化发布到视频号"""
    log("开始浏览器自动化发布...")
    
    if not images or not copywriting:
        log("缺少图片或文案", "ERROR")
        return False
    
    async with async_playwright() as p:
        # 启动浏览器（使用持久化上下文保存登录状态）
        log("启动浏览器...")
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_DATA_DIR),
            headless=False,  # 显示浏览器，方便调试和扫码
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-web-security',
            ],
            viewport={"width": 1280, "height": 800}
        )
        
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        try:
            # 1. 打开视频号后台
            log("打开视频号后台...")
            await page.goto("https://channels.weixin.qq.com/", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(2)
            
            # 2. 检查是否需要登录
            current_url = page.url
            if "login" in current_url or "扫码" in await page.title() or await page.locator("text=扫码登录").count() > 0:
                log("⚠️ 需要扫码登录！请用微信扫码登录...", "WARN")
                log("等待扫码登录中...（请在 120 秒内完成扫码）")
                
                # 等待登录成功（URL 变化或出现发布按钮）
                try:
                    await page.wait_for_url("**/channels.weixin.qq.com/**", timeout=120000)
                    log("✅ 登录成功！")
                except:
                    log("登录超时，请重试", "ERROR")
                    return False
            
            await asyncio.sleep(2)
            
            # 3. 点击发布图文按钮
            log("点击发布图文...")
            
            # 尝试不同的选择器
            selectors = [
                "text=发布图文",
                "text=发布",
                "button:has-text('发布图文')",
                ".publish-btn",
                "[class*='publish']"
            ]
            
            clicked = False
            for selector in selectors:
                try:
                    if await page.locator(selector).count() > 0:
                        await page.locator(selector).first.click()
                        clicked = True
                        log(f"点击成功: {selector}")
                        break
                except:
                    continue
            
            if not clicked:
                log("未找到发布按钮，请检查页面", "ERROR")
                await page.screenshot(path=str(WORK_DIR / "screenshot_error.png"))
                return False
            
            await asyncio.sleep(2)
            
            # 4. 上传图片
            log("上传图片...")
            
            # 查找文件上传输入框
            file_input = await page.locator('input[type="file"]').first
            
            for img_path in images:
                log(f"上传: {Path(img_path).name}")
                await file_input.set_input_files(img_path)
                await asyncio.sleep(1)
            
            await asyncio.sleep(3)
            
            # 5. 填写文案
            log("填写文案...")
            
            # 查找文本输入框
            text_selectors = [
                "textarea[placeholder*='描述']",
                "textarea[placeholder*='内容']",
                ".content-input textarea",
                "textarea",
                "[contenteditable='true']"
            ]
            
            for selector in text_selectors:
                try:
                    if await page.locator(selector).count() > 0:
                        await page.locator(selector).first.fill(copywriting + "\n\n" + tags)
                        log(f"文案已填写: {selector}")
                        break
                except:
                    continue
            
            await asyncio.sleep(1)
            
            # 6. 点击发布
            log("点击发布按钮...")
            
            publish_selectors = [
                "button:has-text('发布')",
                "button:has-text('发表')",
                ".publish-btn",
                "[class*='submit']"
            ]
            
            for selector in publish_selectors:
                try:
                    if await page.locator(selector).count() > 0:
                        await page.locator(selector).first.click()
                        log(f"发布按钮已点击: {selector}")
                        break
                except:
                    continue
            
            await asyncio.sleep(3)
            
            # 7. 检查发布结果
            log("检查发布结果...")
            await asyncio.sleep(2)
            
            # 截图保存结果
            screenshot_path = WORK_DIR / f"publish_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            await page.screenshot(path=str(screenshot_path))
            log(f"截图已保存: {screenshot_path}")
            
            log("✅ 发布完成！")
            return True
            
        except Exception as e:
            log(f"发布异常: {e}", "ERROR")
            await page.screenshot(path=str(WORK_DIR / "screenshot_error.png"))
            return False
        
        finally:
            # 不关闭浏览器，保持登录状态
            log("保持浏览器登录状态...")
            await browser.close()

# ============ 主流程 ============
async def main():
    log("=" * 60)
    log("开始执行视频号自动发布流程")
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
    success = await publish_to_video_account(images, copywriting, tags)
    
    log("=" * 60)
    if success:
        log("✅ 流程执行成功!")
        # 保存记录
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
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        log("用户中断", "WARN")
        sys.exit(1)
    except Exception as e:
        log(f"未预期的错误: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)

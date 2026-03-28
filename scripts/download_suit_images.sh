#!/bin/bash
# 正装男士图片下载脚本 - 不看头像
# 使用 Unsplash 免费图片

mkdir -p /Users/wangantony/.qclaw/workspace/images/suits

cd /Users/wangantony/.qclaw/workspace/images/suits

# 下载正装男士背影/侧影/不露脸图片
echo "正在下载正装男士图片..."

# 图片1: 西装背影
curl -L -o suit_01.jpg "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&q=80" 2>/dev/null

# 图片2: 西装侧影
curl -L -o suit_02.jpg "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=800&q=80" 2>/dev/null

# 图片3: 西装细节
curl -L -o suit_03.jpg "https://images.unsplash.com/photo-1593030761757-71fae45fa0e7?w=800&q=80" 2>/dev/null

# 图片4: 商务穿搭
curl -L -o suit_04.jpg "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=800&q=80" 2>/dev/null

# 图片5: 正装背影
curl -L -o suit_05.jpg "https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?w=800&q=80" 2>/dev/null

# 图片6: 西装外套
curl -L -o suit_06.jpg "https://images.unsplash.com/photo-1592878904946-b3cd8ae243d0?w=800&q=80" 2>/dev/null

echo "下载完成！"
ls -la *.jpg 2>/dev/null || echo "需要检查下载结果"

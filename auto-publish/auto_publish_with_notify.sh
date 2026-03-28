#!/bin/bash
# 自动发布脚本 - 带微信通知

# 执行发布脚本
python3 ~/.qclaw/workspace/auto-publish/auto_publish.py > /tmp/publish_output.txt 2>&1

# 获取执行结果
OUTPUT=$(cat /tmp/publish_output.txt)

# 提取关键信息
TITLE=$(echo "$OUTPUT" | grep "标题:" | head -1 | sed 's/.*标题: //')
XHS_STATUS=$(echo "$OUTPUT" | grep "小红书发布" | tail -1)
TT_STATUS=$(echo "$OUTPUT" | grep "头条号发布" | tail -1)

# 构建微信消息
if echo "$OUTPUT" | grep -q "✅.*发布成功"; then
    MESSAGE="✅ 笔记发布成功！

📱 标题：$TITLE

$XHS_STATUS
$TT_STATUS

时间：$(date '+%Y-%m-%d %H:%M:%S')"
else
    MESSAGE="❌ 笔记发布失败

$OUTPUT

时间：$(date '+%Y-%m-%d %H:%M:%S')"
fi

# 发送微信通知
echo "$MESSAGE"

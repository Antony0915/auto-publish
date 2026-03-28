#!/bin/bash
# 自动发布脚本 - 纯 Bash 版本（改进版）

# 配置
YIXIAOER_API_KEY="2DtnDBGb4f90RB89IknpO"
DOUBAO_API_KEY="40917d42-b88d-4e86-97df-368bb4aeba4f"
DOUBAO_MODEL="doubao-seed-1-8-251228"

LOG_FILE="$HOME/.qclaw/workspace/auto-publish/publish.log"
IMAGE_USED_FILE="$HOME/.qclaw/workspace/auto-publish/images_used.json"
CONTENT_FILE="/tmp/generated_content_$$.txt"

echo "========================================" | tee -a $LOG_FILE
echo "开始执行发布任务 - $(date '+%Y-%m-%d %H:%M:%S')" | tee -a $LOG_FILE
echo "========================================" | tee -a $LOG_FILE

# 1. 获取素材图片列表
echo "🖼️ 获取素材图片..." | tee -a $LOG_FILE

MATERIALS=$(curl -s -X GET "https://www.yixiaoer.cn/api/material?page=1&size=50" \
  -H "Authorization: $YIXIAOER_API_KEY" \
  -H "Content-Type: application/json")

# 提取所有图片ID
ALL_IDS=$(echo "$MATERIALS" | grep -o '"id":"[^"]*"' | sed 's/"id":"//;s/"//' | head -20)

# 读取已使用的图片
if [ -f "$IMAGE_USED_FILE" ]; then
    USED_COUNT=$(wc -c < "$IMAGE_USED_FILE")
    if [ "$USED_COUNT" -gt 2 ]; then
        USED_IDS=$(cat "$IMAGE_USED_FILE")
    else
        USED_IDS=""
    fi
else
    USED_IDS=""
fi

# 找第一张未使用的图片
SELECTED_IMAGE=""
for img_id in $ALL_IDS; do
    if ! echo "$USED_IDS" | grep -q "$img_id"; then
        SELECTED_IMAGE="$img_id"
        break
    fi
done

# 如果都用了就用第一张
if [ -z "$SELECTED_IMAGE" ]; then
    SELECTED_IMAGE=$(echo "$ALL_IDS" | head -1)
fi

if [ -z "$SELECTED_IMAGE" ]; then
    echo "❌ 获取图片失败" | tee -a $LOG_FILE
    exit 1
fi

# 获取选中图片信息
IMAGE_PATH=$(echo "$MATERIALS" | grep "$SELECTED_IMAGE" | sed -n 's/.*"filePath": *"\([^"]*\)".*/\1/p' | head -1)
IMAGE_NAME=$(echo "$MATERIALS" | grep "$SELECTED_IMAGE" | sed -n 's/.*"fileName": *"\([^"]*\)".*/\1/p' | head -1)
IMAGE_KEY=$(echo "$MATERIALS" | grep "$SELECTED_IMAGE" | sed -n 's/.*"fileKey": *"\([^"]*\)".*/\1/p' | head -1)

echo "   使用图片: $IMAGE_NAME (ID: $SELECTED_IMAGE)" | tee -a $LOG_FILE

# 更新已使用记录
echo "$SELECTED_IMAGE" >> "$IMAGE_USED_FILE"

# 2. 生成内容
echo "📝 调用豆包生成文案..." | tee -a $LOG_FILE

PROMPT_TEXT="请为以下主题生成一篇适合小红书和头条号发布的笔记文案：
主题：40+中年男人的职场、健身、心理、成长

要求：
1. 语言风格：自然、真实、有温度，像一个40+成熟男性分享生活
2. 小红书：轻松活泼，加一些表情，适合年轻人看
3. 头条号：正式一些，干货为主
4. 字数：小红书100-300字，头条号300-500字
5. 包含合适的标签

请生成两个版本的文案：
【小红书版】- 小红书风格（活泼、表情）

【头条版】- 头条号风格（正式、干货）

只输出文案内容。"

# 写入临时文件
TEMP_JSON="/tmp/doubao_request_$$.json"
cat > "$TEMP_JSON" << EOF
{
  "model": "${DOUBAO_MODEL}",
  "input": [
    {
      "role": "user",
      "content": [{"type": "input_text", "text": "${PROMPT_TEXT}"}]
    }
  ]
}
EOF

DOUBAO_RESPONSE=$(curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/responses" \
  -H "Authorization: Bearer $DOUBAO_API_KEY" \
  -H "Content-Type: application/json" \
  -d @"$TEMP_JSON" 2>&1)

# 提取生成的内容（改进版）
GENERATED_CONTENT=$(echo "$DOUBAO_RESPONSE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    output = data.get('output', [])
    for item in output:
        if item.get('type') == 'message':
            content_list = item.get('content', [])
            for c in content_list:
                if c.get('type') == 'output_text':
                    print(c.get('text', ''))
except:
    pass
" 2>/dev/null)

if [ -z "$GENERATED_CONTENT" ]; then
    echo "❌ 生成内容失败" | tee -a $LOG_FILE
    echo "$DOUBAO_RESPONSE" | head -c 500 | tee -a $LOG_FILE
    exit 1
fi

echo "   ✅ 内容生成成功" | tee -a $LOG_FILE

# 保存内容到文件便于调试
echo "$GENERATED_CONTENT" > "$CONTENT_FILE"

# 提取标题（取第一行）
TITLE=$(echo "$GENERATED_CONTENT" | head -1 | cut -c1-50)
echo "   标题: $TITLE" | tee -a $LOG_FILE

# 提取小红书版本
BODY_XHS=$(echo "$GENERATED_CONTENT" | sed -n '/【小红书版】/,/【头条版】/p' | sed '1d;$d' | head -c 800)

# 提取头条版本
BODY_TT=$(echo "$GENERATED_CONTENT" | sed -n '/【头条版】/,$p' | sed '1d' | head -c 800)

# 如果提取失败，用整个内容
if [ -z "$BODY_XHS" ]; then
    BODY_XHS=$(echo "$GENERATED_CONTENT" | head -c 400)
fi

if [ -z "$BODY_TT" ]; then
    BODY_TT=$(echo "$GENERATED_CONTENT" | tail -c 400)
fi

# 3. 发布到小红书
echo "" | tee -a $LOG_FILE
echo "📤 发布到 小红书..." | tee -a $LOG_FILE

XHS_PUBLISH=$(curl -s -X POST "https://www.yixiaoer.cn/api/taskSets/v2" \
  -H "Authorization: $YIXIAOER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"platforms\": [\"小红书\"],
    \"publishType\": \"imageText\",
    \"isDraft\": false,
    \"publishChannel\": \"cloud\",
    \"coverKey\": \"$IMAGE_KEY\",
    \"desc\": \"$TITLE\",
    \"publishArgs\": {
      \"accountForms\": [
        {
          \"platformAccountId\": \"694c788c22f9fa4f9cfa4fa2\",
          \"contentPublishForm\": {
            \"title\": \"$TITLE\",
            \"text\": \"$BODY_XHS\",
            \"images\": [\"$IMAGE_PATH\"]
          }
        }
      ],
      \"content\": \"$BODY_XHS\"
    }
  }" 2>&1)

if echo "$XHS_PUBLISH" | grep -q '"statusCode":0'; then
    echo "   ✅ 小红书发布成功!" | tee -a $LOG_FILE
else
    echo "   ❌ 小红书发布失败" | tee -a $LOG_FILE
    echo "   $XHS_PUBLISH" | head -c 200 | tee -a $LOG_FILE
fi

# 4. 发布到头条号
echo "" | tee -a $LOG_FILE
echo "📤 发布到 头条号..." | tee -a $LOG_FILE

TT_PUBLISH=$(curl -s -X POST "https://www.yixiaoer.cn/api/taskSets/v2" \
  -H "Authorization: $YIXIAOER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"platforms\": [\"头条号\"],
    \"publishType\": \"imageText\",
    \"isDraft\": false,
    \"publishChannel\": \"cloud\",
    \"coverKey\": \"$IMAGE_KEY\",
    \"desc\": \"$TITLE\",
    \"publishArgs\": {
      \"accountForms\": [
        {
          \"platformAccountId\": \"692438d83b864e9db2b7b61a\",
          \"contentPublishForm\": {
            \"title\": \"$TITLE\",
            \"text\": \"$BODY_TT\",
            \"images\": [\"$IMAGE_PATH\"]
          }
        }
      ],
      \"content\": \"$BODY_TT\"
    }
  }" 2>&1)

if echo "$TT_PUBLISH" | grep -q '"statusCode":0'; then
    echo "   ✅ 头条号发布成功!" | tee -a $LOG_FILE
else
    echo "   ❌ 头条号发布失败" | tee -a $LOG_FILE
    echo "   $TT_PUBLISH" | head -c 200 | tee -a $LOG_FILE
fi

echo "" | tee -a $LOG_FILE
echo "========================================" | tee -a $LOG_FILE
echo "发布任务完成 - $(date '+%Y-%m-%d %H:%M:%S')" | tee -a $LOG_FILE
echo "========================================" | tee -a $LOG_FILE

# 清理临时文件
rm -f "$TEMP_JSON" "$CONTENT_FILE"
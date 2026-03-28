#!/bin/bash
# 自动发布脚本 - 直接执行版

cd ~/.qclaw/workspace

echo "========================================"
echo "自动发布任务 - $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# 根据当前时间判断执行哪个任务
HOUR=$(date +%H)

if [ "$HOUR" -ge 7 ] && [ "$HOUR" -lt 12 ]; then
    echo "📌 早间任务"
    echo ""
    echo "1️⃣ 万金油大叔..."
    python3 auto-publish/auto_publish.py
    echo ""
    echo "2️⃣ 心理疗愈..."
    python3 auto-publish/xl_publish.py
elif [ "$HOUR" -ge 12 ] && [ "$HOUR" -lt 18 ]; then
    echo "📌 午间任务"
    echo ""
    echo "1️⃣ 万金油大叔..."
    python3 auto-publish/auto_publish.py
    echo ""
    echo "2️⃣ 心理疗愈..."
    python3 auto-publish/xl_publish.py
    echo ""
    echo "3️⃣ 希腊简报..."
    python3 scripts/greek_daily_email.py
else
    echo "📌 晚间任务"
    echo ""
    echo "1️⃣ 万金油大叔..."
    python3 auto-publish/auto_publish.py
    echo ""
    echo "2️⃣ 心理疗愈..."
    python3 auto-publish/xl_publish.py
fi

echo ""
echo "========================================"
echo "任务完成 - $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

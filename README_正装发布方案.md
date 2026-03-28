# 正装男士视频号自动发布方案

## 📁 项目结构

```
~/.qclaw/workspace/
├── images/suits/          # 正装男士图片库
│   ├── suit_01.jpg
│   ├── suit_02.jpg
│   └── ...
├── content/
│   └── suit_video_scripts.md   # 文案库
├── config/
│   └── yixiaoer_config.json    # 配置文件
├── scripts/
│   ├── download_suit_images.sh  # 图片下载脚本
│   └── publish_suit_daily.py    # 自动发布脚本
└── logs/
    └── daily_publish_*.log      # 发布日志
```

## ⚙️ 配置步骤

### 1. 获取蚁小二 API Key

1. 登录蚁小二官网: https://www.yixiaoer.cn
2. 进入「设置」→「API接口」
3. 生成并复制 API Key
4. 确保团队已开通 VIP 功能

### 2. 获取视频号账号ID

1. 在蚁小二中绑定视频号账号
2. 进入「账号管理」
3. 复制视频号账号ID

### 3. 更新配置文件

编辑 `config/yixiaoer_config.json`:

```json
{
  "yixiaoer_api_key": "替换为你的API Key",
  "video_account_id": "替换为你的视频号账号ID"
}
```

### 4. 测试发布

```bash
python3 /Users/wangantony/.qclaw/workspace/scripts/publish_suit_daily.py
```

## ⏰ 定时任务

已设置每天 **9:00、12:00、18:00** 自动发布3条内容

查看定时任务状态：
- 任务ID: `03b8a675-3f64-41c0-b4ce-d7dc00de6e63`
- 下次执行: 2025-03-26 18:00 (GMT+8)

## 📝 文案库

包含4大风格：
- 商务精英风
- 生活品味风
- 励志成长风
- 季节搭配风

每天随机选择3条不同风格发布

## 🔄 日常维护

### 添加新图片
```bash
# 下载更多图片
curl -L -o ~/.qclaw/workspace/images/suits/suit_new.jpg "图片URL"
```

### 添加新文案
编辑 `content/suit_video_scripts.md`

### 查看发布日志
```bash
cat ~/.qclaw/workspace/logs/daily_publish_*.log
```

## ⚠️ 注意事项

1. 确保蚁小二账号已开通 VIP
2. 视频号需要先在蚁小二中绑定
3. 图片使用前请确认版权（Unsplash 可免费商用）
4. 如遇发布失败，检查 API Key 是否过期

## 📊 后续优化建议

1. **数据追踪**: 记录每条内容的播放量、点赞、转发数据
2. **A/B测试**: 对比不同风格文案的效果
3. **图片更新**: 定期补充新图片避免重复
4. **热点结合**: 结合节日、季节调整文案主题

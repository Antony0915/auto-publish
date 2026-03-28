# 蚁小二视频号绑定指南

## 📋 绑定步骤

### 第一步：登录蚁小二后台
1. 访问 https://www.yixiaoer.cn
2. 点击右上角"进入后台"
3. 用你的账号登录（手机号/邮箱）

### 第二步：进入账号管理
1. 登录后进入后台首页
2. 左侧菜单找到"账号管理"或"账号中心"
3. 点击"添加账号"或"绑定账号"

### 第三步：选择视频号平台
1. 在平台列表中选择"微信视频号"
2. 点击"授权"或"绑定"

### 第四步：微信授权
1. 会弹出微信二维码
2. 用你的微信扫描二维码
3. 在微信中确认授权
4. 选择要绑定的视频号账号

### 第五步：完成绑定
1. 授权成功后，视频号会显示在账号列表中
2. 记下视频号的"账号ID"（后面发布时需要用）

---

## 🔑 获取 API Key

### 方式1：在后台生成
1. 登录蚁小二后台
2. 进入"设置" → "API接口"
3. 点击"生成API Key"
4. 复制 API Key

### 方式2：联系客服
- 蚁小二客服电话：400-xxx-xxxx
- 官网右下角有在线客服

---

## 📝 配置文件更新

绑定完成后，编辑配置文件：

```bash
nano ~/.qclaw/workspace/config/yixiaoer_config.json
```

填入：
```json
{
  "yixiaoer_api_key": "你的API Key",
  "video_account_id": "你的视频号账号ID",
  "publish_times": ["09:00", "12:00", "18:00"],
  "daily_count": 3,
  "image_dir": "/Users/wangantony/.qclaw/workspace/images/real_suit",
  "log_dir": "/Users/wangantony/.qclaw/workspace/logs"
}
```

---

## ✅ 验证绑定

配置完成后，运行测试：

```bash
python3 ~/.qclaw/workspace/scripts/publish_suit_daily.py
```

如果输出：
```
✅ 团队: xxx
✅ VIP状态: 已开通
✅ 找到 8 张图片
✅ 已选择 3 条文案
```

说明绑定成功！

---

## ⚠️ 常见问题

### Q: 找不到"账号管理"菜单？
A: 可能是版本不同，试试找"账号中心"或"我的账号"

### Q: 微信授权失败？
A: 
- 确保用的是个人微信（不是企业号）
- 视频号需要已激活
- 试试用另一个浏览器

### Q: API Key 生成失败？
A: 
- 确保账号已开通 VIP
- 联系蚁小二客服

### Q: 发布时提示"账号ID错误"？
A: 
- 检查 config.json 中的 video_account_id 是否正确
- 可以在后台账号列表中复制

---

## 📞 需要帮助？

完成绑定后，告诉我：
1. ✅ 视频号已绑定
2. ✅ API Key 已获取
3. ✅ config.json 已更新

然后我们就可以开始自动发布了！

# 自动发布系统 - GitHub Actions 24/7 运行

社媒自动发布 + 希腊小报，每天 9 个定时任务，全部由 GitHub Actions 自动执行。

## 📅 发布时间表

| 时间 | 任务 | 平台 |
|------|------|------|
| **07:00** | 心理疗愈 - 中年男人的心理 | 小红书 |
| **07:30** | 心理疗愈 - 情绪管理 | 小红书 |
| **07:30** | 万金油大叔 - 积极生活篇 | 小红书+头条号 |
| **08:00** | 🇬🇷 希腊小报每日简报 | 邮件 |
| **12:30** | 心理疗愈 - 职场压力 | 小红书 |
| **19:30** | 万金油大叔 - 人生智慧篇 | 小红书+头条号 |
| **22:00** | 万金油大叔 - 走心的中年相关 | 小红书+头条号 |
| **22:30** | 心理疗愈 - 家庭情感 | 小红书 |
| **23:30** | 万金油大叔 - 温暖陪伴篇 | 小红书+头条号 |

## 🔧 配置 Secrets

在 GitHub 仓库设置中添加以下 Secrets：

1. **YIXIAOER_API_KEY** - 蚁小二 API Key
2. **DOUBAO_API_KEY** - 豆包 API Key  
3. **EMAIL_SMTP_PASSWORD** - QQ 邮箱授权码

## 📁 项目结构

```
.
├── auto-publish/
│   ├── xl_publish.py          # 心理疗愈发布脚本
│   ├── auto_publish.py        # 万金油大叔发布脚本
│   └── ...
├── scripts/
│   ├── greek_daily_email.py   # 希腊小报脚本
│   └── send_email.py          # 邮件发送工具
├── .github/workflows/         # GitHub Actions 工作流
│   ├── publish-psychology-*.yml
│   ├── publish-wanjinyou-*.yml
│   └── greek-newsletter.yml
└── README.md
```

## 🚀 使用

所有任务自动按时间表执行。也可以手动触发：

```bash
gh workflow run publish-psychology-0700.yml
```

## 📊 监控

在 GitHub Actions 标签页查看每次执行的日志和结果。

---

**最后更新**: 2026-03-28

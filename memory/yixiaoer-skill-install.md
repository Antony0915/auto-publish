# 蚁小二 (yixiaoer) Skill 安装指南

## Skill 能力总结

### 核心能力
1. **内容发布** - 一键发布到 60+ 自媒体平台
2. **账号数据查询** - 账号概览、作品数据
3. **批量发布** - 多账号、多任务批量发布
4. **素材管理** - 素材库上传/分组
5. **任务管理** - 任务集创建、发布追踪

### 支持平台（部分）
抖音、快手、小红书、B站、视频号、微博、知乎、头条号、百家号、YouTube、Twitter 等

### 技术信息
- **Base URL**: `https://www.yixiaoer.cn/api`
- **鉴权**: HTTP Header 中传 `Authorization: <apikey>`
- **要求**: 蚁小二 VIP 会员

## 安装问题

由于当前环境缺少必要工具（Homebrew、Node.js），无法自动安装。

## 手动安装步骤

### 步骤 1: 安装 Homebrew
在终端中运行：
```bash
/bin/bash -c "$(curl -fsSL https://mirrors.ustc.edu.cn/misc/brew-install.sh)"
```

### 步骤 2: 安装 Node.js
```bash
brew install node
```

### 步骤 3: 安装 ClawHub CLI
```bash
npm install -g clawhub
```

### 步骤 4: 安装 yixiaoer skill
```bash
clawhub install wangzj141/yixiaoer
```

或者直接克隆到 skills 目录：
```bash
git clone https://github.com/wangzj141/yixiaoer.git ~/.qclaw/skills/yixiaoer
```

## 配置

获取 API Key 后，在 openclaw.json 中配置：
```json
{
  "skills": {
    "entries": {
      "yixiaoer": {
        "env": {
          "YIXIAOER_API_KEY": "你的APIKey"
        }
      }
    }
  }
}
```

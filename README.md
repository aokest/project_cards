# Project Cards & Timeline Generator

这是一个基于 Web 的项目卡片及推进表生成器，旨在帮助项目经理快速创建标准化、美观的项目卡片，并自动生成项目推进时间表。

## 功能特性

- **项目卡片编辑器** (`cardv8.html`)
  - 现代化 UI，支持拖拽调整模块高度、自定义字体大小。
  - 内置 AI 润色功能（支持 OpenAI 格式接口），支持前后对比与撤销。
  - 支持 Markdown 文件批量导入。
  - 数据自动同步到本地数据库。
  - 导出为 JSON 或 Markdown。
  - **安全配置**：API Key 等敏感配置可导出为本地 JSON 文件，不上传云端。

- **项目列表** (`index.html`)
  - 概览所有项目卡片。
  - 支持启用/禁用卡片（控制是否显示在时间表中）。
  - 支持 Grid 和 List 两种视图。

- **项目推进表** (`project_timeline.html`)
  - 自动根据卡片中的“项目周期”生成甘特图/时间轴。
  - 支持手动微调时间，并同步回数据库。

## 快速开始

### 1. 启动服务

本项目使用 Python 内置服务器作为轻量级后端。

```bash
# 确保已安装 Python 3
python3 server.py
```

服务默认运行在 `http://localhost:18889`。

### 2. 访问页面

- **首页列表**: [http://localhost:18889/index.html](http://localhost:18889/index.html)
- **卡片编辑**: [http://localhost:18889/cardv8.html](http://localhost:18889/cardv8.html)
- **推进表**: [http://localhost:18889/project_timeline.html](http://localhost:18889/project_timeline.html)

## 数据存储

- 本地数据存储在 `project_cards.json`（已被 `.gitignore` 忽略，不会提交远端）。
- 测试/脱敏数据位于 `env/test/project_cards.json`（默认 `[]`），通过 `docker-compose.test.yml` 挂载到容器中。
- 请定期备份本地 `project_cards.json`。

## 配置管理

- AI 配置（Base URL, API Key）默认保存在浏览器 `localStorage` 中。
- 在“AI 设置”弹窗中，点击 **“导出配置”** 可将 Key 保存为本地 JSON 文件。
- 换机或清除缓存后，点击 **“导入配置”** 即可一键恢复。

## 目录结构

```
.
├── cardv8.html          # 卡片编辑器核心代码
├── index.html           # 项目列表页
├── project_timeline.html # 时间轴视图
├── server.py            # 轻量级 Python 后端
├── docs/                # 项目文档（含开发规范）
│   ├── 00-项目说明.md
│   ├── 01-开发规范.md
├── projects/            # 示例或导入的 Markdown 文件
├── project_cards.json   # 本地数据（自动生成，不提交）
├── env/test/project_cards.json # 测试/脱敏数据（空）
├── docker-compose.test.yml     # 测试环境 Compose（端口 18898）
└── .gitignore           # Git 忽略配置
```

## 测试环境（脱敏）

启动一个不含真实数据的测试环境：

```bash
docker compose -f docker-compose.test.yml up -d
# 访问 http://localhost:18898/
```

该环境会挂载 `env/test/project_cards.json`（默认空数组），用于功能验证与对外同步代码前的脱敏测试。

## 扩展开发

如需进行二次开发或接入 CRM/后端系统：
1. 修改 `server.py` 以连接真实数据库。
2. 前端页面均为原生 HTML/JS/React(CDN)，无需构建步骤，直接修改即可生效。

# FlowCard-PM (项目卡片与甘特图生成器)

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Version](https://img.shields.io/badge/version-v9.2-green.svg)

**FlowCard-PM** 是一个极客风的轻量级项目管理工具，专注于“项目卡片”的可视化生成与全生命周期管理。它集成了**项目管理**、**甘特图自动生成**、**项目流程图**梳理以及 **AI 辅助润色**功能，旨在帮助技术团队和项目经理以最少的操作成本，输出标准化、美观的交付物。

> 关键词：项目卡片, 项目管理, 甘特图, 项目流程图, Project Cards, Gantt Chart, AI 辅助, 可视化管理

## 🚀 核心特性

### 1. 极客风项目卡片 (Project Cards)
- **所见即所得**：现代化 UI 编辑器 (`cardv8.html`)，支持拖拽调整布局、实时预览。
- **AI 智能润色**：内置 AI 接口（支持 OpenAI/DeepSeek 等），一键优化项目描述，提升专业度。
- **Markdown 友好**：支持 Markdown 文件批量导入/导出，完美融入技术文档流。
- **标准化输出**：自动生成 16:9 标准比例卡片，适合汇报与大屏展示。

### 2. 自动化甘特图 (Auto Gantt Chart)
- **智能解析**：自动解析卡片中的“项目周期”文本（如“2025年1月-3月”），生成动态甘特图。
- **全局/局部视图**：支持查看所有项目的全局时间表，或进入单项目详情页查看特定任务的推进表。
- **交互式微调**：支持在时间轴上直接点击编辑，数据实时同步。

### 3. 多项目流程管理 (Project Flow)
- **项目看板**：`projects.html` 提供全局视角，管理所有项目状态（进行中/规划中/已完成）。
- **层级架构**：支持 **Project (项目) -> SubProject (子卡片)** 的两级管理架构，自动聚合预算与工时。
- **数据安全**：所有敏感数据（API Key、项目信息）均存储在本地或通过 Docker 挂载，完全私有化部署。

## 🛠️ 快速开始

### 方式一：Python 直接启动 (macOS/Linux/Windows)

本项目使用 Python 内置服务器作为轻量级后端，无需复杂配置。

```bash
# 1. 克隆仓库
git clone https://github.com/your-repo/FlowCard-PM.git
cd FlowCard-PM

# 2. 启动服务 (默认端口 8000)
python3 server.py 8000
```

访问：[http://localhost:8000/projects.html](http://localhost:8000/projects.html)

### 方式二：Docker 容器化部署

```bash
# 启动服务
docker compose up -d
```

访问：[http://localhost:8000/projects.html](http://localhost:8000/projects.html)

> **注意**：测试环境（`docker-compose.test.yml`）默认挂载空数据文件，用于脱敏演示。

## 📂 目录结构

```text
.
├── projects.html          # [入口] 项目看板与全局设置
├── project_detail.html    # 项目详情与卡片聚合页
├── cardv8.html            # 核心卡片编辑器
├── project_timeline.html  # 甘特图/时间表视图
├── server.py              # 轻量级 Python API 网关
├── data/                  # 数据存储目录 (JSON)
│   ├── projects.json      # 项目元数据
│   ├── project_cards.json # 卡片数据
│   └── ...
├── docs/                  # 开发文档与规范
└── projects/              # 原始 Markdown 归档
```

## 🔐 数据安全与隐私

- **本地优先**：所有业务数据默认存储在本地 JSON 文件中 (`project_cards.json`, `projects.json`)。
- **Git 脱敏**：`.gitignore` 已配置忽略真实数据文件，仓库中仅包含 `*.example.json` 示例文件。
- **AI 配置**：API Key 等敏感信息仅保存在浏览器 LocalStorage 或本地导出文件中，绝不上传云端。

## 🤝 贡献与扩展

欢迎提交 Issue 或 PR！
- 前端：原生 HTML/JS + Tailwind CSS + React (CDN)，无需构建，修改即生效。
- 后端：Python `http.server` 扩展，易于迁移至 Flask/FastAPI。

## 📄 License

MIT License

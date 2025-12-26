# FlowCard-PM | 轻量级卡片式项目管理系统

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-active-green)

**FlowCard-PM** 是一款专为敏捷团队设计的轻量级项目管理工具。它基于“卡片”核心理念，将复杂的项目拆解为独立的执行单元（卡片），通过可视化看板、自动化甘特图和 AI 辅助功能，帮助团队高效推进项目交付。

> **核心关键词**：项目管理, 项目卡片, 甘特图, 项目流程图, 预算管理, AI 辅助, 敏捷开发

---

## ✨ 核心特性 (Features)

### 1. 多项目可视化看板
- **直观概览**：首页看板展示所有项目状态、预算进度及关联卡片数量。
- **快速筛选**：支持按项目名称、客户、状态（进行中/规划中/已完成）快速检索。
- **关键指标**：自动统计项目群的总预算、活跃项目数。

### 2. 卡片式任务管理
- **颗粒度拆解**：将项目拆解为标准的“卡片”，每张卡片包含目标、周期、预算、里程碑及交付物。
- **灵活关联**：通过统一的编号规则（Customer-Project-Suffix）自动关联卡片与项目。
- **批量操作**：支持卡片的批量导出（Excel/Markdown）、删除及状态切换。

### 3. 自动化项目推进表 (Gantt & Timeline)
- **自动生成**：基于卡片中的“项目周期”和“里程碑”信息，自动生成全局或单项目的甘特图。
- **时间轴视图**：清晰展示项目的时间跨度、关键节点及并行关系。
- **交互式筛选**：支持按客户、项目进行时间轴过滤，便于资源冲突检查。

### 4. AI 智能辅助
- **多模型支持**：内置 AI 配置面板，支持 OpenAI 格式接口（ChatGPT, DeepSeek, Claude 等）。
- **智能分析**：AI 可辅助生成卡片内容、优化项目描述、拆解任务结构。
- **隐私安全**：AI 配置存储于本地浏览器（LocalStorage），API Key 不上传服务器。

### 5. 预算与工时追踪
- **自动聚合**：自动从卡片中提取“预算金额”和“工时（人天）”，汇总至项目维度。
- **统计报表**：提供选中卡片的预算统计弹窗，支持导出 Excel 用于财务汇报。

### 6. 数据安全与备份
- **本地化存储**：所有数据以 JSON 文件形式存储于部署服务器/本地，无云端依赖。
- **一键备份**：支持将所有项目数据、卡片数据及系统配置打包导出备份。
- **无缝恢复**：支持从备份文件一键恢复数据，保障数据安全。

---

## 🛠 技术栈 (Tech Stack)

- **后端**：Python 3 (http.server) - 零依赖，极致轻量。
- **前端**：HTML5, Vanilla JavaScript
- **UI 框架**：Tailwind CSS (CDN)
- **图标库**：Lucide Icons
- **数据存储**：JSON 文件系统

---

## 🚀 快速开始 (Quick Start)

### 1. 克隆仓库
```bash
git clone https://github.com/aokest/project_cards.git
cd project_cards
```

### 2. 初始化数据
首次运行时，需要基于示例文件创建实际的数据文件（已在 .gitignore 中忽略，保障隐私）：

```bash
# 复制项目数据示例
cp projects.example.json projects.json

# 复制卡片数据示例
cp project_cards.example.json project_cards.json

# 创建数据目录（如不存在）
mkdir -p data
```

### 3. 启动服务
确保已安装 Python 3：

```bash
# 默认端口 18889
python3 server.py

# 或者指定端口
python3 server.py 8000
```

### 4. 访问系统
打开浏览器访问：`http://localhost:18889` (或您指定的端口)

---

## ⚙️ 系统配置

### AI 配置
1. 点击右上角 **设置图标** -> **AI 模型配置**。
2. 点击 **新增模型**，输入 API Key、Base URL (如 `https://api.deepseek.com/v1`) 和模型名称。
3. 点击 **验证** 测试连接，并设为激活状态。

### 数据备份
1. 点击右上角 **设置图标** -> **数据备份与恢复**。
2. 勾选需要备份的内容（项目、卡片、配置），点击 **立即备份**。

---

## 📂 目录结构

```text
.
├── server.py                 # 核心后端服务
├── projects.html             # 项目看板（首页）
├── project_detail.html       # 项目详情页
├── project_timeline.html     # 全局推进表/甘特图
├── cardv8.html               # 卡片编辑器
├── projects.json             # [数据] 项目元数据 (需自行创建)
├── project_cards.json        # [数据] 卡片数据 (需自行创建)
├── docs/                     # 开发文档
└── ...
```

---

## ⚠️ 注意事项

- **数据隐私**：本项目设计为本地或内网部署，不包含用户鉴权系统。请勿直接部署在公网环境。
- **浏览器兼容性**：推荐使用 Chrome, Edge, Firefox 等现代浏览器。

---

## 📄 License

MIT License

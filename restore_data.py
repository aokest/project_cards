import json
import os

# 1. Read existing data
with open('project_cards.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

# 2. Define the missing cards
missing_cards = [
    {
        "id": "CARD-RECOVERED-12",
        "cardId": "1205-S1-S03-B",
        "title": "资产漏洞情报预警服务",
        "rawText": "项目编号：1205-S1-S03-B\n项目名称：资产漏洞情报预警服务\n项目目标：监控与现有资产相关的漏洞情报，对最新爆发的已知漏洞或潜在漏洞做持续监控，为公共关系应对及安全应急争取主动性。\n现状分析：目前有大量已知的资产漏洞；市场通用的威胁情报有大量噪声，容易失焦。无资产关联的漏洞预警服务；\n项目周期：持续监控；即时预警；月度汇报\n预算投入：10万/200资产·年\n所需支持：协助补充、完善资产字段信息\n项目内容：\n1. 监控与现有资产相关的漏洞情报，对最新爆发的已知漏洞或潜在漏洞做持续监控\n2. 对监控情况每月提供定制月报\n参与部门：信息安全部；产品线研发部\n相关产品及解决方案：漏洞情报预警服务\n输出物：即时预警；定制月报",
        "updatedAt": "2025-12-24T20:15:30.000Z",
        "themeColor": "#0f172a",
        "accentColor": "#f1f5f9",
        "textColor": "#334155",
        "cardBg": "#FFFFFF",
        "budgetColor": "#b45309",
        "sectionConfig": { "项目周期": {"fontPx": 16, "minHeight": 260}, "现状分析": {"fontPx": 16, "minHeight": 220}, "预算投入": {"fontPx": 18, "minHeight": 200}, "项目目标": {"fontPx": 16, "minHeight": 200}, "项目内容": {"fontPx": 16, "minHeight": 280}, "所需支持": {"fontPx": 16, "minHeight": 200}, "参与部门": {"fontPx": 16, "minHeight": 120}, "相关产品及解决方案": {"fontPx": 16, "minHeight": 120}, "输出物": {"fontPx": 16, "minHeight": 180} },
        "layoutConfig": { "mainRightCols": 5, "row3BudgetCols": 5, "outputSpan": 5, "outputAlign": "right" }
    },
    {
        "id": "CARD-RECOVERED-13",
        "cardId": "1205-S1-S04",
        "title": "机密敏感信息扫描监测服务",
        "rawText": "项目编号：1205-S1-S04\n项目名称：机密敏感信息扫描监测服务\n项目目标：针对文档、研发等平台监控明文编码或易被获取机密敏感信息，进行预警提示，避免机密敏感信息泄露。\n现状分析：无机密信息扫描与监测机制；已经发现有针对机密信息的获取及恶意利用行为存在，产生严重实际损失；\n项目周期：持续监控；即时预警；月度汇报\n预算投入：15万/年，采购SAST后可由产品能力进行覆盖\n所需支持：提供易被获取机密敏感信息的关键字段；提供可能的潜在信息源。\n项目内容：\n1. 监控文档、研发等平台，对明文编码或易被获取机密敏感信息做持续监控\n2. 对监控情况每月提供定制周报\n参与部门：信息安全部；产品线研发部\n相关产品及解决方案：机密敏感信息扫描监测服务\n输出物：即时预警；定制周报",
        "updatedAt": "2025-12-24T20:14:19.000Z",
        "themeColor": "#0f172a",
        "accentColor": "#f1f5f9",
        "textColor": "#334155",
        "cardBg": "#FFFFFF",
        "budgetColor": "#b45309",
        "sectionConfig": { "项目周期": {"fontPx": 16, "minHeight": 260}, "现状分析": {"fontPx": 16, "minHeight": 220}, "预算投入": {"fontPx": 18, "minHeight": 200}, "项目目标": {"fontPx": 16, "minHeight": 200}, "项目内容": {"fontPx": 16, "minHeight": 280}, "所需支持": {"fontPx": 16, "minHeight": 200}, "参与部门": {"fontPx": 16, "minHeight": 120}, "相关产品及解决方案": {"fontPx": 16, "minHeight": 120}, "输出物": {"fontPx": 16, "minHeight": 180} },
        "layoutConfig": { "mainRightCols": 5, "row3BudgetCols": 5, "outputSpan": 5, "outputAlign": "right" }
    },
    {
        "id": "CARD-RECOVERED-14",
        "cardId": "1205-S1-S05",
        "title": "安全制度建设及推广",
        "rawText": "项目编号：1205-S1-S05\n项目名称：安全制度建设及推广\n项目目标：建立完善的安全管理制度，从源头降低“低级错误”引发的风险。通过面向研发、运维人员的“学-练-测-证”闭环，量化全员安全能力；推行“持证上岗”，确保接触生产环境人员具备实操技能。\n现状分析：在CI/CD全生命周期缺乏管理制度。开发缺乏安全编码知识，运维配置失误频发；缺乏客观标准评估团队能力，传统宣贯无法度量且难以留痕。\n项目周期：2026年1月\n预算投入：总计 37万/年\n制度流程建设：15人天，共6万\n平台订阅费： 1000人次，共9万\n定制开发费： 20人天，共12万\n课程开发费： 10万\n所需支持：\n研发管理层： 明确“持证”与代码提交/发布权限挂钩。\nHR部门： 将认证结果纳入绩效或技能档案。\n提供人员编号，以及平台数据接口\n项目内容：\n实战课程定制： 结合公司业务代码特征，定制开发15节以上专属课程（覆盖安全编码、容器配置等），替代通用理论课。\n能力评估体系： 基于“企安殿”构建开发、运维、测试分角色题库。\n接口自动化： 打通学习平台与HR系统，实现账号同步与证书自动归档。\n双周期考核： 组织全员集训与通关考试，颁发内部“安全上岗证”。\n参与部门：信息安全部、人力资源部、研发中心、运维部\n相关产品及解决方案：永信至诚企安殿人才发展系统、永信至诚数字风洞系统、课程及接口定制服务\n输出物：\nCI/CD安全管理制度\n2026年度1月研发安全能力考核结果\n集团CI/CD全员安全能力矩阵图谱 \n1套企业专属安全实战课程体系（15+节） \n500份员工安全资质电子证书（存证入档）",
        "updatedAt": "2025-12-24T20:13:18.000Z",
        "themeColor": "#0f172a",
        "accentColor": "#f1f5f9",
        "textColor": "#334155",
        "cardBg": "#FFFFFF",
        "budgetColor": "#b45309",
        "sectionConfig": { "项目周期": {"fontPx": 16, "minHeight": 260}, "现状分析": {"fontPx": 16, "minHeight": 220}, "预算投入": {"fontPx": 18, "minHeight": 200}, "项目目标": {"fontPx": 16, "minHeight": 200}, "项目内容": {"fontPx": 16, "minHeight": 280}, "所需支持": {"fontPx": 16, "minHeight": 200}, "参与部门": {"fontPx": 16, "minHeight": 120}, "相关产品及解决方案": {"fontPx": 16, "minHeight": 120}, "输出物": {"fontPx": 16, "minHeight": 180} },
        "layoutConfig": { "mainRightCols": 5, "row3BudgetCols": 5, "outputSpan": 5, "outputAlign": "right" }
    }
]

# 3. Check duplicates
existing_ids = set(c['cardId'] for c in cards)
final_cards = cards[:]

for nc in missing_cards:
    if nc['cardId'] not in existing_ids:
        final_cards.append(nc)
        print(f"Added {nc['cardId']}")
    else:
        print(f"Skipped {nc['cardId']} (Already exists)")

# 4. Save
with open('project_cards.json', 'w', encoding='utf-8') as f:
    json.dump(final_cards, f, ensure_ascii=False, indent=2)

print(f"Total cards now: {len(final_cards)}")

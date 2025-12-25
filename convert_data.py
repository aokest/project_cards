import json
import re
import datetime

def parse_md(file_path):
    projects = []
    current_project = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('- 卡片编号:'):
            if current_project:
                projects.append(current_project)
            current_project = {'id': f"CARD-{len(projects)+1}", 'updatedAt': datetime.datetime.now().isoformat()}
            current_project['cardId'] = line.split(':', 1)[1].strip()
        elif line.startswith('- 项目名称:'):
            current_project['title'] = line.split(':', 1)[1].strip()
        elif line.startswith('- 时间:'):
            time_str = line.split(':', 1)[1].strip()
            # Construct rawText
            raw_text = f"项目编号：{current_project.get('cardId', '')}\n"
            raw_text += f"项目名称：{current_project.get('title', '')}\n"
            raw_text += f"项目周期：{time_str}\n"
            raw_text += "项目目标：[待补充]\n现状分析：[待补充]\n项目内容：[待补充]\n所需支持：[待补充]\n预算投入：[待补充]\n参与部门：[待补充]\n相关产品及解决方案：[待补充]\n输出物：[待补充]"
            current_project['rawText'] = raw_text
            
            # Default configs
            current_project['themeColor'] = '#0f172a'
            current_project['accentColor'] = '#f1f5f9'
            current_project['textColor'] = '#334155'
            current_project['cardBg'] = '#FFFFFF'
            current_project['budgetColor'] = '#b45309'
            current_project['sectionConfig'] = {
                '项目周期': {'fontPx': 16, 'minHeight': 260},
                '现状分析': {'fontPx': 16, 'minHeight': 220},
                '预算投入': {'fontPx': 18, 'minHeight': 200},
                '项目目标': {'fontPx': 16, 'minHeight': 200},
                '项目内容': {'fontPx': 16, 'minHeight': 280},
                '所需支持': {'fontPx': 16, 'minHeight': 200},
                '参与部门': {'fontPx': 16, 'minHeight': 120},
                '相关产品及解决方案': {'fontPx': 16, 'minHeight': 120},
                '输出物': {'fontPx': 16, 'minHeight': 180}
            }
            current_project['layoutConfig'] = {'mainRightCols': 5, 'row3BudgetCols': 5, 'outputSpan': 5, 'outputAlign': 'right'}
            
    if current_project:
        projects.append(current_project)
        
    return projects

data = parse_md('projects_timetable.md')
with open('initial_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Successfully converted {len(data)} projects to initial_data.json")

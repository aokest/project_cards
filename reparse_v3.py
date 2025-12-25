import re
import json
import uuid
import datetime

MD_FILE = 'projects/project_card_1205_V2.md'
JSON_FILE = 'project_cards.json'

def parse_markdown(md_content):
    # Normalize newlines
    md_content = md_content.replace('\r\n', '\n')
    
    # Split by separator line (---)
    # Using a robust regex that handles optional whitespace around dashes
    sections = re.split(r'\n-{3,}\n', md_content)
    
    cards = []
    
    for section in sections:
        if not section.strip(): continue
        
        # Skip the header section if it doesn't look like a card
        # The first section might be "# 项目卡片导出 (14个)" without card data
        if section.strip().startswith('# ') and '项目编号' not in section:
            continue
            
        card = {
            "id": f"CARD-{uuid.uuid4().hex[:8]}",
            "updatedAt": datetime.datetime.now().isoformat(),
            "themeColor": "#0f172a",
            "accentColor": "#f1f5f9",
            "textColor": "#334155",
            "cardBg": "#FFFFFF",
            "budgetColor": "#b45309",
            "sectionConfig": { "项目周期": {"fontPx": 16, "minHeight": 260}, "现状分析": {"fontPx": 16, "minHeight": 220}, "预算投入": {"fontPx": 18, "minHeight": 200}, "项目目标": {"fontPx": 16, "minHeight": 200}, "项目内容": {"fontPx": 16, "minHeight": 280}, "所需支持": {"fontPx": 16, "minHeight": 200}, "参与部门": {"fontPx": 16, "minHeight": 120}, "相关产品及解决方案": {"fontPx": 16, "minHeight": 120}, "输出物": {"fontPx": 16, "minHeight": 180} },
            "layoutConfig": { "mainRightCols": 5, "row3BudgetCols": 5, "outputSpan": 5, "outputAlign": "right" },
            "data": {} # Initialize data object
        }
        
        # 1. Parse Title (## Title)
        title_match = re.search(r'##\s+(.+)', section)
        if title_match:
            card['title'] = title_match.group(1).strip()
        
        # 2. Extract Fields into `data` map
        known_keys = ['项目编号', '项目名称', '项目目标', '现状分析', '项目周期', '预算投入', '所需支持', '项目内容', '参与部门', '相关产品及解决方案', '输出物', '编号', '更新时间']
        
        lines = section.split('\n')
        current_key = None
        current_val = []
        
        for line in lines:
            line = line.strip()
            if not line: continue
            if line.startswith('##'): continue # Skip title line
            if line.startswith('**编号**') or line.startswith('**更新时间**'): continue # Skip metadata lines
            
            # Check if line starts with a known key
            found_key = False
            for k in known_keys:
                if line.startswith(k + '：') or line.startswith(k + ':'):
                    # Save previous
                    if current_key:
                        full_val = '\n'.join(current_val).strip()
                        card['data'][current_key] = full_val
                        
                        if current_key == '项目编号': card['cardId'] = full_val
                        if current_key == '项目名称': card['title'] = full_val # Override title
                        
                    current_key = k
                    # Value is everything after the colon
                    val_start = line.find('：') if '：' in line else line.find(':')
                    current_val = [line[val_start+1:].strip()]
                    found_key = True
                    break
            
            if not found_key:
                if current_key:
                    current_val.append(line)
        
        # Capture last field
        if current_key:
            full_val = '\n'.join(current_val).strip()
            card['data'][current_key] = full_val
            if current_key == '项目编号': card['cardId'] = full_val
            if current_key == '项目名称': card['title'] = full_val

        # 3. Construct `rawText`
        # Always reconstruct from data to ensure clean format for the frontend parser
        parts = []
        # Title is special, usually mapped from '项目名称'
        # But we might want to keep the original rawText if it contains extra info not in known keys?
        # No, the user wants structured data editing. Rebuilding is safer for "Blank Card" issue.
        
        # Order matters for the editor
        ordered_keys = ['项目编号', '项目名称', '项目目标', '现状分析', '项目周期', '预算投入', '所需支持', '项目内容', '参与部门', '相关产品及解决方案', '输出物']
        
        for k in ordered_keys:
            val = card['data'].get(k)
            if val:
                parts.append(f"{k}：{val}")
        
        # Add any other keys found in data but not in ordered_list
        for k, v in card['data'].items():
            if k not in ordered_keys and k not in ['编号', '更新时间']:
                parts.append(f"{k}：{v}")

        clean_text = "\n\n".join(parts)
        card['rawText'] = clean_text
        
        # Ensure cardId exists
        if 'cardId' not in card:
            # Fallback extract from raw text
            cid = re.search(r'项目编号[：:]\s*([A-Za-z0-9-]+)', section)
            if cid: card['cardId'] = cid.group(1)
            else: card['cardId'] = f"UNKNOWN-{uuid.uuid4().hex[:4]}"

        cards.append(card)

    return cards

if __name__ == '__main__':
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cards = parse_markdown(content)
    
    # Deduplicate IDs
    seen_ids = {}
    final_cards = []
    for c in cards:
        cid = c.get('cardId')
        if not cid: continue
        
        if cid in seen_ids:
            # Modify the ID of the SECOND occurrence
            new_id = f"{cid}-B"
            c['cardId'] = new_id
            # Also update rawText to reflect new ID
            c['rawText'] = c['rawText'].replace(cid, new_id)
            c['data']['项目编号'] = new_id
            print(f"Renamed duplicate {cid} to {new_id}")
        
        seen_ids[cid] = True
        final_cards.append(c)
        
    print(f"Parsed {len(final_cards)} cards.")
    
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_cards, f, ensure_ascii=False, indent=2)

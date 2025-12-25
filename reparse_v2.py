import re
import json
import uuid
import datetime

MD_FILE = 'projects/project_card_1205_V2.md'
JSON_FILE = 'project_cards.json'

def parse_markdown(md_content):
    # Split by separator line
    sections = re.split(r'\n-+\n', md_content)
    cards = []
    
    for section in sections:
        if not section.strip(): continue
        
        card = {
            "id": f"CARD-{uuid.uuid4().hex[:8]}",
            "updatedAt": datetime.datetime.now().isoformat(),
            "sectionConfig": { "项目周期": {"fontPx": 16, "minHeight": 260}, "现状分析": {"fontPx": 16, "minHeight": 220}, "预算投入": {"fontPx": 18, "minHeight": 200}, "项目目标": {"fontPx": 16, "minHeight": 200}, "项目内容": {"fontPx": 16, "minHeight": 280}, "所需支持": {"fontPx": 16, "minHeight": 200}, "参与部门": {"fontPx": 16, "minHeight": 120}, "相关产品及解决方案": {"fontPx": 16, "minHeight": 120}, "输出物": {"fontPx": 16, "minHeight": 180} },
            "layoutConfig": { "mainRightCols": 5, "row3BudgetCols": 5, "outputSpan": 5, "outputAlign": "right" }
        }
        
        # 1. Parse Title (## Title)
        title_match = re.search(r'##\s+(.+)', section)
        if title_match:
            card['title'] = title_match.group(1).strip()
        
        # 2. Parse Fields
        # Strategy: Find "Key: Value" or "Key：Value"
        # Since values can be multi-line, we look for the next known key to stop.
        known_keys = ['项目编号', '项目名称', '项目目标', '现状分析', '项目周期', '预算投入', '所需支持', '项目内容', '参与部门', '相关产品及解决方案', '输出物', '编号', '更新时间']
        
        lines = section.split('\n')
        current_key = None
        current_val = []
        
        for line in lines:
            line = line.strip()
            if not line: continue
            if line.startswith('##') or line.startswith('**编号**') or line.startswith('**更新时间**'): continue
            
            # Check if line starts with a known key
            found_key = False
            for k in known_keys:
                if line.startswith(k + '：') or line.startswith(k + ':'):
                    # Save previous
                    if current_key:
                        full_val = '\n'.join(current_val).strip()
                        if current_key == '项目编号': card['cardId'] = full_val
                        if current_key == '项目名称': card['title'] = full_val # Override title
                        
                        # Store in rawText reconstruction
                        pass 
                        
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
            if current_key == '项目编号': card['cardId'] = full_val
            if current_key == '项目名称': card['title'] = full_val

        # Reconstruct rawText (easier than parsing into 'data' object for now, as the frontend uses rawText heavily)
        # But wait, the user wants STRUCTURED TIME.
        # So let's extract '项目周期' specifically into a structured field.
        
        # Let's rebuild the `rawText` because the frontend relies on it for display.
        # We will just dump the original section content as rawText for now, OR reconstruct it cleanly.
        # The user provided markdown has "Key: Value". Let's use the section content but clean up the "## Title" part.
        
        # Extract specific structured data for Project Cycle
        cycle_match = re.search(r'项目周期[：:]([\s\S]*?)(?=预算投入|现状分析|所需支持|项目内容|参与部门|相关产品|输出物|$)', section)
        if cycle_match:
            raw_time = cycle_match.group(1).strip()
            card['structuredTime'] = parse_time_structure(raw_time)
            # We also ensure the rawText contains this field for the regex parser in frontend fallback
        
        # For simplicity and robustness, we treat the entire section (minus the ## header) as rawText
        # But we remove the top metadata like "**编号**" to avoid duplication if we re-export.
        clean_text = re.sub(r'##\s+.+\n', '', section)
        clean_text = re.sub(r'\*\*编号\*\*:.+\n', '', clean_text)
        clean_text = re.sub(r'\*\*更新时间\*\*:.+\n', '', clean_text)
        card['rawText'] = clean_text.strip()
        
        # Ensure cardId exists
        if 'cardId' not in card:
            # Fallback extract from raw text
            cid = re.search(r'项目编号[：:]\s*([A-Za-z0-9-]+)', section)
            if cid: card['cardId'] = cid.group(1)
            else: card['cardId'] = f"UNKNOWN-{uuid.uuid4().hex[:4]}"

        # Deduplicate Logic: If cardId is "1205-S1-S03", check if title contains "漏洞" or "黑客" to disambiguate?
        # The user said "1205-S1-S03" is duplicate.
        # We can append -B if we see a duplicate.
        
        cards.append(card)

    return cards

def parse_time_structure(text):
    """
    Parse text like "第一阶段（1-3周）：演练方案设计" into 
    [ { "phase": "设计规划", "time": "1-3周", "desc": "演练方案..." }, ... ]
    """
    segments = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Regex for "Stage X (Time): Content"
        # e.g. "第一阶段（1-3周）：演练方案设计"
        m = re.match(r'(第.+阶段|.+期)[（(](.+)[）)][：:](.+)', line)
        if m:
            segments.append({
                "phase": m.group(1),
                "time": m.group(2),
                "desc": m.group(3),
                "type": classify_phase(m.group(1) + m.group(3))
            })
            continue
            
        # Regex for "Month: Content"
        # e.g. "4-5月春季考核认证"
        m2 = re.match(r'(\d{1,2}[-~]\d{1,2}月)(.+)', line)
        if m2:
             segments.append({
                "phase": "执行阶段",
                "time": m2.group(1),
                "desc": m2.group(2),
                "type": "execution"
            })
             continue
             
        # Regex for simple ranges "2026年3月-5月"
        m3 = re.match(r'(\d{4}年\d{1,2}月[-~]\d{1,2}月)', line)
        if m3:
             segments.append({
                "phase": "整体周期",
                "time": m3.group(1),
                "desc": "项目整体执行",
                "type": "execution"
            })
             continue

    if not segments:
        # If no structured lines found, return the whole text as one 'execution' block
        return [{ "phase": "执行", "time": text, "desc": text, "type": "execution" }]
        
    return segments

def classify_phase(text):
    if any(x in text for x in ['设计', '规划', '准备', '方案', '访谈', '梳理']): return 'prep'
    if any(x in text for x in ['实施', '执行', '演练', '部署', '开发', '建设']): return 'execution'
    if any(x in text for x in ['验收', '复盘', '总结', '汇报', '收尾']): return 'closing'
    return 'execution'

if __name__ == '__main__':
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cards = parse_markdown(content)
    
    # Post-processing for duplicates
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
            print(f"Renamed duplicate {cid} to {new_id}")
        
        seen_ids[cid] = True
        final_cards.append(c)
        
    print(f"Parsed {len(final_cards)} cards.")
    
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_cards, f, ensure_ascii=False, indent=2)

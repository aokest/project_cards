const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const MD_FILE = path.join(__dirname, 'projects', 'project_card_1205_V2.md');
const JSON_FILE = path.join(__dirname, 'project_cards.json');

function uuid() {
    return 'CARD-' + crypto.randomBytes(4).toString('hex');
}

function parseMarkdown(content) {
    // Normalize newlines
    content = content.replace(/\r\n/g, '\n');
    
    // Split by separator line (---)
    const sections = content.split(/\n-{3,}\n/);
    
    const cards = [];
    const seenIds = new Set();
    
    for (const section of sections) {
        if (!section.trim()) continue;
        
        // Skip header
        if (section.trim().startsWith('# ') && !section.includes('项目编号')) continue;
        
        const card = {
            id: uuid(),
            updatedAt: new Date().toISOString(),
            themeColor: "#0f172a",
            accentColor: "#f1f5f9",
            textColor: "#334155",
            cardBg: "#FFFFFF",
            budgetColor: "#b45309",
            sectionConfig: { "项目周期": {"fontPx": 16, "minHeight": 260}, "现状分析": {"fontPx": 16, "minHeight": 220}, "预算投入": {"fontPx": 18, "minHeight": 200}, "项目目标": {"fontPx": 16, "minHeight": 200}, "项目内容": {"fontPx": 16, "minHeight": 280}, "所需支持": {"fontPx": 16, "minHeight": 200}, "参与部门": {"fontPx": 16, "minHeight": 120}, "相关产品及解决方案": {"fontPx": 16, "minHeight": 120}, "输出物": {"fontPx": 16, "minHeight": 180} },
            layoutConfig: { "mainRightCols": 5, "row3BudgetCols": 5, "outputSpan": 5, "outputAlign": "right" },
            data: {}
        };
        
        // Parse Title
        const titleMatch = section.match(/##\s+(.+)/);
        if (titleMatch) {
            card.title = titleMatch[1].trim();
        }
        
        // Parse fields
        const lines = section.split('\n');
        let currentKey = null;
        let currentVal = [];
        
        const knownKeys = ['项目编号', '项目名称', '项目目标', '现状分析', '项目周期', '预算投入', '所需支持', '项目内容', '参与部门', '相关产品及解决方案', '输出物', '编号', '更新时间'];
        
        for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed) continue;
            if (trimmed.startsWith('##')) continue;
            if (trimmed.startsWith('**编号**') || trimmed.startsWith('**更新时间**')) continue;
            
            let foundKey = false;
            for (const k of knownKeys) {
                if (trimmed.startsWith(k + '：') || trimmed.startsWith(k + ':')) {
                    if (currentKey) {
                        card.data[currentKey] = currentVal.join('\n').trim();
                    }
                    currentKey = k;
                    const sepIndex = line.indexOf('：') !== -1 ? line.indexOf('：') : line.indexOf(':');
                    currentVal = [line.substring(sepIndex + 1).trim()];
                    foundKey = true;
                    break;
                }
            }
            
            if (!foundKey && currentKey) {
                currentVal.push(trimmed);
            }
        }
        
        if (currentKey) {
            card.data[currentKey] = currentVal.join('\n').trim();
        }
        
        // Post-process
        if (card.data['项目编号']) card.cardId = card.data['项目编号'];
        if (card.data['项目名称']) card.title = card.data['项目名称'];
        
        if (!card.cardId) {
             const match = section.match(/项目编号[：:]\s*([A-Za-z0-9-]+)/);
             if (match) card.cardId = match[1];
        }

        // Handle duplicates
        if (card.cardId) {
            if (seenIds.has(card.cardId)) {
                const newId = card.cardId + '-B';
                console.log(`Renaming duplicate ${card.cardId} to ${newId}`);
                card.cardId = newId;
                card.data['项目编号'] = newId;
            }
            seenIds.add(card.cardId);
        }
        
        // Reconstruct rawText
        const parts = [];
        const orderedKeys = ['项目编号', '项目名称', '项目目标', '现状分析', '项目周期', '预算投入', '所需支持', '项目内容', '参与部门', '相关产品及解决方案', '输出物'];
        
        for (const k of orderedKeys) {
            if (card.data[k]) parts.push(`${k}：${card.data[k]}`);
        }
        
        card.rawText = parts.join('\n\n');
        cards.push(card);
    }
    
    return cards;
}

const content = fs.readFileSync(MD_FILE, 'utf-8');
const cards = parseMarkdown(content);
console.log(`Parsed ${cards.length} cards.`);
fs.writeFileSync(JSON_FILE, JSON.stringify(cards, null, 2));

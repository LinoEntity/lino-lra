#!/usr/bin/env python3
"""Patch lra.py: integrate TF-IDF into generate_summary for better sentence selection."""

with open('/work/lra/lra.py', 'r') as f:
    content = f.read()

# 1. Replace the sentence collection block to add TF-IDF scoring
old1 = '''    # Raccogli tutte le frasi pulite con attribuzione
    all_sentences = []
    for s in sources:
        title = s.get("title", "Fonte")
        content = s.get("content", "")
        sentences = smart_split_sentences(content)
        for sent in sentences:
            if len(sent) >= 40:
                all_sentences.append((title, sent))
    
    if not all_sentences:
        lines.append("_(contenuti insufficienti per un riassunto)_")
        return "\\n".join(lines)
    
    # Identifica i temi principali: keyword presenti in almeno 2 fonti
    theme_keywords = common_keywords(sources, n=8)'''

new1 = '''    # Raccogli tutte le frasi pulite con attribuzione
    all_sentences = []
    for s in sources:
        title = s.get("title", "Fonte")
        content = s.get("content", "")
        sentences = smart_split_sentences(content)
        for sent in sentences:
            if len(sent) >= 40:
                all_sentences.append((title, sent))
    
    if not all_sentences:
        lines.append("_(contenuti insufficienti per un riassunto)_")
        return "\\n".join(lines)
    
    # TF-IDF: seleziona le frasi piu informative (parole rare = punteggio alto)
    all_text = " ".join(s.get("content", "") for s in sources)
    tfidf_sentences = extract_key_sentences(all_text, n=12)
    # Mantieni solo le frasi che sono anche in all_sentences (per attribuzione)
    tfidf_set = set(s.strip().lower()[:80] for s in tfidf_sentences)
    scored_sentences = []
    for title, sent in all_sentences:
        if sent.strip().lower()[:80] in tfidf_set:
            scored_sentences.append((title, sent))
    if not scored_sentences:
        scored_sentences = all_sentences[:12]  # fallback
    
    # Identifica i temi principali: keyword presenti in almeno 2 fonti
    theme_keywords = common_keywords(sources, n=8)'''

if old1 in content:
    content = content.replace(old1, new1)
    print("✅ Blocco frasi sostituito")
else:
    print("❌ Blocco frasi non trovato")
    idx = content.find("Raccogli tutte le frasi")
    if idx >= 0:
        print(content[idx:idx+400])

# 2. Update else branch to use scored_sentences
old2 = '''    else:
        seen_titles = set()
        for title, sent in all_sentences[:6]:
            if title not in seen_titles:
                lines.append(f"> **{title}**: {sent[:200]}")
                lines.append("")
                seen_titles.add(title)'''

new2 = '''    else:
        seen_titles = set()
        for title, sent in scored_sentences[:6]:
            if title not in seen_titles:
                lines.append(f"> **{title}**: {sent[:200]}")
                lines.append("")
                seen_titles.add(title)'''

if old2 in content:
    content = content.replace(old2, new2)
    print("✅ Else branch aggiornato")
else:
    print("❌ Else branch non trovato")

with open('/work/lra/lra.py', 'w') as f:
    f.write(content)
print("✅ lra.py salvato")
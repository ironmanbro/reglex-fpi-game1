import re
def clean(path):
    out=[];skip=False
    for ln in open(path,encoding='utf-8',errors='ignore').read().split('\n'):
        s=ln.strip()
        if skip:
            if re.search(r'w\.e\.f\.?\s*[\d\-\. ]+\.?\s*$',s) or s.endswith('”') or s=='' : skip=False
            continue
        if re.match(r'^(Substituted|Inserted|Ibid|Prior to|Sub-regulation 9 omitted|The words “in technological)',s):
            skip=not (re.search(r'w\.e\.f\.?\s*[\d\-\. ]+\.?\s*$',s) or s=='Ibid.')
            continue
        if re.match(r'^Page \d+ of \d+$',s) or re.match(r'^\d{1,3}$',s) or re.match(r'^\(?[ivxlc]+\)?\.?$',s) or s in ('','',''): continue
        out.append(s)
    t=' '.join(out)
    t=re.sub(r'Page \d+ of \d+','',t)
    t=re.sub(r'\[\*\*\*\]','',t)
    t=re.sub(r'(?<![\w$])\d{1,2}\s*\[','',t)
    t=t.replace('[','').replace(']','')
    t=re.sub(r'\s+',' ',t)
    return t
DOCS={'R':clean('src/regs.raw.txt'),'O':clean('src/og.raw.txt'),'C':clean('src/circ.raw.txt'),'S':clean('src/sop.raw.txt')}
def norm(s): return re.sub(r'\s+',' ',s.replace('’',"'").replace('‘',"'")).strip()
for k in DOCS: DOCS[k]=DOCS[k].replace('’',"'").replace('‘',"'")
def grab(doc,start,end):
    t=DOCS[doc]; a=t.find(norm(start))
    if a<0: return None,'start not found'
    b=t.find(norm(end),a)
    if b<0: return None,'end not found'
    return t[a:b+len(norm(end))].strip(),None

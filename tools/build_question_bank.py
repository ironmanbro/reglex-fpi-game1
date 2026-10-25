import json, csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

cases = json.load(open('data/questions.json'))
assert all(len(c['facts']) <= 4 for c in cases)
L = "ABCD"
COLS = [
 ("ref",16,"Unique ID, e.g. ONB/CAT/105. Never reuse an ID."),
 ("status",10,"live = shown to players · draft = waiting for review · retired = rule changed, hidden"),
 ("chapter",10,"II, III, IV, V, VI, FEE, SW (SWAGAT-FI) or GS (GS-FPI)"),
 ("difficulty",11,"1 = Easy, 2 = Medium, 3 = Hard"),
 ("title",34,"Short case title shown on the file card"),
]
for i in range(1,5):
    COLS += [(f"fact{i}_label",16,f"Fact {i} label (optional)"),(f"fact{i}_value",34,f"Fact {i} value (optional)")]
COLS += [("question",40,"The question the player answers")]
COLS += [(f"option_{x}",36,f"Answer option {x}") for x in L]
COLS += [("answer",9,"Letter of the correct option: A, B, C or D"),
         ("explanation",60,"Why the correct option is right")]
COLS += [(f"why_not_{x}",44,f"Why option {x} is wrong. Leave blank for the correct option.") for x in L]
COLS += [("quote_1_source",30,"Where quote 1 comes from (document and clause)"),
         ("quote_1",70,"Exact wording of the regulation, shown after the answer"),
         ("quote_2_source",30,"Optional second clause: its source"),
         ("quote_2",70,"Optional second clause: exact wording")]
COLS += [("citation",40,"Regulation / circular reference shown under the explanation"),
         ("verify",8,"Y = based on secondary sources; shows a Verify tag"),
         ("as_of",11,"Date the rule was checked"),
         ("reviewer_notes",36,"Your notes. Ignored by the website."),
         ("check",22,"Automatic. Shows OK or what to fix. Ignored by the website.")]
HDR = [c[0] for c in COLS]

def row_for(c):
    r = {k:"" for k in HDR}
    r.update(ref=c["ref"], status=c.get("status","live"), chapter=c['ch'], difficulty=c['d'], title=c['title'],
             question=c['q'], answer=L[c['ans']], explanation=c['why'], citation=c['cite'],
             verify="Y" if c.get('t')=='secondary' else "", as_of="Oct 2026",
             quote_1_source=c.get('q1s',''), quote_1=c.get('q1',''), quote_2_source=c.get('q2s',''), quote_2=c.get('q2',''))
    for i,(k,v) in enumerate(c['facts'],1):
        r[f"fact{i}_label"]=k; r[f"fact{i}_value"]=v
    for i,x in enumerate(L):
        r[f"option_{x}"]=c['opts'][i]
        r[f"why_not_{x}"]=c['no'][i] or ""
    return r
rows=[row_for(c) for c in cases]

# ---------- workbook ----------
wb = Workbook()
F = "Arial"
thin = Side(style="thin", color="C9D2DA")
hdr_fill = PatternFill("solid", fgColor="13202B")
edit_fill = PatternFill("solid", fgColor="FFF9DB")
auto_fill = PatternFill("solid", fgColor="EEF1F4")

# Guide sheet
g = wb.active; g.title = "How to use"
g.sheet_view.showGridLines = False
g.column_dimensions['A'].width = 3; g.column_dimensions['B'].width = 26; g.column_dimensions['C'].width = 95
g['B2'] = "Custody Desk League · Question bank"; g['B2'].font = Font(name=F, size=16, bold=True, color="13202B")
g['B3'] = "One row per question on the Questions sheet. Only rows with status = live reach players."; g['B3'].font = Font(name=F, size=11, color="5A6774")
steps = [
 ("Edit","Work on the Questions sheet. Yellow columns are yours to fill; the grey Check column fills itself."),
 ("Review drafts","New questions arrive as status = draft. Read each one, fix anything, then change status to live."),
 ("Check column","Every live row should say OK. Anything else names the problem (missing option, wrong answer letter, etc.)."),
 ("Retire","When SEBI changes a rule, set status = retired. The question disappears without being deleted."),
 ("Quotes","quote_1 and quote_2 hold the exact wording of the regulation. The site shows them after each answer under What the regulation says. Paste text exactly as published; list numbering may be dropped."),
 ("Export","File → Save As → choose 'CSV UTF-8 (Comma delimited) (*.csv)' → file name questions.csv. Excel saves only the active sheet, so have the Questions sheet open when you do this."),
 ("Upload","Put questions.csv in the custody-desk-league folder next to index.html, then drag the folder onto app.netlify.com/projects/reglex/deploys."),
 ("Confirm","Open the site. The start screen shows how many live questions loaded from questions.csv, and how many rows were skipped."),
 ("Keep this file","Save the .xlsx too. It is your master copy; the CSV is just what the website reads."),
]
r=5
g.cell(r,2,"Step").font=Font(name=F,bold=True,color="FFFFFF"); g.cell(r,3,"What to do").font=Font(name=F,bold=True,color="FFFFFF")
for col in (2,3): g.cell(r,col).fill=hdr_fill
for k,v in steps:
    r+=1; g.cell(r,2,k).font=Font(name=F,bold=True); g.cell(r,3,v).font=Font(name=F)
    g.cell(r,3).alignment=Alignment(wrap_text=True,vertical="top"); g.cell(r,2).alignment=Alignment(vertical="top")
r+=2
g.cell(r,2,"Column").font=Font(name=F,bold=True,color="FFFFFF"); g.cell(r,3,"Meaning").font=Font(name=F,bold=True,color="FFFFFF")
for col in (2,3): g.cell(r,col).fill=hdr_fill
for name,_,desc in COLS:
    r+=1; g.cell(r,2,name).font=Font(name="Consolas"); g.cell(r,3,desc).font=Font(name=F)
    g.cell(r,3).alignment=Alignment(wrap_text=True,vertical="top")
r+=2
g.cell(r,2,"Rules the website applies").font=Font(name=F,bold=True)
for t in ["A row is used only if status = live, it has all four options, and answer is A–D.",
          "difficulty must be 1, 2 or 3. Anything else is skipped.",
          "Don't rename or delete the header row. Column order can change; names can't.",
          "Keep commas and quotes as normal text. Excel's CSV export handles them."]:
    r+=1; g.cell(r,3,"• "+t).font=Font(name=F); g.cell(r,3).alignment=Alignment(wrap_text=True)

# Questions sheet
ws = wb.create_sheet("Questions")
for j,(name,w,_) in enumerate(COLS,1):
    c=ws.cell(1,j,name); c.font=Font(name=F,bold=True,color="FFFFFF"); c.fill=hdr_fill
    c.alignment=Alignment(vertical="center")
    ws.column_dimensions[get_column_letter(j)].width=w
ws.row_dimensions[1].height=22
ci = {n:i+1 for i,n in enumerate(HDR)}
col = lambda n: get_column_letter(ci[n])
for i,rw in enumerate(rows, start=2):
    for n in HDR[:-1]:
        v=rw[n]; cell=ws.cell(i,ci[n],v)
        cell.font=Font(name=F,size=10); cell.alignment=Alignment(wrap_text=True,vertical="top")
        cell.border=Border(bottom=thin)
    # check formula
    o=f"{col('option_A')}{i}:{col('option_D')}{i}"; wn=f"{col('why_not_A')}{i}:{col('why_not_D')}{i}"
    a=f"{col('answer')}{i}"; e=f"{col('explanation')}{i}"; d=f"{col('difficulty')}{i}"; q=f"{col('question')}{i}"; s=f"{col('status')}{i}"
    f=(f'=IF({col("ref")}{i}="","",'
       f'IF(COUNTA({o})<4,"Needs 4 options",'
       f'IF(ISERROR(FIND(UPPER({a}),"ABCD"))+(LEN({a})<>1),"Answer must be A-D",'
       f'IF(OR({d}<1,{d}>3),"Difficulty must be 1-3",'
       f'IF(OR({q}="",{e}=""),"Missing question or explanation",'
       f'IF(COUNTBLANK({wn})<>1,"Need 3 why-not texts",'
       f'IF(INDEX({wn},1,FIND(UPPER({a}),"ABCD"))<>"","Why-not filled for the answer",'
       f'IF(AND({s}<>"live",{s}<>"draft",{s}<>"retired"),"Status must be live/draft/retired","OK"))))))))')
    c=ws.cell(i,ci['check'],f); c.font=Font(name=F,size=10,bold=True); c.fill=auto_fill; c.alignment=Alignment(vertical="top")
last = len(rows)+1
maxr = 3000
# editable fill on header? mark editable columns lightly in header row 1 via comment row? use column fill for data rows
for n in HDR[:-1]:
    if n=="reviewer_notes": continue
    for i in range(2,last+1):
        pass
ws.freeze_panes = "F2"
ws.auto_filter.ref = f"A1:{get_column_letter(len(HDR))}{last}"
# validations
def dv(formula, colname, prompt):
    v=DataValidation(type="list", formula1=formula, allow_blank=True, showErrorMessage=True, errorTitle="Not allowed", error=prompt)
    v.add(f"{col(colname)}2:{col(colname)}{maxr}"); ws.add_data_validation(v)
dv('"live,draft,retired"','status','Choose live, draft or retired.')
dv('"II,III,IV,V,VI,FEE,SW,GS"','chapter','Choose a chapter code.')
dv('"1,2,3"','difficulty','Choose 1, 2 or 3.')
dv('"A,B,C,D"','answer','Choose A, B, C or D.')
dv('"Y"','verify','Y or leave blank.')
# conditional formatting on check
rng=f"{col('check')}2:{col('check')}{maxr}"
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND({col("check")}2<>"",{col("check")}2<>"OK")'], fill=PatternFill("solid",fgColor="F8E6E4"), font=Font(color="B0281F",bold=True)))
ws.conditional_formatting.add(rng, FormulaRule(formula=[f'{col("check")}2="OK"'], font=Font(color="1D6A46",bold=True)))
sr=f"{col('status')}2:{col('status')}{maxr}"
ws.conditional_formatting.add(sr, FormulaRule(formula=[f'{col("status")}2="draft"'], fill=PatternFill("solid",fgColor="FBF0DC")))
ws.conditional_formatting.add(sr, FormulaRule(formula=[f'{col("status")}2="retired"'], font=Font(color="93A1AE",italic=True)))

# Summary sheet
sm = wb.create_sheet("Summary")
sm.sheet_view.showGridLines=False
sm.column_dimensions['A'].width=3; sm.column_dimensions['B'].width=32
for x in "CDEFG": sm.column_dimensions[x].width=12
sm['B2']="Question bank summary"; sm['B2'].font=Font(name=F,size=14,bold=True)
sm['B3']="Updates automatically from the Questions sheet."; sm['B3'].font=Font(name=F,color="5A6774")
hdrs=["Chapter","Live","Draft","Retired","Live Easy","Live Medium","Live Hard"]
# use B..H
sm.column_dimensions['H'].width=12
for j,hname in enumerate(hdrs):
    c=sm.cell(5,2+j,hname); c.font=Font(name=F,bold=True,color="FFFFFF"); c.fill=hdr_fill
chapters=[("II","Ch II · Registration of FPIs"),("III","Ch III · Approval of DDPs"),("IV","Ch IV · Investment conditions"),("V","Ch V · FPI obligations"),("VI","Ch VI · DDP obligations"),("FEE","2nd Schedule · Fees"),("SW","SWAGAT-FI"),("GS","GS-FPI")]
Q="Questions!"
chc=f"{Q}${col('chapter')}$2:${col('chapter')}${maxr}"; stc=f"{Q}${col('status')}$2:${col('status')}${maxr}"; dfc=f"{Q}${col('difficulty')}$2:${col('difficulty')}${maxr}"
r=6
for code,label in chapters:
    sm.cell(r,2,label).font=Font(name=F)
    sm.cell(r,9,code).font=Font(name=F,color="FFFFFF")  # hidden helper key
    k=f"$I{r}"
    sm.cell(r,3,f'=COUNTIFS({chc},{k},{stc},"live")')
    sm.cell(r,4,f'=COUNTIFS({chc},{k},{stc},"draft")')
    sm.cell(r,5,f'=COUNTIFS({chc},{k},{stc},"retired")')
    for j,dval in enumerate([1,2,3]):
        sm.cell(r,6+j,f'=COUNTIFS({chc},{k},{stc},"live",{dfc},{dval})')
    for j in range(3,9): sm.cell(r,j).font=Font(name=F)
    r+=1
sm.cell(r,2,"Total").font=Font(name=F,bold=True)
for j in range(3,9):
    L_=get_column_letter(j); c=sm.cell(r,j,f"=SUM({L_}6:{L_}{r-1})"); c.font=Font(name=F,bold=True); c.border=Border(top=Side(style="thin"))
r+=2
sm.cell(r,2,"Rows needing a fix").font=Font(name=F,bold=True)
sm.cell(r,3,f'=COUNTIFS({Q}${col("check")}$2:${col("check")}${maxr},"<>OK",{Q}${col("ref")}$2:${col("ref")}${maxr},"<>")').font=Font(name=F,bold=True,color="B0281F")
sm.cell(r+1,2,"Live questions needed for a 25-question round").font=Font(name=F,color="5A6774")
sm.cell(r+1,3,25).font=Font(name=F,color="0000FF")

wb.move_sheet("Questions", offset=-1)
wb.active = 0
wb.save("../question-bank/Question_Bank.xlsx")

# CSV the website reads
with open("../questions.csv","w",newline="",encoding="utf-8-sig") as fh:
    w=csv.writer(fh)
    w.writerow(HDR[:-1])
    for rw in rows: w.writerow([rw[n] for n in HDR[:-1]])
print("rows",len(rows))

#!/usr/bin/env python3
# SKILL NOTE (funding-opportunities-pipeline): the b2/b3 account lists and the contacts
# list embedded below are a SNAPSHOT dated 2026-07-12, and the transcript-
# parsing block for batch 1 only works in the original session. Before a
# rebuild: pull fresh accounts/contacts per references/monday-ids.md recipes,
# replace those data blocks, then run. After building, ALWAYS run
#   python /mnt/skills/public/xlsx/scripts/recalc.py <output.xlsx>
# and ship only on status=success with zero errors.
# The UP=/mnt/user-data/uploads list files and TRANSCRIPT path below are
# EXAMPLE INPUTS from one operator's 2026-07-12 rebuild; point them at your
# own uploaded lists/transcript before running.
"""Build JE Strategic Selling Workbook: live ICP scoring, contact map, blue sheet, gap analysis."""
import re, csv, difflib, warnings, unicodedata
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
warnings.filterwarnings('ignore')

UP = '/mnt/user-data/uploads/'
TRANSCRIPT = '/mnt/transcripts/2026-07-12-17-52-56-je-funding-pipeline-monday.txt'

# ---------- 1. Operator's book: parse batches from transcript (EXAMPLE INPUT) ----------
raw = open(TRANSCRIPT, encoding='utf-8', errors='ignore').read()
raw_u = raw.replace('\\\\"', '"').replace('\\"', '"').replace('\\\\n', ' ').replace('\\n', ' ')
pat = re.compile(r'"id":\s*"(\d+)",\s*"name":\s*"([^"]+)",\s*"url":\s*"https://johnston-engineering\.monday\.com/boards/7253021439/pulses/\d+"[^}]*?"column_values":\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}', re.S)
book = {}  # name -> dict
for m in pat.finditer(raw_u):
    iid, name, cols = m.group(1), m.group(2), m.group(3)
    def grab(cid):
        mm = re.search('"'+cid+r'":\s*(?:"([^"]*)"|null)', cols)
        return mm.group(1) if mm and mm.group(1) else ''
    book[name] = dict(id=iid, status=grab('color_mm1hq3s1'), loc=grab('location_mm1hwpre'),
                      ind=grab('dropdown_mm1sga1v'), fit=grab('dropdown_mm1h5y5v'))

# ---------- batch 2 (this session, typed) ----------
b2 = [
("Repela","Suspect","Detroit, MI","Manufacturing","Product Development"),
("Irrigreen","Suspect","Edina, MN","Hardware","Robotics Engineering, Product Development"),
("Brelyon","Suspect","San Mateo, CA","Consumer Electronics","Electronics Packaging, Product Development"),
("Eko Health","Suspect","Emeryville, CA","",""),
("Goiku Battery","Suspect","Osaka, Japan","Energy","Battery, Electronics Packaging"),
("Echandia","Suspect","Solna, Sweden","",""),
("LineVision","Suspect","Boston, MA","Energy","Sensors, Grid Scale"),
("SafeTraces","Suspect","Pleasanton, CA","Health Care","HVAC, Air Purification, Sensors"),
("Sojo Industries","Suspect","Bristol, PA","Manufacturing","Custom Machinery, Robotics Engineering, Manufacturing"),
("Elegen","Suspect","Menlo Park, CA","",""),
("CoreLift Inc.","Suspect","Sudbury, ON, Canada","Manufacturing","Mining, Custom Machinery"),
("Dimatec Inc.","Suspect","Manitoba, Canada","",""),
("Hevi","Suspect","East Windsor, NJ","Manufacturing","EV Technology, Custom Machinery, Battery"),
("Hidroport","Suspect","Ankara, Turkey","Manufacturing","Mining, Custom Machinery"),
("Icefield Tools Corporation","Suspect","Whitehorse, YT, Canada","Manufacturing","Mining, Sensors, Custom Machinery"),
("MARL Technologies Inc.","Suspect","Edmonton, AB, Canada","Manufacturing","Mining, Custom Machinery"),
("Minepro Hydraulics","Suspect","Sudbury, ON, Canada","Manufacturing","Mining, Fluid Analysis, Custom Machinery"),
("NACE Corp.","Suspect","Golden, CO","Natural Resources","Mining, Critical Mineral Recovery, Custom Machinery"),
("Njordair","Suspect","Bridgehampton, NY","Manufacturing","Structural, Custom System"),
("Blue World Technologies","Suspect","Aalborg, Denmark","Energy","Fuel Cells, Thermal Analysis, Electrochemical Process"),
("PopWheels","Suspect","Brooklyn, NY","",""),
("Attonics Systems","Suspect","Singapore","Science and Engineering","Electronics Packaging, Sensors"),
("Carbice","Suspect","Atlanta, GA","Consumer Electronics","Thermal Analysis, Electronics Packaging, Space"),
("Relectrify","Suspect","Melbourne, Australia","",""),
("Flexomarine S.A.","Suspect","Guarulhos, Brazil","Manufacturing","Fluid Analysis, Structural"),
("Fosina","Suspect","Danbury, CT","Sales and Marketing","Sensors"),
("FOXWATER","Suspect","Santo Antonio de Posse, Brazil","Manufacturing","Water Purification"),
("Enchi Corporation","Suspect","Hanover, NH","",""),
("Versogen","Suspect","Wilmington, DE","",""),
("AssetCool","Suspect","Leeds, UK","Energy","Robotics Engineering, Grid Scale, Custom Machinery"),
("Invinity Energy Systems","Suspect","London, UK","Energy","Energy Storage, Long Duration Energy Storage, Battery"),
("Foreseeson Technology Inc.","Suspect","Richmond, BC, Canada","Manufacturing","Electronics Packaging, EV Technology"),
("Intrinsic Power","Suspect","Los Angeles, CA","Energy","EV Technology, Power Conversion"),
("Aetherflux","Suspect","San Carlos, CA","Energy","Space, Aerospace, Solar"),
("ClimateCrete","Suspect","San Jose, CA","Sustainability","CO2 - Utilization, Decarbonization, Manufacturing"),
("Reefcycle","Suspect","New York, NY","Sustainability","CO2 - Utilization, Bioengineering"),
("Koniku","Suspect","San Rafael, CA","Biotechnology","Sensors, Biotechnology, Electronics Packaging"),
("Solx Energy","Suspect","Aguadilla, PR","Energy","Solar, Advanced Manufacturing, Renewable Energy"),
("Inovues","Suspect","Houston, TX","Energy","HVAC, Sustainable Aviation Fuels, Net Zero"),
("Novasolix","Suspect","Newark, CA","Energy","Solar, Semiconductor, Advanced Manufacturing"),
("Safire","Suspect","Pietermaritzburg, South Africa","Energy","Battery, Military, Defense"),
("Solight Design","Suspect","New York, NY","Consumer Goods","Solar, Product Development"),
("Nugen Systems","Suspect","Norcross, GA","Energy","Energy Storage, Battery"),
("Nxu","Suspect","Mesa, AZ","",""),
("Starstone","Suspect","Rehovot, Israel","Manufacturing","Chemical Process, Decarbonization, Bioengineering"),
("Rotostitch","Suspect","San Francisco, CA","Manufacturing","Custom Machinery, Advanced Manufacturing"),
("Planted Solar","Suspect","Oakland, CA","",""),
("GaNify LLC","Suspect","Santa Barbara, CA","Hardware","Semiconductor, Power Conversion, Fusion"),
("Mana Battery, Inc.","Suspect","Denver, CO","Energy","Battery, Energy Storage, Defense"),
("Chemspeed Technologies, Inc.","Suspect","Fullinsdorf, Switzerland","Science and Engineering","Chemical Process"),
("Oceanit Laboratories Inc.","Suspect","Honolulu, HI","",""),
("24M Technologies","Suspect","Cambridge, MA","Energy","Battery, Advanced Manufacturing, Energy Storage"),
("SeaLion Energy Inc.","Suspect","Pittsburgh, PA","Energy","Battery, Energy Storage"),
("Flexnode, Inc.","Suspect","Bethesda, MD","Information Technology","Containerized System, Cooling, Custom System"),
("2Witech Solutions LLC","Suspect","Lowell, MA","Sustainability","Sensors, Water Purification"),
("Aerodyne Research, Inc.","Suspect","Billerica, MA","Science and Engineering","Sensors, Aerospace"),
("AGC Plasma Technology Solutions","Suspect","Lauenforde, Germany","Manufacturing","Advanced Manufacturing, Electronics Packaging"),
("MetOx Technologies, Inc.","Suspect","Houston, TX","Energy","Grid Scale, Advanced Manufacturing, Energy Technology"),
("Opcondys, Inc.","Suspect","Manteca, CA","Energy","Power Conversion, EV Technology, Semiconductor"),
("American Elements","Suspect","Los Angeles, CA","Manufacturing","Critical Mineral Recovery"),
]
for n,s,l,i,f in b2:
    if n not in book:
        book[n] = dict(id='', status=s, loc=l, ind=i, fit=f)

# ---------- batch 3 (this session, typed) ----------
b3 = [
("Clarivate","Suspect","London, UK","Data and Analytics","Research Commercialization"),
("HighT-Tech","Suspect","Beltsville, MD","Manufacturing","Thermal Analysis, Advanced Manufacturing, Decarbonization"),
("Halliburton & Technology Partners LLC","Suspect","Houston, TX","Energy","Sensors, Geothermal"),
("MAHLE Powertrain","Suspect","Northampton, UK","Transportation","EV Technology, Product Development"),
("Naval Reactors","Suspect","Washington, DC","Government and Military","Nuclear, Military"),
("Sylvatex, Inc.","Suspect","Alameda, CA","Energy","Battery, Manufacturing, Chemical Process"),
("Advanced Cooling Technologies, Inc.","Suspect","Lancaster, PA","Manufacturing","Thermal Analysis, HVAC, Cooling"),
("JETCOOL Technologies, Inc.","Suspect","Littleton, MA","",""),
("Melni Technologies","Suspect","Twin Falls, ID","Hardware","Electronics Packaging, Product Development"),
("NovoLINC, Inc.","Suspect","Pittsburgh, PA","Hardware","Thermal Analysis, Electronics Packaging, Semiconductor"),
("OnTo Technology, LLC","Suspect","Bend, OR","Energy","Battery, Recycling, Chemical Process"),
("PowerN, Inc.","Suspect","Raleigh, NC","",""),
("QuesTek Innovations LLC","Suspect","Evanston, IL","Science and Engineering","Product Development, DFM"),
("Serinus Labs, Inc.","Suspect","Berkeley, CA","Hardware","Sensors, Semiconductor, Electronics Packaging"),
("Scaled Power Solutions","Suspect","Arlington, VA","Energy","Power Conversion, Grid Scale, Electronics Packaging"),
("Solid Power, Inc.","Suspect","Louisville, CO","Energy","Battery, EV Technology, Manufacturing"),
("SixPoint Materials, Inc.","Suspect","Buellton, CA","Hardware","Semiconductor, Manufacturing"),
("South 8 Technologies, Inc.","Suspect","San Diego, CA","",""),
("Virtus Solis Technologies, Inc.","Suspect","Troy, MI","",""),
("FyberX","Suspect","Williamsburg, VA","Sustainability","Circular Materials, Manufacturing"),
("Aesir Technologies","Suspect","Joplin, MO","Energy","Battery, Manufacturing, Defense"),
("Renewlogy","Suspect","Salt Lake City, UT","Sustainability","Pyrolysis, Recycling, Chemical Process"),
("Capro-X","Suspect","Ithaca, NY","Biotechnology","Bioreactor, Biomanufacturing, Chemical Process"),
("Sulas Industries","Suspect","Silverthorne, CO","Energy","Solar, Custom Machinery"),
("OptiFuel Systems","Suspect","Beaufort, SC","",""),
("Methylennium Energy","Suspect","Falls Church, VA","Energy","CO2 - Utilization, Chemical Process, Hydrogen"),
("Elven Technologies","Suspect","Rancho Cordova, CA","",""),
("PowerTap Hydrogen Fueling Corp.","Suspect","Aliso Viejo, CA","",""),
("Raven Sr","Suspect","Pinedale, WY","Energy","Hydrogen, Chemical Process, Custom Machinery"),
("Leading Edge Equipment Technologies","Suspect","Wilmington, MA","Manufacturing","Solar, Custom Machinery, Semiconductor"),
("Avium","Suspect","Lawrence, KS","Energy","Electrolyzer, Hydrogen, Electrochemical Process"),
("Vespene Energy","Suspect","Berkeley, CA","",""),
("Skip Technology","Suspect","Portland, OR","Energy","Energy Storage, Long Duration Energy Storage, Battery"),
("Lydian","Suspect","Cambridge, MA","Energy","Sustainable Aviation Fuels, Chemical Process, Custom Machinery"),
("Anode","Suspect","San Francisco, CA","Energy","Energy Storage, Battery, Custom System"),
("Alchemist Material Inc.","Suspect","Sunnyvale, CA","Sustainability","Hydrogen, Recycling, Chemical Process"),
("Phuc Labs","Suspect","Boston, MA","",""),
("Estes Energy","Suspect","San Francisco, CA","",""),
("Claros Technologies","Suspect","Minneapolis, MN","Sustainability","Water Remediation, Chemical Process, Custom Machinery"),
("Agami Zero","Suspect","Boulder, CO","Energy","Hydrogen, Electrolyzer, Custom System"),
("Influit Energy","Suspect","Chicago, IL","Energy","Energy Storage, Battery, Chemical Process"),
("NOMAD Transportable Power Systems","Suspect","Waterbury, VT","Energy","Energy Storage, Containerized System, Battery"),
("Johnson Energy Storage","Suspect","Atlanta, GA","",""),
("Split Energy llc","Suspect","New York, NY","Energy","Energy Storage, Battery"),
("Unicorn Biotechnologies","Suspect","Sheffield, UK","",""),
("Factorial Energy","Suspect","Woburn, MA","Energy","Battery, EV Technology, Manufacturing"),
("Carbonade","Suspect","Ness Ziona, Israel","Sustainability","CO2 - Utilization, Electrochemical Process, Chemical Process"),
("Fenix Energy","Suspect","Lyon, France","Energy","Thermal Analysis, HVAC, Energy Technology"),
("Midnight Sun Mining","Suspect","Vancouver, Canada","Natural Resources","Mining, Metals & Mining Solutions"),
("ExxonMobil","Suspect","Spring, TX","",""),
("Astral Materials","Suspect","Mountain View, CA","Hardware","Space, Semiconductor, Custom Machinery"),
("Matereal","Suspect","Denver, CO","Sustainability","Circular Materials, Manufacturing"),
("Ares Industries","Suspect","El Segundo, CA","Government and Military","Defense, Custom Machinery, Manufacturing"),
("Woodland Biomass Innovations","Suspect","Wellsboro, PA","",""),
("AMS","Suspect","Everett, WA","Hardware","Thermal Analysis, Electronics Packaging"),
("New Frontier Aerospace","Suspect","Kent, WA","Government and Military","Aerospace, Defense, Custom Machinery"),
("MightyFly","Suspect","San Francisco, CA","Transportation","Aerospace, Robotics Engineering, Custom Machinery"),
("ZeroMark","Suspect","New York, NY","",""),
("Varda Space Industries","Suspect","El Segundo, CA","",""),
("Juno Propulsion","Suspect","Seattle, WA","",""),
]
for n,s,l,i,f in b3:
    if n not in book:
        book[n] = dict(id='', status=s, loc=l, ind=i, fit=f)

print(f"Book size: {len(book)} accounts (transcript batches + batch 3)")

# ---------- funding angle map ----------
angle = {
"Hybrium":"DARPA ExCAIPE (7/22) + DoD 8/19 wave","XtraLit":"CMMA TA3 (7/23) + DARPA Smash","Pure Energy Minerals":"CMMA TA3 + NV lithium corridor","NORAM NESI":"CMMA TA3 + ISC Canada","Bardo Climate":"CMMA TA3 + CO OEDIT","NACE Corp.":"CMMA TA3 + CO OEDIT","American Elements":"CMMA TA3 + DARPA Smash","Critical Materials Recycling":"CMI/Ames licensee (ADR) + E-Scrap Prize","Intel-E-Waste":"E-Scrap Prize + PA Ben Franklin","Cool Amps":"Argonne ReCell license + CMI Li-ion leach patent","24M Technologies":"DARPA ExPEDitions (8/19) + Argonne ACCESS","Mana Battery, Inc.":"DARPA ExPEDitions (8/19) — defense battery bullseye","SeaLion Energy Inc.":"ExPEDitions + PA Ben Franklin","Safire":"ExPEDitions (VERIFY: wrong-company contacts loaded)","Aesir Technologies":"ExPEDitions + defense battery","Influit Energy":"ExPEDitions (nanoelectrofuel)","Goiku Battery":"ExPEDitions / Argonne ACCESS","Nugen Systems":"ExPEDitions / Argonne ACCESS","Hevi":"Argonne ACCESS + EV/battery","Invinity Energy Systems":"Grid storage — WA CEF / NYSERDA","Solid Power, Inc.":"CO OEDIT + ExPEDitions (solid-state)","Factorial Energy":"ExPEDitions (solid-state) + MA","OnTo Technology, LLC":"OR Business Oregon + Argonne ReCell + E-Scrap Prize","Skip Technology":"OR Business Oregon + LDES","Renewlogy":"Re-X Before Recycling Prize","Phuc Labs":"E-Scrap Prize (vision-based sorting)","H Quest":"WY REE-from-coal + PA BFTP + DoD 8/19","SunToWater":"DARPA ExCAIPE (water) + CA CalSEED","Hydroplane":"DoD 8/19 (H2 aviation) + CA","BWR Innovations":"DoD 8/19 (portable fuel cell) + ND","STARS Technology Corporation":"WA CEF + DOE H2 (NLR HydroGEN)","ExoFusion":"DOE fusion + WA CEF","Jetti":"CO OEDIT + critical minerals","Capra Biosciences":"DARPA BTO BAA (9/30) — already DoD-funded","Koniku":"DARPA BTO BAA (9/30)","Carbice":"DoD 8/19 (thermal) + GA","Aetherflux":"DoD/SDA space power","Oceanit":"DoD 8/19 — SBIR powerhouse partner","Raven Sr":"WY Energy Authority match — Pinedale HQ","Avium":"DOE H2 + KS","Agami Zero":"CO OEDIT + DOE H2","Claros Technologies":"Launch MN match + water/PFAS","Melni Technologies":"ID IGEM + DLA","GaNify LLC":"CMMA GaN topics + DoD (VERIFY contact email)","Opcondys, Inc.":"CMMA/ARPA-E power electronics","Novasolix":"CMMA GaN/solar mfg","NOMAD Transportable Power Systems":"DoD expeditionary + containerized","Capro-X":"NYSERDA + USDA SBIR","Sulas Industries":"CO OEDIT + solar machinery","Matereal":"CO OEDIT + circular materials","Astral Materials":"DoD space + semiconductor","Ares Industries":"DoD 8/19 + defense mfg","New Frontier Aerospace":"DoD 8/19 + WA","Varda Space Industries":"DoD/space mfg","QuesTek Innovations":"DoD materials (ICMD) + DFM synergy","Advanced Cooling Technologies, Inc.":"DoD thermal + PA BFTP","NovoLINC, Inc.":"DoD thermal + PA BFTP","JETCOOL Technologies, Inc.":"DoD thermal / datacenter cooling",
}

# ---------- ICP industry-fit prefill from tags ----------
CORE = ['custom machinery','thermal analysis','battery','electrolyzer','hydrogen','critical mineral','electrochemical','chemical process','energy storage','electronics packaging','dfm','containerized','recycling','fuel cell','bioreactor','robotics','power conversion','semiconductor','aerospace','defense','mining','sensors','cooling','hvac','custom system','nuclear','pyrolysis','solar','manufacturing','structural','fluid analysis','test']
def industry_fit(fit, ind):
    t = (fit or '').lower()
    hits = sum(1 for k in CORE if k in t)
    if hits >= 3: return 5
    if hits == 2: return 4
    if hits == 1: return 3
    if (ind or '') in ('Energy','Manufacturing','Hardware','Government and Military','Natural Resources','Science and Engineering','Sustainability','Biotechnology','Transportation'): return 2
    if ind: return 1
    return ''

# ---------- normalize & match ----------
SUFFIX = re.compile(r'\b(inc|llc|corp|corporation|ltd|co|company|plc|sa|s\.a\.|gmbh|technologies|technology|tech|systems|solutions|energy|group|holdings|labs|laboratories)\b\.?', re.I)
def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode()
    s = re.sub(r'\([^)]*\)',' ', s)
    s = re.sub(r'[^a-z0-9 ]',' ', s.lower())
    s = SUFFIX.sub(' ', s)
    return re.sub(r'\s+',' ',s).strip()
book_norm = {norm(n): n for n in book}
book_norm_keys = list(book_norm.keys())
def in_book(name):
    n = norm(name)
    if not n: return None
    if n in book_norm: return book_norm[n]
    for bk in book_norm_keys:
        if bk and n and (bk == n or (len(n)>4 and len(bk)>4 and (bk.startswith(n) or n.startswith(bk)))):
            return book_norm[bk]
    close = difflib.get_close_matches(n, book_norm_keys, n=1, cutoff=0.92)
    return book_norm[close[0]] if close else None

# ---------- load lists ----------
JUNK = re.compile(r'\b(association|institute|society|network|news|media|university|college|jobs|magazine|coalition|consortium|department|administration|summit|conference|expo|journal|academy|council|agency|ministry|foundation|alliance|committee|bureau|command|office of|club|festival|press|review|times|weekly|\.gov|air force|navy|army|nsin|clearedjobs|advisor|advisors|partnership|consulting|consultants|capital|ventures|fund|investor|millennial|recruiting|staffing|marketing)\b', re.I)
gap = {}  # norm -> dict(name, sources set, desc, score)
KW = {5:['critical mineral','rare earth','electrolyz','battery recycl','lithium extract','battery manufactur','solid.state batter','hydrogen product','fuel cell','direct air capture','pilot plant','thermal management','magnet recycl'],
      4:['battery','energy storage','hydrogen','geotherm','nuclear','reactor','carbon capture','co2','electrochem','recycling','desalin','water treat','semiconductor','power electron','gan ','sic ','mining','critical material','heat exchang','turbine','propulsion','biomanufactur','bioreactor','pyrolysis','grid.scale','microgrid','long.duration'],
      3:['solar','wind','clean energy','renewable','manufactur','robotic','aerospace','defense','drone','sensor','thermal','cooling','hvac','materials','3d print','additive','ev charg','electric vehicle','space','satellite','machin','hardware','automation','storage']}
def kw_score(text):
    t = ' '+re.sub(r'[^a-z0-9 ]',' ', str(text).lower())+' '
    for sc in (5,4,3):
        for k in KW[sc]:
            if re.search(k, t): return sc, k.strip()
    return 0, ''
def add_gap(name, source, desc=''):
    name = str(name).strip()
    if not name or len(name)<3 or name.lower()=='nan': return
    if JUNK.search(name): return
    n = norm(name)
    if not n: return
    hit = in_book(name)
    if hit: return  # already in the operator's book
    sc, kw = kw_score(name+' '+str(desc))
    if sc < 3: return
    d = str(desc).strip()[:160] if desc and str(desc)!='nan' else ''
    if n in gap:
        gap[n]['sources'].add(source)
        if sc > gap[n]['score']: gap[n]['score'], gap[n]['kw'] = sc, kw
        if d and len(d) > len(gap[n]['desc']): gap[n]['desc'] = d
    else:
        gap[n] = dict(name=name, sources={source}, desc=d, score=sc, kw=kw)

# energy.xlsx
df = pd.read_excel(UP+'energy.xlsx', sheet_name='Sheet2')
for _, r in df.iterrows():
    add_gap(r.get('company name'), 'energy.xlsx', f"{r.get('Unnamed: 1','')} | {r.get('Unnamed: 3','')} | {r.get('Unnamed: 4','')}")
# energy_TECH.csv
for row in csv.reader(open(UP+'energy_TECH.csv', encoding='utf-8', errors='ignore')):
    if row: add_gap(row[0], 'energy_TECH.csv')
# ARPA-E Summit
df = pd.read_excel(UP+'ARPAE_Energy_Innovation_Summit_2026_April_7-9___San_Diego.xlsx')
for _, r in df.iterrows(): add_gap(r.get('Company Name'), 'ARPA-E Summit 2026', r.get('Description',''))
# Cali qualified (pre-qualified: force include)
df = pd.read_excel(UP+'Cali_Clean_Energy_Conference_Qualified.xlsx')
for _, r in df.iterrows():
    nm = str(r.get('Company Name','')).strip()
    if not nm or in_book(nm): continue
    n = norm(nm)
    d = str(r.get('Hardware Indicator',''))[:160]
    if n in gap: gap[n]['sources'].add('Cali Clean Energy Conf'); gap[n]['score']=max(gap[n]['score'],4)
    else: gap[n] = dict(name=nm, sources={'Cali Clean Energy Conf'}, desc=d, score=4, kw='pre-qualified')
# TechCrunch battlefield
df = pd.read_excel(UP+'startup_battlefield_TECHCRUNCH.xlsx', sheet_name='Startups Table')
for _, r in df.iterrows(): add_gap(r.get('Company'), 'TechCrunch Battlefield', f"{r.get('Category','')} | {r.get('Location','')} | {r.get('Funding','')}")
# 75 top startups
xl = pd.ExcelFile(UP+'75_top_american_start_ups.xlsx')
try:
    d2 = xl.parse('Sheet2')
    for _, r in d2.iterrows(): add_gap(r.get('Company'), '75 Top US Startups', r.get('Description',''))
except Exception: pass
try:
    d1 = xl.parse('Sheet1', index_col=0)
    for nm, r in d1.iterrows(): add_gap(nm, '75 Top US Startups', str(r.get('Location','')))
except Exception: pass
# Space tech
df = pd.read_excel(UP+'Airtable_-_Grid_view_Space_Tech_startups.xlsx')
for _, r in df.iterrows(): add_gap(r.get('Company Name'), 'Space Tech list', 'space tech startup')
# Food biotech (col 0)
df = pd.read_excel(UP+'Airtable_-_Food_BioTech_Startups.xlsx')
for v in df.iloc[:,0].dropna(): add_gap(v, 'Food BioTech list', 'food biotech startup')
# OTC QX
df = pd.read_excel(UP+'Best_50_OTC_QX_2026.xlsx')
for _, r in df.iterrows(): add_gap(r.get('Company'), 'OTC-QX Best 50', 'public small-cap')
# Energy Storage Coalition
df = pd.read_excel(UP+'Energy_Storage_Coalition.xlsx')
for _, r in df.iterrows(): add_gap(r.get('Company Name'), 'Energy Storage Coalition', 'energy storage coalition member')
# ACS
df = pd.read_excel(UP+'ACS__American_Chemical_Society___conference_list.xlsx')
for v in df.iloc[:,0].dropna(): add_gap(v, 'ACS conference list', 'chemistry/materials')

gaps = sorted(gap.values(), key=lambda d: (-d['score'], -len(d['sources']), d['name']))
multi = [g for g in gaps if len(g['sources'])>1]
print(f"Gap candidates (qualified, not in book): {len(gaps)}; on multiple lists: {len(multi)}")

# ---------- contacts (84 pulled this session) ----------
E,T,U='Economic Buyer','Technical Buyer','User Buyer'
contacts = [
("Bardo Climate","Allison Crow","Senior Chemical Engineer","Sr. Engineer / Scientist","allison@bardoclimate.com",""),
("Raven Sr","John Scanlon","General Counsel","Other","john.scanlon@ravensr.com",""),
("Raven Sr","Julianne Thomas","Director Of External Affairs","Director","julianne.thomas@ravensr.com",""),
("STARS Technology","Richard Zheng","Chief Engineer","C-Suite","richard.zheng@starsh2.com",T),
("STARS Technology","Dennis Walters","","","Dennis.Walters@StarsH2.com",""),
("Jetti","Carrie Boyle","Director of Instructor Training","Director","","⚠ verify right Jetti"),
("Cool Amps","Lonnie Garris","Chief Executive Officer","C-Suite","lonnie@coolamps.tech",E),
("Cool Amps","Joe Transue","Director of Manufacturing","Director","joe@coolamps.tech",U),
("Capra Biosciences","Elizabeth Onderko","Chief Executive Officer","C-Suite","liz@caprabiosciences.com",E),
("Capra Biosciences","Andrew Magyar","Co-Founder","Co-Founder","andrew@caprabiosciences.com",E),
("Capra Biosciences","Ryan Bing","Metabolic Engineering Group Lead","Lead","ryan@caprabiosciences.com",U),
("Capra Biosciences","Hillary Roberts","Chief of Staff, Business Lead","Other","hr@caprabiosciences.com",""),
("Capra Biosciences","Faraseldin Ali","Software & Electronics Instrumentation Engineer","Engineer / Scientist","faraseldinali@caprabiosciences.com",U),
("H Quest","Vignesh Viswanathan","Technical Program Manager","Manager","vignesh.viswanathan@h-quest.com",U),
("H Quest","Kurt Zeller","Senior Microwave Engineer","Sr. Engineer / Scientist","kurt.zeller@h-quest.com",T),
("H Quest","Christian Johns","Senior R&D Specialist & Facility Manager","Sr. Manager","christian.johns@h-quest.com",U),
("H Quest","Steve Hubbard","Chief Financial Officer","C-Suite","steve.hubbard@h-quest.com",E),
("H Quest","Nicholas Murolo","Systems Engineer II","Engineer / Scientist","",U),
("SunToWater","Martin Greenstein","Water Resources Specialist","Analyst / Specialist","martin@suntowater.com",U),
("SunToWater","Alexia Borenstein","Director of Public Relations","Director","",""),
("NACE Corp.","Fabrice Demtare","CEO","C-Suite","fabrice.demtare@nacecorp.com",E),
("NACE Corp.","Jonathan Payne","VP of Exploration","VP","jon.payne@nacecorp.com",U),
("NACE Corp.","Carl T. Delfeld","Chairman of the Executive Board","President / Chairman","carl.delfeld@nacecorp.com",E),
("Claros Technologies","Michelle Bellanca","Chief Executive Officer","C-Suite","michelle@clarostech.com",E),
("Claros Technologies","Heidi Zinky","Director of Engineering Implementation","Director","heidi@clarostech.com",U),
("Claros Technologies","John Brockgreitens","VP of Product Development","VP","john@clarostech.com",T),
("Claros Technologies","James McKone","Senior Director of R&D","Sr. Director","jmckone@pitt.edu",T),
("Claros Technologies","Evan Bloom","Engineer III","Engineer / Scientist","evan@clarostech.com",U),
("Factorial Energy","Siyu Huang","Founder and CEO","C-Suite","sh1@factorialenergy.com",E),
("Factorial Energy","Alex Yu","Founder and CTO","C-Suite","yy377@factorialenergy.com",T),
("Factorial Energy","Srinath Chakravarthy","Sr. Director - R&D, Simulation and AI","Sr. Director","sc@factorialenergy.com",T),
("Factorial Energy","Fanny Qing Chen","Senior Director, Operations","Sr. Director","fc@factorialenergy.com",U),
("Factorial Energy","Joanna Burdynska","Director R&D","Director","jburdynska@factorialenergy.com",T),
("Factorial Energy","Fang Hao","Director, Process","Director","fh@factorialenergy.com",U),
("Factorial Energy","Chee Neo","Sr. Manager of Process Development","Sr. Manager","chee.neo@factorialenergy.com",U),
("Factorial Energy","Daniel Jossman","VP of Business Operations","VP","jd@factorialenergy.com",""),
("Factorial Energy","Hyunseok Kim","VP of R&D","VP","hk@factorialenergy.com",T),
("Carbice","Baratunde Cola","CEO and Founder","C-Suite","bara.cola@carbice.com",E),
("Carbice","Craig Green, PhD","Chief Technology Officer","C-Suite","craig.green@carbice.com",T),
("Carbice","Hal Lasky","Chief Operating Officer","C-Suite","hal.lasky@carbice.com",E),
("Carbice","Jeff Freeman","Director Of Operations","Director","jeff.freeman@carbice.com",U),
("Carbice","Leonardo Prinzi","Product Director","Director","leo.prinzi@carbice.com",U),
("Invinity Energy Systems","Andy Klassen","Chief Technology Officer","C-Suite","aklassen@invinity.com",T),
("Invinity Energy Systems","Anthony Van Grol","Director Of Hardware Engineering","Director","avangrol@invinity.com",U),
("Invinity Energy Systems","Mike Meehan","Director of Products","Director","mmeehan@invinity.com",U),
("Invinity Energy Systems","Nicola Watson","Director - Solutions Engineering (BESS)","Director","nwatson@invinity.com",U),
("Invinity Energy Systems","Steve Mallinson","Director, Program Management","Director","smallinson@invinity.com",U),
("Invinity Energy Systems","Hitesh Kansodariya","Lead Power Block Team","Lead","hkansodariya@invinity.com",U),
("Invinity Energy Systems","Eric Brooker, P.Eng.","Team Lead - Balance Of Systems Design","Lead","ebrooker@invinity.com",U),
("Invinity Energy Systems","Rupak Banerjee, PhD","Battery Stack Mechanical Engineer","Engineer / Scientist","rbanerjee@invinity.com",U),
("Invinity Energy Systems","David Hunter","Manufacturing Engineering Manager","Manager","dhunter@invinity.com",U),
("Mana Battery","Nick Singstock","Co-founder and CTO","C-Suite","nick@manabattery.us",T),
("Mana Battery","Tyler Evans","Co-Founder, CEO","C-Suite","tyler@manabattery.us",E),
("Mana Battery","Tyler Bassett","Staff Process Engineer","Sr. Engineer / Scientist","tyler@manabattery.us",U),
("Mana Battery","Sam Jaffe","VP of Business Development and Product","VP","sam@manabattery.us",""),
("Mana Battery","Peter Hosbein","Senior Cell Engineer","Sr. Engineer / Scientist","peter@manabattery.us",T),
("Safire","Megan Stella","Chief Operating Officer","C-Suite","mstella@safireinsurance.com","⚠ WRONG CO (insurance)"),
("Safire","Neil Huntley","Head Of Risk","Head of","nhuntley@safireinsurance.com","⚠ WRONG CO (insurance)"),
("Safire","Kevin Meyer","Head of Capital","Head of","kmeyer@safireinsurance.com","⚠ WRONG CO (insurance)"),
("Safire","Gregory Botha","Claims Manager","Manager","gbotha@safireinsurance.com","⚠ WRONG CO (insurance)"),
("Safire","Julie Harvey","Head of Internal Audit","Head of","jharvey@safireinsurance.com","⚠ WRONG CO (insurance)"),
("GaNify","Yixin Xiong","Senior Device and Process Engineer","Sr. Engineer / Scientist","yxiong@google.com","⚠ google email — verify"),
("Opcondys","Stephen E. Sampayan","Chief Technology Officer","C-Suite","stephensa@opcondys.com",T),
("Opcondys","Kristin Sampayan","CEO","C-Suite","kristinsa@opcondys.com",E),
("24M Technologies","Hiroyuki Yumoto","SVP, Product and Development","EVP / SVP","hyumoto@24-m.com",T),
("24M Technologies","Jenny Carter","SVP, Global Operations","EVP / SVP","jcarter@24-m.com",U),
("24M Technologies","Tyler Eusden","Director of Engineering Operations","Director","teusden@24-m.com",U),
("24M Technologies","Daniel C","Manager, Advanced Manufacturing","Manager","danny@24-m.com",U),
("24M Technologies","Ben Sloan","Director, Impervio Program Management","Director","bsloan@24-m.com",U),
("24M Technologies","Richard Chleboski","CFO and COO","C-Suite","rchleboski@24-m.com",E),
("24M Technologies","Panuporn Udompansa","Director Of Products","Director","pudompansa@24-m.com",U),
("24M Technologies","Glenn Jordan","Senior Principal Engineer","Principal","gjordan@24-m.com",T),
("24M Technologies","Nutthaphon Phattharasupakun","R&D Engineering Manager","Manager","nphattharasupakun@24-m.com",U),
("24M Technologies","Xiaoming Liu","Manager, Advanced R&D","Manager","xliu@24-m.com",U),
("American Elements","Scott Michel","COO","C-Suite","scott.michel@americanelements.com",E),
("American Elements","Gabriel D. Leis","Head of Additive Manufacturing","Head of","gabriel.leis@americanelements.com",U),
("American Elements","Annie Simons","Director of Sales & Business Development","Director","annie.simons@americanelements.com",""),
("Solid Power","Josh Buettner-Garrett","CTO","C-Suite","josh.garrett@solidpowerbattery.com",T),
("Solid Power","Derek Johnson","Chief Operating Officer","C-Suite","derek.johnson@solidpowerbattery.com",E),
("Solid Power","Emily Achterberg","Sr Director Operations Engineering","Sr. Director","emily.achterberg@solidpowerbattery.com",U),
("Solid Power","Joseph Duchaj","Senior Director of Equipment Engineering","Sr. Director","joe.duchaj@solidpowerbattery.com",U),
("Solid Power","Lauren McCabe","EVP, Strategic Ops & Electrolyte Tech","EVP / SVP","lauren.mccabe@solidpowerbattery.com",E),
("OnTo Technology","Steve Sloop","President","President / Chairman","ssloop@onto-technology.com",E),
("OnTo Technology","Laura Nussel","Process Engineer","Engineer / Scientist","lnussel@onto-technology.com",U),
]
NO_CONTACT = ["Hybrium Energy","XtraLit","BWR Innovations","ExoFusion","Aetherflux","Oceanit Laboratories","Avium","Pure Energy Minerals","NORAM NESI","Intel-E-Waste","Critical Materials Recycling"]

# ================= BUILD WORKBOOK =================
wb = openpyxl.Workbook()
AR = 'Arial'
def F(sz=10, b=False, c='000000'): return Font(name=AR, size=sz, bold=b, color=c)
BLUE = Font(name=AR, size=10, color='0000FF'); YEL = PatternFill('solid', fgColor='FFFF00')
HDR = PatternFill('solid', fgColor='1F3864'); HDRF = Font(name=AR, size=10, bold=True, color='FFFFFF')
SUB = PatternFill('solid', fgColor='D9E1F2'); GOLD = PatternFill('solid', fgColor='FFC000')
thin = Side(style='thin', color='BFBFBF'); BORD = Border(left=thin,right=thin,top=thin,bottom=thin)

# ---- READ ME ----
ws = wb.active; ws.title = 'READ ME'
ws.column_dimensions['A'].width = 118
rows = [
("JOHNSTON ENGINEERING — STRATEGIC SELLING WORKBOOK", 14, True),
("Built from the 2026 Strategic Selling training (Miller/Heiman) + your monday CRM (180 accounts, 84 contacts at top targets).", 10, False),
("", 10, False),
("HOW THE LIVE SCORING WORKS (Account Scorecard tab)", 11, True),
("• The 5 Ideal Customer Criteria from the training: Industry Fit, Company Size Fit, Compelling Event Present, Access to Economic Buyer, Growth/Follow-On Work Potential. Score each 0–5 (5 = best aligned).", 10, False),
("• Row 2 holds the WEIGHTS (blue cells). Change a weight and every account re-scores and re-ranks instantly. Default = 1.0 each; e.g. set Compelling Event to 2.0 to favor deals with a live funding deadline.", 10, False),
("• Weighted Score % = SUMPRODUCT(your scores × weights) ÷ max possible. Rank and A–D tier update automatically.", 10, False),
("• Industry Fit is pre-scored from your CRM capability tags (blue = my suggestion, edit freely). Yellow cells are yours to fill — blanks count as 0, and the 'Criteria left' column shows how many are unscored.", 10, False),
("", 10, False),
("COLOR LEGEND: blue text = editable input/suggestion · yellow fill = fill these in · black = live formula (don't overwrite)", 10, True),
("", 10, False),
("TABS", 11, True),
("• Account Scorecard — all 180 accounts, live weighted ICP ranking + funding angle from your pipeline board.", 10, False),
("• Buying Influences — contact map for top accounts. Role/Degree/Mode/Rating dropdowns straight from the training. 21 obvious Economic/Technical/User buyers are pre-tagged (also pushed to monday); Coaches are never auto-assigned — the deck says you develop them. Red-flag rows list accounts with ZERO contacts (uncovered bases).", 10, False),
("• Blue Sheet — one-deal Strategic Analysis Plan modeled on your JE template. Duplicate the tab per deal.", 10, False),
("• Gap Analysis — qualified companies found across your uploaded lists (ARPA-E Summit, Cali conference, TechCrunch, energy lists, storage coalition, etc.) that are NOT in your book. Sorted by fit; multi-list appearances flagged.", 10, False),
("", 10, False),
("Data note: Safire contacts in the CRM are from Safire Insurance (South Africa) — wrong company vs. your defense-battery Safire. GaNify's contact has a google.com email. Both flagged in Buying Influences.", 10, False),
]
for i,(t,sz,b) in enumerate(rows,1):
    ws.cell(row=i,column=1,value=t).font = F(sz,b); ws.cell(row=i,column=1).alignment = Alignment(wrap_text=True, vertical='top')

# ---- Lists (validation sources) ----
wl = wb.create_sheet('Lists')
lists = {
 'A': ('Role', ['Economic Buyer','User Buyer','Technical Buyer','Coach']),
 'B': ('Degree', ['High','Medium','Low']),
 'C': ('Mode', ['Growth','Trouble','Even Keel','Overconfident']),
 'D': ('Rating', ['+5 Strong Positive','+3 Mild Positive','0 Neutral','-3 Mild Negative','-5 Strong Negative']),
 'E': ('Competition', ['Exclusive','Dominant','Shared','Zero']),
 'F': ('Funnel', ['Universe','Above','In','Best Few','Won','Lost']),
 'G': ('Timing', ['Urgent','Active','Work It In','Later']),
 'H': ('Score05', ['0','1','2','3','4','5']),
}
for col,(nm,vals) in lists.items():
    wl[f'{col}1'] = nm; wl[f'{col}1'].font = F(10,True)
    for i,v in enumerate(vals,2): wl[f'{col}{i}'] = v; wl[f'{col}{i}'].font = F()
wl.sheet_state = 'hidden'

# ---- Account Scorecard ----
sc = wb.create_sheet('Account Scorecard')
crit = ['Industry Fit','Company Size Fit','Compelling Event Present','Access to Economic Buyer','Growth/Follow-On Potential']
sc['A1'] = 'ACCOUNT SCORECARD — live weighted ICP ranking (edit blue/yellow; formulas do the rest)'; sc['A1'].font = F(12,True)
sc['A2'] = 'WEIGHTS →'; sc['A2'].font = F(10,True); sc['A2'].alignment = Alignment(horizontal='right')
headers = ['Account','Status','Industry','Capability tags','Location','Funding angle (from pipeline board)'] + crit + ['Weighted Score %','Rank','Tier','Criteria left']
CI = {h: i+1 for i,h in enumerate(headers)}
for h,i in CI.items():
    c = sc.cell(row=3, column=i, value=h); c.font = HDRF; c.fill = HDR; c.alignment = Alignment(wrap_text=True, vertical='center'); c.border = BORD
for j in range(len(crit)):
    w = sc.cell(row=2, column=CI['Industry Fit']+j, value=1.0); w.font = BLUE; w.fill = YEL; w.border = BORD
WT1 = get_column_letter(CI['Industry Fit']); WT2 = get_column_letter(CI['Growth/Follow-On Potential'])
acct_rows = sorted(book.items(), key=lambda kv: ({'Lead':0,'Prospect':1,'Suspect':2}.get(kv[1]['status'],3), kv[0].lower()))
r = 4
for name, d in acct_rows:
    sc.cell(row=r, column=CI['Account'], value=name).font = F(10,True)
    sc.cell(row=r, column=CI['Status'], value=d['status']).font = F()
    sc.cell(row=r, column=CI['Industry'], value=d['ind']).font = F()
    sc.cell(row=r, column=CI['Capability tags'], value=d['fit']).font = F(9)
    sc.cell(row=r, column=CI['Location'], value=d['loc']).font = F(9)
    ang = ''
    for k,v in angle.items():
        if norm(k) == norm(name) or norm(k) in norm(name) or norm(name) in norm(k): ang = v; break
    sc.cell(row=r, column=CI['Funding angle (from pipeline board)'], value=ang).font = F(9, c='7030A0')
    ifit = industry_fit(d['fit'], d['ind'])
    c1 = sc.cell(row=r, column=CI['Industry Fit'], value=ifit if ifit != '' else None); c1.font = BLUE; c1.border = BORD
    for j in range(1,5):
        cc = sc.cell(row=r, column=CI['Industry Fit']+j); cc.fill = YEL; cc.border = BORD; cc.font = BLUE
    sr1 = f'{WT1}{r}'; sr2 = f'{WT2}{r}'
    sc.cell(row=r, column=CI['Weighted Score %'], value=f'=IFERROR(SUMPRODUCT({sr1}:{sr2},${WT1}$2:${WT2}$2)/(5*SUM(${WT1}$2:${WT2}$2)),0)').font = F(10,True)
    sc.cell(row=r, column=CI['Weighted Score %']).number_format = '0.0%'
    last = 3 + len(acct_rows)
    WS = get_column_letter(CI['Weighted Score %'])
    sc.cell(row=r, column=CI['Rank'], value=f'=IF({WS}{r}=0,"",RANK({WS}{r},${WS}$4:${WS}${last}))').font = F()
    sc.cell(row=r, column=CI['Tier'], value=f'=IF({WS}{r}>=0.75,"A",IF({WS}{r}>=0.55,"B",IF({WS}{r}>=0.35,"C",IF({WS}{r}>0,"D","—"))))').font = F(10,True)
    sc.cell(row=r, column=CI['Criteria left'], value=f'=COUNTBLANK({sr1}:{sr2})').font = F(9, c='808080')
    r += 1
widths = {'Account':30,'Status':9,'Industry':17,'Capability tags':38,'Location':22,'Funding angle (from pipeline board)':40,'Weighted Score %':11,'Rank':6,'Tier':6,'Criteria left':9}
for h,wd in widths.items(): sc.column_dimensions[get_column_letter(CI[h])].width = wd
for cname in crit: sc.column_dimensions[get_column_letter(CI[cname])].width = 10
sc.freeze_panes = 'B4'
dv05 = DataValidation(type='list', formula1='=Lists!$H$2:$H$7', allow_blank=True)
sc.add_data_validation(dv05); dv05.add(f'{WT1}4:{WT2}{3+len(acct_rows)}')

# ---- Buying Influences ----
bi = wb.create_sheet('Buying Influences')
bi['A1'] = 'BUYING INFLUENCES — contact map (Roles: E=final approval · U=lives with the work · T=screens on specs · C=coach, develop don\'t assign)'; bi['A1'].font = F(12,True)
bh = ['Account','Contact','Title','Seniority','Email','Role (E/U/T/C)','Degree (H/M/L)','Mode','Rating','Win-Results statement (their personal win)','Base covered? evidence / notes']
for i,h in enumerate(bh,1):
    c = bi.cell(row=2, column=i, value=h); c.font = HDRF; c.fill = HDR; c.alignment = Alignment(wrap_text=True); c.border = BORD
r = 3
for acct,nm,ti,sen,em,role in contacts:
    vals = [acct,nm,ti,sen,em]
    for i,v in enumerate(vals,1): bi.cell(row=r,column=i,value=v).font = F(9)
    rc = bi.cell(row=r, column=6, value=role if role in (E,T,U) else None)
    rc.font = BLUE; rc.border = BORD
    if role.startswith('⚠'):
        bi.cell(row=r, column=11, value=role).font = F(9, True, 'C00000')
        for i in range(1,12): bi.cell(row=r,column=i).fill = PatternFill('solid', fgColor='FCE4EC')
    for col in (7,8,9):
        cc = bi.cell(row=r, column=col); cc.fill = YEL; cc.border = BORD; cc.font = BLUE
    bi.cell(row=r, column=10).fill = YEL
    r += 1
r += 1
bi.cell(row=r, column=1, value='🚩 RED FLAGS — accounts with ZERO contacts in CRM (uncovered bases per the training):').font = F(10,True,'C00000'); r += 1
for nm in NO_CONTACT:
    bi.cell(row=r, column=1, value=nm).font = F(10, c='C00000')
    bi.cell(row=r, column=2, value='No buying influences identified — critical information missing').font = F(9, c='C00000')
    r += 1
for col,wd in zip('ABCDEFGHIJK', [24,22,34,17,30,15,12,13,16,42,32]): bi.column_dimensions[col].width = wd
bi.freeze_panes = 'A3'
for col,f1 in ((6,'=Lists!$A$2:$A$5'),(7,'=Lists!$B$2:$B$4'),(8,'=Lists!$C$2:$C$5'),(9,'=Lists!$D$2:$D$6')):
    dv = DataValidation(type='list', formula1=f1, allow_blank=True); bi.add_data_validation(dv)
    dv.add(f'{get_column_letter(col)}3:{get_column_letter(col)}{2+len(contacts)}')

# ---- Blue Sheet ----
bs = wb.create_sheet('Blue Sheet')
bs['A1'] = 'STRATEGIC ANALYSIS PLAN (Blue Sheet) — Johnston Engineering | Confidential & Proprietary'; bs['A1'].font = F(12,True)
bs['A2'] = 'Duplicate this tab per sales objective. Objective format: TO SELL {service} to {company/area} FOR {revenue} BY {close date}.'; bs['A2'].font = F(9)
left = [('BDR / Owner',''),('Customer Name',''),('Sales Objective',''),('Potential Revenue',''),('Close Date',''),('Initial Start Date',''),('Last Updated','=TODAY()')]
r = 4
for lab,val in left:
    bs.cell(row=r,column=1,value=lab).font = F(10,True)
    c = bs.cell(row=r,column=2,value=val if val else None)
    c.fill = YEL if not val else PatternFill(); c.font = BLUE if not val else F(); c.border = BORD
    if lab in ('Close Date','Initial Start Date'): c.number_format = 'yyyy-mm-dd'
    if lab=='Last Updated': c.number_format = 'yyyy-mm-dd'; c.font = F()
    r += 1
pos = [('My Position VS Competition','=Lists!$E$2:$E$5'),('Place in Sales Funnel','=Lists!$F$2:$F$7'),('Timing for Priorities','=Lists!$G$2:$G$5')]
r = 4
for lab,f1 in pos:
    bs.cell(row=r,column=4,value=lab).font = F(10,True)
    c = bs.cell(row=r,column=6); c.fill = YEL; c.border = BORD; c.font = BLUE
    dv = DataValidation(type='list', formula1=f1, allow_blank=True); bs.add_data_validation(dv); dv.add(c.coordinate)
    r += 1
bs.cell(row=7,column=4,value='"How do I feel right now about closing this?" (-5 PANIC … +5 EUPHORIA)').font = F(9)
cfeel = bs.cell(row=7,column=6); cfeel.fill = YEL; cfeel.border = BORD; cfeel.font = BLUE
bs.cell(row=4,column=8,value='IDEAL CUSTOMER CRITERIA (5 = best aligned, 0 = worst)').font = F(10,True)
for i,cn in enumerate(crit):
    bs.cell(row=5+i,column=8,value=cn).font = F(10)
    cc = bs.cell(row=5+i,column=10); cc.fill = YEL; cc.border = BORD; cc.font = BLUE
    dv = DataValidation(type='list', formula1='=Lists!$H$2:$H$7', allow_blank=True); bs.add_data_validation(dv); dv.add(cc.coordinate)
bs.cell(row=10,column=8,value='TOTAL (max 25)').font = F(10,True)
bs.cell(row=10,column=10,value='=SUM(J5:J9)').font = F(10,True)
bs.cell(row=12,column=1,value='ROLES: E=Economic · U=User · T=Technical · C=Coach     DEGREE: H/M/L     MODE: G=Growth · T=Trouble · EK=Even Keel · OC=Overconfident     RATING: +5…-5').font = F(9,c='606060')
gh = ['Buying Influence (Name, Title, Location)','Role','Degree','Mode','Rating','Key Win-Result (personal win statement)','How well is base covered? Evidence:']
for i,h in enumerate(gh,1):
    c = bs.cell(row=13,column=i,value=h); c.font = HDRF; c.fill = HDR; c.alignment = Alignment(wrap_text=True); c.border = BORD
for rr in range(14,24):
    for i in range(1,8):
        c = bs.cell(row=rr,column=i); c.border = BORD
        if i in (2,3,4,5): c.fill = YEL
for col,f1 in ((2,'=Lists!$A$2:$A$5'),(3,'=Lists!$B$2:$B$4'),(4,'=Lists!$C$2:$C$5'),(5,'=Lists!$D$2:$D$6')):
    dv = DataValidation(type='list', formula1=f1, allow_blank=True); bs.add_data_validation(dv)
    dv.add(f'{get_column_letter(col)}14:{get_column_letter(col)}23')
sect = [(25,'STRENGTHS (differentiation; relevant to objective; diminish price)', '00B050'),(31,'RED FLAGS (missing info · untested assumption · uncovered base · new player · reorg)', 'C00000')]
for row0,lab,color in sect:
    bs.cell(row=row0,column=1,value=lab).font = F(10,True,color)
    for rr in range(row0+1,row0+5):
        bs.cell(row=rr,column=1).border = BORD
        bs.merge_cells(start_row=rr,start_column=1,end_row=rr,end_column=5)
bs.cell(row=25,column=6,value='BEST ACTION PLAN').font = F(10,True)
for i,h in enumerate(['What','Who','When'],6): bs.cell(row=26,column=i,value=h).font = HDRF; bs.cell(row=26,column=i).fill = HDR
for rr in range(27,32):
    for i in (6,7,8): bs.cell(row=rr,column=i).border = BORD
bs.cell(row=33,column=6,value='INFORMATION NEEDED / FROM WHOM').font = F(10,True)
for rr in range(34,37):
    for i in (6,7): bs.cell(row=rr,column=i).border = BORD
for col,wd in zip('ABCDEFGHIJ', [34,14,10,12,16,26,26,30,4,8]): bs.column_dimensions[col].width = wd

# ---- Gap Analysis ----
ga = wb.create_sheet('Gap Analysis')
ga['A1'] = f'GAP ANALYSIS — qualified companies from your lists NOT in your {len(book)}-account book (sorted by fit; ★ = on 2+ lists)'
ga['A1'].font = F(12,True)
gh2 = ['Company','Fit (0-5)','On lists','Source list(s)','Evidence / description','Keyword hit','Suggested next step']
for i,h in enumerate(gh2,1):
    c = ga.cell(row=2,column=i,value=h); c.font = HDRF; c.fill = HDR; c.border = BORD
r = 3
for g in gaps:
    star = '★ ' if len(g['sources'])>1 else ''
    ga.cell(row=r,column=1,value=star+g['name']).font = F(10, len(g['sources'])>1)
    ga.cell(row=r,column=2,value=g['score']).font = F()
    ga.cell(row=r,column=3,value=len(g['sources'])).font = F()
    ga.cell(row=r,column=4,value=', '.join(sorted(g['sources']))).font = F(9)
    ga.cell(row=r,column=5,value=g['desc']).font = F(9)
    ga.cell(row=r,column=6,value=g['kw']).font = F(9,c='7030A0')
    step = 'Add as Suspect + research' if g['score']>=4 else 'Quick qualify vs ICP'
    if len(g['sources'])>1: step = 'PRIORITY: add as Suspect — multi-list signal'
    ga.cell(row=r,column=7,value=step).font = F(9)
    if len(g['sources'])>1:
        for i in range(1,8): ga.cell(row=r,column=i).fill = PatternFill('solid', fgColor='FFF2CC')
    r += 1
for col,wd in zip('ABCDEFG', [34,8,8,34,60,18,34]): ga.column_dimensions[col].width = wd
ga.freeze_panes = 'A3'
ga.auto_filter.ref = f'A2:G{r-1}'

# tab order & colors
wb.move_sheet('READ ME', offset=0)
for nm,c in [('READ ME','1F3864'),('Account Scorecard','00B050'),('Buying Influences','FFC000'),('Blue Sheet','7030A0'),('Gap Analysis','C00000')]:
    wb[nm].sheet_properties.tabColor = c

out = '/home/claude/JE_Strategic_Selling_Workbook.xlsx'
wb.save(out)
print('Saved', out)
print(f"Scorecard rows: {len(acct_rows)} | Contacts: {len(contacts)} | Gap rows: {len(gaps)} (multi-list: {len(multi)})")
print("Top 15 gap candidates:")
for g in gaps[:15]:
    print(f"  [{g['score']}] {'★' if len(g['sources'])>1 else ' '} {g['name']} <- {', '.join(sorted(g['sources']))} | {g['desc'][:60]}")

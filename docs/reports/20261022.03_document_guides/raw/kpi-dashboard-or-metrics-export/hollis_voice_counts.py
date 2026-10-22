"""Counts from the Hollis Voice room used in the metrics-group guides.
Run: python3 -I hollis_voice_counts.py > hollis_voice_counts_output.txt
Reads data_room/hollis_voice and data_room/answer_key.json. Writes nothing else.
"""
import csv, json, pathlib
from collections import defaultdict
import openpyxl

ROOT = pathlib.Path('/Users/kennethstclair/Documents/workspace/tricorder/data_room')
ROOM = ROOT / 'hollis_voice'
key = json.loads((ROOT / 'answer_key.json').read_text())

print('== monthly_metrics.csv')
mm = list(csv.DictReader(open(ROOM / '03_metrics/monthly_metrics.csv')))
print('rows', len(mm), 'first', mm[0]['month'], 'last', mm[-1]['month'])
print('columns', list(mm[0].keys()))
print('arr == 12 x mrr in every row:', all(int(r['arr']) == 12 * int(r['mrr']) for r in mm))
print('last row', mm[-1])
cum = [int(r['accounts_created_cumulative']) for r in mm]
print('accounts_created_cumulative never decreases:', all(b >= a for a, b in zip(cum, cum[1:])))
pay = [int(r['paying_accounts']) for r in mm]
print('paying_accounts month-over-month decreases:', sum(1 for a, b in zip(pay, pay[1:]) if b < a))

print('== customer_mrr_by_month.csv')
cf = list(csv.DictReader(open(ROOM / '03_metrics/customer_mrr_by_month.csv')))
print('rows', len(cf), 'columns', list(cf[0].keys()))
print('distinct customers', len({r['customer_id'] for r in cf}))
pt = defaultdict(int)
for r in cf: pt[r['product_type']] += 1
print('rows by product_type', dict(pt))
months = sorted({r['month'] for r in cf})
print('months', len(months), months[0], months[-1])
last = months[-1]
sub = [(r['customer_id'], r['customer_name'], int(r['mrr'])) for r in cf if r['month'] == last and r['product_type'] == 'Subscription']
tot = sum(m for _, _, m in sub)
sub.sort(key=lambda x: -x[2])
print('last month subscription MRR', tot, 'subscription rows', len(sub))
print('top1', sub[0], round(sub[0][2] / tot * 100, 1), 'percent')
print('top3 share', round(sum(m for _, _, m in sub[:3]) / tot * 100, 1), 'percent')
pil = [(r['customer_id'], r['customer_name'], int(r['mrr'])) for r in cf if r['month'] == last and r['product_type'] == 'Pilot']
print('pilot rows in last month', pil)
print('subscription + pilot MRR in last month', tot + sum(m for _, _, m in pil))
print('rows where billings differ from mrr + one_time_fee:', sum(1 for r in cf if int(r['billings']) != int(r['mrr']) + int(r['one_time_fee'])))
cust = sorted({r['customer_id'] for r in cf})
print('customers with more than one location in last month:', sum(1 for r in cf if r['month'] == last and int(r['locations']) > 1))

print('== cohorts rebuilt from the customer file')
by_c = defaultdict(dict)
first = {}
for r in cf:
    if r['product_type'] != 'Subscription': continue
    m = int(r['mrr'])
    by_c[r['customer_id']][r['month']] = m
for c, d in by_c.items():
    pos = [mo for mo in sorted(d) if d[mo] > 0]
    if pos: first[c] = pos[0]
def add_months(ym, n):
    y, m = int(ym[:4]), int(ym[5:])
    t = y * 12 + (m - 1) + n
    return f'{t // 12:04d}-{t % 12 + 1:02d}'
cohorts = defaultdict(list)
for c, f in first.items(): cohorts[f].append(c)
start = end = capped = 0
n = 0
for co in ['2025-%02d' % i for i in range(1, 10)]:
    ids = cohorts.get(co, [])
    s = e = cp = 0
    for c in ids:
        a = by_c[c].get(co, 0); b = by_c[c].get(add_months(co, 12), 0)
        s += a; e += b; cp += min(a, b)
    print(co, 'customers', len(ids), 'start', s, 'end', e)
    start += s; end += e; capped += cp; n += len(ids)
print('nine cohorts: customers', n, 'NRR_12', round(end / start * 100, 1), 'GRR_12', round(capped / start * 100, 1))
wb = openpyxl.load_workbook(ROOM / '02_financials/financial_model.xlsx', data_only=True)
ws = wb['Cohorts']
print('Cohorts tab row 14:', [c.value for c in ws[14]][:5])
print('Cohorts tab A2:', ws['A2'].value)
print('Cohorts tab: columns beyond M0 present:', [c.value for c in ws[4]][:8])

print('== sales and marketing spend and new customers')
pl = wb['P&L']
hdr = [c.value for c in pl[4]]
print('P&L header', hdr[:6], '...', hdr[-3:])
rows = {}
for r in pl.iter_rows(min_row=5, values_only=True):
    if r[0]: rows[r[0]] = r[2:]
sm_lines = ['Payroll: sales, marketing and implementation', 'Customer support specialists', 'Marketing programs']
months_hdr = hdr[2:]
idx = {m: i for i, m in enumerate(months_hdr)}
print('model months', months_hdr[0], months_hdr[-1])
new_by_month = defaultdict(int)
for c, f in first.items(): new_by_month[f] += 1
win = ['2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09']
sm_all = sum(rows[l][idx[m]] for l in sm_lines for m in win)
sm_nosup = sum(rows[l][idx[m]] for l in sm_lines if l != 'Customer support specialists' for m in win)
newc = sum(new_by_month[m] for m in win)
print('window', win[0], win[-1], 'new paying customers', newc)
print('S&M all three lines', round(sm_all), 'CAC', round(sm_all / newc), '| without support specialists', round(sm_nosup), 'CAC', round(sm_nosup / newc))
mrr = int(mm[-1]['mrr']) - 15000
arpa = (tot) / int(mm[-1]['paying_accounts'])
print('ARPA (subscription MRR / paying accounts)', round(arpa, 2))
for name, cac in (('all three lines', sm_all / newc), ('without support', sm_nosup / newc)):
    for gm_name, gm in (('deck 80%', 0.80), ('rebuilt 58.1%', 0.581)):
        print('payback months', name, gm_name, round(cac / (arpa * gm), 1))


print('== customer file shape')
dups = defaultdict(int)
for r in cf: dups[(r['month'], r['customer_id'], r['product_type'])] += 1
print('duplicate month, customer, product_type keys:', sum(1 for v in dups.values() if v > 1))
gaps = 0
for c, d in by_c.items():
    pos = [mo for mo in sorted(d) if d[mo] > 0]
    if not pos: continue
    span = [m for m in months if pos[0] <= m <= pos[-1]]
    if any(d.get(m, 0) == 0 for m in span): gaps += 1
print('subscription customers with a zero-revenue month between two paid months:', gaps)
print('subscription customers who have no paid month:', sum(1 for c, d in by_c.items() if not any(v > 0 for v in d.values())))
last_paid = {c: max(mo for mo in d if d[mo] > 0) for c, d in by_c.items() if any(v > 0 for v in d.values())}
print('customers whose last paid month is before', last, ':', sum(1 for v in last_paid.values() if v < last))
ob = [r for r in cf if r['product_type'] == 'Onboarding']
print('onboarding rows: mrr is zero in', sum(1 for r in ob if int(r['mrr']) == 0), 'of', len(ob), '; one_time_fee values', sorted({int(r['one_time_fee']) for r in ob}))
brk = [r for r in cf if r['customer_name'].startswith('Brookline Row')]
print('Brookline Row rows with billings above zero:', [(r['month'], r['mrr'], r['billings']) for r in brk if int(r['billings']) > 0])


print('== hiring plan, sales department')
hp = list(csv.DictReader(open(ROOM / '05_team/hiring_plan.csv')))
sales = [r for r in hp if r['department'] == 'Sales']
print('planned hires', len(hp), 'in Sales', len(sales))
for r in sales: print(' ', r['hire_id'], r['role'], r['start_date'])

print('== files in the room')
files = key['full_room_files']; seed = key['seed_drop_files']
print('full room files', len(files), 'seed drop files', len(seed))
for kw in ['pipeline', 'update', 'cohort', 'unit', 'kpi', 'dashboard']:
    print(kw, [f for f in files if kw in f.lower()])

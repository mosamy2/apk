"""Session-time estimator: one recitation takes the recording length x PACE plus a short tap pause."""
import json, sys
t = json.load(open('audio/timings.json', encoding='utf8'))
dur = {k.split('_', 1)[1]: v['duration'] for k, v in t.items() if k.startswith('boy_')}
for k, v in t.items():
    if k.startswith('husary_'): dur[k.split('_', 1)[1]] = v['duration']
dur['girl'] = None
PACE, TAP, STATION = 1.3, 0.6, 12     # kids recite slower than the recording; seconds of train ride/intro per station
DAYS = [['ikh', 'sub', 'rad', 'ist', 'sal'], ['kur', 'aud', 'hwl', 'sub', 'hmd'], ['sey', 'hyy', 'ist', 'sal', 'lai'], ['bis', 'hsb', 'ikh', 'sub', 'hmd']]
CT = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
def session(lv, day):
    keys = DAYS[day - 1] + ['fal', 'nas']
    tot = 0
    for k in keys:
        n = CT[k][lv - 1]; tot += n * (dur[k] * PACE + TAP) + STATION
    return tot
worst = 0
for lv in range(1, 6):
    row = [session(lv, d) for d in range(1, 5)]
    worst = max(worst, max(row))
    print('L%d' % lv, ' '.join('%5.1f min' % (x / 60) for x in row), ' taps/day', [sum(CT[k][lv - 1] for k in DAYS[d - 1] + ['fal', 'nas']) for d in range(1, 5)])
print('worst', round(worst / 60, 1), 'min')

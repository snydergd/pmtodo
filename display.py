#!/usr/bin/python27

from datetime import date, timedelta
from math import ceil

def monthAfter(m):
    return date(m.year + (1 if m.month == 12 else 0), (m.month + 1) if m.month < 12 else 1, 1)
def aDate(dates):
    dates.sort()
    cal = [' ' for x in range((dates[-1]-dates[0]).days+2)]
    for i in range(len(dates)):
        cal[(date(dates[i].year, dates[i].month, dates[i].day)-date(dates[0].year, dates[0].month, dates[0].day)).days] = 'X'
    
    # add compute values for each calendar position
    name_spacing = []
    d = dates[0]
    inc = timedelta(1)
    i = 0
    while d < dates[-1]:
        if cal[i] == ' ':
            if d.month % 2 == 0: cal[i] = '|'
            else: cal[i] = '-'
        if d.day == 1:
            if i > 0: name_spacing.append(ceil(i/7)*2)
            cal[i] += '_'
            if i-7 > 0: cal[i-7] = cal[i-7][0] + '_'
        else: cal[i] += ' '
        i += 1
        d = d + inc

    # display
    labels = [' ' for x in range((int(ceil(len(cal)/7)+1)*2)+4)]
    m = monthAfter(date(dates[0].year, dates[0].month, 1))
    for i in range(6, -1, -1):
        line = ''
        for j in range(i-dates[0].weekday()-1, len(cal), 7):
            if j >= 0:
                line += cal[j]
                if len(cal[j]) > 1 and cal[j][1] == '_' and (j+7 >= len(cal) or len(cal[j+7]) <= 1 or cal[j+7][1] != '_'):
                    base = int((j-(j%7))/7)*2
                    mn = m.strftime("%b" + str(i))
                    for k in range(len(mn)):
                        labels[base+k] = mn[k]
                    if base < 3:
                        for l in range(0, base):
                            labels[l] = ' '
                    m = monthAfter(m)
                    print "movingToNext"
            else: line += '  '
        print line
    print ''.join(labels)
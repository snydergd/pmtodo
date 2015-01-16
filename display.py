#!/usr/bin/python27

from datetime import date, timedelta
from calendar import monthrange
from math import ceil

def incMonth(d, months):
    year = int(months/12)
    month = months % 12 + d.month
    if month > 12:
        year += 1
        month -= 12
    day = d.day
    if day > monthrange(year, month)[1]:
        day -= monthrange(year, month)[1]
        month += 1
        if month > 12:
            year += 1
            month = 1
    return date(year, month, day)
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
    for i in range(6, -1, -1):
        line = ''
        for j in range(i-dates[0].weekday()-1, len(cal), 7):
            if j >= 0:
                line += cal[j]
                if len(cal[j]) > 1 and cal[j][1] == '_' and (j+7 >= len(cal) or len(cal[j+7]) <= 1 or cal[j+7][1] != '_'):
                    base = int(ceil((j+2)/7)*2)
                    m = (dates[0] + timedelta(j))
                    mn = m.strftime("%b")
                    for k in range(len(mn)):
                        labels[base+k] = mn[k]
                    if base < 3:
                        for l in range(0, base):
                            labels[l] = ' '
            else: line += '  '
        print line
    print ''.join(labels)
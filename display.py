#!/usr/bin/python27

from datetime import date, timedelta
from math import ceil

def aDate(dates):
    dates.sort()
    cal = [' ' for x in range((dates[-1]-dates[0]).days+1)]
    for i in range(len(dates)):
        cal[(dates[i]-dates[0]).days] = 'X'
    
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
#    print name_spacing
    labels = ''
    d = dates[0]
    for i in range(len(name_spacing)+1):
        labels += ('%' + (str(int(name_spacing[i])) if i < len(name_spacing) else '') + 's') % d.strftime('%b')
        d = date(d.year if d.month < 12 else d.year+1, d.month+1 if d.month < 12 else 1, 1)
#    print labels
    for i in range(6, -1, -1):
        line = ''
        for j in range(i-dates[0].weekday()-1, len(cal), 7):
            line += cal[j] if j >= 0 else '  '
        print line

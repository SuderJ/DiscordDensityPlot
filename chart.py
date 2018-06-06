from PIL import Image, ImageDraw
import os
import datetime
import json
import matplotlib.pyplot as plt
from dateutil import tz
import math as nm

def toLocal(x):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')

    # METHOD 2: Auto-detect zones:
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # utc = datetime.utcnow()
    utc = x

    # Tell the datetime object that it's in UTC time zone since 
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    return utc.astimezone(to_zone)

def determineColor(x, mode='row'):
    if mode == 'row':
        if x <= 1/3:
            return (int(x*3*255),0,0)
        elif x <= 2/3:
            return (255,int((x-(1/3))*3*255),0)
        elif x <= 1:
            return (255,255,int((x-(2/3))*3*255))
    if mode == 'bw':
        return (int(x*255),int(x*255),int(x*255))

while(True):
    userid = ''

    userid = input('ID: ')

    if userid == '':
        userid = '155113093775491073'
    elif userid == 'exit':
        break

    chart_height = int(input('Resolution: '))

    pixeltime = 86400.0/chart_height

    times = []

    for x in range(0, chart_height):
        times.append((x+1)*pixeltime)

    fileid = '155107359872647168.json'

    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Logs', fileid)

    with open(filename, 'r', encoding = 'utf8') as f:
        l = json.loads(f.read())

    time = {}

    for x in times:
        time[x] = 0

    days = {}

    for x in l:
        z = toLocal(datetime.datetime.fromtimestamp(int(float(x['time']))))
        days[z.date()] = dict(time)

    for x in l:
        if x['author_id'] == str(userid):
            z = toLocal(datetime.datetime.fromtimestamp(int(float(x['time']))))
            date = z.date()
            for y in times:
                if (z - z.replace(hour = 0, minute = 0, second = 0, microsecond=0)).total_seconds() < y:
                    days[date][y] += 1
                    break

    chart_width = len(list(days.values()))

    mode = 'RGB'
    size = (chart_width,chart_height)
    color = (0,0,0)

    filename = os.path.join('output', userid + 'x' + str(chart_height) + '.png')

    img = Image.new(mode,size,color)
    px = img.load()

    m = max([max(list(x.values())) for x in list(days.values())])

    cons = 45

    for j,time in enumerate(list(days.values())):
        
        sortedlist = sorted(time.items(), key=lambda x: x[0])

        values = [x[1] for x in sortedlist]

        if(max(values) != 0):
            #norm = [(float(i)/max(values)) for i in values]
            norm = [nm.erf(float(i)/cons) for i in values]
        else:
            norm = [0 for i in values]

        for i,x in enumerate(norm):
            px[chart_width - j - 1,i] = determineColor(x, mode = 'bw')

    img.save(os.path.join(os.path.dirname(os.path.realpath(__file__)),filename))

    print('Image saved to', os.path.abspath(filename))

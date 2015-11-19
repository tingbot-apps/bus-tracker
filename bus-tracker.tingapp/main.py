import tingbot
from tingbot import screen
import requests
import json
from datetime import datetime


@tingbot.every(seconds=30)
def refresh():
    screen.fill(color=(26,26,26))
    
    screen.rectangle(
        xy=(0,16),
        align='left',
        size=(320,31),
        color=(255,30,82),
    )
    
    screen.text(
        'Bustle',
        xy=(10,15),
        align='left',
        color='white',
        font='Arial Rounded Bold.ttf',
        font_size=14,    
    )
    
    screen.text(
        'J, Green Park Station',
        xy=(310,17),
        align='right',
        color='white',
        font='JohnstonITCStd-Light.ttf',
        font_size=14,   
    )

    r = requests.get('http://countdown.api.tfl.gov.uk/interfaces/ura/instant_V1?StopCode1=52053&DirectionID=1&VisitNumber=1&ReturnList=StopPointName,LineName,DestinationText,EstimatedTime')

    json_lines = list(json.loads(line) for line in r.iter_lines())
    first_line = json_lines[0]
    current_time = datetime.fromtimestamp(first_line[2] / 1000)

    buses = json_lines[1:]
    
    row_y = 31
    
    for line_num, bus in enumerate(buses):
        if line_num > 3:
            break

        print bus
        
        screen.rectangle(
            xy=(0,row_y),
            align='topleft',
            size=(320,51),
            color=(39,40,34),
        )
        
        bus_number = bus[2]
        bus_destination = bus[3]
        bus_estimated_time = datetime.fromtimestamp(bus[4]/1000)
        bus_delta = bus_estimated_time - current_time
        bus_minutes = int(bus_delta.total_seconds() / 60)
        
        screen.text(
            bus_number,
            xy=(35,row_y+27),
            align='center',
            color='white',
            font='JohnstonITCStd-Bold.ttf',
            font_size=26,
        )
        
        screen.text(
            bus_destination,
            xy=(75,row_y+27),
            align='left',
            color=(220,220,220),
            font='JohnstonITCStd-Light.ttf',
            font_size=17,
        )
        
        screen.text(
            'due' if bus_minutes == 0 else '%i min' % bus_minutes,
            xy=(305,row_y+27),
            align='right',
            color='white',
            font='JohnstonITCStd-Bold.ttf',
            font_size=18,
        )
        
        row_y += 52
    
tingbot.run()

import re
import json

# Manually corrected stop list to avoid ID mismatch
COORDINATES = {
    "rtc_complex": (17.7200, 83.3050),
    "jagadamba": (17.7190, 83.2985),
    "rk_beach": (17.7213, 83.3374),
    "vizag_railway": (17.7225, 83.2966),
    "gajuwaka": (17.6847, 83.2091),
    "nad": (17.7010, 83.2350),
    "simhachalam": (17.7683, 83.2537),
    "maddilapalem": (17.7354, 83.3150),
    "mvp_colony": (17.7469, 83.3297),
    "madhurawada": (17.7861, 83.3467),
    "pendurthi": (17.8360, 83.2178),
    "bhimili": (17.8916, 83.4540),
    "kothavalasa": (17.9000, 83.1500),
    "gopalapatnam": (17.7655, 83.2823),
    "kancharapalem": (17.6998, 83.2792),
    "town_kotharoad": (17.7050, 83.2950),
    "ohpo": (17.6950, 83.2850),
    "airport": (17.7121, 83.2384),
    "tagarapuvalasa": (17.9300, 83.4200),
    "anandapuram": (17.8800, 83.3500),
    "kurmannapalem": (17.7330, 83.2505),
    "steel_plant": (17.6902, 83.1790),
    "scindia": (17.6850, 83.2500),
    "malkapuram": (17.6750, 83.2250),
    "bhpv": (17.6800, 83.2150),
    "mindi": (17.6700, 83.1900),
    "sheelanagar": (17.7050, 83.2200),
    "arilova": (17.7550, 83.3250),
    "kailashagiri": (17.7614, 83.3790),
    "gurudwara": (17.7250, 83.3100),
    "pm_palem": (17.7550, 83.3350),
    "vizianagaram": (18.1200, 83.4100),
    "anakapalle": (17.6909, 83.0030),
    "chodavaram": (17.8300, 82.9300),
    "convent": (17.6980, 83.2840),
    "zoo_park": (17.7660, 83.3450),
    "mvp_complex": (17.7469, 83.3297),
    "waltair": (17.7250, 83.3300),
    "vuda_park": (17.725, 83.335),
    "tenneti_park": (17.7450, 83.3500)
}

def clean_id(name):
    n = name.lower().strip()
    if 'rtc' in n and 'complex' in n: return 'rtc_complex'
    if 'gajuwaka' in n: return 'gajuwaka'
    if 'rk beach' in n or 'ramakrishna' in n: return 'rk_beach'
    if 'railway station' in n: return 'vizag_railway'
    if 'nad' in n and len(n) <= 12: return 'nad'
    return re.sub(r'[^a-z0-9]', '_', n).strip('_')

raw_routes = [
    ["6", "Simhachalam", "OHPO", "Gopalapatnam, NAD, Kancharapalem, Convent junction, Town Kotharoad"],
    ["6A/H", "RTC complex", "Simhachalam hills", "Railway Station, Kancharapalem, NAD, Gopalapatnam"],
    ["10A", "Visakhapatnam Airport", "RK Beach", "NAD, Gurudwara, RTC Complex, Jagadamba"],
    ["111", "Kurmannapalem", "Tagarapuvalasa", "Gajuwaka, NAD, Gurudwara, RTC Complex, Madhurawada"],
    ["28", "RK Beach", "Simhachalam", "Jagadamba, RTC Complex, NAD, Gopalapatnam"],
    ["38", "RTC Complex", "Gajuwaka", "Gurudwara, NAD, BHPV"],
    ["38K", "RTC Complex", "Steel Plant", "Gurudwara, NAD, BHPV, Gajuwaka"],
    ["500", "RTC Complex", "Anakapalle", "Gurudwara, NAD, Gajuwaka, Kurmannapalem"],
    ["900K", "RTC Complex", "Bhimili", "Waltair, MVP Colony, Rushikonda, INS Kalinga"],
    ["211", "Railway Station", "Vizianagaram", "RTC Complex, Maddilapalem, Madhurawada, Tagarapuvalasa"],
    ["400", "RTC Complex", "Kurmannapalem", "Railway Station, Scindia, Malkapuram, Gajuwaka"],
    ["400S", "Maddilapalem", "Narava", "RTC Complex, Railway Station, Scindia, Gajuwaka, Kurmannapalem"],
    ["38A", "RTC Complex", "Mindi", "Gurudwara, NAD, BHPV"],
    ["38B", "RTC Complex", "Bhanojithota", "Gurudwara, NAD, Sheelanagar"],
    ["55", "Simhachalam", "Scindia", "Gopalapatnam, NAD, BHPV, Gajuwaka, Malkapuram"]
]

stops_dict = {}
routes_data = []

for no, start, end, via in raw_routes:
    via_list = [v.strip() for v in via.replace('Via.','').split(',')]
    all_stops_names = [start] + [v for v in via_list if v] + [end]
    route_stop_ids = []
    for sname in all_stops_names:
        sid = clean_id(sname)
        if sid not in stops_dict:
            lat, lng = (17.72, 83.30)
            for k, v in COORDINATES.items():
                if k in sid or sid in k: lat, lng = v; break
            stops_dict[sid] = {"id": sid, "name": sname, "lat": lat, "lng": lng, "zone": "general"}
        route_stop_ids.append(sid)
    
    seen = set()
    unique_stops = [x for x in route_stop_ids if not (x in seen or seen.add(x))]
    
    routes_data.append({
        "id": no.replace('/', '_'),
        "number": no,
        "type": "Metro Express" if 'K' in no or no in ['111','500','900'] else "City Ordinary",
        "typeCode": "ME" if 'K' in no or no in ['111','500','900'] else "CO",
        "name": f"{start} \u2013 {end}",
        "stops": unique_stops,
        "baseFare": 15 if 'K' in no else 10,
        "typicalTimeMin": 30 + (len(unique_stops) * 4),
        "crowdLevel": "medium",
        "note": "Connects major Vizag hubs"
    })

data = {
    "stops": list(stops_dict.values()),
    "routes": routes_data,
    "touristSpots": [
        {"id":"rk", "name":"Ramakrishna Beach", "nearestStop":"rk_beach", "description":"Beach", "routes":["10A","28"]},
        {"id":"sim", "name":"Simhachalam", "nearestStop":"simhachalam", "description":"Temple", "routes":["6","28"]}
    ],
    "fares": {"oneDayPass": 50, "studentConcession": 0.5},
    "crowdByHour": {i: "medium" for i in range(24)},
    "translations": {
        "en": {"appName": "M\u0101rgaDarshi", "tagline": "Smart Bus Companion", "from": "From", "to": "To", "search": "Find Buses", "features": "Features", "howItWorks": "How It Works", "touristSpots": "Tourist Spots", "timetable": "Timetable", "map": "Map", "tips": "Tips", "community": "Community", "chatbot": "Assistant", "faq": "FAQ", "fare": "Fare", "time": "Time", "crowd": "Crowd", "cityOrdinary": "Ordinary", "metroExpress": "Express", "oneDayPass": "Pass", "disclaimer": "Approx. times.", "loginRequired": "Login required.", "noRoutes": "No buses found.", "selectFrom": "Start Stop", "selectTo": "End Stop"},
        "te": {"appName": "\u0c2e\u0c3e\u0c30\u0c4d\u0c17\u0c2a\u0c41\u0c24\u0c4d\u0c30", "tagline": "Smart Bus Guide", "from": "\u0c28\u0c41\u0c02\u0c21\u0c3f", "to": "\u0c35\u0c30\u0c15\u0c41", "search": "\u0c35\u0c46\u0c24\u0c41\u0c15\u0c41", "features": "\u0c32\u0c15\u0c4d\u0c37\u0c23\u0c3e\u0c32\u0c41", "howItWorks": "\u0c2a\u0c28\u0c3f \u0c35\u0c3f\u0c27\u0c3e\u0c28\u0c02", "touristSpots": "\u0c2a\u0c4d\u0c30\u0c26\u0c47\u0c36\u0c3e\u0c32\u0c41", "timetable": "\u0c38\u0c2e\u0c2f\u0c2a\u0c1f\u0c4d\u0c1f\u0c3f\u0c15", "map": "\u0c2e\u0c4d\u0c2f\u0c3e\u0c2a\u0c4d", "tips": "\u0c1a\u0c3f\u0c1f\u0c4d\u0c15\u0c3e\u0c32\u0c41", "community": "\u0c15\u0c2e\u0c4d\u0c2f\u0c42\u0c28\u0c3f\u0c1f\u0c40", "chatbot": "\u0c1a\u0c3e\u0c1f\u0c4d", "faq": "\u0c2a\u0c4d\u0c30\u0c36\u0c4d\u0c28\u0c32\u0c41", "fare": "\u0c27\u0c30", "time": "\u0c38\u0c2e\u0c2f\u0c02", "crowd": "\u0c30\u0c26\u0c4d\u0c26\u0c40", "cityOrdinary": "\u0c06\u0c30\u0c4d\u0c21\u0c3f\u0c28\u0c30\u0c40", "metroExpress": "\u0c0e\u0c15\u0c4d\u0c38\u0c4d\u0c2a\u0c4d\u0c30\u0c46\u0c38\u0c4d", "oneDayPass": "\u0c21\u0c47 \u0c2a\u0c3e\u0c38\u0c4d", "disclaimer": "\u0c38\u0c2e\u0c2f\u0c3e\u0c32\u0c41.", "loginRequired": "\u0c32\u0c3e\u0c17\u0c3f\u0c28\u0c4d.", "noRoutes": "\u0c32\u0c47\u0c35\u0c41.", "selectFrom": "\u0c28\u0c41\u0c02\u0c21\u0c3f", "selectTo": "\u0c35\u0c30\u0c15\u0c41"}
    },
    "chatbot": {"greetings": ["hi"], "farewords": ["bye"], "responses": [{"patterns":["beach"],"reply":"Take Bus 10A to RK Beach!"}]},
    "timetable": {r["id"]: {"departures": ["08:00", "12:00", "16:00"]} for r in routes_data}
}

with open('C:/Users/user/Margadarshi/data/vizag_routes.js', 'w', encoding='utf-8') as f:
    f.write('const VIZAG_DATA = ' + json.dumps(data, indent=2) + ';\nif (typeof module !== \"undefined\") module.exports = VIZAG_DATA;\n')

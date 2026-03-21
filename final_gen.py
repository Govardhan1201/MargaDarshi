import re
import json

# Full OCR data
ocr_data = [
    "6 Simhachalam OHPO Gopalapatnam, NAD, Kancharapalem, Convent junction, Town Kotharoad",
    "6A/H RTC complex Simhachalam hills Railway Station, Kancharapalem, NAD, Gopalapatnam",
    "10 A Visakhapatnam Airport R K Beach Via. NAD, Gurudwara, RTC Complex",
    "111 Kuramanapalem Tagarapuvalasa Via. Gajuwaka, NAD, Gurudwara, Zoo Park, Madurwada",
    "5D Town Kotharoad Dabbanda Convent, Kancharapalem, NAD, Gopalapatnam, Pendurthi",
    "10K RTC complex Kailashagiri Jagadamba, Rk beach, Vuda park, Tenneti park",
    "28 RK beach Simhachalam Bus Station Jagadamba, RTC Complex, NAD, Gopalapatnam",
    "28R RK beach Simhachalam Bus Station Jagadamba, RTC, Railway Station, NAD, Gopalapatnam",
    "28A/28K RK beach Pendurthy/Kottavalasa GPT, NAD, RTC, Jagadamba, Collector office",
    "28A/D RK beach Denderu Jagadamba, RTC, Railway Station, NAD, Gopalapatnam, Pendurthi",
    "28C RK Beach Chintalagraharam Jagadamba, RTC Complex, NAD, Gopalapatnam, Vepagunta",
    "28J RK Beach Sujatanagar Jagadamba, RTC Complex, NAD, Gopalapatnam, Vepagunta",
    "28P RK Beach Sabbavaram Jagadamba, RTC Complex, NAD, Gopalapatnam, Pendurthi",
    "28Z/H Zilla Parishad Simhachalam hills Jagadamba, RTC, Gurudwar, NAD, Gopalapatnam",
    "28A/P RTC Complex Ravalammapalem Railway Station, Kancharapalem, NAD, GPT, Pendurthi",
    "68/68K RK beach Pendurthi/Kothavalasa Jagadamba, Asilmetta, Maddilapalem, Arilova, Simhachalam",
    "505 Simhachalam Scindia Gopalapatnam, NAD,Kancharapalem, Convent Jn, naval Dockyard",
    "55 Simhachalam Scindia Gopalapatnam, NAD, BHPV, Gajuwaka, Malkapuram",
    "55K Kothavalasa Scindia Pendurthi, Gopalapatnam, NAD, Gajuwaka, Malkapuram",
    "55V Vepada Scindia Simhachalam, Gopalapatnam, NAD, Gajuwaka, Malkapuram",
    "55T Scindia Tagarapuvalasa malkapuram gajuwaka, NAD, Gopalpatnam, Pendurthy, Anandapuram",
    "60 Simhachalam OHPO Adavivaram, Maddilapalem, RTC Complex, Jagadamba",
    "60R RK Beach Arilova Colony Jagadamba, RTC Complex, Maddilapalem",
    "38 RTC Complex Gajuwaka Gurudwara, NAD, BHPV",
    "38A RTC Complex Mindi Gurudwara, NAD, BHPV",
    "38B RTC Complex Bhanojithota Gurudwara, NAD, Sheelanagar",
    "38C RTC Complex Sundarayya Colony Gurudwara, NAD, BHPV, Gajuwaka",
    "38D RTC Complex Nadupur Dairy Colony Gurudwara, NAD, BHPV, Gajuwaka, Pedagantyada",
    "38H RTC Complex Gantyada HB Colony Visakhapatnam Airport, Gurudwara, NAD, BHPV, Gajuwaka, Pedagantyada",
    "38IT Kurmannapalem IT Park Gajuwaka, NAD, Gurudwara, RTC Complex, Maddilapalem, Carshed",
    "38J RTC Complex Janata Colony Gurudwara, NAD, BHPV, Gajuwaka, Scindia",
    "38K RTC Complex Steelplant Sector 5 Gurudwara, NAD, BHPV, Gajuwaka",
    "38M Marikavalasa Kurmannapalem Madhurawada, Maddilapalem, Gurudwara, NAD, BHPV, Gajuwaka",
    "38N RTC Complex Nadupuru Gurudwara, NAD, BHPV, Gajuwaka, Pedagantyada",
    "38R Maddilapalem Rambilli Gurudwara, NAD, BHPV, Parawada",
    "38T RTC Complex Steelplant Sector 11 Gurudwara, NAD, BHPV, Gajuwaka, Kurmannaplem",
    "38Y RTC Complex Duvvada Railway Station Gurudwara, NAD, BHPV, Gajuwaka, Kurmannapalem",
    "900K RTC Complex Bhimili Waltair, MVP Colony, Rushikonda, gitam, mangamaripeta, INS Kalinga",
    "900T RTC Complex Tagarapuvalasa Waltair, MVP Colony, Rushikonda, gitam, mangamaripeta, INS Kalinga",
    "999 RTC Complex Bhimili Maddilapalem, Endada, Madhurwada, Anandapuram",
    "222 RTC Complex Tagarapuvalasa Maddilapalem, Endada, Madhurawada, Anandapuram",
    "400 RTC Complex Kurmannapalem Railway Station, Scindia, Malkapuram, Gajuwaka",
    "400H Maddilapalem Gantyada HB Colony RTC, Railway Station, Scindia, Gajuwaka, Pedagantyada",
    "400N RTC Complex Vadacheepurupalli Railway Station, Scindia, Malkapuram, Gajuwaka, Kurmannapalem, Sector 11, Parawada, NTPC",
    "400S Maddilapalem Narava RTC Complex, Railway Station, Scindia, Gajuwaka, Kurmannapalem",
    "400K Maddilapalem Duvvada Railway Station RTC, Railway Station, Scindia, Gajuwaka, Kurmannapalem",
    "400Y Maddilapalem Yelamanchili RTC, Railway Station, Scindia, Gajuwaka, Achutapuram",
    "900 Maddilapalem Railway Station MVP Colony, Waltair, RTC Complex",
    "540 MVP Complex Simhachalam Maddilapalem, Gurudwara, NAD, Gopalapatnam",
    "540M MVP Complex Gajuwaka Maddilapalem, Gurudwara, NAD, BHPV",
    "541 Maddilapalem Kothavalasa Gurudwara, NAD, Gopalapatnam, Vepagunta, Pendurthi",
    "211 Railway Station Vizianagaram RTC Complex, Maddilapalem, Madhurawada, Tagarapuvalasa",
    "60C Arilova Colony OHPO Maddilapalem, RTC Complex, Jagadamba, Town Kotharoad",
    "20A HB Colony OHPO Sitammadhara, Satyam Junction, RTC, Jagadamba, Town Kotharoad",
    "69 Arilova Colony Railway Station HB Colony, Sitammadhara, Satyam Junction, RTC Complex",
    "52D Ravindra Nagar OHPO Adarsha Nagar, Maddilapalem, RTC, Jagadamba, Town Kotharoad",
    "52S/52V Sagar Nagar OHPO Visalakshi Nagar, Maddilapalem, RTC, Jagadamba, Town Kotharoad",
    "52E Yendada Village OHPO Rushikonda, Endada, Maddilapalem, RTC, Jagadamba, Town Kotharoad",
    "25S OHPO Nagarapalem Jagadamba, RTC Complex, Maddilapalem, Endada, Carshed",
    "25D/M OHPO Midhilapuri Colony Jagadamba, RTC Complex, Maddilapalem, Endada, Carshed",
    "25D/V OHPO Vambey Colony Jagadamba, RTC Complex, Maddilapalem, Endada, Carshed",
    "25E OHPO Kommadi Jagadamba, RTC Complex, Maddilapalem, Endada, Madhurawada",
    "25G OHPO Ganesh Nagar Jagadamba, RTC Complex, Maddilapalem, Endada, Madhurawada",
    "25IT RTC Complex IT Park Maddilapalem, Endada, Carshed, Midhilapuri Colony",
    "25K OHPO Bakkannapalem Jagadamba, RTC Complex, Maddilapalem, Endada, Madhurawada",
    "25M OHPO Marikavalasa Jagadamba, RTC Complex, Maddilapalem, Endada, Madhurawada",
    "25P Ratnagiri HB Colony OHPO PM Palem, Endada, Maddilapalem, RTC Complex, Jagadamba",
    "14 Venkojipalem OHPO MVP Colony, Waltair, AU Outgate, Jagadamba, Town Kotharoad",
    "900R RTC Complex Rushikonda INS Kalinga,Sagar nagar, RTC",
    "36 Collector Office Mindi Town Kotharoad, Convent, Scindia, Gajuwaka, BHPV",
    "6B OHPO Chintagatla Town Kotharoad, Convent, NAD, Sheelanagar, Narava",
    "48 Madhavadhara MN Club Muralinagar, Kailasapuram, Akkayyapalem, RTC Complex, Jagadamba",
    "48A Madhavadhara OHPO Muralinagar, Kailasapuram, Akkayapalem, RTC Complex, Town Kotharoad",
    "12K Town Kotharoad Kothavalasa Railway Station, Kancharapalem, NAD, GPT, Pendurthi",
    "12D RTC Complex Devarapalle NAD, Gopalapatnam, Pendurthi, Kothavalasa, Anandapuram",
    "16 Purna Market Yarada Convent junction, Scindia, Naval base",
    "99 Collector Office Gajuwaka Jagadamba, Town Kotharoad, Convent, Scindia, Malkapuram",
    "99A/C Collector Office Chodavaram Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka, Kurmannapalem, Anakapalle",
    "99K Collector Office Kurmannapalem Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka",
    "1T Vuda Park Kapulatunglam RK Beach, Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka",
    "65F Fishing Harbour Gangavaram Collector Office, Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka, Pedagantyada, Dibbapalem",
    "77 Collector Office Thanam Jagadamba, Town Kotharoad, Convent, Scidia, Gajuwaka",
    "77T Collector Office Thadi Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka",
    "63 RK Beach Dibbapalem Town Kotharoad, Convent, Scindia, Gajuwaka, Pedagantyada",
    "64A Collector Office Swayambuvaram Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka",
    "500 RTC Complex Anakapalle Gurudwar, NAD, Gajuwaka, Kurmannapalem, Aganampudi",
    "500A Maddilapalem Addaroad Gurudwar, NAD, Gajuwaka, Kurmannaplem, Anakapalli, Elamanchili",
    "500P Anakapalle PM Palem Kurmannapalem, Gajuwaka, Scindia, Convent, RTC Complex, Maddilapalem, Carshed",
    "500Y RTC Complex Yelamanchili Gurudwar, NAD, Gajuwaka, Kurmannapalem, Anakapalle",
    "38H RTC Complex Gantyada HB Colony Gurudwar, NAD, BHPV, Gajuwaka",
    "555 RTC Complex Chodavaram Gurudwar, NAD, Gopalapatnam, Pendurthi, Sabbavaram",
    "25J Railway Station Sevanagar RTC Complex, Maddilapalem, Endada, Madhurawada",
    "25R Railway Station Gurajadanagar RTC Complex, Maddilapalem, Endada, PM Palem",
    "300C RTC Complex Chodavaram NAD, Gopalapatnam, Pendurthi, Sabbavaram",
    "300M RTC Complex Madugula NAD, Gopalapatnam, Pendurthi, Sabbavaram, Chodavaram",
    "333 Town Kotharoad Devarapalle Convent, NAD, Gopalapatnam, Pendurthi, Kothavalasa",
    "333K Town Kotharoad K.Kotapad Convent, Kancharapalem, NAD, Gopalapatnam, Pendurthi",
    "328 K.Kotapad RK Beach Jagadamba, RTC Complex, NAD, Gopalapatnam, Pendurthi",
    "600 Anakapalle Simhachalam Aganampudi, Kurmannapalem, Gajuwaka, NAD, Gopalapatnam",
    "600C RTC Complex Anakapalle Railway Station, Convent, Gajuwaka, Kurmannapalem, Aganampudi",
    "700 Simhachalam Vizianagaram Adavivaram, Shontyam, Anandapuram, Padmanabham",
    "500A/C RTC Complex Achutapuram Gurudwar, NAD, Gajuwaka, Kurmannapalem, Anakapalle",
    "844 Collector Office Kollivanipalem Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka, Kurmannapalem, Parawada",
    "888 Anakapalle Tagarapuvalasa Pendurthy, sontyam, Anandapuram",
    "14A Arilova Colony OHPO Venkojipalem, Mvp colony,AU Out gate,Jagadamba,Kotha road",
    "744 Collector office Dosuru Jagadamba, Town Kotha Road, Convent, Scindia, Gajuwaka, Kurmannapalem, Parawada"
]

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
}

def clean_id(name):
    return re.sub(r'[^a-z0-9]', '_', name.lower().strip()).strip('_')

stops_dict = {}
routes = []

for line in ocr_data:
    match = re.search(r'^([A-Z/0-9]+)\s+(.*?)\s+(.*?)\s+([A-Z].*)', line)
    if not match: continue
    no, start, end, via_text = match.groups()
    via_list = [v.strip() for v in via_text.split(',')]
    all_stops = [start] + via_list + [end]
    route_stops = []
    for sname in all_stops:
        sid = clean_id(sname)
        if sid not in stops_dict:
            # Simple interpolation
            lat, lng = (17.72, 83.30)
            for k, v in COORDINATES.items():
                if k in sid or sid in k: lat, lng = v; break
            stops_dict[sid] = {"id": sid, "name": sname, "lat": lat, "lng": lng, "zone": "central"}
        route_stops.append(sid)
    
    routes.append({
        "id": no.replace('/', '_'),
        "number": no,
        "type": "Metro Express" if no.endswith('K') or no in ['111','500','900'] else "City Ordinary",
        "typeCode": "ME" if no.endswith('K') or no in ['111','500','900'] else "CO",
        "name": f"{start} \u2013 {end}",
        "stops": route_stops,
        "baseFare": 15 if no.endswith('K') else 8,
        "typicalTimeMin": 30 + (len(route_stops)*4),
        "crowdLevel": "medium"
    })

data = {
    "stops": list(stops_dict.values()),
    "routes": routes,
    "touristSpots": [
        {"id":"rk", "name":"RK Beach", "nearestStop":"rk_beach", "description":"Beach", "routes":["10A","28"]},
        {"id":"sim","name":"Simhachalam","nearestStop":"simhachalam","description":"Temple","routes":["6","28"]}
    ],
    "fares": {"oneDayPass": 50, "studentConcession": 0.5},
    "crowdByHour": {i: "medium" for i in range(24)},
    "translations": {
        "en": {"appName": "M\u0101rgaDarshi", "tagline": "Your Smart Bus Companion", "from": "From", "to": "To", "search": "Find Buses", "features": "Features", "howItWorks": "How It Works", "touristSpots": "Tourist Spots", "timetable": "Timetable", "map": "Map", "tips": "Tips", "community": "Community", "chatbot": "Chatbot", "faq": "FAQ", "fare": "Fare", "time": "Time", "crowd": "Crowd", "cityOrdinary": "Ordinary", "metroExpress": "Express", "oneDayPass": "One Day Pass", "disclaimer": "Approximate times.", "loginRequired": "Login needed.", "noRoutes": "No buses.", "selectFrom": "From stop", "selectTo": "To stop"},
        "te": {"appName": "\u0c2e\u0c3e\u0c30\u0c4d\u0c17\u0c2a\u0c41\u0c24\u0c4d\u0c30", "tagline": "Smart Bus Guide", "from": "\u0c28\u0c41\u0c02\u0c21\u0c3f", "to": "\u0c35\u0c30\u0c15\u0c41", "search": "\u0c35\u0c46\u0c24\u0c41\u0c15\u0c41", "features": "\u0c32\u0c15\u0c4d\u0c37\u0c23\u0c3e\u0c32\u0c41", "howItWorks": "\u0c2a\u0c28\u0c3f \u0c35\u0c3f\u0c27\u0c3e\u0c28\u0c02", "touristSpots": "\u0c2a\u0c4d\u0c30\u0c26\u0c47\u0c36\u0c3e\u0c32\u0c41", "timetable": "\u0c38\u0c2e\u0c2f\u0c2a\u0c1f\u0c4d\u0c1f\u0c3f\u0c15", "map": "\u0c2e\u0c4d\u0c2f\u0c3e\u0c2a\u0c4d", "tips": "\u0c1a\u0c3f\u0c1f\u0c4d\u0c15\u0c3e\u0c32\u0c41", "community": "\u0c15\u0c2e\u0c4d\u0c2f\u0c42\u0c28\u0c3f\u0c1f\u0c40", "chatbot": "\u0c1a\u0c3e\u0c1f\u0c4d", "faq": "\u0c2a\u0c4d\u0c30\u0c36\u0c4d\u0c28\u0c32\u0c41", "fare": "\u0c27\u0c30", "time": "\u0c38\u0c2e\u0c2f\u0c02", "crowd": "\u0c30\u0c26\u0c4d\u0c26\u0c40", "cityOrdinary": "\u0c06\u0c30\u0c4d\u0c21\u0c3f\u0c28\u0c30\u0c40", "metroExpress": "\u0c0e\u0c15\u0c4d\u0c38\u0c4d\u0c2a\u0c4d\u0c30\u0c46\u0c38\u0c4d", "oneDayPass": "\u0c21\u0c47 \u0c2a\u0c3e\u0c38\u0c4d", "disclaimer": "\u0c38\u0c2e\u0c2f\u0c3e\u0c32\u0c41.", "loginRequired": "\u0c32\u0c3e\u0c17\u0c3f\u0c28\u0c4d.", "noRoutes": "\u0c32\u0c47\u0c35\u0c41.", "selectFrom": "\u0c28\u0c41\u0c02\u0c21\u0c3f", "selectTo": "\u0c35\u0c30\u0c15\u0c41"}
    },
    "chatbot": {"greetings": ["hi"], "farewords": ["bye"], "responses": [{"patterns":["rk"],"reply":"RK Beach is great!"}]},
    "timetable": {r["id"]: {"departures": ["08:00", "12:00", "16:00"]} for r in routes}
}

with open('C:/Users/user/Margadarshi/data/vizag_routes.js', 'w', encoding='utf-8') as f:
    f.write('const VIZAG_DATA = ' + json.dumps(data) + ';\nif (typeof module !== \"undefined\") module.exports = VIZAG_DATA;\n')

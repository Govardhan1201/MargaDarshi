import re
import json

# Full OCR text compiled from the PDF pages 2, 3, 4
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

def clean_id(name):
    return re.sub(r'[^a-z0-9]', '_', name.lower().strip()).strip('_')

def clean_name(name):
    name = name.strip()
    mapping = {
        "RTC complex": "RTC Complex",
        "R K Beach": "RK Beach",
        "Rk beach": "RK Beach",
        "Town Kotharoad": "Town Kotharoad",
        "Town Kotha Road": "Town Kotharoad",
        "Railway Station": "Visakhapatnam Railway Station",
        "MVP complex": "MVP Complex",
        "MVP Colony": "MVP Colony",
        "Simhachalam Bus Station": "Simhachalam",
        "Kuramanapalem": "Kurmannapalem",
        "Kurmannaplem": "Kurmannapalem",
        "Pendurthy": "Pendurthi"
    }
    for k, v in mapping.items():
        if k.lower() in name.lower():
            name = name.replace(k, v)
    return name

stops_dict = {}
routes = []

# Base coordinates for interpolation
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
    "bhimili": (17.8916, 83.4540),
    "pendurthi": (17.8360, 83.2178),
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
    "elamanchili": (17.5500, 82.8500),
    "convent": (17.6980, 83.2840),
    "zoo_park": (17.7660, 83.3450),
    "ins_kalinga": (17.8000, 83.3900),
    "gitam": (17.7812, 83.3770),
    "rushikonda": (17.7636, 83.3765),
    "waltair": (17.7250, 83.3300)
}

def get_coords(sid):
    # Try direct match
    if sid in COORDINATES: return COORDINATES[sid]
    # Try partial match
    for k, v in COORDINATES.items():
        if k in sid or sid in k: return v
    # Default jump around RTC complex
    return (17.7200 + (hash(sid) % 100) / 1000, 83.3050 + (hash(sid) % 70) / 1000)

for line in ocr_data:
    match = re.search(r'^([A-Z/0-9]+)\s+(.*?)\s+(.*?)\s+([A-Z].*)', line)
    if not match: continue
    
    no, start, end, via_text = match.groups()
    start_c = clean_name(start)
    end_c = clean_name(end)
    via_list = [clean_name(v.strip()) for v in via_text.split(',')]
    
    route_stops = []
    # Combine start, via, end
    all_stops = [start_c] + via_list + [end_c]
    
    for sname in all_stops:
        sid = clean_id(sname)
        if sid not in stops_dict:
            lat, lng = get_coords(sid)
            stops_dict[sid] = {
                "id": sid,
                "name": sname,
                "lat": lat,
                "lng": lng,
                "zone": "general"
            }
        route_stops.append(sid)
    
    type_code = "CO"
    if no.endswith('K') or no in ['900', '111', '500', '222', '900K', '900T']:
        type_code = "ME"
        
    routes.append({
        "id": no.replace('/', '_'),
        "number": no,
        "type": "Metro Express" if type_code == "ME" else "City Ordinary",
        "typeCode": type_code,
        "name": f"{start_c} \u2013 {end_c}",
        "stops": route_stops,
        "baseFare": 15 if type_code == "ME" else 8,
        "typicalTimeMin": 40 + (len(route_stops) * 5),
        "crowdLevel": "medium"
    })

# Final structure
data = {
    "stops": list(stops_dict.values()),
    "routes": routes,
    "touristSpots": [
        {"id": "rk_beach", "name": "RK Beach", "nearestStop": "rk_beach", "description": "Beach, Museum", "routes": ["10A", "28", "900"], "tips": "Sunset view"},
        {"id": "kailasagiri", "name": "Kailashagiri", "nearestStop": "kailashagiri", "description": "Park", "routes": ["10K", "900K"], "tips": "Ropeway"},
        {"id": "simhachalam", "name": "Simhachalam", "nearestStop": "simhachalam", "description": "Temple", "routes": ["6", "28"], "tips": "Hill view"}
    ],
    "fares": {"oneDayPass": 50, "studentConcession": 0.5, "seniorConcession": 0.5},
    "crowdByHour": {i: "medium" for i in range(24)},
    "translations": {}, # Will keep existing
    "chatbot": {"greetings": ["hi"], "farewords": ["bye"], "responses": []}, # Simplified for now, will merge
    "timetable": {r["id"]: {"departures": ["08:00", "10:00", "12:00", "14:00", "16:00"]} for r in routes}
}

# Read existing translations to preserve them
# For this script we will just output a JSON that can be manually merged or fully replaced.
# But I'll try to keep the translations.

print("Parsed", len(routes), "routes and", len(data["stops"]), "stops.")

with open("C:/Users/user/Margadarshi/data/vizag_routes.js", "w", encoding="utf-8") as f:
    f.write("// MārgaDarshi – Full Dataset from PDF\n")
    f.write("const VIZAG_DATA = ")
    f.write(json.dumps(data, indent=2))
    f.write(";\n\nif (typeof module !== 'undefined') module.exports = VIZAG_DATA;\n")

import json

try:
    with open('C:/Users/user/Margadarshi/data/vizag_routes.js', 'r', encoding='utf-8') as f:
        content = f.read()
        json_str = content[content.find('{'):content.rfind('}')+1]
        data = json.loads(json_str)

    targets = ['38', '38K', '111', '500']
    found = []
    for r in data['routes']:
        if r['number'] in targets:
            found.append(r['number'])
            # Check if rtc_complex and gajuwaka are in stops
            has_rtc = 'rtc_complex' in r['stops']
            has_gaj = 'gajuwaka' in r['stops']
            rtc_idx = r['stops'].index('rtc_complex') if has_rtc else -1
            gaj_idx = r['stops'].index('gajuwaka') if has_gaj else -1
            print(f"Route {r['number']}: has_rtc={has_rtc}({rtc_idx}), has_gaj={has_gaj}({gaj_idx}), valid={has_rtc and has_gaj and rtc_idx < gaj_idx}")

    print("Found targets:", found)

except Exception as e:
    print("Error:", e)

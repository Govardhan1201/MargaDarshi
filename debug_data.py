import json

try:
    with open('C:/Users/user/Margadarshi/data/vizag_routes.js', 'r', encoding='utf-8') as f:
        content = f.read()
        json_str = content.split('const VIZAG_DATA = ')[1].rsplit(';', 1)[0]
        data = json.loads(json_str)

    print("Total Routes:", len(data['routes']))
    print("Total Stops:", len(data['stops']))

    targets = ['38', '38K', '111', '500']
    for r in data['routes']:
        if r['number'] in targets:
            print(f"Route {r['number']}: {r['stops']}")
            
    # Check for rtc_complex and gajuwaka in stops
    stop_ids = [s['id'] for s in data['stops']]
    print("rtc_complex in stops:", 'rtc_complex' in stop_ids)
    print("gajuwaka in stops:", 'gajuwaka' in stop_ids)

except Exception as e:
    print("Error:", e)

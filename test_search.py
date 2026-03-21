import json

try:
    with open('C:/Users/user/Margadarshi/data/vizag_routes.js', 'r', encoding='utf-8') as f:
        content = f.read()
        json_str = content[content.find('{'):content.rfind('}')+1]
        data = json.loads(json_str)

    from_id = 'rtc_complex'
    to_id = 'gajuwaka'
    
    print(f"Searching {from_id} to {to_id}")
    matches = []
    for r in data['routes']:
        if from_id in r['stops'] and to_id in r['stops']:
            f_idx = r['stops'].index(from_id)
            t_idx = r['stops'].index(to_id)
            if f_idx < t_idx:
                matches.append(r['number'])
    
    print("Matches:", matches)
    print("Total Routes in file:", len(data['routes']))

except Exception as e:
    print("Error:", e)

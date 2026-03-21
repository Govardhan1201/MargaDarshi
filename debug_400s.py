import json

try:
    with open('C:/Users/user/Margadarshi/data/vizag_routes.js', 'r', encoding='utf-8') as f:
        content = f.read()
        json_str = content[content.find('{'):content.rfind('}')+1]
        data = json.loads(json_str)

    num = '400S'
    for r in data['routes']:
        if r['number'] == num:
            print(f"Route {num} stops: {r['stops']}")
            
    # Also check if 400 is there
    for r in data['routes']:
        if r['number'] == '400':
            print(f"Route 400 stops: {r['stops']}")

except Exception as e:
    print("Error:", e)

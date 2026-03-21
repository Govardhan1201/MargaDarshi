import re
import json

# Paths
TXT_FILE = "C:/Users/user/Margadarshi/BUS ROUTES.txt"
JS_FILE = "C:/Users/user/Margadarshi/data/vizag_routes.js"

with open(TXT_FILE, 'r', encoding='utf-8') as f:
    raw_text = f.read()

# Read the existing JS file to preserve metadata
with open(JS_FILE, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Extract the JSON part from JS file
json_str_match = re.search(r'const\s+VIZAG_DATA\s*=\s*(\{.*?\})\s*;\s*\n', js_content, re.DOTALL)
if json_str_match:
    json_str = json_str_match.group(1)
    
    # We might need to do some cleanup as JS objects can sometimes have trailing commas or unquoted keys, 
    # but VIZAG_DATA seems to be valid JSON.
    # Let's clean up single quotes to double quotes if any, and remove trailing commas if they break json.loads
    json_str = re.sub(r',\s*\}', '}', json_str)
    json_str = re.sub(r',\s*\]', ']', json_str)
    
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing existing JSON: {e}")
        exit(1)
else:
    print("Could not find VIZAG_DATA in JS file")
    exit(1)

existing_stops = {stop['id']: stop for stop in data.get('stops', [])}
# Also map by name to find existing ones
name_to_id = {stop['name'].lower().strip(): stop['id'] for stop in data.get('stops', [])}

existing_routes = {route['id']: route for route in data.get('routes', [])}
number_to_route = {route['number']: route for route in data.get('routes', [])}

# Parse the text file
routes = []
current_route = None

lines = raw_text.split('\n')
i = 0
while i < len(lines):
    line = lines[i].strip()
    
    if line.startswith("Bus Route Name :"):
        if current_route:
            routes.append(current_route)
        name_val = line.split(":", 1)[1].strip()
        current_route = {
            "number": name_val,
            "stops": [],
            "distanceKm": 0,
            "start": "",
            "end": ""
        }
    elif line.startswith("Bus Route Starting Stage Name"):
        start_val = line.split(":", 1)[1].strip()
        if current_route: current_route["start"] = start_val
    elif line.startswith("Bus Route Ending Stage Name"):
        end_val = line.split(":", 1)[1].strip()
        if current_route: current_route["end"] = end_val
    elif line.startswith("Total Distance :"):
        dist_str = line.split(":", 1)[1].strip().split()[0]
        try:
            current_route["distanceKm"] = int(dist_str)
        except:
            pass
    elif line.startswith("Bus Stages Details"):
        # Next lines are stages
        i += 1
        if i < len(lines) and lines[i].strip().startswith("Sl No"):
            i += 1 # skip header
        
        while i < len(lines) and lines[i].strip() and re.match(r'^\d+\.\)', lines[i].strip()):
            stage_line = lines[i].strip()
            stage_name = stage_line.split(".)", 1)[1].strip().rstrip(',')
            current_route["stops"].append(stage_name)
            i += 1
        continue
    
    i += 1

if current_route:
    routes.append(current_route)

# Now merge into existing data
for r in routes:
    num = r['number']
    route_id = num.replace('/', '_').replace(' ', '')
    
    mapped_stops = []
    for stop_name in r['stops']:
        normalized_name = stop_name.lower().strip()
        if normalized_name in name_to_id:
            mapped_stops.append(name_to_id[normalized_name])
        else:
            # Create a new stop ID
            new_id = re.sub(r'[^a-z0-9]+', '_', normalized_name).strip('_')
            # Check if id already exists
            base_id = new_id
            counter = 1
            while new_id in existing_stops:
                new_id = f"{base_id}_{counter}"
                counter += 1
            
            # Add to stops
            new_stop = {
                "id": new_id,
                "name": stop_name.title(),
                "lat": 17.72, # default Vizag lat
                "lng": 83.3,  # default Vizag lng
                "zone": "general"
            }
            existing_stops[new_id] = new_stop
            name_to_id[normalized_name] = new_id
            data['stops'].append(new_stop)
            mapped_stops.append(new_id)
            print(f"Added new stop: {stop_name} (ID: {new_id})")

    if num in number_to_route:
        # Update existing
        existing = number_to_route[num]
        existing['stops'] = mapped_stops
        if r['distanceKm'] > 0:
            existing['distanceKm'] = r['distanceKm']
        
        # Force update name if it looks broken or we have better data
        if r.get('start') and r.get('end'):
            existing['name'] = f"{r['start'].title()} \u2013 {r['end'].title()}"
        elif "\u2013" in existing['name'] and len(existing['name'].strip()) < 5:
            start_name = r['stops'][0].title() if r['stops'] else ""
            end_name = r['stops'][-1].title() if r['stops'] else ""
            existing['name'] = f"{start_name} \u2013 {end_name}"
            
        print(f"Updated existing route {num}")
    else:
        # Create new route
        start_name = r.get('start', r['stops'][0] if r['stops'] else "").title()
        end_name = r.get('end', r['stops'][-1] if r['stops'] else "").title()
        
        # Determine type based on number (heuristic)
        r_type = "City Ordinary"
        r_type_code = "CO"
        if "K" in num or "A" in num or num in ["111", "500"]:
            r_type = "Metro Express"
            r_type_code = "ME"
            
        new_route = {
            "id": route_id,
            "number": num,
            "type": r_type,
            "typeCode": r_type_code,
            "name": f"{start_name} \u2013 {end_name}",
            "stops": mapped_stops,
            "baseFare": 15 if r_type_code == "ME" else 10,
            "typicalTimeMin": max(30, r['distanceKm'] * 2), # rough estimate
            "crowdLevel": "medium",
            "note": "Imported from new data"
        }
        if r['distanceKm'] > 0:
            new_route['distanceKm'] = r['distanceKm']
            
        data['routes'].append(new_route)
        number_to_route[num] = new_route
        print(f"Added new route {num}")

# Write back to JS file
js_output = f"const VIZAG_DATA = {json.dumps(data, indent=2)};\n\nif (typeof module !== 'undefined' && module.exports) module.exports = VIZAG_DATA;\n"

with open(JS_FILE, 'w', encoding='utf-8') as f:
    f.write(js_output)

print(f"Successfully processed {len(routes)} routes from text file.")
print(f"Total routes now: {len(data['routes'])}")
print(f"Total stops now: {len(data['stops'])}")

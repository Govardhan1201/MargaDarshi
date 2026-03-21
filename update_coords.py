import re
import json

TXT_FILE = "C:/Users/user/Margadarshi/BUS STOPP.txt"
JS_FILE = "C:/Users/user/Margadarshi/data/vizag_routes.js"

with open(TXT_FILE, 'r', encoding='utf-8') as f:
    raw_text = f.read()

# Read the existing JS file
with open(JS_FILE, 'r', encoding='utf-8') as f:
    js_content = f.read()

json_str_match = re.search(r'const\s+VIZAG_DATA\s*=\s*(\{.*?\})\s*;\s*\n', js_content, re.DOTALL)
if json_str_match:
    json_str = json_str_match.group(1)
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        exit(1)
else:
    print("Could not find VIZAG_DATA in JS file")
    exit(1)

stops = data.get('stops', [])
name_to_stop = {s['name'].lower().strip(): s for s in stops}
id_to_stop = {s['id']: s for s in stops}

# Parse coordinates
pattern = re.compile(r'(.*?)\n?\[(.*?)\]', re.DOTALL)
matches = pattern.findall(raw_text)

updated_count = 0
for text_part, coords_part in matches:
    text_part = text_part.strip()
    if not text_part or "the below are same stops" in text_part.lower():
        continue
    
    # Parse coords
    try:
        lat_str, lng_str = coords_part.split(',')
        lat = float(lat_str.strip())
        lng = float(lng_str.strip())
    except Exception as e:
        print(f"Error parsing coords for {text_part}: {e}")
        continue
    
    # Extract names: "A and B (C)" or just "A"
    names_to_try = []
    
    # If there are parentheses, extract that as primary
    paren_match = re.search(r'\((.*?)\)', text_part)
    if paren_match:
        names_to_try.append(paren_match.group(1).lower().strip())
    
    # Split by 'and', ',', etc.
    clean_text = re.sub(r'\(.*?\)', '', text_part).replace(' and ', ',')
    parts = [p.strip().lower() for p in clean_text.split(',')]
    names_to_try.extend([p for p in parts if p])
    
    matched = False
    for n in names_to_try:
        if n in name_to_stop:
            stop = name_to_stop[n]
            stop['lat'] = lat
            stop['lng'] = lng
            print(f"Updated {stop['name']} ({stop['id']}) with coords {lat}, {lng}")
            updated_count += 1
            matched = True
            break
        # also try checking if ID matches
        potential_id = re.sub(r'[^a-z0-9]+', '_', n).strip('_')
        if potential_id in id_to_stop:
            stop = id_to_stop[potential_id]
            stop['lat'] = lat
            stop['lng'] = lng
            print(f"Updated {stop['name']} ({stop['id']}) with coords {lat}, {lng}")
            updated_count += 1
            matched = True
            break
            
    if not matched:
        print(f"No match found for: {text_part} (tried {names_to_try})")

print(f"Successfully updated {updated_count} stops.")

js_output = f"const VIZAG_DATA = {json.dumps(data, indent=2)};\n\nif (typeof module !== 'undefined' && module.exports) module.exports = VIZAG_DATA;\n"

with open(JS_FILE, 'w', encoding='utf-8') as f:
    f.write(js_output)

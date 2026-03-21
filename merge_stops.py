import json
import re

JS_FILE = "C:/Users/user/Margadarshi/data/vizag_routes.js"

# Duplicate mapping: { CorrectName: { 'aliases': [list of bad names], 'coords': [lat, lng] } }
merges = {
    "Akkayyapalem": {"aliases": ["Akkayyapalem", "Akkayapalem"], "coords": [17.73625339318663, 83.29979319130885]},
    "Anakapalli": {"aliases": ["Anakapalle", "Anakapalli"], "coords": [17.67480572793532, 83.00072970972529]},
    "Arilova": {"aliases": ["Arilova", "Arilova colony"], "coords": [17.76578115855434, 83.31710178081683]},
    "AU Outgate": {"aliases": ["AU Out gate", "Au Outgate"], "coords": [17.722175894303675, 83.32761265483975]},
    "Convent Jn": {"aliases": ["Convent", "Convent Jn", "Convent Junction"], "coords": [17.717637884574902, 83.29023910892546]},
    "Yelamanchili": {"aliases": ["elamanchili", "Yelamanchili"], "coords": [17.546649975636022, 82.85387701193353]},
    "Yendada": {"aliases": ["endada", "yendada village"], "coords": [17.78286239493434, 83.35801591968006]},
    "Gopalapatnam": {"aliases": ["Gopalpatnam", "Gopalapatnam", "gpt"], "coords": [17.746640682273533, 83.22134357847699]},
    "Gurudwara": {"aliases": ["Gurudwar", "Gurudwara"], "coords": [17.736752380532323, 83.30731046506783]},
    "Kurmannapalem": {"aliases": ["kuramannapalem", "kurmannapalem", "kuramannaplem"], "coords": [17.685525906352943, 83.16847971892675]},
    "Madhurawada": {"aliases": ["Madhurawada", "Madhurwada", "Madurwada"], "coords": [17.814423558194008, 83.35635805403801]},
    "Malkapuram": {"aliases": ["Malkapuram", "Malkapuram Gajuwaka"], "coords": [17.688611324791193, 83.24614186832345]},
    "MVP Colony": {"aliases": ["Mvp colony", "mvp complex"], "coords": [17.74155128758011, 83.34346699110982]},
    "Naval Dockyard": {"aliases": ["Naval base", "naval dockyard"], "coords": [17.698343496326277, 83.2693765263235]},
    "Pendurthi": {"aliases": ["Pendurti", "Pendhurty"], "coords": [17.81179726391017, 83.20749884929646]},
    "RK Beach": {"aliases": ["RK Beach", "R K beach"], "coords": [17.71131382255581, 83.3181805829017]},
    "RTC Complex": {"aliases": ["Rtc", "RTC Complex"], "coords": [17.724012695166742, 83.30644972304506]},
    "Scindia": {"aliases": ["Scindia", "scidia"], "coords": [17.68823281500555, 83.26795923551329]},
    "Steel plant Sector 11": {"aliases": ["Sector 11", "steelplant sector 11"], "coords": [17.652154177961627, 83.13349009732067]},
    "Simhachalam": {"aliases": ["Simhachalam", "Simhachalam Bus station"], "coords": [17.77186277030809, 83.24356202836081]},
    "Town Kotharoad": {"aliases": ["Town Kotharoad", "Town Kotha Road"], "coords": [17.702142399223977, 83.29654077148736]}
}

with open(JS_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const VIZAG_DATA = (\{.*\});', content, re.DOTALL)
if not match:
    print("Could not find VIZAG_DATA in existing JS.")
    exit(1)
    
data = json.loads(match.group(1))

stops_list = data["stops"]
routes_list = data["routes"]

# Map aliases to primary IDs
replacement_map = {} # old_id -> new_id
new_stops_to_add = {} # new_id -> stop_obj

# First, normalize the stops array 
filtered_stops = []

def generate_id(name):
    return name.lower().replace(" ", "_").replace("-", "_")

for correct_name, info in merges.items():
    primary_id = generate_id(correct_name)
    aliases_lower = [a.lower().strip() for a in info["aliases"]]
    aliases_lower.append(correct_name.lower().strip())
    
    # Create the unified stop
    new_stops_to_add[primary_id] = {
        "id": primary_id,
        "name": correct_name,
        "lat": info["coords"][0],
        "lng": info["coords"][1]
    }
    
    # Identify all old stops that match aliases
    for s in stops_list:
        if s["name"].lower().strip() in aliases_lower:
            replacement_map[s["id"]] = primary_id

# Now rebuild the final stops list
final_stops = []
for s in stops_list:
    if s["id"] not in replacement_map:
        final_stops.append(s)

# Add the newly consolidated stops
for primary_id, stop_obj in new_stops_to_add.items():
    final_stops.append(stop_obj)

data["stops"] = final_stops

# Update all routes to replace old IDs with the consolidated ID
for route in routes_list:
    new_route_stops = []
    seen = set()
    for sid in route["stops"]:
        # If it needs replacement, replace it
        mapped_id = replacement_map.get(sid, sid)
        # Avoid consecutive duplicates caused by merging
        if not new_route_stops or new_route_stops[-1] != mapped_id:
            new_route_stops.append(mapped_id)
    route["stops"] = new_route_stops

# Write back
new_json_str = json.dumps(data, indent=4)
new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]

with open(JS_FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Successfully merged {len(merges)} groups of stops.")
print(f"Removed {len(replacement_map)} redundant stop entries and added {len(new_stops_to_add)} consolidated ones.")

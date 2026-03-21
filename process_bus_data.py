
import re

ocr_text = """
6 Simhachalam OHPO Gopalapatnam, NAD, Kancharapalem, Convent junction, Town Kotharoad
6A/H RTC complex Simhachalam hills Railway Station, Kancharapalem, NAD, Gopalapatnam
10 A Visakhapatnam Airport R K Beach Via. NAD, Gurudwara, RTC Complex
111 Kuramanapalem Tagarapuvalasa Via. Gajuwaka, NAD, Gurudwara, Zoo Park, Madurwada
5D Town Kotharoad Dabbanda Convent, Kancharapalem, NAD, Gopalapatnam, Pendurthi
10K RTC complex Kailashagiri Jagadamba, Rk beach, Vuda park, Tenneti park
28 RK beach Simhachalam Bus Station Jagadamba, RTC Complex, NAD, Gopalapatnam
28R RK beach Simhachalam Bus Station Jagadamba, RTC, Railway Station, NAD, Gopalapatnam
28A/28K RK beach Pendurthy/Kottavalasa GPT, NAD, RTC, Jagadamba, Collector office
28A/D RK beach Denderu Jagadamba, RTC, Railway Station, NAD, Gopalapatnam, Pendurthi
28C RK Beach Chintalagraharam Jagadamba, RTC Complex, NAD, Gopalapatnam, Vepagunta
28J RK Beach Sujatanagar Jagadamba, RTC Complex, NAD, Gopalapatnam, Vepagunta
28P RK Beach Sabbavaram Jagadamba, RTC Complex, NAD, Gopalapatnam, Pendurthi
28Z/H Zilla Parishad Simhachalam hills Jagadamba, RTC, Gurudwar, NAD, Gopalapatnam
28A/P RTC Complex Ravalammapalem Railway Station, Kancharapalem, NAD, GPT, Pendurthi
68/68K RK beach Pendurthi/Kothavalasa Jagadamba, Asilmetta, Maddilapalem, Arilova, Simhachalam
505 Simhachalam Scindia Gopalapatnam, NAD,Kancharapalem, Convent Jn, naval Dockyard
55 Simhachalam Scindia Gopalapatnam, NAD, BHPV, Gajuwaka, Malkapuram
55K Kothavalasa Scindia Pendurthi, Gopalapatnam, NAD, Gajuwaka, Malkapuram
55V Vepada Scindia Simhachalam, Gopalapatnam, NAD, Gajuwaka, Malkapuram
55T Scindia Tagarapuvalasa malkapuram gajuwaka, NAD, Gopalpatnam, Pendurthy, Anandapuram
60 Simhachalam OHPO Adavivaram, Maddilapalem, RTC Complex, Jagadamba
60R RK Beach Arilova Colony Jagadamba, RTC Complex, Maddilapalem
38 RTC Complex Gajuwaka Gurudwara, NAD, BHPV
38A RTC Complex Mindi Gurudwara, NAD, BHPV
38B RTC Complex Bhanojithota Gurudwara, NAD, Sheelanagar
38C RTC Complex Sundarayya Colony Gurudwara, NAD, BHPV, Gajuwaka
38D RTC Complex Nadupur Dairy Colony Gurudwara, NAD, BHPV, Gajuwaka, Pedagantyada
38H RTC Complex Gantyada HB Colony Visakhapatnam Airport, Gurudwara, NAD, BHPV, Gajuwaka, Pedagantyada
38IT Kurmannapalem IT Park Gajuwaka, NAD, Gurudwara, RTC Complex, Maddilapalem, Carshed
38J RTC Complex Janata Colony Gurudwara, NAD, BHPV, Gajuwaka, Scindia
38K RTC Complex Steelplant Sector 5 Gurudwara, NAD, BHPV, Gajuwaka
38M Marikavalasa Kurmannapalem Madhurawada, Maddilapalem, Gurudwara, NAD, BHPV, Gajuwaka
38N RTC Complex Nadupuru Gurudwara, NAD, BHPV, Gajuwaka, Pedagantyada
38R Maddilapalem Rambilli Gurudwara, NAD, BHPV, Parawada
38T RTC Complex Steelplant Sector 11 Gurudwara, NAD, BHPV, Gajuwaka, Kurmannaplem
38Y RTC Complex Duvvada Railway Station Gurudwara, NAD, BHPV, Gajuwaka, Kurmannapalem
900K RTC Complex Bhimili Waltair, MVP Colony, Rushikonda, gitam, mangamaripeta, INS Kalinga
900T RTC Complex Tagarapuvalasa Waltair, MVP Colony, Rushikonda, gitam, mangamaripeta, INS Kalinga
999 RTC Complex Bhimili Maddilapalem, Endada, Madhurwada, Anandapuram
222 RTC Complex Tagarapuvalasa Maddilapalem, Endada, Madhurawada, Anandapuram
400 RTC Complex Kurmannapalem Railway Station, Scindia, Malkapuram, Gajuwaka
400H Maddilapalem Gantyada HB Colony RTC, Railway Station, Scindia, Gajuwaka, Pedagantyada
400N RTC Complex Vadacheepurupalli Railway Station, Scindia, Malkapuram, Gajuwaka, Kurmannapalem, Sector 11, Parawada, NTPC
400S Maddilapalem Narava RTC Complex, Railway Station, Scindia, Gajuwaka, Kurmannapalem
400K Maddilapalem Duvvada Railway Station RTC, Railway Station, Scindia, Gajuwaka, Kurmannapalem
400Y Maddilapalem Yelamanchili RTC, Railway Station, Scindia, Gajuwaka, Achutapuram
900 Maddilapalem Railway Station MVP Colony, Waltair, RTC Complex
540 MVP Complex Simhachalam Maddilapalem, Gurudwara, NAD, Gopalapatnam
540M MVP Complex Gajuwaka Maddilapalem, Gurudwara, NAD, BHPV
541 Maddilapalem Kothavalasa Gurudwara, NAD, Gopalapatnam, Vepagunta, Pendurthi
211 Railway Station Vizianagaram RTC Complex, Maddilapalem, Madhurawada, Tagarapuvalasa
60C Arilova Colony OHPO Maddilapalem, RTC Complex, Jagadamba, Town Kotharoad
20A HB Colony OHPO Sitammadhara, Satyam Junction, RTC, Jagadamba, Town Kotharoad
69 Arilova Colony Railway Station HB Colony, Sitammadhara, Satyam Junction, RTC Complex
52D Ravindra Nagar OHPO Adarsha Nagar, Maddilapalem, RTC, Jagadamba, Town Kotharoad
52S/52V Sagar Nagar OHPO Visalakshi Nagar, Maddilapalem, RTC, Jagadamba, Town Kotharoad
52E Yendada Village OHPO Rushikonda, Endada, Maddilapalem, RTC, Jagadamba, Town Kotharoad
25S OHPO Nagarapalem Jagadamba, RTC Complex, Maddilapalem, Endada, Carshed
25D/M OHPO Midhilapuri Colony Jagadamba, RTC Complex, Maddilapalem, Endada, Carshed
25D/V OHPO Vambey Colony Jagadamba, RTC Complex, Maddilapalem, Endada, Carshed
25E OHPO Kommadi Jagadamba, RTC Complex, Maddilapalem, Endada, Madhurawada
25G OHPO Ganesh Nagar Jagadamba, RTC Complex, Maddilapalem, Endada, Madhurawada
25IT RTC Complex IT Park Maddilapalem, Endada, Carshed, Midhilapuri Colony
25K OHPO Bakkannapalem Jagadamba, RTC Complex, Maddilapalem, Endada, Madhurawada
25M OHPO Marikavalasa Jagadamba, RTC Complex, Maddilapalem, Endada, Madhurawada
25P Ratnagiri HB Colony OHPO PM Palem, Endada, Maddilapalem, RTC Complex, Jagadamba
14 Venkojipalem OHPO MVP Colony, Waltair, AU Outgate, Jagadamba, Town Kotharoad
900R RTC Complex Rushikonda INS Kalinga,Sagar nagar, RTC
36 Collector Office Mindi Town Kotharoad, Convent, Scindia, Gajuwaka, BHPV
6B OHPO Chintagatla Town Kotharoad, Convent, NAD, Sheelanagar, Narava
48 Madhavadhara MN Club Muralinagar, Kailasapuram, Akkayyapalem, RTC Complex, Jagadamba
48A Madhavadhara OHPO Muralinagar, Kailasapuram, Akkayapalem, RTC Complex, Town Kotharoad
12K Town Kotharoad Kothavalasa Railway Station, Kancharapalem, NAD, GPT, Pendurthi
12D RTC Complex Devarapalle NAD, Gopalapatnam, Pendurthi, Kothavalasa, Anandapuram
16 Purna Market Yarada Convent junction, Scindia, Naval base
99 Collector Office Gajuwaka Jagadamba, Town Kotharoad, Convent, Scindia, Malkapuram
99A/C Collector Office Chodavaram Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka, Kurmannapalem, Anakapalle
99K Collector Office Kurmannapalem Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka
1T Vuda Park Kapulatunglam RK Beach, Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka
65F Fishing Harbour Gangavaram Collector Office, Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka, Pedagantyada, Dibbapalem
77 Collector Office Thanam Jagadamba, Town Kotharoad, Convent, Scidia, Gajuwaka
77T Collector Office Thadi Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka
63 RK Beach Dibbapalem Town Kotharoad, Convent, Scindia, Gajuwaka, Pedagantyada
64A Collector Office Swayambuvaram Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka
500 RTC Complex Anakapalle Gurudwar, NAD, Gajuwaka, Kurmannapalem, Aganampudi
500A Maddilapalem Addaroad Gurudwar, NAD, Gajuwaka, Kurmannaplem, Anakapalli, Elamanchili
500P Anakapalle PM Palem Kurmannapalem, Gajuwaka, Scindia, Convent, RTC Complex, Maddilapalem, Carshed
500Y RTC Complex Yelamanchili Gurudwar, NAD, Gajuwaka, Kurmannapalem, Anakapalle
38H RTC Complex Gantyada HB Colony Gurudwar, NAD, BHPV, Gajuwaka
555 RTC Complex Chodavaram Gurudwar, NAD, Gopalapatnam, Pendurthi, Sabbavaram
25J Railway Station Sevanagar RTC Complex, Maddilapalem, Endada, Madhurawada
25R Railway Station Gurajadanagar RTC Complex, Maddilapalem, Endada, PM Palem
300C RTC Complex Chodavaram NAD, Gopalapatnam, Pendurthi, Sabbavaram
300M RTC Complex Madugula NAD, Gopalapatnam, Pendurthi, Sabbavaram, Chodavaram
333 Town Kotharoad Devarapalle Convent, NAD, Gopalapatnam, Pendurthi, Kothavalasa
333K Town Kotharoad K.Kotapad Convent, Kancharapalem, NAD, Gopalapatnam, Pendurthi
328 K.Kotapad RK Beach Jagadamba, RTC Complex, NAD, Gopalapatnam, Pendurthi
600 Anakapalle Simhachalam Aganampudi, Kurmannapalem, Gajuwaka, NAD, Gopalapatnam
600C RTC Complex Anakapalle Railway Station, Convent, Gajuwaka, Kurmannapalem, Aganampudi
700 Simhachalam Vizianagaram Adavivaram, Shontyam, Anandapuram, Padmanabham
500A/C RTC Complex Achutapuram Gurudwar, NAD, Gajuwaka, Kurmannapalem, Anakapalle
844 Collector Office Kollivanipalem Jagadamba, Town Kotharoad, Convent, Scindia, Gajuwaka, Kurmannapalem, Parawada
888 Anakapalle Tagarapuvalasa Pendurthy, sontyam, Anandapuram
14A Arilova Colony OHPO Venkojipalem, Mvp colony,AU Out gate,Jagadamba,Kotha road
744 Collector office Dosuru Jagadamba, Town Kotha Road, Convent, Scindia, Gajuwaka, Kurmannapalem, Parawada
"""

def clean_name(name):
    name = name.strip()
    # Normalize common names
    mapping = {
        "RTC complex": "RTC Complex",
        "R K Beach": "RK Beach",
        "Rk beach": "RK Beach",
        "Town Kotharoad": "Town Kotharoad",
        "Town Kotha Road": "Town Kotharoad",
        "Railway Station": "Visakhapatnam Railway Station",
        "MVP complex": "MVP Complex",
        "MVP Colony": "MVP Colony",
        "Mvp colony": "MVP Colony",
        "Simhachalam Bus Station": "Simhachalam",
        "Kuramanapalem": "Kurmannapalem",
        "Kurmannaplem": "Kurmannapalem",
        "Pendurthy": "Pendurthi",
        "Kottavalasa": "Kothavalasa",
        "GPT": "Gopalapatnam",
        "Gopalpatnam": "Gopalapatnam",
        "naval Dockyard": "Naval Dockyard",
        "Gurudwara": "Gurudwara",
        "Gurudwar": "Gurudwara",
        "Carshed": "Car Shed",
        "Midhilapuri Colony": "Mithilapuri Colony",
        "Akkayyapalem": "Akkayyapalem",
        "Akkayapalem": "Akkayyapalem"
    }
    for k, v in mapping.items():
        if k in name:
            name = name.replace(k, v)
    return name

stops = set()
routes = []

# Simple line-by-line processing
for line in ocr_text.strip().split('\n'):
    line = line.strip()
    if not line: continue
    
    # Try multiple strategies to find From/To/Via
    # Pattern 1: No Start ... End ... via1, via2, ...
    # This is rough because "From" and "To" can be multi-word
    # But usually "via" starts with common landmarks
    
    parts = line.split(' ')
    if len(parts) < 4: continue
    
    no = parts[0]
    
    # Regex attempt to find the "via" section which usually starts with a capitalized word after some middle words
    match = re.search(r'^([A-Z0-9/]+)\s+(.*?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+([A-Z].*)$', line)
    if match:
        no, start, end, via_str = match.groups()
        start = clean_name(start)
        end = clean_name(end)
        stops.add(start)
        stops.add(end)
        vias = [clean_name(v.strip()) for v in via_str.split(',') if v.strip()]
        for v in vias: stops.add(v)
        routes.append({"no": no, "start": start, "end": end, "vias": vias})
    else:
        # Fallback for lines that don't match perfectly
        # Just grab unique words that look like stop names (capitalized)
        for part in parts[1:]:
            p = clean_name(part.rstrip(',.'))
            if p and p[0].isupper():
                stops.add(p)

sorted_stops = sorted(list(stops))
print(f"Total Unique Stops: {len(sorted_stops)}")
for s in sorted_stops:
    print(s)

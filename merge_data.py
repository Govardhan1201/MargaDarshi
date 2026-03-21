import json

with open('C:/Users/user/Margadarshi/data/vizag_routes.js', 'r', encoding='utf-8') as f:
    content = f.read()
    json_str = content.split('const VIZAG_DATA = ')[1].rsplit(';', 1)[0]
    data = json.loads(json_str)

data['translations'] = {
    'en': {
        'appName': 'M\u0101rgaDarshi',
        'tagline': 'Your Smart Bus Companion in Visakhapatnam',
        'from': 'From',
        'to': 'To',
        'search': 'Find Buses',
        'features': 'Features',
        'howItWorks': 'How It Works',
        'touristSpots': 'Tourist Spots',
        'timetable': 'Bus Timetable',
        'map': 'Bus Map',
        'tips': 'Smart Tips',
        'community': 'Community',
        'chatbot': 'Chat Assistant',
        'faq': 'FAQ',
        'fare': 'Fare',
        'time': 'Travel Time',
        'crowd': 'Crowd Level',
        'cityOrdinary': 'City Ordinary',
        'metroExpress': 'Metro Express',
        'oneDayPass': 'One Day Pass',
        'disclaimer': '\u26a0\ufe0f Times shown are APSRTC scheduled times and may vary.',
        'loginRequired': 'Please login to submit a report.',
        'noRoutes': 'No direct buses found. Try changing stops.',
        'selectFrom': 'Select departure stop',
        'selectTo': 'Select destination stop',
    },
    'te': {
        'appName': '\u0c2e\u0c3e\u0c30\u0c4d\u0c17\u0c2a\u0c41\u0c24\u0c4d\u0c30',
        'tagline': '\u0c35\u0c3f\u0c36\u0c3e\u0c16\u0c2a\u0c1f\u0c4d\u0c28\u0c02\u0c32\u0c4b \u0c2e\u0c40 \u0c38\u0c4d\u0c2e\u0c3e\u0c30\u0c4d\u0c1f\u0c4d \u0c2c\u0c38\u0c4d \u0c38\u0c39\u0c3e\u0c2f\u0c15\u0c41\u0c21\u0c41',
        'from': '\u0c28\u0c41\u0c02\u0c21\u0c3f',
        'to': '\u0c35\u0c30\u0c15\u0c41',
        'search': '\u0c2c\u0c38\u0c4d\u0c38\u0c41\u0c32\u0c41 \u0c35\u0c46\u0c24\u0c15\u0c02\u0c21\u0c3f',
        'features': '\u0c32\u0c15\u0c4d\u0c37\u0c23\u0c3e\u0c32\u0c41',
        'howItWorks': '\u0c01\u0c32\u0c3e \u0c2a\u0c28\u0c3f \u0c1a\u0c47\u0c38\u0c4d\u0c24\u0c41\u0c02\u0c26\u0c3f',
        'touristSpots': '\u0c2a\u0c30\u0c4d\u0c2f\u0c3e\u0c1f\u0c15 \u0c2a\u0c4d\u0c30\u0c26\u0c47\u0c36\u0c3e\u0c32\u0c41',
        'timetable': '\u0c2c\u0c38\u0c4d \u0c38\u0c2e\u0c2f\u0c2a\u0c1f\u0c4d\u0c1f\u0c3f\u0c15',
        'map': '\u0c2c\u0c38\u0c4d \u0c2e\u0c4d\u0c2f\u0c3e\u0c2a\u0c4d',
        'tips': '\u0c38\u0c4d\u0c2e\u0c3e\u0c30\u0c4d\u0c1f\u0c4d \u0c1a\u0c3f\u0c1f\u0c4d\u0c15\u0c3e\u0c32\u0c41',
        'community': '\u0c15\u0c2e\u0c4d\u0c2f\u0c42\u0c28\u0c3f\u0c1f\u0c40',
        'chatbot': '\u0c1a\u0c3e\u0c1f\u0c4d \u0c38\u0c39\u0c3e\u0c2f\u0c15\u0c41\u0c21\u0c41',
        'faq': '\u0c24\u0c30\u0c1a\u0c41\u0c17\u0c3e \u0c05\u0c21\u0c3f\u0c17\u0c47 \u0c2a\u0c4d\u0c30\u0c36\u0c4d\u0c28\u0c32\u0c41',
        'fare': '\u0c1a\u0c3e\u0c30\u0c4d\u0c1c\u0c4d',
        'time': '\u0c2a\u0c4d\u0c30\u0c2f\u0c3e\u0c23 \u0c38\u0c2e\u0c2f\u0c02',
        'crowd': '\u0c30\u0c26\u0c4d\u0c26\u0c40 \u0c38\u0c4d\u0c25\u0c3e\u0c2f\u0c3f',
        'cityOrdinary': '\u0c38\u0c3f\u0c1f\u0c40 \u0c06\u0c30\u0c4d\u0c21\u0c3f\u0c28\u0c30\u0c40',
        'metroExpress': '\u0c2e\u0c46\u0c1f\u0c4d\u0c30\u0c4b \u0c0e\u0c15\u0c4d\u0c38\u0c4d\u0c2a\u0c4d\u0c30\u0c46\u0c38\u0c4d',
        'oneDayPass': '\u0c35\u0c28\u0c4d \u0c21\u0c47 \u0c2a\u0c3e\u0c38\u0c4d',
        'disclaimer': '\u26a0\ufe0f \u0c2a\u0c4d\u0c30\u0c26\u0c30\u0c4d\u0c36\u0c3f\u0c02\u0c1a\u0c3f\u0c28 \u0c38\u0c2e\u0c2f\u0c3e\u0c32\u0c41 APSRTC \u0c37\u0c46\u0c21\u0c4d\u0c2f\u0c42\u0c32\u0c41 \u0c38\u0c2e\u0c2f\u0c3e\u0c32\u0c41.',
        'loginRequired': '\u0c26\u0c2f\u0c1a\u0c47\u0c38\u0c3f \u0c32\u0c3e\u0c17\u0c3f\u0c28\u0c4d \u0c1a\u0c47\u0c2f\u0c02\u0c21\u0c3f.',
        'noRoutes': '\u0c28\u0c47\u0c30\u0c41\u0c17\u0c3e \u0c2c\u0c38\u0c4d\u0c38\u0c41\u0c32\u0c41 \u0c26\u0c4a\u0c30\u0c15\u0c32\u0c47\u0c26\u0c41.',
        'selectFrom': '\u0c2c\u0c2f\u0c32\u0c41\u0c26\u0c47\u0c30\u0c47 \u0c38\u0c4d\u0c1f\u0c3e\u0c2a\u0c4d \u0c0e\u0c02\u0c1a\u0c41\u0c15\u0c4b\u0c02\u0c21\u0c3f',
        'selectTo': '\u0c17\u0c2e\u0c4d\u0c2f\u0c02 \u0c38\u0c4d\u0c1f\u0c3e\u0c2a\u0c4d \u0c0e\u0c02\u0c1a\u0c41\u0c15\u0c4b\u0c02\u0c21\u0c3f'
    }
}

data['chatbot'] = {
    'greetings': ['hello', 'hi', 'namaste', 'hey'],
    'farewords': ['bye', 'goodbye', 'thank you', 'thanks'],
    'responses': [
      {'patterns': ['rk beach', 'beach'], 'reply': '🚌 Take Bus 10A or 28 to RK Beach!'},
      {'patterns': ['airport', 'flight'], 'reply': '✈️ Take Bus 10A to the Airport.'},
      {'patterns': ['complex', 'rtc'], 'reply': '🏢 RTC Complex is the main hub for most buses.'}
    ]
}

with open('C:/Users/user/Margadarshi/data/vizag_routes.js', 'w', encoding='utf-8') as f:
    f.write('// M\u0101rgaDarshi \u2013 Full Dataset from PDF\n')
    f.write('const VIZAG_DATA = ' + json.dumps(data, indent=2) + ';\n')
    f.write('if (typeof module !== \"undefined\") module.exports = VIZAG_DATA;\n')

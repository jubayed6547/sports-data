import json
import requests
import datetime
import pytz

# ১. ESPN ওপেন এপিআই থেকে আজকের আসল খেলার নাম আনা
def get_todays_featured_match():
    sports_endpoints = [
        {"name": "FOOTBALL", "url": "https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard"}, # La Liga
        {"name": "FOOTBALL", "url": "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"}, # Premier League
        {"name": "NBA", "url": "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"},     # Basketball
        {"name": "NHL", "url": "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"}         # Ice Hockey
    ]

    for sport in sports_endpoints:
        try:
            res = requests.get(sport["url"], timeout=8)
            if res.ok:
                data = res.json()
                events = data.get("events", [])
                if events:
                    match = events[0]
                    match_name = match.get("name", "Top Live Match")
                    status = match.get("status", {}).get("type", {}).get("shortDetail", "LIVE")
                    return match_name, f"{sport['name']} • {status.upper()}"
        except Exception:
            continue

    return "Global Sports Arena - Live Satellite Feed", "LIVE SPORTS HD"

# ২. আসল স্পোর্টস চ্যানেলগুলোর এমবেড স্ট্রিম লিংক (আইফ্রেম)
def get_real_sports_embeds():
    # এই লিংকগুলো সরাসরি স্পোর্টস টিভি সম্প্রচার প্রোভাইডারদের এমবেড প্লেয়ার
    embed_streams = [
        {
            "streamer": "Server 1: TNT Sports",
            "channel": "TNT Sports 1 UK",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 1,
            "lang": "English",
            "url": "https://epicstream.net/embed/tnt1"
        },
        {
            "streamer": "Server 2: Sky Sports",
            "channel": "Sky Sports Main Event",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 2,
            "lang": "English",
            "url": "https://epicstream.net/embed/skymain"
        },
        {
            "streamer": "Server 3: beIN Sports",
            "channel": "beIN Sports 1 English",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 1,
            "lang": "English",
            "url": "https://epicstream.net/embed/bein1"
        },
        {
            "streamer": "Server 4: Movistar LaLiga",
            "channel": "Movistar LaLiga HD",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 2,
            "lang": "Spanish",
            "url": "https://epicstream.net/embed/movistarliga"
        },
        {
            "streamer": "Server 5: DAZN Sport",
            "channel": "DAZN 1 Live Feed",
            "mobile": "yes",
            "quality": "1080p Ultra",
            "ads": 1,
            "lang": "English",
            "url": "https://epicstream.net/embed/dazn1"
        },
        {
            "streamer": "Server 6: ESPN USA",
            "channel": "ESPN Live USA",
            "mobile": "yes",
            "quality": "720p HD",
            "ads": 2,
            "lang": "English",
            "url": "https://epicstream.net/embed/espn"
        },
        {
            "streamer": "Server 7: Fox Sports",
            "channel": "Fox Sports 1 (FS1)",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 1,
            "lang": "English",
            "url": "https://epicstream.net/embed/fs1"
        },
        {
            "streamer": "Server 8: Sony Sports",
            "channel": "Sony Sports Ten 1",
            "mobile": "yes",
            "quality": "HD",
            "ads": 1,
            "lang": "Hindi/Eng",
            "url": "https://epicstream.net/embed/sonyten1"
        },
        {
            "streamer": "Server 9: Premier Sports",
            "channel": "Premier Sports 1",
            "mobile": "yes",
            "quality": "HD",
            "ads": 2,
            "lang": "English",
            "url": "https://epicstream.net/embed/premiersports1"
        },
        {
            "streamer": "Server 10: SuperSport",
            "channel": "SuperSport Premier",
            "mobile": "yes",
            "quality": "HD",
            "ads": 1,
            "lang": "English",
            "url": "https://epicstream.net/embed/supersport"
        },
        {
            "streamer": "Server 11: Willow Cricket",
            "channel": "Willow Cricket Live",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 1,
            "lang": "English",
            "url": "https://epicstream.net/embed/willow"
        },
        {
            "streamer": "Server 12: Eurosport",
            "channel": "Eurosport 1 Live",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 2,
            "lang": "English",
            "url": "https://epicstream.net/embed/eurosport1"
        }
    ]
    return embed_streams

def run_automation():
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.datetime.now(tz)
    current_time_str = now.strftime("%I:%M %p LIVE")

    match_title, category = get_todays_featured_match()
    streams = get_real_sports_embeds()

    payload = {
        "title": match_title,
        "category": category,
        "time": current_time_str,
        "telegramLink": "https://t.me/your_channel",
        "streams": streams
    }

    with open("live.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Updated live.json with Live Sports Embeds! Match: {match_title}")

if __name__ == "__main__":
    run_automation()

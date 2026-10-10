import json
import requests
import datetime
import pytz

def get_todays_featured_match():
    sports_endpoints = [
        {"name": "FOOTBALL", "url": "https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard"},
        {"name": "FOOTBALL", "url": "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"},
        {"name": "NBA", "url": "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"},
        {"name": "NHL", "url": "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"}
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

def get_real_sports_embeds():
    # সরাসরি ওপেন এমবেড ফিড (TopEmbed & Streamed)
    embed_streams = [
        {
            "streamer": "Server 1: TNT Sports",
            "channel": "TNT Sports 1 HD",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 1,
            "lang": "English",
            "url": "https://topembed.pw/channel/TNTSports1"
        },
        {
            "streamer": "Server 2: Sky Sports",
            "channel": "Sky Sports Main Event",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 2,
            "lang": "English",
            "url": "https://topembed.pw/channel/SkySportsMainEvent"
        },
        {
            "streamer": "Server 3: beIN Sports",
            "channel": "beIN Sports 1 English",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 1,
            "lang": "English",
            "url": "https://topembed.pw/channel/beINSports1"
        },
        {
            "streamer": "Server 4: Movistar LaLiga",
            "channel": "Movistar LaLiga HD",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 2,
            "lang": "Spanish",
            "url": "https://topembed.pw/channel/MovistarLaLiga"
        },
        {
            "streamer": "Server 5: DAZN Sport",
            "channel": "DAZN 1 Live Feed",
            "mobile": "yes",
            "quality": "1080p Ultra",
            "ads": 1,
            "lang": "English",
            "url": "https://topembed.pw/channel/DAZN1"
        },
        {
            "streamer": "Server 6: ESPN USA",
            "channel": "ESPN USA Live HD",
            "mobile": "yes",
            "quality": "720p HD",
            "ads": 2,
            "lang": "English",
            "url": "https://topembed.pw/channel/ESPN"
        },
        {
            "streamer": "Server 7: Fox Sports 1",
            "channel": "Fox Sports 1 (FS1)",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 1,
            "lang": "English",
            "url": "https://topembed.pw/channel/FS1"
        },
        {
            "streamer": "Server 8: Sony Sports",
            "channel": "Sony Sports Ten 1",
            "mobile": "yes",
            "quality": "HD",
            "ads": 1,
            "lang": "Hindi/Eng",
            "url": "https://topembed.pw/channel/SonySportsTen1"
        },
        {
            "streamer": "Server 9: Premier Sports",
            "channel": "Premier Sports 1",
            "mobile": "yes",
            "quality": "HD",
            "ads": 2,
            "lang": "English",
            "url": "https://topembed.pw/channel/PremierSports1"
        },
        {
            "streamer": "Server 10: SuperSport",
            "channel": "SuperSport Premier",
            "mobile": "yes",
            "quality": "HD",
            "ads": 1,
            "lang": "English",
            "url": "https://topembed.pw/channel/SuperSportPremierLeague"
        },
        {
            "streamer": "Server 11: Willow Cricket",
            "channel": "Willow Cricket Live",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 1,
            "lang": "English",
            "url": "https://topembed.pw/channel/WillowCricket"
        },
        {
            "streamer": "Server 12: Eurosport 1",
            "channel": "Eurosport 1 Live HD",
            "mobile": "yes",
            "quality": "1080p HD",
            "ads": 2,
            "lang": "English",
            "url": "https://topembed.pw/channel/Eurosport1"
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

    print(f"Updated live.json with TopEmbed Streams! Match: {match_title}")

if __name__ == "__main__":
    run_automation()

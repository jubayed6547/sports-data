import json
import re
import requests
import datetime
import pytz

# ১. ESPN ওপেন এপিআই থেকে আজকের সেরা খেলার নাম ও সময় বের করা
def get_todays_featured_match():
    # চেক করার স্পোর্টস তালিকা: ফুটবল, এনবিএ বাস্কেটবল, এনএইচএল হকি
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
                    # প্রথম ম্যাচটি পিক করা
                    match = events[0]
                    match_name = match.get("name", "Top Live Match")
                    status = match.get("status", {}).get("type", {}).get("shortDetail", "LIVE")
                    return match_name, f"{sport['name']} • {status.upper()}"
        except Exception as e:
            continue

    # কোনো লাইভ না পেলে ডিফল্ট হেডার
    return "Global Sports Arena - Live Satellite Feed", "LIVE SPORTS HD"

# ২. iptv-org থেকে স্পোর্টস চ্যানেলের রিয়েল m3u8 লিংক পার্স করা
def parse_iptv_org_streams():
    # iptv-org এর স্পোর্টস চ্যানেল এবং স্পোর্টসট্রাইবাল প্লেলিস্ট
    m3u_urls = [
        "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/uk_sportstribal.m3u",
        "https://iptv-org.github.io/iptv/categories/sports.m3u"
    ]

    streams = []

    for m3u_url in m3u_urls:
        try:
            response = requests.get(m3u_url, timeout=10)
            if response.ok:
                lines = response.text.splitlines()
                current_channel = None

                for line in lines:
                    line = line.strip()
                    # #EXTINF থেকে চ্যানেলের নাম বের করা
                    if line.startswith("#EXTINF"):
                        name_match = re.search(r',(.+)$', line)
                        if name_match:
                            current_channel = name_match.group(1).strip()
                        else:
                            current_channel = "Sports Live HD"
                    # পরবর্তী লাইন যা http দিয়ে শুরু হয় তা-ই হলো m3u8 লিংক
                    elif line.startswith("http") and current_channel:
                        streams.append({
                            "streamer": f"Server {len(streams) + 1}",
                            "channel": current_channel[:25], # নাম বেশি বড় হলে ট্রিম করা
                            "mobile": "yes",
                            "quality": "1080p" if "1080" in current_channel else "HD",
                            "ads": 1 if len(streams) % 2 == 0 else 2,
                            "lang": "English",
                            "url": line
                        })
                        current_channel = None

                    # ১২টি লাইভ সার্ভার পেয়ে গেলে লুপ থামাবে
                    if len(streams) >= 12:
                        break
            if len(streams) >= 12:
                break
        except Exception as e:
            print(f"Error fetching from {m3u_url}: {e}")

    # ব্যাকআপ স্ট্রিম (যদি iptv-org ডাউন থাকে)
    if not streams:
        streams.append({
            "streamer": "Server 1 Main",
            "channel": "Sports Grid Live",
            "mobile": "yes",
            "quality": "HD",
            "ads": 1,
            "lang": "English",
            "url": "https://sportsgrid-tribal.amagi.tv/playlist.m3u8"
        })

    return streams

def run_automation():
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.datetime.now(tz)
    current_time_str = now.strftime("%I:%M %p LIVE")

    # অটোমেটিক ম্যাচের নাম আনা
    match_title, category = get_todays_featured_match()

    # iptv-org থেকে আসল স্পোর্টস চ্যানেলের লিংক নিয়ে আসা
    streams = parse_iptv_org_streams()

    payload = {
        "title": match_title,
        "category": category,
        "time": current_time_str,
        "telegramLink": "https://t.me/your_channel",
        "streams": streams
    }

    with open("live.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Automated Update Complete! Featured Match: {match_title}")

if __name__ == "__main__":
    run_automation()

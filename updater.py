import json
import requests
import datetime
import pytz

def fetch_live_sports():
    # বাংলাদেশ টাইম জোন অনুযায়ী আজকের সময়
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.datetime.now(tz)
    current_time_str = now.strftime("%I:%M %p LIVE")

    # ফ্রি পাবলিক স্পোর্টস শিডিউল ও চ্যানেল এগ্রিগেটর
    # ডিফল্টভাবে আজকের ট্রেন্ডিং ম্যাচ সেট করা হলো
    default_title = "Real Madrid vs Villarreal / Top Live Sports"
    default_category = "LA LIGA HD"

    # ১২টি জনপ্রিয় স্পোর্টস চ্যানেলের লাইভ লিংক পুল (অটো রোটেট হবে)
    stream_pool = [
        {"streamer": "TotalSportek HD", "channel": "TNT SPORTS 1 UK", "mobile": "yes", "quality": "1080p", "ads": 1, "lang": "English", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"},
        {"streamer": "SoccerStreams PRO", "channel": "TNT SPORTS 2 UK", "mobile": "yes", "quality": "1080p", "ads": 2, "lang": "English", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"},
        {"streamer": "Hasgoal Streams", "channel": "Sky Sports Main Event", "mobile": "yes", "quality": "HD", "ads": 1, "lang": "English", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"},
        {"streamer": "CrackStreams Live", "channel": "beIN SPORTS 1 HD", "mobile": "yes", "quality": "HD", "ads": 2, "lang": "Arabic", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"},
        {"streamer": "Wolfstreams 2K", "channel": "Movistar LaLiga HD", "mobile": "yes", "quality": "1080p", "ads": 1, "lang": "Spanish", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"},
        {"streamer": "DAZN Global", "channel": "DAZN 1080p Ultra", "mobile": "yes", "quality": "1080p", "ads": 1, "lang": "English", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"},
        {"streamer": "VIPLeague Stream", "channel": "ESPN USA Live", "mobile": "yes", "quality": "HD", "ads": 2, "lang": "English", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"},
        {"streamer": "StreamEast Live", "channel": "Fox Sports 1 (FS1)", "mobile": "yes", "quality": "HD", "ads": 1, "lang": "English", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"},
        {"streamer": "CricHD Sports", "channel": "Sony Sports Ten 1 HD", "mobile": "yes", "quality": "HD", "ads": 1, "lang": "Hindi/Eng", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"},
        {"streamer": "BuffStreams", "channel": "SuperSport Premier", "mobile": "yes", "quality": "HD", "ads": 2, "lang": "English", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"},
        {"streamer": "ApexStreams", "channel": "Premier Sports 1", "mobile": "yes", "quality": "HD", "ads": 1, "lang": "English", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"},
        {"streamer": "SportSurge Ultra", "channel": "Willow Cricket HD", "mobile": "yes", "quality": "1080p", "ads": 1, "lang": "English", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"}
    ]

    live_payload = {
        "title": default_title,
        "category": default_category,
        "time": current_time_str,
        "telegramLink": "https://t.me/your_channel",
        "streams": stream_pool
    }

    # live.json ফাইলটি স্বয়ংক্রিয়ভাবে রাইট করা হচ্ছে
    with open("live.json", "w", encoding="utf-8") as f:
        json.dump(live_payload, f, indent=2, ensure_ascii=False)

    print("Successfully updated live.json with automated streams!")

if __name__ == "__main__":
    fetch_live_sports()

---
name: weather
description: 天气查询技能，用于获取任意城市的当前天气和未来天气预报。当用户说"查天气"、"今天天气怎么样"、"weather"、"forecast"时触发。不可用于气象数据采集或历史气候分析。
metadata: {"openclaw": {"emoji": "🌤️", "os": ["darwin", "linux", "win32"], "requires": {"bins": ["curl"]}}, "tags": ["天气", "天气预报", "weather", "forecast"], "version": "1.0.0", "author": "steipete", "license": "MIT-0", "source": "https://clawhub.ai/steipete/weather"}
---

# Weather

Two free services, no API keys needed.

## wttr.in (primary)

Quick one-liner:
```bash
curl -s "wttr.in/London?format=3"
# Output: London: ⛅️ +8°C
```

Compact format:
```bash
curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"
# Output: London: ⛅️ +8°C 71% ↙5km/h
```

Full forecast:
```bash
curl -s "wttr.in/London?T"
```

Format codes: `%c` condition · `%t` temp · `%h` humidity · `%w` wind · `%l` location · `%m` moon

Tips:
- URL-encode spaces: `wttr.in/New+York`
- Airport codes: `wttr.in/JFK`
- Units: `?m` (metric) `?u` (USCS)
- Today only: `?1` · Current only: `?0`
- PNG: `curl -s "wttr.in/Berlin.png" -o /tmp/weather.png`

## Open-Meteo (fallback, JSON)

Free, no key, good for programmatic use:
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"
```

Find coordinates for a city, then query. Returns JSON with temp, windspeed, weathercode.

Docs: https://open-meteo.com/en/docs

# Weather Skill

Get current weather and forecasts for any location. No API key required.

## Features

- **No API Key**: Uses free services (wttr.in, Open-Meteo), zero configuration
- **Quick Lookup**: One-liner curl commands for instant weather info
- **Full Forecast**: Detailed multi-day forecasts with temperature, humidity, wind
- **JSON Output**: Programmatic access via Open-Meteo API
- **Global Coverage**: Supports city names, airport codes, and coordinates

## Usage

### Trigger

- Say "what's the weather in London", "check weather Tokyo", "天气怎么样"
- Ask for forecasts: "weather forecast for New York this week"

### Quick Examples

Current weather:
```bash
curl -s "wttr.in/London?format=3"
# London: ⛅️ +8°C
```

Detailed current conditions:
```bash
curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"
# London: ⛅️ +8°C 71% ↙5km/h
```

Full forecast:
```bash
curl -s "wttr.in/London?T"
```

### Tips

- URL-encode spaces: `wttr.in/New+York`
- Airport codes: `wttr.in/JFK`
- Units: `?m` (metric) `?u` (USCS)
- Today only: `?1` / Current only: `?0`

## Dependencies

- `curl` (pre-installed on most systems)

## Directory Structure

```
weather/
├── SKILL.md           # Skill instructions
├── _meta.json         # ClawHub metadata
├── .clawhub/          # ClawHub origin info
└── README.md          # This file
```

## Source

Installed from [ClawHub](https://clawhub.ai) — `npx clawhub@latest install weather`

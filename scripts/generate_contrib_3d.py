#!/usr/bin/env python3
"""
Generate 3D Isometric Contribution Topography Map SVG for GitHub Profile.
Fetches real contribution data via GitHub GraphQL API and renders
an isometric voxel topography map with Crency agency brutalist aesthetics.
"""

import os
import json
import urllib.request
import subprocess

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER") or "ayonm95"

query = """query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
            weekday
          }
        }
      }
    }
  }
}"""

if GITHUB_TOKEN:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": USERNAME}}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "User-Agent": "GitHub-Profile-3D-Contrib-Generator",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req) as response:
        payload = json.loads(response.read().decode("utf-8"))
else:
    cmd = f"gh api graphql -f query='{query}' -F login='{USERNAME}'"
    res = subprocess.check_output(cmd, shell=True)
    payload = json.loads(res)

cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
total_contribs = cal["totalContributions"]
weeks = cal["weeks"]

def get_block_styles(cnt):
    if cnt == 0:
        h = 3.0
        top = "#1b0c36"
        left = "#130728"
        right = "#170a2f"
        stroke = "#28124d"
        glow = False
    elif cnt <= 2:
        h = 13.0
        top = "#38bdf8"
        left = "#0284c7"
        right = "#0369a1"
        stroke = "#7dd3fc"
        glow = False
    elif cnt <= 5:
        h = 26.0
        top = "#22d3ee"
        left = "#06b6d4"
        right = "#0891b2"
        stroke = "#67e8f9"
        glow = True
    elif cnt <= 9:
        h = 42.0
        top = "#c2ec40"
        left = "#84cc16"
        right = "#65a30d"
        stroke = "#d9f99d"
        glow = True
    elif cnt <= 15:
        h = 58.0
        top = "#fbd402"
        left = "#eab308"
        right = "#ca8a04"
        stroke = "#fef08a"
        glow = True
    else:  # 16+
        h = 78.0
        top = "#f04c8a"
        left = "#db2777"
        right = "#be185d"
        stroke = "#f472b6"
        glow = True
    return h, top, left, right, stroke, glow

X0 = 78.0
Y0 = 175.0
dx_w = 12.4
dy_w = 2.5
dx_d = -7.4
dy_d = 12.8
a = 6.2
b = 3.5

month_labels = []
current_month = None
month_abbrs = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
last_wx = -99
for w_idx, w in enumerate(weeks):
    first_day = w["contributionDays"][0]["date"]
    m = int(first_day.split("-")[1])
    if m != current_month:
        current_month = m
        name = month_abbrs[m-1]
        mx = X0 + w_idx * dx_w
        if mx - last_wx >= 32:
            month_labels.append((name, mx, 114))
            last_wx = mx

elements = []
for w_idx, w in enumerate(weeks):
    for d in w["contributionDays"]:
        cnt = d["contributionCount"]
        date_str = d["date"]
        weekday = d["weekday"]
        cx = X0 + w_idx * dx_w + weekday * dx_d
        cy = Y0 + w_idx * dy_w + weekday * dy_d
        elements.append((w_idx + weekday * 1.5, w_idx, weekday, cx, cy, cnt, date_str))

elements.sort(key=lambda item: item[0])

p_top = (X0 - a - 4, Y0 - b - 4)
p_right = (X0 + 52 * dx_w + a + 6, Y0 + 52 * dy_w - b - 4)
p_bottom = (X0 + 52 * dx_w + 6 * dx_d + a + 6, Y0 + 52 * dy_w + 6 * dy_d + b + 6)
p_left = (X0 + 6 * dx_d - a - 4, Y0 + 6 * dy_d + b + 6)

pedestal_top = f"{p_top[0]:.1f},{p_top[1]:.1f} {p_right[0]:.1f},{p_right[1]:.1f} {p_bottom[0]:.1f},{p_bottom[1]:.1f} {p_left[0]:.1f},{p_left[1]:.1f}"
pedestal_left = f"{p_left[0]:.1f},{p_left[1]:.1f} {p_bottom[0]:.1f},{p_bottom[1]:.1f} {p_bottom[0]:.1f},{p_bottom[1]+7:.1f} {p_left[0]:.1f},{p_left[1]+7:.1f}"

svg_parts = []
svg_parts.append('''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="800" height="440" viewBox="0 0 800 440">
  <defs>
    <style><![CDATA[
      .bg { fill: #12072b; }
      .grid-grid { stroke: #231245; stroke-width: 0.8; opacity: 0.6; }
      .header-title { fill: #d3c5f6; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 11px; font-weight: 800; letter-spacing: 0.08em; }
      .stat-label { fill: #94a3b8; font-family: 'SF Mono', Monaco, Menlo, Consolas, monospace; font-size: 9.5px; }
      .stat-val-green { fill: #c2ec40; font-family: 'SF Mono', Monaco, Menlo, Consolas, monospace; font-size: 11px; font-weight: 700; }
      .stat-val-pink { fill: #f04c8a; font-family: 'SF Mono', Monaco, Menlo, Consolas, monospace; font-size: 11px; font-weight: 700; }
      .stat-val-cyan { fill: #22d3ee; font-family: 'SF Mono', Monaco, Menlo, Consolas, monospace; font-size: 11px; font-weight: 700; }
      .stat-val-gold { fill: #fbd402; font-family: 'SF Mono', Monaco, Menlo, Consolas, monospace; font-size: 11px; font-weight: 700; }
      
      .axis-label { fill: #a5b4fc; font-family: 'SF Mono', Monaco, monospace; font-size: 9px; font-weight: 600; opacity: 0.9; }

      .hud-pill {
        cursor: pointer;
        transition: transform 0.22s cubic-bezier(0.23, 1, 0.32, 1);
      }
      .hud-pill:hover {
        transform: translateY(-2px);
      }
      .hud-pill-bg {
        fill: #190938;
        stroke: #381b70;
        stroke-width: 1;
        transition: stroke 0.22s ease, fill 0.22s ease;
      }
      .hud-pill:hover .hud-pill-bg {
        stroke: #c2ec40;
        fill: #240d4f;
      }

      .tile {
        cursor: pointer;
        transition: transform 0.25s cubic-bezier(0.23, 1, 0.32, 1), filter 0.25s ease;
      }
      .tile:hover {
        transform: translateY(-6px);
        filter: url(#tileGlow);
      }

      @keyframes spinStar {
        from { transform: rotate(0deg); }
        to   { transform: rotate(360deg); }
      }
      .starburst-anim {
        transform-origin: 765px 22px;
        animation: spinStar 18s linear infinite;
        cursor: pointer;
      }
      .starburst-anim:hover {
        animation-duration: 3s;
      }

      @keyframes beaconPulse {
        0%, 100% { transform: scale(0.9) rotate(0deg); opacity: 0.8; }
        50%      { transform: scale(1.25) rotate(180deg); opacity: 1; }
      }
      .peak-star {
        transform-origin: center;
        animation: beaconPulse 2.8s ease-in-out infinite;
      }

      @media (prefers-reduced-motion: reduce) {
        *, polygon, g {
          animation: none !important;
          transform: none !important;
        }
      }
    ]]></style>

    <filter id="tileGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="peakBloom" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="mapBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3d71ff" stop-opacity="0.85"/>
      <stop offset="40%" stop-color="#c2ec40" stop-opacity="0.9"/>
      <stop offset="80%" stop-color="#f04c8a" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#fbd402" stop-opacity="0.8"/>
    </linearGradient>

    <radialGradient id="terrainGlow" cx="55%" cy="60%" r="50%">
      <stop offset="0%" stop-color="#a78bfa" stop-opacity="0.25"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#12072b" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="800" height="440" rx="14" class="bg"/>
  <ellipse cx="430" cy="270" rx="360" ry="140" fill="url(#terrainGlow)"/>

  <g class="grid-grid">
    <line x1="30" y1="42" x2="770" y2="42"/>
    <line x1="30" y1="388" x2="770" y2="388"/>
    <line x1="190" y1="42" x2="190" y2="388" stroke-dasharray="3 3"/>
    <line x1="400" y1="42" x2="400" y2="388" stroke-dasharray="3 3"/>
    <line x1="600" y1="42" x2="600" y2="388" stroke-dasharray="3 3"/>
  </g>

  <rect width="800" height="42" rx="14" fill="#180a38" stroke="#2d1859" stroke-width="1"/>
  <rect y="22" width="800" height="20" fill="#180a38"/>
  <line x1="0" y1="42" x2="800" y2="42" stroke="#351a66" stroke-width="1"/>

  <circle cx="22" cy="21" r="5.5" fill="#ea3323"/>
  <circle cx="40" cy="21" r="5.5" fill="#fbd402"/>
  <circle cx="58" cy="21" r="5.5" fill="#c2ec40"/>

  <text x="82" y="22" class="header-title" dominant-baseline="middle">
    AYON MOITRA <tspan fill="#f04c8a">//</tspan> 3D ACTIVITY TOPOGRAPHY [ISOMETRIC PROOF-OF-WORK]
  </text>

  <g class="starburst-anim">
    <path d="M 765,13 L 767,20 L 774,22 L 767,24 L 765,31 L 763,24 L 756,22 L 763,20 Z" fill="#fbd402" filter="url(#tileGlow)"/>
    <circle cx="765" cy="22" r="2.5" fill="#ffffff"/>
  </g>

  <!-- HUD Metrics -->
  <g class="hud-pill" transform="translate(26, 54)">
    <rect width="170" height="30" rx="6" class="hud-pill-bg"/>
    <circle cx="14" cy="15" r="3.5" fill="#c2ec40"/>
    <text x="26" y="19" class="stat-label">TOTAL COMMITS: <tspan class="stat-val-green">''' + str(total_contribs) + '''</tspan></text>
  </g>

  <g class="hud-pill" transform="translate(208, 54)">
    <rect width="182" height="30" rx="6" class="hud-pill-bg"/>
    <circle cx="14" cy="15" r="3.5" fill="#f04c8a"/>
    <text x="26" y="19" class="stat-label">1-DAY VELOCITY: <tspan class="stat-val-pink">21 SPIKE</tspan></text>
  </g>

  <g class="hud-pill" transform="translate(402, 54)">
    <rect width="186" height="30" rx="6" class="hud-pill-bg"/>
    <circle cx="14" cy="15" r="3.5" fill="#22d3ee"/>
    <text x="26" y="19" class="stat-label">PROJECTION: <tspan class="stat-val-cyan">ISOMETRIC 3D</tspan></text>
  </g>

  <g class="hud-pill" transform="translate(600, 54)">
    <rect width="174" height="30" rx="6" class="hud-pill-bg"/>
    <circle cx="14" cy="15" r="3.5" fill="#fbd402"/>
    <text x="26" y="19" class="stat-label">STATUS: <tspan class="stat-val-gold">VERIFIED ACTIVE</tspan></text>
  </g>

  <g>
''')

for name, mx, my in month_labels:
    svg_parts.append(f'    <text x="{mx:.1f}" y="{my:.1f}" class="axis-label" text-anchor="middle">{name}</text>\n')

days_short = ["Sun", "Tue", "Thu", "Sat"]
for idx, d_idx in enumerate([0, 2, 4, 6]):
    lx = X0 + d_idx * dx_d - 36
    ly = Y0 + d_idx * dy_d + 4
    svg_parts.append(f'    <text x="{lx:.1f}" y="{ly:.1f}" class="axis-label">{days_short[idx]}</text>\n')

svg_parts.append('''  </g>

  <polygon points="''' + pedestal_top + '''" fill="#150830" stroke="#28114f" stroke-width="1"/>
  <polygon points="''' + pedestal_left + '''" fill="#0c041d" stroke="#220d44" stroke-width="0.8"/>

  <g id="isometric-monoliths">
''')

peak_stars = []

for _, w_idx, weekday, cx, cy, cnt, date_str in elements:
    h, top_col, left_col, right_col, stroke_col, glow = get_block_styles(cnt)
    top_pts = f"{cx:.1f},{cy - b - h:.1f} {cx + a:.1f},{cy - h:.1f} {cx:.1f},{cy + b - h:.1f} {cx - a:.1f},{cy - h:.1f}"
    
    if cnt == 0:
        svg_parts.append(f'    <polygon points="{top_pts}" fill="{top_col}" stroke="{stroke_col}" stroke-width="0.5"/>\n')
    else:
        left_pts = f"{cx - a:.1f},{cy - h:.1f} {cx:.1f},{cy + b - h:.1f} {cx:.1f},{cy + b:.1f} {cx - a:.1f},{cy:.1f}"
        right_pts = f"{cx:.1f},{cy + b - h:.1f} {cx + a:.1f},{cy - h:.1f} {cx + a:.1f},{cy:.1f} {cx:.1f},{cy + b:.1f}"
        
        glow_filter = ' filter="url(#tileGlow)"' if glow else ''
        svg_parts.append(f'''    <g class="tile"{glow_filter}>
      <title>{cnt} contributions on {date_str}</title>
      <polygon points="{left_pts}" fill="{left_col}" stroke="{stroke_col}" stroke-width="0.6"/>
      <polygon points="{right_pts}" fill="{right_col}" stroke="{stroke_col}" stroke-width="0.6"/>
      <polygon points="{top_pts}" fill="{top_col}" stroke="{stroke_col}" stroke-width="0.7"/>
    </g>\n''')

        if cnt >= 16:
            peak_stars.append((cx, cy - h - 10, cnt, date_str))

for sx, sy, scnt, sdate in peak_stars:
    svg_parts.append(f'''    <g transform="translate({sx:.1f}, {sy:.1f})" filter="url(#peakBloom)">
      <line x1="0" y1="4" x2="0" y2="10" stroke="#f472b6" stroke-width="1" stroke-dasharray="2 1"/>
      <path d="M 0,-4 L 1.2,-1.2 L 4,0 L 1.2,1.2 L 0,4 L -1.2,1.2 L -4,0 L -1.2,-1.2 Z" fill="#ffffff" class="peak-star"/>
      <circle cx="0" cy="0" r="1.2" fill="#fbd402"/>
    </g>\n''')

svg_parts.append('''  </g>

  <line x1="0" y1="392" x2="800" y2="392" stroke="#2d1354" stroke-width="1.2"/>
  <rect y="393" width="800" height="47" rx="14" fill="#14082e"/>
  <rect y="393" width="800" height="20" fill="#14082e"/>

  <text x="26" y="420" class="stat-label">
    TIMEFRAME: <tspan fill="#d3c5f6">OCTOBER 2025 &#x2014; OCTOBER 2026</tspan>  &#x00B7;  52 WEEKS PROOF-OF-WORK
  </text>

  <g transform="translate(470, 411)">
    <text x="0" y="9" class="stat-label">MAP SCALE:</text>
    <rect x="70" y="0" width="11" height="11" rx="2" fill="#1b0c36" stroke="#28124d" stroke-width="0.8"/>
    <rect x="88" y="0" width="11" height="11" rx="2" fill="#38bdf8" stroke="#7dd3fc" stroke-width="0.8"/>
    <rect x="106" y="0" width="11" height="11" rx="2" fill="#22d3ee" stroke="#67e8f9" stroke-width="0.8"/>
    <rect x="124" y="0" width="11" height="11" rx="2" fill="#c2ec40" stroke="#d9f99d" stroke-width="0.8"/>
    <rect x="142" y="0" width="11" height="11" rx="2" fill="#fbd402" stroke="#fef08a" stroke-width="0.8"/>
    <rect x="160" y="0" width="11" height="11" rx="2" fill="#f04c8a" stroke="#f472b6" stroke-width="0.8"/>
    <text x="180" y="9" class="stat-label">PEAK SPIKE</text>
  </g>

  <rect width="800" height="440" rx="14" stroke="url(#mapBorder)" stroke-width="1.5" fill="none"/>
</svg>''')

output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "contrib-3d.svg")
with open(output_path, "w") as f:
    f.write("".join(svg_parts))

print(f"Generated {output_path} successfully!")

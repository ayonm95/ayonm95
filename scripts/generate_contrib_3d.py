#!/usr/bin/env python3
"""
Generate a 3D isometric GitHub contribution map for the past 5 months (22 weeks).
Pure Python standard library (no external dependencies required).
"""

import os
import sys
import json
import urllib.request
import subprocess
from datetime import datetime

def fetch_contributions(username="ayonm95"):
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                contributionLevel
                date
                weekday
              }
            }
          }
        }
      }
    }
    """
    token = os.environ.get("GITHUB_TOKEN")
    
    if token:
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query, "variables": {"login": username}}).encode("utf-8"),
            headers={
                "Authorization": f"bearer {token}",
                "User-Agent": "profile-3d-contrib-5m",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    else:
        # Fallback to local gh CLI
        cmd = f"gh api graphql -f query='{query}' -f login='{username}'"
        res = subprocess.check_output(cmd, shell=True)
        data = json.loads(res)
        
    return data['data']['user']['contributionsCollection']['contributionCalendar']

def generate_svg(cal):
    all_weeks = cal['weeks']
    # Keep last 22 weeks (~5 months: 154 days)
    weeks = all_weeks[-22:]
    total_commits_5m = sum(d['contributionCount'] for w in weeks for d in w['contributionDays'])

    # Canvas Dimensions
    WIDTH = 800
    HEIGHT = 380

    # 3D Grid Parameters (Centered)
    X0 = 225.0
    Y0 = 105.0
    dx_w = 20.0   # along week axis (0..21)
    dy_w = 7.0
    dx_d = -15.0  # along day axis (0..6, Sun..Sat)
    dy_d = 11.5

    def proj(w, d, h=0):
        x = X0 + w * dx_w + d * dx_d
        y = Y0 + w * dy_w + d * dy_d - h
        return (x, y)

    def get_level_info(count):
        if count == 0:
            return {
                'level': 0, 'h': 2,
                'top': '#161b22', 'left': '#0d1117', 'right': '#10141a',
                'stroke': '#21262d', 'glow': False
            }
        elif count <= 3:
            return {
                'level': 1, 'h': 14,
                'top': '#0e4429', 'left': '#082a1a', 'right': '#0b3520',
                'stroke': '#196c3e', 'glow': False
            }
        elif count <= 8:
            return {
                'level': 2, 'h': 28,
                'top': '#006d32', 'left': '#004721', 'right': '#005728',
                'stroke': '#26a641', 'glow': False
            }
        elif count <= 15:
            return {
                'level': 3, 'h': 46,
                'top': '#26a641', 'left': '#197a2e', 'right': '#1e8e37',
                'stroke': '#39d353', 'glow': True
            }
        else:
            return {
                'level': 4, 'h': 65,
                'top': '#39d353', 'left': '#2ea043', 'right': '#34b34b',
                'stroke': '#56ff74', 'glow': True
            }

    # Month milestones across the 22 weeks
    clean_months = [
        ("Jun", 2.0),
        ("Jul", 6.5),
        ("Aug", 11.0),
        ("Sep", 15.5),
        ("Oct", 19.5),
    ]

    month_svg_parts = []
    for m_name, w_pos in clean_months:
        mx = X0 + w_pos * dx_w - 7.5 * dx_d * 0.3
        month_svg_parts.append(
            f'<text x="{mx:.1f}" y="74" fill="#8b949e" font-size="11" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Helvetica,Arial,sans-serif" font-weight="600" text-anchor="middle">{m_name}</text>'
        )

    # Weekday labels
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    day_svg_parts = []
    for d_idx, d_name in day_labels:
        lx, ly = proj(0, d_idx, h=0)
        day_svg_parts.append(
            f'<text x="{lx-18:.1f}" y="{ly+6:.1f}" fill="#7d8590" font-size="10" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Helvetica,Arial,sans-serif" font-weight="500" text-anchor="end">{d_name}</text>'
        )

    # Base Pedestal Slab
    num_weeks = len(weeks)
    p00 = proj(0, 0, 0)
    pW0 = proj(num_weeks, 0, 0)
    pWD = proj(num_weeks, 7, 0)
    p0D = proj(0, 7, 0)
    thick = 8

    pedestal_svg = f'''
  <!-- Pedestal Ground Shadow -->
  <polygon points="{p0D[0]:.1f},{p0D[1]+thick+6:.1f} {pWD[0]:.1f},{pWD[1]+thick+6:.1f} {pWD[0]+12:.1f},{pWD[1]+thick+2:.1f} {p0D[0]-12:.1f},{p0D[1]+thick+2:.1f}" fill="#000000" opacity="0.35" filter="url(#shadowBlur)" />

  <!-- Pedestal Base -->
  <polygon points="{p00[0]:.1f},{p00[1]:.1f} {pW0[0]:.1f},{pW0[1]:.1f} {pWD[0]:.1f},{pWD[1]:.1f} {p0D[0]:.1f},{p0D[1]:.1f}" fill="#11161d" stroke="#21262d" stroke-width="1" />
  <!-- Pedestal Front-Left Face -->
  <polygon points="{p0D[0]:.1f},{p0D[1]:.1f} {pWD[0]:.1f},{pWD[1]:.1f} {pWD[0]:.1f},{pWD[1]+thick:.1f} {p0D[0]:.1f},{p0D[1]+thick:.1f}" fill="#0d1117" stroke="#1b1f24" stroke-width="1" />
  <!-- Pedestal Front-Right Face -->
  <polygon points="{pW0[0]:.1f},{pW0[1]:.1f} {pWD[0]:.1f},{pWD[1]:.1f} {pWD[0]:.1f},{pWD[1]+thick:.1f} {pW0[0]:.1f},{pW0[1]+thick:.1f}" fill="#080c10" stroke="#161b22" stroke-width="1" />
'''

    # Depth sort blocks: painter's algorithm
    items = []
    peak_item = None
    max_count = 0

    for w in range(num_weeks):
        for d in range(len(weeks[w]['contributionDays'])):
            c_count = weeks[w]['contributionDays'][d].get('contributionCount', 0)
            c_date = weeks[w]['contributionDays'][d].get('date', '')
            info = get_level_info(c_count)
            item = {
                'w': w, 'd': d,
                'count': c_count,
                'date': c_date,
                'info': info,
                'depth': w * 2.0 + d * 1.0
            }
            items.append(item)
            if c_count > max_count:
                max_count = c_count
                peak_item = item

    items.sort(key=lambda x: x['depth'])

    blocks_svg = []
    for it in items:
        w = it['w']
        d = it['d']
        info = it['info']
        h = info['h']
        
        gap = 0.14
        p_a = (X0 + (w + gap) * dx_w + (d + gap) * dx_d,
               Y0 + (w + gap) * dy_w + (d + gap) * dy_d)
        p_b = (X0 + (w + 1 - gap) * dx_w + (d + gap) * dx_d,
               Y0 + (w + 1 - gap) * dy_w + (d + gap) * dy_d)
        p_c = (X0 + (w + 1 - gap) * dx_w + (d + 1 - gap) * dx_d,
               Y0 + (w + 1 - gap) * dy_w + (d + 1 - gap) * dy_d)
        p_d = (X0 + (w + gap) * dx_w + (d + 1 - gap) * dx_d,
               Y0 + (w + gap) * dy_w + (d + 1 - gap) * dy_d)
        
        if info['level'] == 0:
            pts = f"{p_a[0]:.1f},{p_a[1]:.1f} {p_b[0]:.1f},{p_b[1]:.1f} {p_c[0]:.1f},{p_c[1]:.1f} {p_d[0]:.1f},{p_d[1]:.1f}"
            blocks_svg.append(f'<polygon points="{pts}" fill="#161b22" stroke="#21262d" stroke-width="0.5" opacity="0.9" />')
        else:
            t_a = (p_a[0], p_a[1] - h)
            t_b = (p_b[0], p_b[1] - h)
            t_c = (p_c[0], p_c[1] - h)
            t_d = (p_d[0], p_d[1] - h)
            
            pts_front = f"{p_d[0]:.1f},{p_d[1]:.1f} {p_c[0]:.1f},{p_c[1]:.1f} {t_c[0]:.1f},{t_c[1]:.1f} {t_d[0]:.1f},{t_d[1]:.1f}"
            pts_right = f"{p_c[0]:.1f},{p_c[1]:.1f} {p_b[0]:.1f},{p_b[1]:.1f} {t_b[0]:.1f},{t_b[1]:.1f} {t_c[0]:.1f},{t_c[1]:.1f}"
            pts_top = f"{t_a[0]:.1f},{t_a[1]:.1f} {t_b[0]:.1f},{t_b[1]:.1f} {t_c[0]:.1f},{t_c[1]:.1f} {t_d[0]:.1f},{t_d[1]:.1f}"
            
            glow_filter = 'filter="url(#greenGlow)" ' if info['glow'] else ''
            block_str = f'''<g {glow_filter}>
  <polygon points="{pts_right}" fill="{info['right']}" stroke="{info['stroke']}" stroke-width="0.6" />
  <polygon points="{pts_front}" fill="{info['left']}" stroke="{info['stroke']}" stroke-width="0.6" />
  <polygon points="{pts_top}" fill="{info['top']}" stroke="{info['stroke']}" stroke-width="0.8" />
</g>'''
            blocks_svg.append(block_str)

    blocks_markup = "\n".join(blocks_svg)
    month_markup = "\n".join(month_svg_parts)
    day_markup = "\n".join(day_svg_parts)

    peak_callout = ""
    if peak_item:
        pw = peak_item['w']
        pd = peak_item['d']
        ph = peak_item['info']['h']
        pt_x, pt_y = proj(pw + 0.5, pd + 0.5, h=ph)
        peak_callout = f'''
  <!-- Peak Callout Pin -->
  <g transform="translate({pt_x:.1f}, {pt_y:.1f})">
    <line x1="0" y1="0" x2="0" y2="-20" stroke="#39d353" stroke-width="1.2" stroke-dasharray="2,2" />
    <circle cx="0" cy="0" r="3" fill="#39d353" />
    <rect x="-44" y="-36" width="88" height="18" rx="4" fill="#161b22" stroke="#39d353" stroke-width="1" />
    <text x="0" y="-24" fill="#39d353" font-size="9" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',monospace" font-weight="700" text-anchor="middle">Peak: {peak_item['count']} commits</text>
  </g>'''

    start_date_str = weeks[0]['contributionDays'][0]['date']
    end_date_str = weeks[-1]['contributionDays'][-1]['date']

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#070a0e" />
    </linearGradient>
    <filter id="greenGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="shadowBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" />
    </filter>
  </defs>

  <!-- Background Canvas -->
  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="12" fill="url(#bgGrad)" stroke="#30363d" stroke-width="1" />

  <!-- Top Navigation Header -->
  <g transform="translate(20, 16)">
    <circle cx="6" cy="6" r="4" fill="#ff5f56" />
    <circle cx="20" cy="6" r="4" fill="#ffbd2e" />
    <circle cx="34" cy="6" r="4" fill="#27c93f" />
    <text x="50" y="9.5" fill="#f0f6fc" font-size="12" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-weight="600">ayonm95 <tspan fill="#7d8590">/ 3D Contribution Map</tspan></text>
    
    <!-- Timeframe Pill -->
    <rect x="{WIDTH-230}" y="-3" width="190" height="20" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1" />
    <circle cx="{WIDTH-218}" cy="7" r="3" fill="#39d353" />
    <text x="{WIDTH-208}" y="10.5" fill="#c9d1d9" font-size="10" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',monospace" font-weight="600">Past 5 Months ({total_commits_5m} Commits)</text>
  </g>

  <!-- Divider Line -->
  <line x1="0" y1="42" x2="{WIDTH}" y2="42" stroke="#21262d" stroke-width="1" />

  <!-- Month Labels -->
  <g>
    {month_markup}
  </g>

  <!-- Weekday Labels -->
  <g>
    {day_markup}
  </g>

  <!-- 3D Pedestal and Cubes -->
  {pedestal_svg}
  {blocks_markup}
  {peak_callout}

  <!-- Bottom Proof-of-Work Footer & Intensity Legend -->
  <line x1="0" y1="{HEIGHT-44}" x2="{WIDTH}" y2="{HEIGHT-44}" stroke="#21262d" stroke-width="1" />
  
  <g transform="translate(20, {HEIGHT-24})">
    <text x="0" y="0" fill="#8b949e" font-size="11" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-weight="500">
      <tspan fill="#39d353" font-weight="700">{total_commits_5m} contributions</tspan> from {start_date_str} to {end_date_str}
    </text>
  </g>
  
  <g transform="translate({WIDTH-180}, {HEIGHT-24})">
    <text x="-8" y="0" fill="#7d8590" font-size="10" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',monospace" text-anchor="end">Less</text>
    <rect x="0" y="-8" width="10" height="10" rx="2" fill="#161b22" stroke="#30363d" stroke-width="0.5" />
    <rect x="14" y="-8" width="10" height="10" rx="2" fill="#0e4429" />
    <rect x="28" y="-8" width="10" height="10" rx="2" fill="#006d32" />
    <rect x="42" y="-8" width="10" height="10" rx="2" fill="#26a641" />
    <rect x="56" y="-8" width="10" height="10" rx="2" fill="#39d353" />
    <text x="74" y="0" fill="#7d8590" font-size="10" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',monospace">More</text>
  </g>
</svg>'''

def main():
    username = os.environ.get("GITHUB_REPOSITORY_OWNER") or os.environ.get("USERNAME") or "ayonm95"
    print(f"Fetching GitHub contributions for {username}...")
    cal = fetch_contributions(username)
    svg = generate_svg(cal)

    # Save to contrib-3d.svg and profile-3d-contrib/profile-night-green.svg
    os.makedirs("profile-3d-contrib", exist_ok=True)
    with open("contrib-3d.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    with open("profile-3d-contrib/profile-night-green.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    with open("profile-3d-contrib/profile-green.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Saved contrib-3d.svg and profile-3d-contrib/ SVGs successfully!")

if __name__ == "__main__":
    main()

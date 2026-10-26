#!/usr/bin/env python3
"""
Generate a realistic 3D architectural micro-cityscape GitHub contribution map for the past 5 months (22 weeks).
Pure Python standard library (no external dependencies required).
"""

import os
import sys
import json
import urllib.request
import subprocess

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
                "User-Agent": "profile-3d-contrib-architectural",
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
    HEIGHT = 390

    # 3D Grid Parameters (Isometric Projection)
    X0 = 225.0
    Y0 = 112.0
    dx_w = 20.0   # along week axis (0..21)
    dy_w = 7.0
    dx_d = -15.0  # along day axis (0..6, Sun..Sat)
    dy_d = 11.5

    def proj(w, d, h=0):
        x = X0 + w * dx_w + d * dx_d
        y = Y0 + w * dy_w + d * dy_d - h
        return (x, y)

    def get_building_info(count):
        if count == 0:
            return {
                'level': 0, 'h': 0, 'stories': 0,
                'fill': '#161c24', 'stroke': 'rgba(240, 246, 252, 0.16)',
                'glow': False, 'spire': False
            }
        elif count <= 3:
            # Low-rise / Townhouse
            return {
                'level': 1, 'h': 18, 'stories': 2,
                'top': '#2b5c40', 'front': '#1f4831', 'right': '#173926',
                'stroke': '#388e5a', 'glow': False, 'spire': False
            }
        elif count <= 8:
            # Mid-rise / Commercial Block
            return {
                'level': 2, 'h': 34, 'stories': 4,
                'top': '#1e7b44', 'front': '#155f34', 'right': '#104d2a',
                'stroke': '#34b34b', 'glow': False, 'spire': False
            }
        elif count <= 15:
            # High-rise / Modern Glass Tower
            return {
                'level': 3, 'h': 54, 'stories': 6,
                'top': '#26a641', 'front': '#1a7e32', 'right': '#146427',
                'stroke': '#56ff74', 'glow': True, 'spire': False
            }
        else:
            # Supertall Skyscraper / Architectural Monolith
            return {
                'level': 4, 'h': 76, 'stories': 8,
                'top': '#39d353', 'front': '#249e3d', 'right': '#1d8332',
                'stroke': '#7ee787', 'glow': True, 'spire': True
            }

    # Month milestones across the 22 weeks (Jun, Jul, Aug, Sep, Oct)
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
            f'<text x="{mx:.1f}" y="76" fill="#8b949e" font-size="11" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Helvetica,Arial,sans-serif" font-weight="600" text-anchor="middle">{m_name}</text>'
        )

    # Weekday labels
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    day_svg_parts = []
    for d_idx, d_name in day_labels:
        lx, ly = proj(0, d_idx, h=0)
        day_svg_parts.append(
            f'<text x="{lx-18:.1f}" y="{ly+6:.1f}" fill="#7d8590" font-size="10" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Helvetica,Arial,sans-serif" font-weight="500" text-anchor="end">{d_name}</text>'
        )

    # Base Pedestal Slab with Light Silver/Platinum Accent Rim
    num_weeks = len(weeks)
    p00 = proj(0, 0, 0)
    pW0 = proj(num_weeks, 0, 0)
    pWD = proj(num_weeks, 7, 0)
    p0D = proj(0, 7, 0)
    thick = 10

    pedestal_svg = f'''
  <!-- Pedestal Soft Ground Ambient Shadow -->
  <polygon points="{p0D[0]:.1f},{p0D[1]+thick+8:.1f} {pWD[0]:.1f},{pWD[1]+thick+8:.1f} {pWD[0]+16:.1f},{pWD[1]+thick+2:.1f} {p0D[0]-16:.1f},{p0D[1]+thick+2:.1f}" fill="#000000" opacity="0.45" filter="url(#shadowBlur)" />

  <!-- Pedestal Base Top Surface (Light-tinted architectural granite/slate) -->
  <polygon points="{p00[0]:.1f},{p00[1]:.1f} {pW0[0]:.1f},{pW0[1]:.1f} {pWD[0]:.1f},{pWD[1]:.1f} {p0D[0]:.1f},{p0D[1]:.1f}" fill="#151b24" stroke="rgba(240, 246, 252, 0.3)" stroke-width="1.2" />

  <!-- Illuminated Light-Colored Bevel Rim (Subtle Silver/Platinum Accent) -->
  <polyline points="{p00[0]:.1f},{p00[1]:.1f} {p0D[0]:.1f},{p0D[1]:.1f} {pWD[0]:.1f},{pWD[1]:.1f}" fill="none" stroke="rgba(240, 246, 252, 0.55)" stroke-width="1.2" />

  <!-- Pedestal Front-Left Face (Architectural plinth wall with horizontal accent band) -->
  <polygon points="{p0D[0]:.1f},{p0D[1]:.1f} {pWD[0]:.1f},{pWD[1]:.1f} {pWD[0]:.1f},{pWD[1]+thick:.1f} {p0D[0]:.1f},{p0D[1]+thick:.1f}" fill="#0d1117" stroke="rgba(240, 246, 252, 0.2)" stroke-width="0.8" />
  <line x1="{p0D[0]:.1f}" y1="{p0D[1]+5:.1f}" x2="{pWD[0]:.1f}" y2="{pWD[1]+5:.1f}" stroke="rgba(240, 246, 252, 0.15)" stroke-width="0.6" />

  <!-- Pedestal Front-Right Face -->
  <polygon points="{pW0[0]:.1f},{pW0[1]:.1f} {pWD[0]:.1f},{pWD[1]:.1f} {pWD[0]:.1f},{pWD[1]+thick:.1f} {pW0[0]:.1f},{pW0[1]+thick:.1f}" fill="#090d13" stroke="rgba(240, 246, 252, 0.15)" stroke-width="0.8" />
'''

    # Depth sort blocks: painter's algorithm
    items = []
    peak_item = None
    max_count = 0

    for w in range(num_weeks):
        for d in range(len(weeks[w]['contributionDays'])):
            c_count = weeks[w]['contributionDays'][d].get('contributionCount', 0)
            c_date = weeks[w]['contributionDays'][d].get('date', '')
            info = get_building_info(c_count)
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
        stories = info['stories']
        
        gap = 0.11
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
            blocks_svg.append(f'<polygon points="{pts}" fill="{info["fill"]}" stroke="{info["stroke"]}" stroke-width="0.65" />')
        else:
            t_a = (p_a[0], p_a[1] - h)
            t_b = (p_b[0], p_b[1] - h)
            t_c = (p_c[0], p_c[1] - h)
            t_d = (p_d[0], p_d[1] - h)
            
            pts_front = f"{p_d[0]:.1f},{p_d[1]:.1f} {p_c[0]:.1f},{p_c[1]:.1f} {t_c[0]:.1f},{t_c[1]:.1f} {t_d[0]:.1f},{t_d[1]:.1f}"
            pts_right = f"{p_c[0]:.1f},{p_c[1]:.1f} {p_b[0]:.1f},{p_b[1]:.1f} {t_b[0]:.1f},{t_b[1]:.1f} {t_c[0]:.1f},{t_c[1]:.1f}"
            pts_top = f"{t_a[0]:.1f},{t_a[1]:.1f} {t_b[0]:.1f},{t_b[1]:.1f} {t_c[0]:.1f},{t_c[1]:.1f} {t_d[0]:.1f},{t_d[1]:.1f}"
            
            # Floor bands (story division lines)
            floor_lines = []
            for s in range(1, stories):
                frac = s / stories
                fy_base = p_d[1] * (1 - frac) + t_d[1] * frac
                # Front wall floor band
                f1_x = p_d[0]
                f1_y = p_d[1] - h * frac
                f2_x = p_c[0]
                f2_y = p_c[1] - h * frac
                floor_lines.append(f'<line x1="{f1_x:.1f}" y1="{f1_y:.1f}" x2="{f2_x:.1f}" y2="{f2_y:.1f}" stroke="rgba(255,255,255,0.22)" stroke-width="0.5" />')
                # Right wall floor band
                f3_x = p_b[0]
                f3_y = p_b[1] - h * frac
                floor_lines.append(f'<line x1="{f2_x:.1f}" y1="{f2_y:.1f}" x2="{f3_x:.1f}" y2="{f3_y:.1f}" stroke="rgba(255,255,255,0.12)" stroke-width="0.5" />')

            # Vertical window mullions for taller towers (stories >= 4)
            mullions = []
            if stories >= 4:
                for frac_u in [0.33, 0.67]:
                    m_b_x = p_d[0] + frac_u * (p_c[0] - p_d[0])
                    m_b_y = p_d[1] + frac_u * (p_c[1] - p_d[1])
                    mullions.append(f'<line x1="{m_b_x:.1f}" y1="{m_b_y:.1f}" x2="{m_b_x:.1f}" y2="{m_b_y - h:.1f}" stroke="rgba(255,255,255,0.12)" stroke-width="0.4" stroke-dasharray="1,2" />')

            # Inset roof crown / mechanical terrace
            inset_a = (t_a[0] * 0.8 + t_c[0] * 0.2, t_a[1] * 0.8 + t_c[1] * 0.2)
            inset_b = (t_b[0] * 0.8 + t_d[0] * 0.2, t_b[1] * 0.8 + t_d[1] * 0.2)
            inset_c = (t_c[0] * 0.8 + t_a[0] * 0.2, t_c[1] * 0.8 + t_a[1] * 0.2)
            inset_d = (t_d[0] * 0.8 + t_b[0] * 0.2, t_d[1] * 0.8 + t_b[1] * 0.2)
            pts_inset = f"{inset_a[0]:.1f},{inset_a[1]:.1f} {inset_b[0]:.1f},{inset_b[1]:.1f} {inset_c[0]:.1f},{inset_c[1]:.1f} {inset_d[0]:.1f},{inset_d[1]:.1f}"

            # Rooftop Spire & Beacon for Supertall Monolith
            spire_markup = ""
            if info['spire']:
                cx = (t_a[0] + t_b[0] + t_c[0] + t_d[0]) / 4.0
                cy = (t_a[1] + t_b[1] + t_c[1] + t_d[1]) / 4.0
                spire_markup = f'''
  <!-- Architectural Spire Antenna & Beacon Light -->
  <line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx:.1f}" y2="{cy-12:.1f}" stroke="#ffffff" stroke-width="1" />
  <circle cx="{cx:.1f}" cy="{cy-12:.1f}" r="2.2" fill="#ffffff" filter="url(#beaconGlow)" />
'''

            floors_str = "\n  ".join(floor_lines)
            mullions_str = ("\n  " + "\n  ".join(mullions)) if mullions else ""
            glow_filter = 'filter="url(#greenGlow)" ' if info['glow'] else ''

            block_str = f'''<g {glow_filter}>
  <!-- Right Shadow Wall -->
  <polygon points="{pts_right}" fill="{info['right']}" stroke="{info['stroke']}" stroke-width="0.6" />
  <!-- Front Sunlit Wall -->
  <polygon points="{pts_front}" fill="{info['front']}" stroke="{info['stroke']}" stroke-width="0.6" />
  <!-- Architectural Facade Grid (Stories & Windows) -->
  {floors_str}{mullions_str}
  <!-- Rooftop Parapet Surface -->
  <polygon points="{pts_top}" fill="{info['top']}" stroke="{info['stroke']}" stroke-width="0.8" />
  <!-- Inset Roof Terrace / Crown -->
  <polygon points="{pts_inset}" fill="{info['front']}" stroke="rgba(255,255,255,0.3)" stroke-width="0.5" opacity="0.9" />
  {spire_markup}
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
        pt_x, pt_y = proj(pw + 0.5, pd + 0.5, h=ph + 14)
        peak_callout = f'''
  <!-- Peak Skyscraper Callout -->
  <g transform="translate({pt_x:.1f}, {pt_y:.1f})">
    <line x1="0" y1="0" x2="0" y2="-16" stroke="#56ff74" stroke-width="1.2" stroke-dasharray="2,2" />
    <circle cx="0" cy="0" r="3" fill="#ffffff" stroke="#39d353" stroke-width="1.2" />
    <rect x="-46" y="-32" width="92" height="18" rx="4" fill="#141c24" stroke="#56ff74" stroke-width="1" />
    <text x="0" y="-20" fill="#7ee787" font-size="9" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',monospace" font-weight="700" text-anchor="middle">Peak: {peak_item['count']} commits</text>
  </g>'''

    start_date_str = weeks[0]['contributionDays'][0]['date']
    end_date_str = weeks[-1]['contributionDays'][-1]['date']

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f15" />
      <stop offset="100%" stop-color="#070a0e" />
    </linearGradient>
    <filter id="greenGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3.5" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="beaconGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.5" result="blur" />
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
    <text x="50" y="9.5" fill="#f0f6fc" font-size="12" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-weight="600">ayonm95 <tspan fill="#8b949e">/ 3D Architectural Topography</tspan></text>
    
    <!-- Timeframe Pill -->
    <rect x="{WIDTH-230}" y="-3" width="190" height="20" rx="10" fill="#161b22" stroke="rgba(240, 246, 252, 0.25)" stroke-width="1" />
    <circle cx="{WIDTH-218}" cy="7" r="3" fill="#39d353" />
    <text x="{WIDTH-208}" y="10.5" fill="#e6edf3" font-size="10" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',monospace" font-weight="600">Past 5 Months ({total_commits_5m} Commits)</text>
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

  <!-- 3D Pedestal and Buildings -->
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
    <text x="-8" y="0" fill="#8b949e" font-size="10" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',monospace" text-anchor="end">Less</text>
    <rect x="0" y="-8" width="10" height="10" rx="2" fill="#161c24" stroke="rgba(240, 246, 252, 0.2)" stroke-width="0.8" />
    <rect x="14" y="-8" width="10" height="10" rx="2" fill="#2b5c40" stroke="#388e5a" stroke-width="0.5" />
    <rect x="28" y="-8" width="10" height="10" rx="2" fill="#1e7b44" stroke="#34b34b" stroke-width="0.5" />
    <rect x="42" y="-8" width="10" height="10" rx="2" fill="#26a641" stroke="#56ff74" stroke-width="0.5" />
    <rect x="56" y="-8" width="10" height="10" rx="2" fill="#39d353" stroke="#7ee787" stroke-width="0.5" />
    <text x="74" y="0" fill="#8b949e" font-size="10" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',monospace">More</text>
  </g>
</svg>'''

def main():
    username = os.environ.get("GITHUB_REPOSITORY_OWNER") or os.environ.get("USERNAME") or "ayonm95"
    print(f"Fetching GitHub contributions for {username}...")
    cal = fetch_contributions(username)
    svg = generate_svg(cal)

    # Save to contrib-3d.svg and profile-3d-contrib/profile-night-green.svg and profile-green.svg
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

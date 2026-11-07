#!/usr/bin/env python3
"""
Generate a realistic 3D architectural micro-cityscape and geological plateau GitHub contribution map.
Features Alpine mountain horizon, multi-tier bedrock mesa, landscaped pocket parks, and detailed architectural skyscrapers.
Pure Python standard library (no external dependencies required).
"""

import os
import sys
import json
import subprocess
import re
from datetime import date
from calendar import month_abbr

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
        import urllib.request
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query, "variables": {"login": username}}).encode("utf-8"),
            headers={
                "Authorization": f"bearer {token}",
                "User-Agent": "profile-3d-contrib-landscape",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    else:
        cmd = f"gh api graphql -f query='{query}' -f login='{username}'"
        res = subprocess.check_output(cmd, shell=True)
        data = json.loads(res)
        
    return data['data']['user']['contributionsCollection']['contributionCalendar']

def generate_svg(cal):
    all_weeks = cal['weeks']
    today_str = date.today().isoformat()
    weeks = all_weeks[-18:]
    
    # Start at the first week with actual contributions
    active_week = next(
        (idx for idx, week in enumerate(weeks)
         if any(day['date'] <= today_str and day.get('contributionCount', 0) > 0
                for day in week['contributionDays'])),
        0,
    )
    # Ensure at least 10 weeks are displayed for a balanced, expansive cityscape
    if len(weeks) - active_week < 10:
        active_week = max(0, len(weeks) - 10)
    weeks = weeks[active_week:]
    num_weeks = len(weeks)

    total_commits = sum(
        d['contributionCount']
        for w in weeks
        for d in w['contributionDays']
        if d['date'] <= today_str
    )
    active_days = sum(
        d['contributionCount'] > 0
        for w in weeks
        for d in w['contributionDays']
        if d['date'] <= today_str
    )
    max_single_day = max(
        (d['contributionCount']
         for w in weeks
         for d in w['contributionDays']
         if d['date'] <= today_str),
        default=0
    )

    # Canvas Dimensions (Spacious 980 x 650)
    WIDTH = 980
    HEIGHT = 650

    # Isometric Projection Scaling
    target_week_span = 510.0
    dx_w = max(30.0, min(50.0, target_week_span / num_weeks))
    dy_w = dx_w * 0.28
    dx_d = -round(dx_w * 0.70)
    dy_d = round(dx_w * 0.48)

    total_w_x = num_weeks * dx_w
    total_d_x = 7 * abs(dx_d)
    grid_total_w = total_w_x + total_d_x
    X0 = round((WIDTH - grid_total_w) / 2.0 + total_d_x + 10.0)
    Y0 = 230.0

    def proj(w, d, h=0):
        x = X0 + w * dx_w + d * dx_d
        y = Y0 + w * dy_w + d * dy_d - h
        return (x, y)

    # ─────────────────────────────────────────────────────────────
    # 1. MOUNTAIN RANGE HORIZON (Alpine low-poly ridges)
    # ─────────────────────────────────────────────────────────────
    mountains_svg = []

    # Layer 1: Distant Misty Atmospheric Silhouette
    dist_pts = [
        (0, 210), (80, 160), (160, 115), (240, 150), (330, 95), 
        (430, 140), (520, 85), (620, 130), (710, 80), (810, 125), 
        (900, 95), (980, 160), (980, 270), (0, 270)
    ]
    dist_str = " ".join(f"{x},{y}" for x, y in dist_pts)
    mountains_svg.append(f'''
  <!-- Distant Atmospheric Mountain Ridge -->
  <polygon points="{dist_str}" fill="url(#distantMountainGrad)" opacity="0.65" />
''')

    # Layer 2: Faceted Alpine Peaks with Chiseled Ridges
    alpine_peaks = [
        {"pk": (140, 110), "l_base": (20, 240), "r_base": (260, 245),
         "facets": [
             ([(140, 110), (20, 240), (90, 242), (130, 175)], "url(#mountainLitGrad1)", "#283e56"),
             ([(140, 110), (130, 175), (145, 245), (180, 243)], "url(#mountainLitGrad2)", "#203348"),
             ([(140, 110), (145, 245), (260, 245)], "url(#mountainShadowGrad1)", "#121c27")
         ],
         "snow": [(140, 110), (115, 145), (132, 155), (155, 145)]
        },
        {"pk": (310, 80), "l_base": (180, 245), "r_base": (450, 245),
         "facets": [
             ([(310, 80), (180, 245), (260, 248), (300, 160)], "url(#mountainLitGrad1)", "#283e56"),
             ([(310, 80), (300, 160), (325, 246), (360, 246)], "url(#mountainLitGrad2)", "#203348"),
             ([(310, 80), (325, 246), (450, 245)], "url(#mountainShadowGrad1)", "#121c27")
         ],
         "snow": [(310, 80), (280, 125), (305, 138), (335, 125)]
        },
        {"pk": (510, 60), "l_base": (370, 245), "r_base": (650, 245),
         "facets": [
             ([(510, 60), (370, 245), (460, 248), (495, 150)], "url(#mountainLitGrad1)", "#2c445e"),
             ([(510, 60), (495, 150), (525, 246), (570, 246)], "url(#mountainLitGrad2)", "#22374d"),
             ([(510, 60), (525, 246), (650, 245)], "url(#mountainShadowGrad1)", "#101923")
         ],
         "snow": [(510, 60), (475, 110), (502, 128), (542, 112)]
        },
        {"pk": (710, 75), "l_base": (580, 245), "r_base": (840, 245),
         "facets": [
             ([(710, 75), (580, 245), (665, 248), (695, 155)], "url(#mountainLitGrad1)", "#283e56"),
             ([(710, 75), (695, 155), (730, 246), (765, 246)], "url(#mountainLitGrad2)", "#203348"),
             ([(710, 75), (730, 246), (840, 245)], "url(#mountainShadowGrad1)", "#121c27")
         ],
         "snow": [(710, 75), (680, 120), (702, 134), (735, 120)]
        },
        {"pk": (890, 95), "l_base": (780, 245), "r_base": (980, 245),
         "facets": [
             ([(890, 95), (780, 245), (850, 248), (880, 165)], "url(#mountainLitGrad1)", "#283e56"),
             ([(890, 95), (880, 165), (905, 246)], "url(#mountainLitGrad2)", "#203348"),
             ([(890, 95), (905, 246), (980, 245)], "url(#mountainShadowGrad1)", "#121c27")
         ],
         "snow": [(890, 95), (865, 130), (885, 142), (910, 130)]
        }
    ]

    for ap in alpine_peaks:
        for pts, fill, stroke in ap["facets"]:
            pts_str = " ".join(f"{x},{y}" for x, y in pts)
            mountains_svg.append(f'<polygon points="{pts_str}" fill="{fill}" stroke="{stroke}" stroke-width="0.6" />')
        snow_str = " ".join(f"{x},{y}" for x, y in ap["snow"])
        mountains_svg.append(f'<polygon points="{snow_str}" fill="url(#snowGrad)" opacity="0.9" />')

    # Layer 3: Horizon Atmospheric Mist
    mountains_svg.append('''
  <!-- Ambient Horizon Mist Veil -->
  <rect x="0" y="200" width="980" height="90" fill="url(#horizonMistGrad)" opacity="0.88" />
''')

    # ─────────────────────────────────────────────────────────────
    # 2. GEOLOGICAL PLATEAU / MESA FOUNDATION
    # ─────────────────────────────────────────────────────────────
    pm_w = 0.95
    pm_d = 0.85

    pl_00 = proj(-pm_w, -pm_d, 0)
    pl_W0 = proj(num_weeks + pm_w, -pm_d, 0)
    pl_WD = proj(num_weeks + pm_w, 7 + pm_d, 0)
    pl_0D = proj(-pm_w, 7 + pm_d, 0)

    # 3-tier Bedrock Strata
    t1 = 10
    t2 = 22
    t3 = 34

    plateau_svg = f'''
  <!-- Deep Base Ground Ambient Occlusion Shadow -->
  <polygon points="{pl_0D[0]-32:.1f},{pl_0D[1]+t3+14:.1f} {pl_WD[0]+32:.1f},{pl_WD[1]+t3+14:.1f} {pl_W0[0]+38:.1f},{pl_W0[1]+t3+6:.1f} {pl_00[0]-38:.1f},{pl_00[1]+t3+6:.1f}" fill="#000000" opacity="0.58" filter="url(#shadowBlurLarge)" />

  <!-- Bedrock Layer 3: Deep Plutonic Granite Base -->
  <polygon points="{pl_0D[0]:.1f},{pl_0D[1]+t2:.1f} {pl_WD[0]:.1f},{pl_WD[1]+t2:.1f} {pl_WD[0]:.1f},{pl_WD[1]+t3:.1f} {pl_0D[0]:.1f},{pl_0D[1]+t3:.1f}" fill="#070c12" stroke="#162230" stroke-width="0.8" />
  <polygon points="{pl_W0[0]:.1f},{pl_W0[1]+t2:.1f} {pl_WD[0]:.1f},{pl_WD[1]+t2:.1f} {pl_WD[0]:.1f},{pl_WD[1]+t3:.1f} {pl_W0[0]:.1f},{pl_W0[1]+t3:.1f}" fill="#05080c" stroke="#121b26" stroke-width="0.8" />

  <!-- Bedrock Layer 2: Stratified Basalt Cliff with Mineral Fissures -->
  <polygon points="{pl_0D[0]:.1f},{pl_0D[1]+t1:.1f} {pl_WD[0]:.1f},{pl_WD[1]+t1:.1f} {pl_WD[0]:.1f},{pl_WD[1]+t2:.1f} {pl_0D[0]:.1f},{pl_0D[1]+t2:.1f}" fill="#0f1924" stroke="#223447" stroke-width="0.8" />
  <polygon points="{pl_W0[0]:.1f},{pl_W0[1]+t1:.1f} {pl_WD[0]:.1f},{pl_WD[1]+t1:.1f} {pl_WD[0]:.1f},{pl_WD[1]+t2:.1f} {pl_W0[0]:.1f},{pl_W0[1]+t2:.1f}" fill="#0a1118" stroke="#192735" stroke-width="0.8" />
  
  <!-- Exposed Luminous Mineral / Emerald Fault Veins -->
  <line x1="{pl_0D[0]:.1f}" y1="{pl_0D[1]+t1+6:.1f}" x2="{pl_WD[0]:.1f}" y2="{pl_WD[1]+t1+6:.1f}" stroke="#56ff74" stroke-opacity="0.28" stroke-width="0.9" stroke-dasharray="12,6,24,8" />
  <line x1="{pl_0D[0]:.1f}" y1="{pl_0D[1]+t1+14:.1f}" x2="{pl_WD[0]:.1f}" y2="{pl_WD[1]+t1+14:.1f}" stroke="#38bdf8" stroke-opacity="0.20" stroke-width="0.75" stroke-dasharray="16,10,8,6" />

  <!-- Bedrock Layer 1: Retaining Wall & Promenade Plinth -->
  <polygon points="{pl_0D[0]:.1f},{pl_0D[1]:.1f} {pl_WD[0]:.1f},{pl_WD[1]:.1f} {pl_WD[0]:.1f},{pl_WD[1]+t1:.1f} {pl_0D[0]:.1f},{pl_0D[1]+t1:.1f}" fill="#162534" stroke="#334d66" stroke-width="1.1" />
  <polygon points="{pl_W0[0]:.1f},{pl_W0[1]:.1f} {pl_WD[0]:.1f},{pl_WD[1]:.1f} {pl_WD[0]:.1f},{pl_WD[1]+t1:.1f} {pl_W0[0]:.1f},{pl_W0[1]+t1:.1f}" fill="#0e1721" stroke="#25384c" stroke-width="1.1" />

  <!-- Plateau Top Surface: Rich Obsidian Granite & Landscaped Terrace -->
  <polygon points="{pl_00[0]:.1f},{pl_00[1]:.1f} {pl_W0[0]:.1f},{pl_W0[1]:.1f} {pl_WD[0]:.1f},{pl_WD[1]:.1f} {pl_0D[0]:.1f},{pl_0D[1]:.1f}" fill="url(#plateauSurfaceGrad)" stroke="#38546e" stroke-width="1.3" />

  <!-- Luminous Platinum & Emerald Perimeter Edge Bevel -->
  <polyline points="{pl_00[0]:.1f},{pl_00[1]:.1f} {pl_0D[0]:.1f},{pl_0D[1]:.1f} {pl_WD[0]:.1f},{pl_WD[1]:.1f}" fill="none" stroke="url(#perimeterEdgeGrad)" stroke-width="2.0" filter="url(#edgeGlow)" />
'''

    # Perimeter Trees Along the Plateau Rim
    trees_svg = []
    def render_tree(px, py, scale=1.0):
        th = 16 * scale
        cw = 8.0 * scale
        return f'''
  <g>
    <!-- Trunk -->
    <line x1="{px:.1f}" y1="{py:.1f}" x2="{px:.1f}" y2="{py-th*0.35:.1f}" stroke="#3e2e1e" stroke-width="{2.0*scale:.1f}" />
    <!-- Cast Shadow -->
    <ellipse cx="{px+2.5:.1f}" cy="{py:.1f}" rx="{cw*0.9:.1f}" ry="{cw*0.5:.1f}" fill="#000000" opacity="0.45" />
    <!-- Lower Foliage Layer -->
    <polygon points="{px:.1f},{py-th:.1f} {px-cw:.1f},{py-th*0.3:.1f} {px:.1f},{py-th*0.15:.1f}" fill="#238636" />
    <polygon points="{px:.1f},{py-th:.1f} {px:.1f},{py-th*0.15:.1f} {px+cw:.1f},{py-th*0.3:.1f}" fill="#165924" />
    <!-- Upper Foliage Canopy -->
    <polygon points="{px:.1f},{py-th*1.25:.1f} {px-cw*0.75:.1f},{py-th*0.55:.1f} {px:.1f},{py-th*0.35:.1f}" fill="#3fb950" />
    <polygon points="{px:.1f},{py-th*1.25:.1f} {px:.1f},{py-th*0.35:.1f} {px+cw*0.75:.1f},{py-th*0.55:.1f}" fill="#2ea043" />
  </g>'''

    for frac in [0.08, 0.28, 0.48, 0.68, 0.88]:
        tx, ty = proj(num_weeks * frac, -0.45, 0)
        trees_svg.append(render_tree(tx, ty, scale=1.0))
    for frac in [0.2, 0.55, 0.85]:
        tx, ty = proj(-0.55, 7 * frac, 0)
        trees_svg.append(render_tree(tx, ty, scale=1.0))
    for frac in [0.25, 0.65]:
        tx, ty = proj(num_weeks + 0.5, 7 * frac, 0)
        trees_svg.append(render_tree(tx, ty, scale=1.0))

    # Boulevard Streetlights
    streetlights_svg = []
    def render_lamp(px, py):
        return f'''
  <g>
    <!-- Ground Light Pool -->
    <ellipse cx="{px:.1f}" cy="{py:.1f}" rx="7" ry="4" fill="#fef08a" opacity="0.18" filter="url(#edgeGlow)" />
    <!-- Lamp Post -->
    <line x1="{px:.1f}" y1="{py:.1f}" x2="{px:.1f}" y2="{py-14:.1f}" stroke="#94a3b8" stroke-width="0.8" />
    <line x1="{px:.1f}" y1="{py-14:.1f}" x2="{px+2.5:.1f}" y2="{py-14:.1f}" stroke="#94a3b8" stroke-width="0.8" />
    <!-- Glowing Luminaire -->
    <circle cx="{px+2.5:.1f}" cy="{py-13:.1f}" r="1.4" fill="#fef08a" filter="url(#beaconGlow)" />
  </g>'''

    for frac in [0.15, 0.5, 0.85]:
        lx, ly = proj(num_weeks * frac, 3.2, 0)
        streetlights_svg.append(render_lamp(lx, ly))

    # Street Grid Lines
    grid_lines = []
    for w in range(num_weeks + 1):
        p_start = proj(w, 0, 0)
        p_end = proj(w, 7, 0)
        grid_lines.append(f'<line x1="{p_start[0]:.1f}" y1="{p_start[1]:.1f}" x2="{p_end[0]:.1f}" y2="{p_end[1]:.1f}" stroke="#233547" stroke-width="0.9" opacity="0.65" />')
    for d in range(8):
        p_start = proj(0, d, 0)
        p_end = proj(num_weeks, d, 0)
        grid_lines.append(f'<line x1="{p_start[0]:.1f}" y1="{p_start[1]:.1f}" x2="{p_end[0]:.1f}" y2="{p_end[1]:.1f}" stroke="#233547" stroke-width="0.9" opacity="0.65" />')

    # Grand Avenue Centerline (dashed neon-green lane marking)
    blvd_start = proj(0, 3.5, 0)
    blvd_end = proj(num_weeks, 3.5, 0)
    grid_lines.append(f'<polyline points="{blvd_start[0]:.1f},{blvd_start[1]:.1f} {blvd_end[0]:.1f},{blvd_end[1]:.1f}" fill="none" stroke="#39d353" stroke-width="1.8" stroke-dasharray="5,6" opacity="0.55" />')

    # ─────────────────────────────────────────────────────────────
    # 3. ARCHITECTURAL BUILDING SPECIFICATIONS
    # ─────────────────────────────────────────────────────────────
    def get_building_spec(count):
        if count == 0:
            return {
                'level': 0, 'h': 0, 'type': 'park',
                'fill': '#0e161f', 'stroke': '#2ea043', 'stroke_opacity': '0.28',
                'glow': False, 'spire': False
            }
        elif count <= 3:
            return {
                'level': 1, 'h': 34, 'type': 'townhouse', 'stories': 3,
                'top': '#24593c', 'front': '#18422a', 'right': '#123321',
                'stroke': '#2ea043', 'glow': False, 'spire': False
            }
        elif count <= 8:
            return {
                'level': 2, 'h': 72, 'type': 'commercial', 'stories': 6,
                'top': '#1e7b44', 'front': '#145f34', 'right': '#0f4c29',
                'stroke': '#3fb950', 'glow': False, 'spire': False
            }
        elif count <= 15:
            return {
                'level': 3, 'h': 118, 'type': 'skyscraper', 'stories': 9,
                'top': '#26a641', 'front': '#1a8234', 'right': '#136728',
                'stroke': '#56ff74', 'glow': True, 'spire': False
            }
        else:
            return {
                'level': 4, 'h': 170, 'type': 'supertall', 'stories': 13,
                'top': '#39d353', 'front': '#24a63f', 'right': '#1b8131',
                'stroke': '#7ee787', 'glow': True, 'spire': True
            }

    # Painter's Algorithm Depth Sorting
    items = []
    peak_item = None
    max_count = 0

    for w in range(num_weeks):
        for d in range(len(weeks[w]['contributionDays'])):
            c_count = weeks[w]['contributionDays'][d].get('contributionCount', 0)
            c_date = weeks[w]['contributionDays'][d].get('date', '')
            if c_date > today_str:
                continue
            spec = get_building_spec(c_count)
            item = {
                'w': w, 'd': d,
                'count': c_count,
                'date': c_date,
                'spec': spec,
                'depth': w * 2.4 + d * 1.2
            }
            items.append(item)
            if c_count > max_count:
                max_count = c_count
                peak_item = item

    items.sort(key=lambda x: x['depth'])

    buildings_svg = []
    for it in items:
        w = it['w']
        d = it['d']
        spec = it['spec']
        h = spec['h']
        stories = spec.get('stories', 0)

        gap = 0.11
        p_a = proj(w + gap, d + gap, 0)
        p_b = proj(w + 1 - gap, d + gap, 0)
        p_c = proj(w + 1 - gap, d + 1 - gap, 0)
        p_d = proj(w + gap, d + 1 - gap, 0)

        if spec['level'] == 0:
            cx = (p_a[0] + p_b[0] + p_c[0] + p_d[0]) / 4.0
            cy = (p_a[1] + p_b[1] + p_c[1] + p_d[1]) / 4.0
            pts_lot = f"{p_a[0]:.1f},{p_a[1]:.1f} {p_b[0]:.1f},{p_b[1]:.1f} {p_c[0]:.1f},{p_c[1]:.1f} {p_d[0]:.1f},{p_d[1]:.1f}"

            if (w + d) % 2 == 0:
                park_str = f'''<g>
  <polygon points="{pts_lot}" fill="{spec['fill']}" stroke="{spec['stroke']}" stroke-opacity="0.28" stroke-width="0.75" />
  <!-- Stone Terrace -->
  <polygon points="{p_a[0]*0.72+cx*0.28:.1f},{p_a[1]*0.72+cy*0.28:.1f} {p_b[0]*0.72+cx*0.28:.1f},{p_b[1]*0.72+cy*0.28:.1f} {p_c[0]*0.72+cx*0.28:.1f},{p_c[1]*0.72+cy*0.28:.1f} {p_d[0]*0.72+cx*0.28:.1f},{p_d[1]*0.72+cy*0.28:.1f}" fill="#0f1c24" stroke="#1f3b4c" stroke-width="0.6" />
  <!-- Illuminated Pool -->
  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.2" fill="#0284c7" opacity="0.6" />
  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.5" fill="#38bdf8" opacity="0.9" filter="url(#edgeGlow)" />
</g>'''
            else:
                park_str = f'''<g>
  <polygon points="{pts_lot}" fill="{spec['fill']}" stroke="{spec['stroke']}" stroke-opacity="0.28" stroke-width="0.75" />
  <polygon points="{p_a[0]*0.72+cx*0.28:.1f},{p_a[1]*0.72+cy*0.28:.1f} {p_b[0]*0.72+cx*0.28:.1f},{p_b[1]*0.72+cy*0.28:.1f} {p_c[0]*0.72+cx*0.28:.1f},{p_c[1]*0.72+cy*0.28:.1f} {p_d[0]*0.72+cx*0.28:.1f},{p_d[1]*0.72+cy*0.28:.1f}" fill="#12261c" stroke="#1f4e34" stroke-width="0.6" />
  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.8" fill="#2ea043" opacity="0.8" />
</g>'''
            buildings_svg.append(park_str)
        else:
            t_a = (p_a[0], p_a[1] - h)
            t_b = (p_b[0], p_b[1] - h)
            t_c = (p_c[0], p_c[1] - h)
            t_d = (p_d[0], p_d[1] - h)

            pts_front = f"{p_d[0]:.1f},{p_d[1]:.1f} {p_c[0]:.1f},{p_c[1]:.1f} {t_c[0]:.1f},{t_c[1]:.1f} {t_d[0]:.1f},{t_d[1]:.1f}"
            pts_right = f"{p_c[0]:.1f},{p_c[1]:.1f} {p_b[0]:.1f},{p_b[1]:.1f} {t_b[0]:.1f},{t_b[1]:.1f} {t_c[0]:.1f},{t_c[1]:.1f}"
            pts_top   = f"{t_a[0]:.1f},{t_a[1]:.1f} {t_b[0]:.1f},{t_b[1]:.1f} {t_c[0]:.1f},{t_c[1]:.1f} {t_d[0]:.1f},{t_d[1]:.1f}"

            floor_bands = []
            windows = []
            for s in range(1, stories):
                frac = s / stories
                f1_x = p_d[0]
                f1_y = p_d[1] - h * frac
                f2_x = p_c[0]
                f2_y = p_c[1] - h * frac
                floor_bands.append(f'<line x1="{f1_x:.1f}" y1="{f1_y:.1f}" x2="{f2_x:.1f}" y2="{f2_y:.1f}" stroke="#ffffff" stroke-opacity="0.22" stroke-width="0.7" />')

                f3_x = p_b[0]
                f3_y = p_b[1] - h * frac
                floor_bands.append(f'<line x1="{f2_x:.1f}" y1="{f2_y:.1f}" x2="{f3_x:.1f}" y2="{f3_y:.1f}" stroke="#ffffff" stroke-opacity="0.12" stroke-width="0.6" />')

                if stories >= 4:
                    bay_w = 0.22
                    y_top = p_d[1] - h * (frac - 0.72 / stories)
                    y_bot = p_d[1] - h * (frac - 0.20 / stories)
                    for u in (0.16, 0.58):
                        x0 = p_d[0] + u * (p_c[0] - p_d[0])
                        x1 = p_d[0] + (u + bay_w) * (p_c[0] - p_d[0])
                        windows.append(f'<polygon points="{x0:.1f},{y_top:.1f} {x1:.1f},{y_top:.1f} {x1:.1f},{y_bot:.1f} {x0:.1f},{y_bot:.1f}" fill="#b9ffd0" opacity="0.38" />')

            mullions = []
            if stories >= 4:
                for frac_u in [0.33, 0.67]:
                    mb_x = p_d[0] + frac_u * (p_c[0] - p_d[0])
                    mb_y = p_d[1] + frac_u * (p_c[1] - p_d[1])
                    mullions.append(f'<line x1="{mb_x:.1f}" y1="{mb_y:.1f}" x2="{mb_x:.1f}" y2="{mb_y - h:.1f}" stroke="#ffffff" stroke-opacity="0.15" stroke-width="0.6" stroke-dasharray="2,2" />')

            inset_a = (t_a[0] * 0.78 + t_c[0] * 0.22, t_a[1] * 0.78 + t_c[1] * 0.22)
            inset_b = (t_b[0] * 0.78 + t_d[0] * 0.22, t_b[1] * 0.78 + t_d[1] * 0.22)
            inset_c = (t_c[0] * 0.78 + t_a[0] * 0.22, t_c[1] * 0.78 + t_a[1] * 0.22)
            inset_d = (t_d[0] * 0.78 + t_b[0] * 0.22, t_d[1] * 0.78 + t_b[1] * 0.22)
            pts_inset = f"{inset_a[0]:.1f},{inset_a[1]:.1f} {inset_b[0]:.1f},{inset_b[1]:.1f} {inset_c[0]:.1f},{inset_c[1]:.1f} {inset_d[0]:.1f},{inset_d[1]:.1f}"

            spire_markup = ""
            if spec['spire']:
                cx = (t_a[0] + t_b[0] + t_c[0] + t_d[0]) / 4.0
                cy = (t_a[1] + t_b[1] + t_c[1] + t_d[1]) / 4.0
                spire_markup = f'''
  <!-- Architectural Spire Antenna & Beacon Light -->
  <line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx:.1f}" y2="{cy-24:.1f}" stroke="#ffffff" stroke-width="1.6" />
  <circle cx="{cx:.1f}" cy="{cy-24:.1f}" r="3.5" fill="#ffffff" filter="url(#beaconGlow)" />
  <circle cx="{cx:.1f}" cy="{cy-24:.1f}" r="1.8" fill="#56ff74" />
'''

            floors_str = "\n  ".join(floor_bands)
            mullions_str = ("\n  " + "\n  ".join(mullions)) if mullions else ""
            glow_attr = 'filter="url(#greenGlow)" ' if spec['glow'] else ''

            building_str = f'''<g {glow_attr}>
  <!-- Right Shadow Facade -->
  <polygon points="{pts_right}" fill="{spec['right']}" stroke="{spec['stroke']}" stroke-width="0.75" />
  <!-- Front Sunlit Facade -->
  <polygon points="{pts_front}" fill="{spec['front']}" stroke="{spec['stroke']}" stroke-width="0.75" />
  <!-- Facade Stories & Windows -->
  {floors_str}{mullions_str}
  {"".join(windows)}
  <!-- Rooftop Parapet Surface -->
  <polygon points="{pts_top}" fill="{spec['top']}" stroke="{spec['stroke']}" stroke-width="1.0" />
  <!-- Inset Mechanical Penthouse / Sky Terrace -->
  <polygon points="{pts_inset}" fill="{spec['front']}" stroke="#ffffff" stroke-opacity="0.4" stroke-width="0.6" opacity="0.95" />
  {spire_markup}
</g>'''
            buildings_svg.append(building_str)

    # ─────────────────────────────────────────────────────────────
    # 4. MONTH & WEEKDAY AXIS LABELS
    # ─────────────────────────────────────────────────────────────
    clean_months = []
    seen_months = set()
    for w_idx, week in enumerate(weeks):
        for day in week['contributionDays']:
            month_key = day['date'][:7]
            if month_key not in seen_months and day['date'] <= today_str:
                seen_months.add(month_key)
                clean_months.append((month_abbr[int(month_key[5:])], w_idx))

    month_svg_parts = []
    for m_name, w_pos in clean_months:
        mx, my = proj(w_pos + 1.0, -0.9, 0)
        month_svg_parts.append(
            f'<g transform="translate({mx:.1f}, {my-6:.1f})">'
            f'<rect x="-22" y="-14" width="44" height="20" rx="5" fill="#0f172a" stroke="#334155" stroke-width="0.8" />'
            f'<text x="0" y="0" fill="#cbd5e1" font-size="12" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif" font-weight="700" text-anchor="middle">{m_name}</text>'
            f'</g>'
        )

    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    day_svg_parts = []
    for d_idx, d_name in day_labels:
        lx, ly = proj(-0.9, d_idx + 0.5, 0)
        day_svg_parts.append(
            f'<text x="{lx-12:.1f}" y="{ly+4:.1f}" fill="#94a3b8" font-size="12" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif" font-weight="700" text-anchor="end">{d_name}</text>'
        )

    # Peak Skyscraper Callout
    peak_callout = ""
    if peak_item:
        pw = peak_item['w']
        pd = peak_item['d']
        ph = peak_item['spec']['h']
        pt_x, pt_y = proj(pw + 0.5, pd + 0.5, h=ph + 22)
        peak_callout = f'''
  <!-- Peak Skyscraper Callout -->
  <g transform="translate({pt_x:.1f}, {pt_y:.1f})">
    <line x1="0" y1="0" x2="0" y2="-24" stroke="#56ff74" stroke-width="1.5" stroke-dasharray="3,3" />
    <circle cx="0" cy="0" r="4" fill="#ffffff" stroke="#39d353" stroke-width="1.8" />
    <rect x="-65" y="-48" width="130" height="24" rx="7" fill="#0d141c" stroke="#56ff74" stroke-width="1.3" filter="url(#edgeGlow)" />
    <circle cx="-52" cy="-36" r="3.5" fill="#39d353" />
    <text x="7" y="-32" fill="#7ee787" font-size="11" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',monospace" font-weight="700" text-anchor="middle">PEAK: {peak_item['count']} COMMITS</text>
  </g>'''

    visible_dates = [
        d['date'] for w in weeks for d in w['contributionDays']
        if d['date'] <= today_str
    ]
    start_date_str = next(
        (d['date'] for w in weeks for d in w['contributionDays']
         if d['date'] <= today_str and d.get('contributionCount', 0) > 0),
        visible_dates[0],
    )
    end_date_str = visible_dates[-1]

    mountains_str = "\n".join(mountains_svg)
    trees_str = "\n".join(trees_svg)
    streetlights_str = "\n".join(streetlights_svg)
    grid_str = "\n  ".join(grid_lines)
    buildings_str = "\n".join(buildings_svg)
    month_str = "\n  ".join(month_svg_parts)
    day_str = "\n  ".join(day_svg_parts)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" height="auto">
  <defs>
    <!-- Background Canvas Twilight Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#070c14" />
      <stop offset="35%" stop-color="#0a121e" />
      <stop offset="70%" stop-color="#0d1828" />
      <stop offset="100%" stop-color="#070b12" />
    </linearGradient>

    <!-- Mountain Gradients -->
    <linearGradient id="distantMountainGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#142132" />
      <stop offset="100%" stop-color="#0a1320" />
    </linearGradient>
    <linearGradient id="mountainLitGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334b66" />
      <stop offset="60%" stop-color="#24374b" />
      <stop offset="100%" stop-color="#182533" />
    </linearGradient>
    <linearGradient id="mountainLitGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#26394e" />
      <stop offset="100%" stop-color="#15212c" />
    </linearGradient>
    <linearGradient id="mountainShadowGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#141d27" />
      <stop offset="100%" stop-color="#0a0f16" />
    </linearGradient>
    <linearGradient id="snowGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f1f5f9" />
      <stop offset="60%" stop-color="#cbd5e1" />
      <stop offset="100%" stop-color="#94a3b8" />
    </linearGradient>
    <linearGradient id="horizonMistGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0a121e" stop-opacity="0" />
      <stop offset="50%" stop-color="#0d1b2a" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#0a121e" stop-opacity="0" />
    </linearGradient>

    <!-- Plateau Gradients -->
    <linearGradient id="plateauSurfaceGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#162633" />
      <stop offset="50%" stop-color="#111f2c" />
      <stop offset="100%" stop-color="#0c1620" />
    </linearGradient>
    <linearGradient id="perimeterEdgeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="50%" stop-color="#39d353" />
      <stop offset="100%" stop-color="#7ee787" />
    </linearGradient>

    <!-- Filters & Glows -->
    <filter id="greenGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4.5" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="edgeGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3.0" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="beaconGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3.5" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="shadowBlurLarge" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="14" />
    </filter>
  </defs>

  <!-- Background Canvas -->
  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="14" fill="url(#bgGrad)" stroke="#1e293b" stroke-width="1.2" />

  <!-- Stars in Upper Night Sky -->
  <g opacity="0.65">
    <circle cx="75" cy="55" r="1.1" fill="#ffffff" opacity="0.4" />
    <circle cx="140" cy="35" r="1.5" fill="#ffffff" opacity="0.8" />
    <circle cx="210" cy="60" r="1.1" fill="#60a5fa" opacity="0.5" />
    <circle cx="340" cy="30" r="1.3" fill="#ffffff" opacity="0.7" />
    <circle cx="480" cy="25" r="1.6" fill="#38bdf8" opacity="0.9" />
    <circle cx="590" cy="45" r="1.1" fill="#ffffff" opacity="0.5" />
    <circle cx="720" cy="25" r="1.4" fill="#ffffff" opacity="0.7" />
    <circle cx="830" cy="40" r="1.2" fill="#60a5fa" opacity="0.6" />
    <circle cx="910" cy="28" r="1.6" fill="#ffffff" opacity="0.85" />
  </g>

  <!-- Background Mountain Range (Alpine Peaks) -->
  {mountains_str}

  <!-- Top Cockpit Header -->
  <g transform="translate(24, 20)">
    <!-- Terminal Window Controls -->
    <circle cx="6" cy="6" r="4.5" fill="#ff5f56" />
    <circle cx="22" cy="6" r="4.5" fill="#ffbd2e" />
    <circle cx="38" cy="6" r="4.5" fill="#27c93f" />
    <text x="56" y="11" fill="#f8fafc" font-size="14" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-weight="700" letter-spacing="0.3">ayonm95 <tspan fill="#64748b" font-weight="500">/ 3D Contribution Landscape</tspan></text>

    <!-- Right Header Badges -->
    <g transform="translate({WIDTH - 440}, -2)">
      <rect x="0" y="0" width="200" height="22" rx="11" fill="#0f172a" stroke="#334155" stroke-width="1" />
      <circle cx="12" cy="11" r="3.5" fill="#39d353" />
      <text x="24" y="15" fill="#e2e8f0" font-size="11" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',monospace" font-weight="600">Past Months ({num_weeks} Weeks)</text>

      <rect x="210" y="0" width="180" height="22" rx="11" fill="#0b1c14" stroke="#22c55e" stroke-width="1" />
      <circle cx="222" cy="11" r="3.5" fill="#4ade80" filter="url(#edgeGlow)" />
      <text x="234" y="15" fill="#4ade80" font-size="11" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',monospace" font-weight="700">{total_commits} CONTRIBUTIONS</text>
    </g>
  </g>

  <!-- Cockpit Header Divider -->
  <line x1="0" y1="52" x2="{WIDTH}" y2="52" stroke="#1e293b" stroke-width="1" />

  <!-- Metric Quick-Stats Cards (Left Flank) -->
  <g transform="translate(24, 68)">
    <rect x="0" y="0" width="135" height="34" rx="7" fill="#0b131f" stroke="#1e2d42" stroke-width="1" />
    <text x="12" y="15" fill="#64748b" font-size="9" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-weight="700" letter-spacing="0.8">ACTIVE DAYS</text>
    <text x="12" y="28" fill="#f8fafc" font-size="12" font-family="monospace" font-weight="700">{active_days} Days <tspan fill="#39d353">({active_days/(num_weeks*7)*100:.0f}%)</tspan></text>
  </g>

  <g transform="translate(170, 68)">
    <rect x="0" y="0" width="135" height="34" rx="7" fill="#0b131f" stroke="#1e2d42" stroke-width="1" />
    <text x="12" y="15" fill="#64748b" font-size="9" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-weight="700" letter-spacing="0.8">PEAK COMMITS/DAY</text>
    <text x="12" y="28" fill="#f8fafc" font-size="12" font-family="monospace" font-weight="700">{max_single_day} Commits</text>
  </g>

  <g transform="translate(316, 68)">
    <rect x="0" y="0" width="135" height="34" rx="7" fill="#0b131f" stroke="#1e2d42" stroke-width="1" />
    <text x="12" y="15" fill="#64748b" font-size="9" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-weight="700" letter-spacing="0.8">CITY PARCELS</text>
    <text x="12" y="28" fill="#f8fafc" font-size="12" font-family="monospace" font-weight="700">{num_weeks * 7} Plots</text>
  </g>

  <!-- Month Axis Labels -->
  <g>
    {month_str}
  </g>

  <!-- Weekday Axis Labels -->
  <g>
    {day_str}
  </g>

  <!-- Geological Mesa / Plateau Foundation -->
  {plateau_svg}

  <!-- Street Grid & Road Markings -->
  <g>
    {grid_str}
  </g>

  <!-- Landscaped Perimeter Trees -->
  {trees_str}

  <!-- Boulevard Streetlights -->
  {streetlights_str}

  <!-- 3D Architectural Buildings -->
  {buildings_str}

  <!-- Peak Tower Callout -->
  {peak_callout}

  <!-- Bottom Cockpit Footer & Intensity Legend -->
  <line x1="0" y1="{HEIGHT-50}" x2="{WIDTH}" y2="{HEIGHT-50}" stroke="#1e293b" stroke-width="1" />

  <g transform="translate(24, {HEIGHT-24})">
    <text x="0" y="0" fill="#94a3b8" font-size="13" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-weight="500">
      <tspan fill="#39d353" font-weight="700">{total_commits} contributions</tspan> recorded from <tspan fill="#f8fafc">{start_date_str}</tspan> to <tspan fill="#f8fafc">{end_date_str}</tspan>
    </text>
  </g>

  <!-- Stepped Architectural Legend -->
  <g transform="translate({WIDTH-350}, {HEIGHT-24})">
    <text x="-12" y="0" fill="#64748b" font-size="11" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',monospace" text-anchor="end">Less</text>
    
    <rect x="0" y="-10" width="14" height="14" rx="2" fill="#0e161f" stroke="#2ea043" stroke-opacity="0.3" stroke-width="0.8" />
    <rect x="20" y="-10" width="14" height="14" rx="2" fill="#18422a" stroke="#2ea043" stroke-width="0.8" />
    <rect x="40" y="-10" width="14" height="14" rx="2" fill="#145f34" stroke="#3fb950" stroke-width="0.8" />
    <rect x="60" y="-10" width="14" height="14" rx="2" fill="#1a8234" stroke="#56ff74" stroke-width="0.8" />
    <rect x="80" y="-10" width="14" height="14" rx="2" fill="#24a63f" stroke="#7ee787" stroke-width="0.8" />
    
    <text x="104" y="0" fill="#64748b" font-size="11" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',monospace">More</text>
    <text x="155" y="0" fill="#94a3b8" font-size="11" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',monospace">Park · Towers · Spire</text>
  </g>
</svg>'''

def main():
    username = os.environ.get("GITHUB_REPOSITORY_OWNER") or os.environ.get("USERNAME") or "ayonm95"
    print(f"Fetching GitHub contributions for {username}...")
    cal = fetch_contributions(username)
    svg = generate_svg(cal)
    svg = "\n".join(line.rstrip() for line in svg.splitlines()) + "\n"

    # Save to root and profile-3d-contrib directory
    os.makedirs("profile-3d-contrib", exist_ok=True)
    with open("contrib-3d.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    with open("profile-3d-contrib/activity-skyline.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    with open("profile-3d-contrib/profile-night-green.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    with open("profile-3d-contrib/profile-green.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Saved contrib-3d.svg and profile-3d-contrib/ SVGs successfully!")

if __name__ == "__main__":
    main()

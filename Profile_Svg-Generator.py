import html
import os
import requests

THEME = "Dark"   # "Dark" Or "Light"

PALETTES = {
    "Dark":  {"bg": "#09120C", "text": "#C1E8D5", "key": "#22C55E",
              "value": "#6EE7B7", "add": "#10B981", "del": "#FF4B4B", "cc": "#115E59",
              "ascii": "#A3E635", "title": "#2DD4BF", "section": "#FBBF24"},
    "Light": {"bg": "#F0FDF4", "text": "#064E3B", "key": "#16A34A",
              "value": "#059669", "add": "#15803D", "del": "#DC2626", "cc": "#6EE7B7",
              "ascii": "#65A30D", "title": "#0D9488", "section": "#D97706"},
}
PAL = PALETTES[THEME]
OUT_FILE = "DARK_MODE.svg" if THEME == "Dark" else "LIGHT_MODE.svg"


ASCII_ART = [
    "                                 ",
    "   .---------------------------. ",
    "  /  /=======================\\  \\",
    "  | |  [ SYSTEM OVERRIDE ]    | |",
    "  | |                         | |",
    "  | |  root@dev:~# init_      | |",
    "  | |  [+] Core Loaded...     | |",
    "  | |  [+] Node Sync: OK      | |",
    "  | |  [+] Access Granted     | |",
    "  | |                         | |",
    "  | |  root@dev:~# _          | |",
    "  |  \\=======================/  |",
    "  \\_____________________________/",
    "       ||                 ||     ",
    "   ____||_________________||____ ",
    " /______________________________\\",
    " |___===___________________===__|",
    " | [1] [2] [3] [4] [5]       (O)|",
    " |______________________________|",
    "                                 ",
    "  [ SYSTEM STATUS ]              ",
    "  CPU: [########--] 80%          ",
    "  RAM: [#####-----] 50%          ",
    "  NET: [##########] 99%          ",
    "  PWR: [#######---] 72%          ",
]


def fetch_github_stats(username):
    headers = {}
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    
    stats = {"repos": "25", "followers": "—", "stars": "—", "contributions": "274"}
    
    try:
        r = requests.get(f"https://api.github.com/users/{username}", headers=headers)
        if r.status_code == 200:
            data = r.json()
            stats["repos"] = str(data.get("public_repos", stats["repos"]))
            stats["followers"] = str(data.get("followers", stats["followers"]))
        
        r_repos = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers)
        if r_repos.status_code == 200:
            repos_data = r_repos.json()
            total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
            stats["stars"] = str(total_stars)
    except Exception as e:
        print(f"Failed to fetch GitHub stats: {e}")
        
    return stats

def fetch_wakatime_stats():
    api_key = os.environ.get("WAKATIME_API_KEY")
    stats = {"hours": "803"}
    if not api_key:
        return stats
    try:
        r = requests.get(f"https://wakatime.com/api/v1/users/current/stats/all_time?api_key={api_key}")
        if r.status_code == 200:
            data = r.json().get("data", {})
            total_seconds = data.get("total_seconds", 0)
            hours = int(total_seconds / 3600)
            stats["hours"] = str(hours)
    except Exception as e:
        print(f"Failed to fetch WakaTime stats: {e}")
    return stats

def generate_data():
    gh_stats = fetch_github_stats("i8o8i-Developer")
    wk_stats = fetch_wakatime_stats()
    
    return [
        ("title", "i8o8i@developer"),
        ("kv", "OS", "Windows, Linux, Android"),
        ("kv", "Uptime", "18 years, 1 month, 10 days", "age_data"),
        ("kv", "Host", "i8o8i Solutions (Not Open To Hire)"),
        ("kv", "Role", "Full Stack Developer & AI/ML Engineer"),
        ("kv", "IDE", "VS Code, Antigravity IDE, Trae"),
        ("blank",),
        ("kv", "Languages.Programming", "Python, TypeScript, JavaScript, C++, Go"),
        ("kv", "Languages.Computer", "HTML, CSS, GraphQL, PHP, Bash"),
        ("kv", "Languages.Real", "English , Hindi"),
        ("blank",),
        ("kv", "Focus.Backend", "Multi-Agent Workflows, API Architecture"),
        ("kv", "Focus.Systems", "Distributed Systems, Deployment Pipelines"),
        ("blank",),
        ("section", "Contact"),
        ("kv", "Email", "i8o8iworkstation@outlook.com"),
        ("kv", "LinkedIn", "anubhav1608"),
        ("kv", "Telegram", "i8o8i_Developer"),
        ("kv", "YouTube", "i8o8i-Developer"),
        ("kv", "GitHub", "i8o8i-Developer"),
        ("blank",),
        ("section", "GitHub Stats"),
        ("combo", [("Repos", gh_stats["repos"], "repo_data"), ("Private", "0", "contrib_data"),
                   ("2026 Contributions", gh_stats["contributions"], "commit_data")]),
        ("combo", [("Stars", gh_stats["stars"], "star_data"), ("Followers", gh_stats["followers"], "follower_data")]),
        ("combo", [("Lines Written (WakaTime)", "31,400,000", "loc_data"),
                   ("Hours Coded", wk_stats["hours"], "loc_add")]),
    ]

# ──────────────────────────────────────────────────────────────────────────
# 4. LAYOUT CONSTANTS  (rarely need to touch these)
# ──────────────────────────────────────────────────────────────────────────
FONT_SIZE = 16
LINE_HEIGHT = 20
TOP_PAD = 30
LEFT_PAD = 15
ASCII_COL_X = 15
TEXT_COL_X = 360
RIGHT_MARGIN = 45
BOTTOM_MARGIN = 20
CHAR_W = FONT_SIZE * 0.58
DOT_TARGET_COL = 26  

# ──────────────────────────────────────────────────────────────────────────
# Rendering Helpers
# ──────────────────────────────────────────────────────────────────────────

def esc(s):
    return html.escape(str(s), quote=False)


def dots_for(label_len, target_col=DOT_TARGET_COL):
    pad = max(0, target_col - label_len)
    if pad <= 0:
        return " "
    if pad <= 2:
        return " " * pad
    return " " + ("." * pad) + " "


def render_kv(y, key, value, elem_id=None):
    label = f". {key}:"
    dots = dots_for(len(label))
    id_attr_dots = f' id="{elem_id}_dots"' if elem_id else ""
    id_attr_val = f' id="{elem_id}"' if elem_id else ""
    plain_len = len(label) + len(dots) + len(str(value)) + 2
    svg = (
        f'<tspan x="{TEXT_COL_X}" y="{y}" class="cc">. </tspan>'
        f'<tspan class="key">{esc(key)}</tspan>:'
        f'<tspan class="cc"{id_attr_dots}>{esc(dots)}</tspan>'
        f'<tspan class="value"{id_attr_val}>{esc(value)}</tspan>'
    )
    return svg, plain_len


def render_combo(y, pairs):
    parts = ['<tspan class="cc">. </tspan>']
    plain_len = 2
    for i, item in enumerate(pairs):
        key, value = item[0], item[1]
        elem_id = item[2] if len(item) > 2 else None
        if i > 0:
            parts.append('<tspan class="key"> | </tspan>')
            plain_len += 3
        label = f"{key}:"
        dots = dots_for(len(label), target_col=len(label) + 3)  # small fixed gap
        id_attr_val = f' id="{elem_id}"' if elem_id else ""
        parts.append(
            f'<tspan class="key">{esc(key)}</tspan>:'
            f'<tspan class="cc">{esc(dots)}</tspan>'
            f'<tspan class="value"{id_attr_val}>{esc(value)}</tspan>'
        )
        plain_len += len(label) + len(dots) + len(str(value))
    svg = f'<tspan x="{TEXT_COL_X}" y="{y}">' + "".join(parts) + "</tspan>"
    return svg, plain_len


def render_title(y, text, target_len):
    dash_count = max(5, target_len - len(text) - 2)
    svg = f'<tspan x="{TEXT_COL_X}" y="{y}" class="title">{esc(text)}</tspan> <tspan class="cc">-{"-" * dash_count}</tspan>'
    return svg, target_len


def render_section(y, text, target_len):
    dash_count = max(5, target_len - len(text) - 4)
    svg = f'<tspan x="{TEXT_COL_X}" y="{y}" class="section">- {esc(text)}</tspan> <tspan class="cc">-{"-" * dash_count}</tspan>'
    return svg, target_len


def build_svg():
    ascii_tspans = []
    y = TOP_PAD
    max_ascii_len = 0
    for line in ASCII_ART:
        ascii_tspans.append(f'<tspan x="{ASCII_COL_X}" y="{y}">{esc(line)}</tspan>')
        max_ascii_len = max(max_ascii_len, len(line))
        y += LINE_HEIGHT
    ascii_block_height = y

    data = generate_data()

    max_content_len = 0
    for row in data:
        kind = row[0]
        if kind == "kv":
            key, value = row[1], row[2]
            label = f". {key}:"
            dots = dots_for(len(label))
            plen = len(label) + len(dots) + len(str(value)) + 2
            max_content_len = max(max_content_len, plen)
        elif kind == "combo":
            plen = 2
            for i, item in enumerate(row[1]):
                if i > 0: plen += 3
                label = f"{item[0]}:"
                dots = dots_for(len(label), target_col=len(label) + 3)
                plen += len(label) + len(dots) + len(str(item[1]))
            max_content_len = max(max_content_len, plen)

    text_tspans = []
    y = TOP_PAD
    max_text_len = max_content_len
    for row in data:
        kind = row[0]
        if kind == "title":
            svg, plen = render_title(y, row[1], max_content_len)
        elif kind == "section":
            svg, plen = render_section(y, row[1], max_content_len)
        elif kind == "kv":
            key, value = row[1], row[2]
            elem_id = row[3] if len(row) > 3 else None
            svg, plen = render_kv(y, key, value, elem_id)
        elif kind == "combo":
            svg, plen = render_combo(y, row[1])
        elif kind == "blank":
            svg = f'<tspan x="{TEXT_COL_X}" y="{y}" class="cc">. </tspan>'
            plen = 2
        else:
            raise ValueError(f"Unknown Row Type: {kind}")
        text_tspans.append(svg)
        y += LINE_HEIGHT
    text_block_height = y

    width = int(TEXT_COL_X + max_text_len * CHAR_W + RIGHT_MARGIN)
    width = max(width, ASCII_COL_X + int(max_ascii_len * CHAR_W) + TEXT_COL_X)
    height = max(ascii_block_height, text_block_height) + BOTTOM_MARGIN

    svg = f'''<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="{width}px" height="{height}px" font-size="{FONT_SIZE}px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {PAL["key"]};}}
.value {{fill: {PAL["value"]};}}
.addColor {{fill: {PAL["add"]};}}
.delColor {{fill: {PAL["del"]};}}
.cc {{fill: {PAL["cc"]};}}
.ascii {{fill: {PAL["ascii"]};}}
.title {{fill: {PAL["title"]}; font-weight: bold;}}
.section {{fill: {PAL["section"]}; font-weight: bold;}}
text, tspan {{white-space: pre;}}
</style>
<rect width="{width}px" height="{height}px" fill="{PAL["bg"]}" rx="15"/>
<text x="{ASCII_COL_X}" y="{TOP_PAD}" class="ascii">
{chr(10).join(ascii_tspans)}
</text>
<text x="{TEXT_COL_X}" y="{TOP_PAD}" fill="{PAL["text"]}">
{chr(10).join(text_tspans)}
</text>
</svg>
'''
    return svg


if __name__ == "__main__":
    svg = build_svg()
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT_FILE}")
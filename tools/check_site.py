"""정적 사이트 SEO·GEO 점검 (표준 라이브러리만 사용). 실패가 있으면 종료 코드 1.
사용: python3 tools/check_site.py"""
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "public"
SITE = "https://www.hq-tech.co.kr"
PAGES = {"/": "index.html", "/about": "about.html", "/faq": "faq.html", "/csv-guide": "csv-guide.html"}
# 기존 앱(프록시)이 계속 처리하는 경로
LEGACY = ("/consultation", "/services/", "/terms", "/privacy", "/favicon.png", "/og-image.png")
DEFINITION = "컴퓨터 시스템 밸리데이션"
fails, notes = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h, self.cur, self.text, self.links, self.ids, self.meta, self.ld = [], None, [], [], set(), {}, []
        self.skip = 0
        self.in_ld = False

    def handle_starttag(self, t, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if t in ("script", "style", "svg"):
            self.skip += 1
            self.in_ld = t == "script" and a.get("type") == "application/ld+json"
        if re.fullmatch(r"h[1-6]", t):
            self.h.append(int(t[1]))
        if t == "a" and a.get("href"):
            self.links.append(a["href"])
        if t == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k] = a.get("content", "")
        if t == "link" and a.get("rel") == "canonical":
            self.meta["canonical"] = a.get("href")
        if t == "html":
            self.meta["lang"] = a.get("lang")

    def handle_endtag(self, t):
        if t in ("script", "style", "svg"):
            self.skip -= 1
            self.in_ld = False

    def handle_data(self, d):
        if self.in_ld:
            self.ld.append(d)
        elif not self.skip:
            self.text.append(d)


def check(route, fn):
    p = P()
    p.feed((ROOT / fn).read_text(encoding="utf-8"))
    text = re.sub(r"\s+", " ", html.unescape(" ".join(p.text)))
    tag = f"[{route}]"
    if p.meta.get("lang") != "ko":
        fails.append(f"{tag} html lang이 ko가 아님")
    if p.h.count(1) != 1:
        fails.append(f"{tag} H1 개수 {p.h.count(1)}")
    skips = sum(1 for a, b in zip(p.h, p.h[1:]) if b - a > 1)
    if skips:
        fails.append(f"{tag} 제목 단계 건너뜀 {skips}곳")
    if p.meta.get("canonical") != SITE + ("/" if route == "/" else route):
        fails.append(f"{tag} canonical 불일치: {p.meta.get('canonical')}")
    d = p.meta.get("description", "")
    if not 50 <= len(d) <= 160:
        fails.append(f"{tag} description 길이 {len(d)}")
    for k in ("og:title", "og:description", "og:image", "og:url", "twitter:card"):
        if not p.meta.get(k):
            fails.append(f"{tag} {k} 없음")
    graph = []
    for raw in p.ld:
        try:
            j = json.loads(raw)
            graph += j.get("@graph", [j])
        except json.JSONDecodeError as e:
            fails.append(f"{tag} JSON-LD 파싱 실패: {e}")
    types = sorted({t if isinstance(t, str) else "/".join(t) for t in (n.get("@type") for n in graph)})
    for n in graph:
        if n.get("@type") == "FAQPage":
            for q in n["mainEntity"]:
                if q["name"] not in text:
                    fails.append(f"{tag} FAQ 질문이 화면에 없음: {q['name']}")
                ans = re.sub(r"\s+", " ", q["acceptedAnswer"]["text"])[:40]
                if ans not in text:
                    fails.append(f"{tag} FAQ 답변이 화면과 다름: {q['name']}")
    if DEFINITION not in text:
        fails.append(f"{tag} 정의 문장 없음")
    for href in p.links:
        if href.startswith("#") and href[1:] and href[1:] not in p.ids:
            fails.append(f"{tag} 깨진 앵커 {href}")
        path = href.replace(SITE, "") if href.startswith(SITE) else href
        if path.startswith("/") and not path.startswith("//"):
            base = path.split("#")[0] or "/"
            if base not in PAGES and not base.startswith(LEGACY):
                fails.append(f"{tag} 처리되지 않는 내부 링크 {href}")
    for bad in ("/case-studies", "/news", "facebook.com", "instagram.com", "linkedin.com", "youtube.com", "교육 · 사후", "상시 지원"):
        if bad in (ROOT / fn).read_text(encoding="utf-8").replace("/tag/reg-news", ""):
            fails.append(f"{tag} 뺀 항목이 남아 있음: {bad}")
    notes.append(f"{tag} 본문 {len(text):,}자 · H1 1 · 구조화 데이터 {', '.join(types)}")


for r, f in PAGES.items():
    check(r, f)

sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
for loc in re.findall(r"<loc>(.*?)</loc>", sm):
    path = loc.replace(SITE, "") or "/"
    if path not in PAGES and not path.startswith(LEGACY):
        fails.append(f"[sitemap] 처리되지 않는 URL {loc}")
if "Sitemap: https://www.hq-tech.co.kr/sitemap.xml" not in (ROOT / "robots.txt").read_text():
    fails.append("[robots] sitemap 위치 없음")
llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
if "/case-studies" in llms or "hq-tech.co.kr/news" in llms:
    fails.append("[llms.txt] 뺀 페이지 링크가 남아 있음")
for a in ("hq-capabilities.mp4", "hq-capabilities.webm", "hq-capabilities-poster.webp", "hq-logo-dark.webp", "hq-logo-white.webp"):
    if not (ROOT / "assets" / a).exists():
        fails.append(f"[assets] {a} 없음")

print("\n".join(notes))
print(f"\n점검 결과: 실패 {len(fails)}건")
print("\n".join(" - " + f for f in fails))
sys.exit(1 if fails else 0)

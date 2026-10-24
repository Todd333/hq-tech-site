# hq-tech-site

www.hq-tech.co.kr의 홈, 회사 소개, FAQ, CSV 가이드 정적 사이트입니다 (2026-10-24 개편).
나머지 경로(상담 신청, 서비스 상세, 약관, 개인정보처리방침, API)는 기존 React 앱이 계속 처리하고, 이 프로젝트가 그 요청을 기존 앱으로 넘겨 줍니다.

## 구조

| 경로 | 내용 |
| --- | --- |
| `public/` | 배포되는 파일 전부. `index.html`, `about.html`, `faq.html`, `csv-guide.html`, `assets/`, `robots.txt`, `sitemap.xml`, `llms.txt` |
| `vercel.json` | 깔끔한 주소(`/about`), 301 리다이렉트, 보안 헤더, 기존 앱으로 넘기는 규칙 |
| `tools/check_site.py` | SEO·GEO 자동 점검 (푸시할 때마다 GitHub Actions에서 실행) |
| `tools/serve.py` | 로컬 미리 보기 서버 (영상 재생 지원) |
| `backlog.json` | 남은 일과 결정 사항 |
| `docs/` | 설계·비교 기록(NOTES), 하위 페이지 변경표(SUBPAGES), 모션 영상 원본, 이전 버전 보관 |

## 요청이 처리되는 순서 (Vercel)

1. `/case-studies` → `/` (301), `/news` → 블로그 규제뉴스 태그 (301)
2. `public/`에 파일이 있으면 그 파일 (`/`, `/about`, `/faq`, `/csv-guide`, `/assets/hq-*`, `/llms.txt` 등)
3. 그 밖의 모든 경로는 기존 앱(`hq-tech-2026.vercel.app`, Vercel 프로젝트 `hq-tech-2026`)으로 프록시. 주소창 URL은 그대로 유지

## 처음 한 번: 운영 연결

1. **기존 앱 주소 확인**: Vercel 대시보드에서 지금 www.hq-tech.co.kr이 붙어 있는 프로젝트를 열고, Domains에 있는 `*.vercel.app` 주소를 확인합니다.
2. `vercel.json`의 `__LEGACY_ORIGIN__`을 그 주소(예: `hq-tech-xxxx.vercel.app`, `https://` 없이)로 바꿔 커밋합니다.
3. **새 프로젝트**: Vercel → Add New → Project → `Todd333/hq-tech-site` 가져오기 → Framework Preset `Other` → Deploy. 이후 `main`에 푸시하면 자동 배포됩니다.
4. **미리보기 확인**: 새 프로젝트의 `*.vercel.app` 주소에서 홈·회사 소개·FAQ·CSV 가이드, 그리고 `/consultation`(폼 제출까지), `/services/compliance` 등이 열리는지 봅니다.
5. **도메인 이전**: 기존 프로젝트 Settings → Domains에서 `www.hq-tech.co.kr`과 `hq-tech.co.kr`을 제거하고, 새 프로젝트에 같은 이름으로 추가합니다. `hq-tech.co.kr`은 `www`로 리다이렉트되게 설정합니다(기존과 동일). 같은 Vercel 팀 안이면 DNS는 바꿀 필요가 없습니다.
6. Search Console에서 sitemap을 다시 제출합니다.

## 롤백

- **전체 되돌리기 (1~2분)**: 새 프로젝트 Domains에서 두 도메인을 제거하고 기존 프로젝트에 다시 추가합니다. 기존 프로젝트와 소스 저장소는 이번 작업에서 전혀 건드리지 않았습니다.
- **이 사이트의 이전 버전으로**: Vercel → 새 프로젝트 → Deployments → 이전 배포 → Instant Rollback, 또는 `git revert` 후 푸시.

## 로컬 미리 보기

```bash
python3 tools/serve.py   # http://localhost:8090
```

## 점검

```bash
python3 tools/check_site.py
```

H1 개수, 제목 단계, canonical, description, OG, JSON-LD 파싱, FAQ 구조화 데이터와 화면 문구 일치, 정의 문장, 내부 링크, sitemap, robots, llms.txt, 뺀 항목(도입사례·규제뉴스 경로·SNS·사후 지원)이 남아 있지 않은지 확인합니다.

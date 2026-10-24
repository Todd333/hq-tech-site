# HQ-Tech 홈·하위 페이지 개편 · 운영 적용 후보 (2026-10-24)

하위 페이지 3종(회사 소개, FAQ, CSV 가이드)의 변경 내용과 확인 사항은 `SUBPAGES.md`를 보세요.

krackerz.com의 구성과 인터랙션 패턴을 HQ-Tech 브랜드와 콘텐츠로 옮기고, SEO·GEO 점검과 "환자 생명 존중" 색·서체 방향을 반영한 홈페이지입니다. 이 폴더는 www.hq-tech.co.kr 루트에 그대로 올릴 수 있는 형태입니다.

## 폴더 구성

| 파일 | 내용 |
| --- | --- |
| `index.html` | 홈페이지 한 장. `<html lang="ko">`, 완전한 `<head>`(title, description, canonical, OG, JSON-LD) 포함 |
| `assets/hq-logo-dark.webp`, `assets/hq-logo-white.webp` | 현행 사이트 원본 로고를 투명 배경으로 변환 |
| `robots.txt` | 현행과 동일 (전체 허용 + sitemap 위치) |
| `sitemap.xml` | 현행 URL에서 `/case-studies`(운영 안 함)와 `/news`(블로그로 이전)를 뺀 11개, 홈·회사 소개·FAQ·CSV 가이드에 `lastmod` 2026-10-24 |
| `about/`, `faq/`, `csv-guide/` | 하위 페이지 (상세는 `SUBPAGES.md`) |
| `serve.py` | 맥미니 미리 보기 서버 (영상 재생 지원) |
| `NOTES.md` | 비교 분석, SEO·GEO 점검표, 색·서체 결정 기록 |

## 맥미니에서 미리 보기

```bash
cd hq-tech-site-release
python3 serve.py          # http://localhost:8090 (다른 포트: python3 serve.py 8091)
```

`serve.py`는 영상 구간 요청(Range)을 지원하는 미리 보기 서버입니다. `python3 -m http.server`는 이를 지원하지 않아 Safari에서 모션 영상이 재생되지 않습니다.

## 운영 적용 방법 (현행 사이트는 React SPA + 사전 렌더링)

1. **홈만 교체 (가장 빠름)**: 빌드 결과물의 `/index.html`을 이 파일로 바꾸고 `assets/`를 함께 올립니다. 다른 페이지(`/csv-guide`, `/consultation` 등)는 기존 React 앱이 그대로 처리합니다. 서버(또는 호스팅)의 SPA 폴백 설정이 `/` 요청에 이 파일을 주는지 확인하세요.
2. **React 컴포넌트로 이식**: 섹션별로 JSX로 옮기고, `<head>` 내용은 사전 렌더링 단계에서 그대로 출력되게 합니다. 서비스 탭과 참여 방식 내용은 반드시 HTML에 렌더링된 상태로 남겨야 SEO·GEO 점수가 유지됩니다.
3. **Ghost로 옮기는 A안을 계속 추진한다면**: `index.html`을 테마의 `custom-home.hbs`로 바꾸는 것이 가장 가깝습니다.

## 운영 반영 전 확인할 것 (대표님 결정 필요)

- [ ] **수치 근거**: 50+ 프로젝트, 99.9% 감사 통과율, 30+ 고객사, 100% 온타임. 현행 사이트 값을 옮긴 것이라 근거 자료와 맞는지 확인. 근거가 약하면 "감사 대응 실적" 같은 표현으로 조정
- [ ] **고객사 로고**: 게재 승인 받은 곳만 "함께한 고객사" 자리에 넣기 (지금은 빈 자리 표시)
- [ ] **회사 소개 문구**: "엔지니어 출신 컨설턴트" 표현과 역량 표가 실제와 맞는지
- [x] **SNS 계정**: 운영하지 않음 (2026-10-24 확인). 이 파일의 `sameAs`에는 블로그만 넣었고 푸터에 SNS 아이콘 없음
- [ ] **현행 React 앱에서 삭제**: 공통 `<head>`의 Organization JSON-LD `sameAs`에 있는 LinkedIn·GitHub 주소, 공통 푸터의 LinkedIn·Facebook·YouTube 아이콘. 홈만 교체해도 나머지 페이지에는 계속 남음
- [ ] **로그인 메뉴**: 현행 메뉴에 있던 "로그인"은 넣지 않았음. 필요하면 추가
- [ ] **og-image.png**: 새 색상(청록) 기준으로 다시 만들지 결정 (현행 이미지를 그대로 가리킴)

## 배포 후 확인

- Google Search Console: 홈 URL 검사 → 색인 요청, 리치 결과 테스트(FAQ, 조직 정보)
- 카카오톡·LinkedIn에 링크를 붙여 공유 미리보기 이미지 확인
- PageSpeed Insights로 모바일 속도 확인. 느리면 Google Fonts 대신 Pretendard·Noto Serif KR 서브셋 자체 호스팅

## 이번 버전에서 바뀐 점 (운영 적용 후보)

- 메뉴를 현행 사이트 페이지(서비스, CSV 가이드, 도입사례, 규제 뉴스, 회사 소개, 블로그)로 연결. 모바일은 펼침 메뉴
- 모든 상담 버튼을 `/consultation`(현행 상담 신청 페이지)로 연결
- 운영용 독립 HTML로 빌드: `lang="ko"`, `theme-color`, 파비콘, head 정리
- 자동 점검: 원본 HTML 본문 약 6,000자, H1 1개, 제목 단계 건너뜀 0, 구조화 데이터 4종 정상, FAQ 6문항이 화면 문구와 일치, 이미지 alt 누락 0, 모바일 가로 넘침 0

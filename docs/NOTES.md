# HQ-Tech 랜딩 시안 메모 (2026-10-24)

## 파일
- `index.html`: 시안 페이지 (HTML, CSS, JS 한 파일)
- `assets/hq-logo-dark.webp`, `assets/hq-logo-white.webp`: www.hq-tech.co.kr 원본 로고(`/favicon.png`, `/logo-white.png`)를 투명 배경 WebP로 변환한 것

로컬에서 확인할 때는 `index.html` 맨 위에 아래 줄을 붙이면 됩니다(게시 도구가 자동으로 넣던 부분).

```html
<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>
```

## 두 사이트 비교

| 항목 | krackerz.com (참고) | www.hq-tech.co.kr (현재) | 시안에 반영한 것 |
| --- | --- | --- | --- |
| 제작 도구 | Framer (Framer Motion 애니메이션) | React SPA (Vite) + Tailwind CDN | 의존성 없는 정적 HTML |
| 검색 노출 | 서버 렌더링, 본문이 HTML에 있음 | 사전 렌더링으로 본문 일부 노출 (홈 약 3,300자, 2026-10-24 확인) | 본문 전체가 HTML에 있음 (약 6,000자) |
| 첫 화면 | 큰 디스플레이 서체 + 기울인 강조 칩 + CTA 1개 | 어두운 배경, 영문 큰 제목, CTA 2개 | 한글 큰 제목 + 기울인 강조 칩, 핵심 원칙 문장 |
| 내비게이션 | 떠 있는 알약형 메뉴 + 형광 CTA | 고정 상단 바 | 떠 있는 알약형 메뉴, 스크롤 시 로고 숨김 |
| 버튼 | 두꺼운 테두리 + 아래 단단한 그림자, 누르면 내려감 | 둥근 마젠타 버튼 | 같은 눌림 동작, 오로라 인장 화살표 |
| 시각 모티프 | 과자(스캘럽) 가장자리, 한 입 베어 문 카드 | 아이콘, picsum 임시 사진 | 승인 인장(로제트), 접힌 문서 모서리, 문서 표지 카드 |
| 기능 소개 | 폴더 탭 3개, 탭마다 배경색 변경 | 카드 6개 나열 | 바인더 탭 3개(CSV·CSA·교육), 추적성 매트릭스 등 실물 화면 |
| 공감 섹션 | 실명 후기 4개 | 없음 | 자주 듣는 고민 4개 (실명 후기 아님) |
| 신뢰 근거 | 창업자 소개, 수상 이력 표, 경력사 로고 | 수치 6개 | 수치 원장, 역량 표, 고객사 로고 자리 |
| 가격 | 월·연 토글, 3단 요금 | 없음 | 신규 도입 ↔ 변경·재검증 토글, 3단 참여 방식 (견적 문의) |
| 놀이 요소 | 노트북에 스티커 끌어다 붙이기 | 없음 | 처음엔 바인더에 문서 끌어 넣기 → 사용법이 직관적이지 않아 **검증 패키지 8가지 문서 정보 섹션**으로 교체 (2026-10-24 결정) |
| 마무리 | 구름 모양 경계 + 큰 CTA | 단순 CTA 밴드 | 구름 모양 경계 + 연락처 복사 버튼 |

## 일부러 하지 않은 것
- krackerz의 사진, 캐릭터, 스티커, 로고, 유료 서체는 쓰지 않았습니다. 저작권과 브랜드 혼동 문제가 있고, HQ-Tech와 결이 다릅니다. 구조와 인터랙션 패턴만 가져왔습니다.
- 현재 사이트의 사진 2장은 picsum 임시 이미지라 원본으로 쓸 수 없었습니다. 실제 사진(작업 현장, 대표 인물 등)이 있으면 인장 그래픽 자리에 넣으면 됩니다.
- 고객사 실명과 로고는 게재 승인 전이라 자리만 두었습니다.

## 맥미니에서 할 일
1. 서체: Pretendard가 설치되어 있으면 본문은 자동으로 Pretendard가 됩니다. 제목용 Bricolage Grotesque, Gothic A1은 Google Fonts에서 불러옵니다.
2. 수치(50+, 99.9% 등)는 현재 사이트 게시 값을 그대로 옮겼습니다. 근거 자료와 다시 맞춰 보세요.
3. 문의 버튼은 모두 현행 상담 신청 페이지(`/consultation`)로 연결했습니다 (2026-10-24 운영 적용 후보).
4. Ghost로 옮길 경우 각 섹션을 HTML 카드로 넣거나, 테마의 `custom-home.hbs`로 만드는 방법이 있습니다.

## REA로 직접 분석하려면 (맥미니)
이번 작업 환경에서는 두 사이트 모두 네트워크가 막혀 REA로 번들을 받지 못했습니다. 그래서 Chrome에서 실행 중인 페이지의 구조·스타일·애니메이션을 직접 읽어 분석했습니다. 맥미니에서는 아래처럼 실행할 수 있습니다.

```bash
npx -y rea-agents@latest doctor
# 페이지를 열어 스크립트를 수집하고 정적 분석
npx -y rea-agents@latest analyze-web-bundle https://krackerz.com/ --json > krackerz-bundle.json
npx -y rea-agents@latest analyze-web-bundle https://www.hq-tech.co.kr/ --json > hqtech-bundle.json
```

## SEO·GEO 점검 (2026-10-24)

### 현행 www.hq-tech.co.kr
| 항목 | 상태 | 조치 |
| --- | --- | --- |
| 원본 HTML 본문 | 있음 (사전 렌더링, 홈 약 3,300자) | 8월 기록과 달리 개선됨. 하위 페이지는 600~2,200자로 얇음 |
| title, description, canonical, robots | 있음 | 유지 |
| og:image | **없음** (twitter:card는 large_image) | `/og-image.png`가 이미 있으니 `og:image`, `twitter:image` 추가 |
| 구조화 데이터 | Organization, WebSite, `/faq`에 FAQPage | 법인명·별칭(에이치큐테크), 우편번호, `knowsAbout`, 서비스 목록 추가 권장 |
| `sameAs` | LinkedIn, GitHub `hq-tech` | **삭제**. SNS 계정을 운영하지 않음 (2026-10-24 확인). 푸터 SNS 아이콘도 삭제 |
| robots.txt, sitemap.xml | 있음 (13개 URL) | sitemap에 `lastmod` 없음 → 추가 |
| llms.txt | 있음, 내용 충실 | 유지. 서비스 페이지 요약을 한 줄씩 더하면 좋음 |
| 갱신 신호 | 푸터 © 2024, 날짜 없음 | 연도 갱신, 최종 업데이트 날짜 표시 |
| 이미지 | picsum 임시 사진 2장 | 실제 이미지로 교체하거나 삭제 |
| 근거 없는 수치 | "감사 통과율 99.9%" 등 | 근거 자료가 없으면 표현 조정. AI 답변 엔진은 확인 가능한 사실을 우선 인용하고, 의약 분야 광고 표현으로도 위험 |

### 시안에 반영한 것 (자동 점검 통과)
- title 31자, description 157자, canonical, robots, OG 10종, Twitter 4종
- JSON-LD `@graph`: ProfessionalService(법인명, 별칭, 주소·우편번호, 전화, 팩스, 이메일, knowsAbout, 서비스 3종), WebSite, WebPage(`dateModified`), FAQPage 6문항 (화면 문구와 일치 확인)
- H1 1개, 제목 32개, 단계 건너뜀 0
- 서비스 탭 3개와 참여 방식(신규·변경) 내용을 모두 HTML에 직접 기록. JS 없이도 수집됨 (원본 HTML 본문 약 5,900자)
- AI가 인용하기 좋은 정의 문장 1개: "컴퓨터 시스템 밸리데이션(CSV)은 …"
- 회사 개요(법인명·분야·대응 규제·소재지)를 본문 텍스트로 노출
- 최종 업데이트 날짜(`<time>`), 실제 하위 페이지 링크 6개, 모든 이미지 alt·크기 지정

### 맥미니 배포 시 `<head>` 템플릿
게시 도구는 `<html lang>`을 넣지 못해 JS로 보정했습니다. 실제 배포에서는 아래로 시작하세요.

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<!-- 여기에 index.html 맨 위의 <title>~</script>(JSON-LD)까지 붙여넣기 -->
</head>
<body>
```

남은 권장 사항: Google Fonts 4종은 무거우므로(특히 한글) Pretendard·Noto Serif KR을 서브셋으로 자체 호스팅, sitemap `lastmod` 추가, Search Console에서 리치 결과 테스트.

## 색·서체 방향: 환자 생명 존중
- 바탕: 클린룸을 떠올리는 맑은 흰색(#F4F8F7)과 생명의 청록(#0D7C72, 브랜드 틸 #0D9488 계열)
- 어두운 띠: 짙은 청록(#0E3437). 보라·마젠타 계열은 로고에만 남김
- 따뜻한 산호색(#E4795F)은 "환자의 맥박"으로 아주 적게 사용: 히어로의 심전도 선(마지막이 체크 표시로 끝남), 환자 문장 앞 점
- 제목: Noto Serif KR. 진지함과 배려를 담고, 굵기는 900→700으로 낮춤. 본문은 Pretendard(없으면 Gothic A1)
- 기울기·그림자 축소, 숫자·문서 코드는 그대로 또렷하게
- 추가 문구: "검증 문서 한 장 뒤에는, 그 약을 기다리는 환자가 있습니다." / "검증은 결국 환자를 지키는 일입니다."

## 2026-10-24 추가 반영 (참고 사이트 재검토)
- 서비스 탭(CSV·CSA·교육)을 스크롤하면 위로 쌓이는 고정 카드로 변경. 클릭 없이 세 내용이 모두 보임 (모바일·낮은 화면에서는 일반 배치)
- 상담 버튼을 문제 제기, 검증 절차, 검증 패키지, FAQ 뒤에 추가 (총 11곳)
- 히어로 문서 카드 캡션을 문서 이름에서 방문자 상황으로 변경 ("실사 일정이 잡혔을 때" 등)
- 문제 제기 뒤에 "검증을 떠받치는 다섯 가지 기준" 3D 모션 영상 섹션 추가
  - `assets/hq-capabilities.mp4` (1920×1080, 14.5초, 3.3MB), `.webm` (1.5MB), 포스터 `.webp`
  - 무음 자동 반복, 일시정지 버튼, 움직임 줄이기 설정 시 자동 재생 끔
  - 영상 아래에 다섯 기준을 텍스트로 병기, 구조화 데이터 VideoObject 추가
  - 원본 모션 HTML(`motion/motion.html`)을 함께 넣어 문구 수정 후 다시 렌더링 가능


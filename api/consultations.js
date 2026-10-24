// 상담 신청 접수: 기존 React 앱의 폼이 POST /api/consultations 로 보내는 데이터를 NocoDB에 저장합니다.
// 필요한 환경 변수 (Vercel → Settings → Environment Variables):
//   NOCODB_URL       예: https://nocodb.hq-tech.co.kr
//   NOCODB_TOKEN     NocoDB API 토큰 (Team & Settings → Tokens)
//   NOCODB_TABLE_ID  상담 신청 테이블 ID (예: m1a2b3c4d5e6f7g)

const FIELDS = { company: 100, name: 50, email: 120, phone: 40, topic: 60, message: 4000 };

function clean(v, max) {
  return typeof v === 'string' ? v.trim().slice(0, max) : '';
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: '허용되지 않는 요청입니다.' });
  }
  const { NOCODB_URL, NOCODB_TOKEN, NOCODB_TABLE_ID } = process.env;
  if (!NOCODB_URL || !NOCODB_TOKEN || !NOCODB_TABLE_ID) {
    console.error('NocoDB 환경 변수가 설정되지 않았습니다.');
    return res.status(500).json({ error: '접수 설정에 문제가 있습니다. 031.8067.7870 또는 contact@hq-tech.co.kr로 연락해 주세요.' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  body = body || {};
  if (body.website) return res.status(200).json({ ok: true }); // 스팸 봇용 숨김 필드

  const rec = {};
  for (const [k, max] of Object.entries(FIELDS)) rec[k] = clean(body[k], max);
  if (!rec.company || !rec.name || !rec.email || !rec.message) {
    return res.status(400).json({ error: '회사명, 성함, 이메일, 상담 내용을 입력해 주세요.' });
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(rec.email)) {
    return res.status(400).json({ error: '이메일 주소를 확인해 주세요.' });
  }
  rec.status = '신규';
  rec.user_id = clean(body.user_id, 64);
  rec.source = 'www.hq-tech.co.kr/consultation';

  try {
    const r = await fetch(`${NOCODB_URL.replace(/\/$/, '')}/api/v2/tables/${NOCODB_TABLE_ID}/records`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'xc-token': NOCODB_TOKEN },
      body: JSON.stringify(rec),
      signal: AbortSignal.timeout(10000),
    });
    if (!r.ok) {
      console.error('NocoDB 저장 실패', r.status, (await r.text()).slice(0, 300));
      return res.status(502).json({ error: '접수 중 오류가 발생했습니다. 031.8067.7870 또는 contact@hq-tech.co.kr로 연락해 주세요.' });
    }
    const saved = await r.json().catch(() => ({}));
    return res.status(201).json({ ok: true, id: saved.Id ?? saved.id ?? null });
  } catch (e) {
    console.error('NocoDB 연결 실패', e);
    return res.status(502).json({ error: '접수 서버에 연결하지 못했습니다. 031.8067.7870 또는 contact@hq-tech.co.kr로 연락해 주세요.' });
  }
}

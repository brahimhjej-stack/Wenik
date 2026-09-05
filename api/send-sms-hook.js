import { Webhook } from 'standardwebhooks';

const BSB_SEND_URL = 'https://www.bestsmsbulk.com/bestsmsbulkapi/sendSmsAPIJson.php';
const SENDER_ID = 'WENIK';

function getHeader(req, name) {
  const value = req.headers?.[name] ?? req.headers?.[name.toLowerCase()];
  return Array.isArray(value) ? value[0] : value;
}

async function readPayload(req) {
  if (typeof req.body === 'string') return req.body;
  if (Buffer.isBuffer(req.body)) return req.body.toString('utf8');
  if (req.body && typeof req.body === 'object') return JSON.stringify(req.body);
  const chunks = [];
  for await (const chunk of req) chunks.push(Buffer.from(chunk));
  return Buffer.concat(chunks).toString('utf8');
}

function hookSecret(value) {
  if (!value) throw new Error('SEND_SMS_HOOK_SECRET is not configured');
  return value.replace(/^v1,whsec_/, '');
}

function verifyHook(payload, req) {
  const webhook = new Webhook(hookSecret(process.env.SEND_SMS_HOOK_SECRET));
  return webhook.verify(payload, {
    'webhook-id': getHeader(req, 'webhook-id'),
    'webhook-timestamp': getHeader(req, 'webhook-timestamp'),
    'webhook-signature': getHeader(req, 'webhook-signature'),
  });
}

function normalizeDestination(phone) {
  let digits = String(phone || '').replace(/\D/g, '');
  if (digits.startsWith('00')) digits = digits.slice(2);
  if (digits.startsWith('0')) digits = digits.slice(1);
  if (!digits.startsWith('961') && (digits.length === 7 || digits.length === 8)) digits = `961${digits}`;
  if (!/^[1-9]\d{7,14}$/.test(digits)) throw new Error('Invalid destination phone');
  return digits;
}

function smsRequest(phone, otp) {
  if (!/^\d{6}$/.test(otp || '')) throw new Error('Invalid verification code');
  const username = process.env.BSB_API_KEY;
  const password = process.env.BSB_API_SECRET;
  if (!username || !password) throw new Error('BSB credentials are not configured');
  return {
    username,
    password,
    senderid: SENDER_ID,
    destination: normalizeDestination(phone),
    message: `Hello WENIK shopper your otp is: ${otp}`,
  };
}

function safeProviderText(text) {
  return String(text || '')
    .replace(/\b\d{6}\b/g, '[OTP]')
    .replace(/(password|username|api[_ -]?key|api[_ -]?secret)\s*[:=]\s*[^\s&;]+/gi, '$1=[REDACTED]')
    .slice(0, 500);
}

function parseBsbJson(text) {
  try { return JSON.parse(text); } catch { return null; }
}

function assertAccepted(resultText) {
  if (!resultText) throw new Error('BSB empty response');
  const data = parseBsbJson(resultText);
  if (!data) throw new Error(`Unexpected BSB response: ${safeProviderText(resultText)}`);
  const status = Number(data.status ?? data.Status ?? 0);
  if (status === 201) return data;
  const reason = data.message ?? data.error ?? data.description ?? resultText;
  throw new Error(`BSB rejected SMS status ${status || 'unknown'}: ${safeProviderText(reason)}`);
}

async function sendWithBsb(phone, otp) {
  const response = await fetch(BSB_SEND_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify(smsRequest(phone, otp)),
    signal: AbortSignal.timeout(12_000),
  });

  const result = (await response.text()).trim();
  if (!response.ok) {
    console.error('BSB JSON HTTP error:', response.status, safeProviderText(result) || '[empty response]');
    throw new Error(`BSB request failed (${response.status})`);
  }
  const accepted = assertAccepted(result);
  console.info('BSB accepted SMS request', accepted?.confirmationid ? 'with confirmation id' : '');
  return accepted;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: { http_code: 405, message: 'Method not allowed' } });
  }

  try {
    const payload = await readPayload(req);
    const event = verifyHook(payload, req);
    await sendWithBsb(event?.user?.phone, event?.sms?.otp);
    return res.status(200).json({});
  } catch (error) {
    console.error('WENIK SMS hook failed:', error instanceof Error ? error.message : error);
    return res.status(500).json({ error: { http_code: 500, message: 'Unable to send verification code' } });
  }
}

export const __test = { hookSecret, normalizeDestination, smsRequest, safeProviderText, parseBsbJson, assertAccepted };

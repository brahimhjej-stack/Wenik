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

  const apiKey = process.env.BSB_API_KEY;
  const apiSecret = process.env.BSB_API_SECRET;
  if (!apiKey || !apiSecret) throw new Error('BSB credentials are not configured');

  return [{
    api_key: apiKey,
    api_secret: apiSecret,
    senderid: SENDER_ID,
    destination: normalizeDestination(phone),
    message: `WENIK verification code: ${otp}. Do not share this code.`,
  }];
}

async function sendWithBsb(phone, otp) {
  const response = await fetch(BSB_SEND_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(smsRequest(phone, otp)),
    signal: AbortSignal.timeout(12_000),
  });

  const text = await response.text();
  let result;
  try {
    result = JSON.parse(text);
  } catch {
    throw new Error(`BSB returned an invalid response (${response.status})`);
  }

  if (!response.ok || Number(result?.status) !== 201) {
    throw new Error(result?.message || `BSB rejected the SMS (${response.status})`);
  }

  return result;
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
    return res.status(500).json({
      error: {
        http_code: 500,
        message: 'Unable to send verification code',
      },
    });
  }
}

export const __test = { hookSecret, normalizeDestination, smsRequest };

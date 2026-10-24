import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const [,, html, out = 'out.mp4'] = process.argv;
const browser = await chromium.launch({ executablePath: process.env.CHROME });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(pathToFileURL(path.resolve(html)).href);
await page.waitForFunction(() => window.MOTION);
const m = await page.evaluate(async () => { await window.MOTION.ready?.(); const { width, height, duration, fps } = window.MOTION; return { width, height, duration, fps: fps || 30 }; });
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(m.fps), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'slow', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const total = Math.round(m.duration * m.fps);
for (let i = 0; i < total; i++) {
  await page.evaluate(t => new Promise(r => { window.MOTION.seek(t); requestAnimationFrame(() => r()); }), i / m.fps);
  const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
await page.evaluate(t => window.MOTION.seek(t), m.duration * 0.98);
await page.screenshot({ path: out.replace(/\.mp4$/, '-poster.png') });
await browser.close();
console.log('frames', total);

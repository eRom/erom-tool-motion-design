#!/usr/bin/env bun
// Envoie une vidéo d'animation UI à elorian/glimpse (OpenRouter) et imprime une spec motion Markdown sur stdout.
// Les métadonnées (transcodage, ralenti, tokens, coût) partent sur stderr pour ne pas polluer la spec.
//
// Usage : bun glimpse.ts <vidéo> ["<élément ou question>"] [--stack "<cible>"] [--slowmo N] [--effort low|medium|high]

import { parseArgs } from "node:util";
import { tmpdir } from "node:os";
import path from "node:path";
import { unlink } from "node:fs/promises";

const MODEL = "elorian/glimpse";
// Seuil sur le fichier brut : le base64 ajoute ~33 %, donc ~27 Mo sur le fil.
const MAX_RAW_MB = 20;
const REQUEST_TIMEOUT_MS = 300_000;
const DEFAULT_QUESTION = "Rétro-conçois l'animation principale de cette vidéo.";

const MEDIA_TYPES: Record<string, string> = {
  ".mp4": "video/mp4",
  ".webm": "video/webm",
  ".mov": "video/quicktime",
};

function systemPrompt(stack: string, slowmo: number): string {
  const slowmoNote = slowmo > 1
    ? `\nIMPORTANT: this recording was slowed down ${slowmo}x before upload. Every duration and timestamp you measure on screen must be divided by ${slowmo} before you report it. Report real-time values only.`
    : "";
  return `You are a Principal Creative Developer & Motion Engineer reverse-engineering a front-end animation from a screen recording.
Watch the video at the densest frame rate you can. Track each moving element across frames to measure displacement, acceleration, deceleration and layering.${slowmoNote}
Write an actionable technical specification in French, in Markdown, so a coding agent that cannot see the video can implement it directly in ${stack}:
1. **Décomposition chorégraphique (timeline en ms)** - from t=0ms to the end, element by element, with stagger delays.
2. **Propriétés animées** - translations (X/Y in px or %), scale, rotation, opacity, clip-path, blur, parallax. Give start and end values.
3. **Physique et easing** - describe the velocity curve (e.g. fast start, long braking), then give the equivalent cubic-bezier(x1,y1,x2,y2) or spring stiffness/damping/mass.
4. **Code** - a minimal ${stack} implementation of the whole choreography.
5. **Pièges d'implémentation** - transform-origin, will-change, scroll-trigger handling, layer stacking.
6. **Confiance** - for each measured value, say whether it is measured on several frames or estimated from too few frames.
Describe only what is visible. If a value cannot be measured, say so instead of inventing a precise number.`;
}

function fail(message: string, code = 1): never {
  console.error(`glimpse: ${message}`);
  process.exit(code);
}

// Réencode la vidéo : 1280 px max, sans audio (le modèle ne lit pas le son), ralentie si slowmo > 1.
async function transcode(source: string, slowmo: number): Promise<string> {
  if (!Bun.which("ffmpeg")) {
    fail("ffmpeg absent (brew install ffmpeg) : requis pour --slowmo ou une vidéo de plus de 20 Mo.");
  }
  const target = path.join(tmpdir(), `glimpse-${process.pid}.mp4`);
  const filters = [`scale='min(1280,iw)':-2`];
  if (slowmo > 1) filters.push(`setpts=${slowmo}*PTS`);
  const proc = Bun.spawn(
    ["ffmpeg", "-y", "-loglevel", "error", "-i", source,
      "-vf", filters.join(","), "-an",
      "-c:v", "libx264", "-preset", "veryfast", "-crf", "28", target],
    { stderr: "pipe" },
  );
  if ((await proc.exited) !== 0) {
    fail(`ffmpeg a échoué : ${await new Response(proc.stderr).text()}`);
  }
  return target;
}

const { values, positionals } = parseArgs({
  args: Bun.argv.slice(2),
  options: {
    stack: { type: "string", default: "CSS + GSAP" },
    // x8 par défaut : à vitesse réelle Glimpse a halluciné l'animation, x4 a inversé l'easing (recette 2026-10-17).
    slowmo: { type: "string", default: "8" },
    effort: { type: "string", default: "high" },
  },
  allowPositionals: true,
});

const [filePath, question = DEFAULT_QUESTION] = positionals;
if (!filePath) {
  fail('usage : bun glimpse.ts <vidéo> ["<élément ou question>"] [--stack "<cible>"] [--slowmo N] [--effort low|medium|high]', 2);
}
const slowmo = Number(values.slowmo);
if (!Number.isInteger(slowmo) || slowmo < 1 || slowmo > 8) fail(`--slowmo attend un entier de 1 à 8, reçu « ${values.slowmo} »`, 2);
if (!["low", "medium", "high"].includes(values.effort!)) fail(`--effort inconnu « ${values.effort} » (low, medium, high)`, 2);

const apiKey = process.env.OPENROUTER_API_KEY;
if (!apiKey) fail("OPENROUTER_API_KEY absente de l'environnement.");

const source = path.resolve(filePath);
const file = Bun.file(source);
if (!(await file.exists())) fail(`fichier introuvable : ${source}`);

const mime = MEDIA_TYPES[path.extname(source).toLowerCase()];
if (!mime) fail(`format non supporté (${path.extname(source)}) : ${Object.keys(MEDIA_TYPES).join(", ")}`);

let uploadPath = source;
let uploadMime = mime;
const rawMb = file.size / 1024 / 1024;
if (rawMb > MAX_RAW_MB || slowmo > 1) {
  uploadPath = await transcode(source, slowmo);
  uploadMime = "video/mp4";
  const outMb = Bun.file(uploadPath).size / 1024 / 1024;
  console.error(`glimpse: transcodé ${rawMb.toFixed(1)} Mo -> ${outMb.toFixed(1)} Mo, ralenti x${slowmo}`);
  if (outMb > MAX_RAW_MB) fail(`encore ${outMb.toFixed(1)} Mo après transcodage : découpe la vidéo autour de l'animation.`);
}

try {
  const base64 = Buffer.from(await Bun.file(uploadPath).arrayBuffer()).toString("base64");
  const dataUrl = `data:${uploadMime};base64,${base64}`;

  const started = performance.now();
  const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
      "X-Title": "erom-motion-design reverse-animation",
    },
    body: JSON.stringify({
      model: MODEL,
      reasoning: { effort: values.effort },
      usage: { include: true },
      messages: [
        { role: "system", content: systemPrompt(values.stack!, slowmo) },
        { role: "user", content: [{ type: "video_url", video_url: { url: dataUrl } }, { type: "text", text: question }] },
      ],
    }),
    signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
  });

  if (!response.ok) fail(`OpenRouter ${response.status} : ${await response.text()}`);

  const data = await response.json();
  const content: string | undefined = data.choices?.[0]?.message?.content;
  if (!content) fail(`réponse vide : ${JSON.stringify(data).slice(0, 500)}`);

  const usage = data.usage ?? {};
  const seconds = ((performance.now() - started) / 1000).toFixed(1);
  console.error(
    `glimpse: ${seconds} s, ${usage.prompt_tokens ?? "?"} in / ${usage.completion_tokens ?? "?"} out, coût ${usage.cost ?? "?"} $`,
  );
  console.log(content);
} finally {
  if (uploadPath !== source) await unlink(uploadPath).catch(() => {});
}

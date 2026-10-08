#!/usr/bin/env bun
// Recherche dans references/index.tsv : chaque mot compte, les sons qui en contiennent le plus sortent en premier.
// Usage : bun search.ts <mot> [mot…] [--min 0.5] [--max 10] [--cat WHSH] [--limit 15]
import { join } from "node:path";

const INDEX = join(import.meta.dir, "..", "references", "index.tsv");

const args = process.argv.slice(2);
const terms: string[] = [];
let minDuration = 0;
let maxDuration = Infinity;
let catPrefix = "";
let limit = 15;
for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === "--min") minDuration = Number(args[++i]);
  else if (arg === "--max") maxDuration = Number(args[++i]);
  else if (arg === "--cat") catPrefix = args[++i].toUpperCase();
  else if (arg === "--limit") limit = Number(args[++i]);
  else terms.push(arg.toLowerCase());
}

const [header, ...lines] = (await Bun.file(INDEX).text()).trim().split("\n");
const columns = header.split("\t");
const col = (name: string) => columns.indexOf(name);

const hits = lines
  .map((line) => {
    const cells = line.split("\t");
    const duration = Number(cells[col("duration_s")]);
    const catId = cells[col("cat_id")];
    // Texte cherché : catégorie, pack et nom, séparateurs ramenés à des espaces.
    const haystack = `${catId} ${cells[col("pack")]} ${cells[col("name")]}`.toLowerCase().replace(/[_\-.]/g, " ");
    const score = terms.filter((term) => haystack.includes(term)).length;
    return { cells, duration, catId, score };
  })
  .filter((h) => h.duration >= minDuration && h.duration <= maxDuration)
  .filter((h) => !catPrefix || h.catId.toUpperCase().startsWith(catPrefix))
  .filter((h) => terms.length === 0 || h.score > 0)
  .sort((a, b) => b.score - a.score || a.duration - b.duration)
  .slice(0, limit);

if (hits.length === 0) {
  console.log("aucun résultat : essayer des synonymes anglais ou une catégorie (--cat)");
} else {
  for (const h of hits) {
    const c = h.cells;
    console.log(
      `[${h.score}/${terms.length}] ${h.duration.toFixed(1)}s ${c[col("channels")]}ch ${c[col("sample_rate")]}Hz  ${c[col("path")]}`,
    );
  }
}

# 03. Blueprints de Fabrication & Recettes de Code

Ce document rassemble les architectures logicielles, formules mathématiques et composants typés prêts à l'emploi (TypeScript / Remotion, Canvas 2D et SVG) pour reproduire à l'identique les six mécanismes clés de `u40iA4iKOsGi_kWx.mp4`.

---

## Blueprint 1 : Moteur de Rebond Gravitationnel avec Squash & Stretch et Onion-Skinning

### Rôle & Principe Physique
Simule la trajectoire d'une balle soumise à la gravité avec perte d'énergie (coefficient de restitution `e = 0.72`), déformation élastique à l'impact selon le principe de conservation de surface 2D (`scaleX * scaleY = 1.0`), et rendu stroboscopique des frames passées (pelure d'oignon / onion-skinning).

### Formulation Mathématique Frame par Frame
Pour chaque frame $f \in [0, 55]$ :
1. Calcul de la parabole de vol :
   $$y(t) = y_{\text{apex}} + \frac{1}{2} g (t - t_{\text{apex}})^2$$
2. Vitesse verticale : $v_y(t) = g (t - t_{\text{apex}})$.
3. Facteur de squash à l'impact ($y \ge y_{\text{floor}}$) :
   $$s_y = 1.0 - 0.35 \cdot \cos\left(\frac{\pi (f - f_{\text{impact}})}{D_{\text{impact}}}\right), \quad s_x = \frac{1.0}{s_y}$$
4. Facteur de stretch en vol proportionnel à la vitesse verticale :
   $$s_y = 1.0 + 0.008 \cdot |v_y|, \quad s_x = \frac{1.0}{s_y}$$

### Composant TypeScript (Remotion / SVG)

```tsx
import React, { useMemo } from "react";
import { useCurrentFrame, interpolate } from "remotion";

interface BouncingBallProps {
  floorY?: number;
  ballRadius?: number;
  primaryColor?: string;
}

export const BouncingBallSystem: React.FC<BouncingBallProps> = ({
  floorY = 780,
  ballRadius = 28,
  primaryColor = "#1E6BFF",
}) => {
  const frame = useCurrentFrame();

  // Trajectoire frame-accurate calculée sur 60 frames
  const calculateState = (f: number) => {
    // Rebond 1 (F0 - F26), Rebond 2 (F27 - F45), Stabilisation (F46 - F60)
    let x = 280 + f * 20;
    let y = floorY;
    let scaleX = 1;
    let scaleY = 1;

    if (f < 14) {
      // Chute initiale 1
      const t = f / 14;
      y = 150 + Math.pow(t, 2) * (floorY - 150);
      const vy = (2 * (floorY - 150)) / 14 * t;
      scaleY = 1 + vy * 0.005;
      scaleX = 1 / scaleY;
    } else if (f >= 14 && f <= 18) {
      // Phase de Squash à l'impact 1
      const progress = (f - 14) / 4;
      const squashFactor = Math.sin(progress * Math.PI) * 0.45;
      scaleX = 1 + squashFactor;
      scaleY = 1 / scaleX;
      y = floorY - (ballRadius * (scaleY - 1));
    } else if (f > 18 && f <= 36) {
      // Rebond 1 (Ascension puis descente vers apex y: 380)
      const t = (f - 18) / 18;
      // Parabole normalisée : 4 * h * t * (1 - t)
      const height = floorY - 380;
      y = floorY - 4 * height * t * (1 - t);
      const vy = (1 - 2 * t) * height * 0.1;
      scaleY = 1 + Math.abs(vy) * 0.008;
      scaleX = 1 / scaleY;
    } else if (f > 36 && f <= 40) {
      // Squash impact 2
      const progress = (f - 36) / 4;
      const squashFactor = Math.sin(progress * Math.PI) * 0.28;
      scaleX = 1 + squashFactor;
      scaleY = 1 / scaleX;
      y = floorY - (ballRadius * (scaleY - 1));
    } else {
      // Rebond 2 amorti vers la position de repos
      const t = Math.min(1, (f - 40) / 16);
      const height = floorY - 600;
      y = floorY - (1 - t) * 4 * height * t * (1 - t);
      scaleX = 1;
      scaleY = 1;
    }

    return { x, y, scaleX, scaleY };
  };

  const current = calculateState(frame);

  // Échantillonnage de l'historique pour l'effet pelure d'oignon (Onion-Skinning)
  const ghostFrames = useMemo(() => {
    if (frame < 10) return [];
    const pastOffsets = [12, 9, 6, 3];
    return pastOffsets
      .map((offset) => frame - offset)
      .filter((f) => f >= 0)
      .map((f, idx) => ({
        ...calculateState(f),
        opacity: [0.12, 0.22, 0.35, 0.55][idx],
      }));
  }, [frame]);

  return (
    <svg width="1920" height="1080" style={{ position: "absolute", top: 0, left: 0 }}>
      {/* Ligne de sol */}
      <line
        x1="160"
        y1={floorY}
        x2="1760"
        y2={floorY}
        stroke="#111215"
        strokeWidth="3"
        strokeDasharray="12 8"
      />

      {/* Fantômes stroboscopiques onion-skin */}
      {ghostFrames.map((g, i) => (
        <ellipse
          key={i}
          cx={g.x}
          cy={g.y}
          rx={ballRadius * g.scaleX}
          ry={ballRadius * g.scaleY}
          fill={primaryColor}
          opacity={g.opacity}
        />
      ))}

      {/* Balle active */}
      <ellipse
        cx={current.x}
        cy={current.y}
        rx={ballRadius * current.scaleX}
        ry={ballRadius * current.scaleY}
        fill={primaryColor}
      />
    </svg>
  );
};
```

---

## Blueprint 2 : Moteur de Kinetic Typography Physique (Les 4 Mots)

### Rôle & Principe
Gère les quatre comportements physiques de la séquence 3 ("type wordplay") sur fond sombre `#121316` :
1. `BOUNCE` : Effet d'extrusion étagée (stack 2.5D) avec cascade de 6 couches textuelles décalées en diagonale et pondérées en opacité.
2. `STRETCH` : Déformation élastique horizontale régie par un oscillateur harmonique amorti (spring physics).
3. `SPIN` : Rotation 3D sur l'axe Y à 450 degrés avec perspective 1200px et décalage de phase par lettre.
4. `SNAP` : Transformation sans amorti (`no ease`) avec bounding box de manipulation et poignées de transformation vectorielles.

### Composant TypeScript (Remotion)

```tsx
import React from "react";
import { useCurrentFrame, spring } from "remotion";

export const KineticTypographyWordplay: React.FC = () => {
  const frame = useCurrentFrame();

  // Durée de chaque mot : 14 frames (1 temps à 129.2 BPM)
  const wordIndex = Math.floor(frame / 14);
  const localFrame = frame % 14;

  const fontStyle: React.CSSProperties = {
    fontFamily: "'Druk Condensed', 'Tungsten', 'Anton', sans-serif",
    fontSize: "260px",
    fontWeight: 900,
    textTransform: "uppercase",
    lineHeight: 0.82,
    letterSpacing: "-0.02em",
    textAlign: "center",
  };

  // 1. MOT "BOUNCE" (Frames 0 à 13)
  if (wordIndex === 0) {
    // Rebond polynomial rapide
    const bounceProgress = localFrame / 14;
    const yOffset = Math.sin(bounceProgress * Math.PI) * -80;
    const layers = [5, 4, 3, 2, 1, 0]; // Profondeur Z

    return (
      <div style={{ position: "relative", width: 1920, height: 1080, display: "flex", justifyContent: "center", alignItems: "center" }}>
        {layers.map((layer) => {
          const isFront = layer === 0;
          return (
            <div
              key={layer}
              style={{
                ...fontStyle,
                position: "absolute",
                color: isFront ? "#FFFFFF" : "#1E6BFF",
                opacity: isFront ? 1.0 : 0.15 * (6 - layer),
                transform: `translate(${layer * 5}px, ${yOffset + layer * 7}px)`,
              }}
            >
              BOUNCE
            </div>
          );
        })}
      </div>
    );
  }

  // 2. MOT "STRETCH" (Frames 14 à 27)
  if (wordIndex === 1) {
    // Oscillateur harmonique amorti pour scaleX et scaleY
    const spr = spring({
      frame: localFrame,
      fps: 30,
      config: { damping: 14, mass: 0.8, stiffness: 220 },
    });
    // Départ étiré à scaleX: 2.1 puis retour oscillant à 1.0
    const scaleX = 2.1 - spr * 1.1;
    const scaleY = 1 / scaleX; // Conservation de volume
    const blurAmount = Math.max(0, (scaleX - 1.0) * 12);

    return (
      <div style={{ width: 1920, height: 1080, display: "flex", justifyContent: "center", alignItems: "center" }}>
        <div
          style={{
            ...fontStyle,
            color: "#1E6BFF",
            transform: `scale(${scaleX}, ${scaleY})`,
            filter: `blur(${blurAmount}px 0px)`,
          }}
        >
          STRETCH
        </div>
      </div>
    );
  }

  // 3. MOT "SPIN" (Frames 28 à 41)
  if (wordIndex === 2) {
    const letters = "SPIN".split("");
    const rotationTotal = 450; // Rotation 3D sur Y

    return (
      <div
        style={{
          width: 1920,
          height: 1080,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          perspective: 1200,
        }}
      >
        <div style={{ display: "flex" }}>
          {letters.map((char, idx) => {
            // Décalage de 1.2 frame par lettre
            const delayedFrame = Math.max(0, localFrame - idx * 1.2);
            const progress = Math.min(1, delayedFrame / 10);
            const currentRotY = progress * rotationTotal;

            return (
              <span
                key={idx}
                style={{
                  ...fontStyle,
                  display: "inline-block",
                  color: "#FFFFFF",
                  transform: `rotateY(${currentRotY}deg)`,
                  transformOrigin: "center center",
                }}
              >
                {char}
              </span>
            );
          })}
        </div>
      </div>
    );
  }

  // 4. MOT "SNAP" (Frames 42 à 55)
  if (wordIndex === 3) {
    // Aucun amorti : montée en 1 frame
    const isSnapped = localFrame >= 1;

    return (
      <div style={{ position: "relative", width: 1920, height: 1080, display: "flex", justifyContent: "center", alignItems: "center" }}>
        {/* Bounding box vectorielle rouge avec poignées */}
        <div
          style={{
            position: "absolute",
            width: 780,
            height: 320,
            border: "2px dashed #FF334B",
            display: isSnapped ? "block" : "none",
          }}
        >
          {/* Poignées de transformation aux 4 coins et 4 milieux */}
          {[
            { top: -6, left: -6 },
            { top: -6, right: -6 },
            { bottom: -6, left: -6 },
            { bottom: -6, right: -6 },
            { top: -6, left: "50%" },
            { bottom: -6, left: "50%" },
          ].map((pos, i) => (
            <div
              key={i}
              style={{
                position: "absolute",
                width: 12,
                height: 12,
                backgroundColor: "#FF334B",
                ...pos,
              }}
            />
          ))}
        </div>

        <div
          style={{
            ...fontStyle,
            color: "#FF334B",
            transform: isSnapped ? "scale(1)" : "scale(0.8)",
            opacity: isSnapped ? 1 : 0,
          }}
        >
          SNAP
        </div>
      </div>
    );
  }

  return null;
};
```

---

## Blueprint 3 : Éditeur de Courbe de Bézier Interactif (Séquence Easing)

### Rôle & Algorithme
Modélise la transition pédagogique entre l'interpolation linéaire rigide et la courbe sigmoïde "ease in-out" :
1. Calcul du polynôme de Bernstein de degré 3 pour la courbe de Bézier :
   $$B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3$$
2. Animation de la position du curseur de souris tirant la poignée de tangente $P_1$ et $P_2$.
3. Échantillonnage de la position $x(t)$ du carré noir le long du rail horizontal directement asservie à la courbe mathématique active.

### Composant TypeScript (SVG / Remotion)

```tsx
import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

export const InteractiveBezierCurveEditor: React.FC = () => {
  const frame = useCurrentFrame();

  // Origine et dimensions du repère orthonormé
  const originX = 660;
  const originY = 620;
  const graphWidth = 600;
  const graphHeight = 360;

  // Transition de la courbe linéaire vers Bézier (Frames 220 à 245)
  const curveMorph = interpolate(frame, [220, 245], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Points de contrôle de Bézier (P0 et P3 fixes, P1 et P2 animés par le morphing)
  const p0 = { x: originX, y: originY };
  const p3 = { x: originX + graphWidth, y: originY - graphHeight };
  
  // En linéaire : P1 et P2 sont alignés sur la diagonale (1/3 et 2/3)
  // En Bézier (ease-in-out) : P1 tire horizontalement au bas, P2 tire horizontalement en haut
  const p1 = {
    x: originX + graphWidth * (0.33 * (1 - curveMorph) + 0.42 * curveMorph),
    y: originY - graphHeight * (0.33 * (1 - curveMorph) + 0.0 * curveMorph),
  };
  const p2 = {
    x: originX + graphWidth * (0.66 * (1 - curveMorph) + 0.58 * curveMorph),
    y: originY - graphHeight * (0.66 * (1 - curveMorph) + 1.0 * curveMorph),
  };

  // Trajectoire du cube noir (Rail horizontal de y: 740, largeur 1200px)
  const railX = 360;
  const railY = 740;
  const railLength = 1200;

  // Calcul du progrès du cube sur 40 frames
  const runFrame = frame % 40;
  const tNorm = runFrame / 40;

  // Évaluation de l'easing actuel
  let easedT = tNorm;
  if (curveMorph > 0.5) {
    // Approximation cubique de Bernstein sur l'ordonnée
    easedT = Math.pow(1 - tNorm, 3) * 0 +
      3 * Math.pow(1 - tNorm, 2) * tNorm * 0.0 +
      3 * (1 - tNorm) * Math.pow(tNorm, 2) * 1.0 +
      Math.pow(tNorm, 3) * 1.0;
  }
  const cubeX = railX + easedT * railLength;

  return (
    <svg width="1920" height="1080" style={{ position: "absolute", top: 0, left: 0 }}>
      {/* Axes orthonormés */}
      <line x1={originX} y1={originY} x2={originX + graphWidth + 40} y2={originY} stroke="#8C8E96" strokeWidth="2" />
      <line x1={originX} y1={originY} x2={originX} y2={originY - graphHeight - 40} stroke="#8C8E96" strokeWidth="2" />
      <text x={originX + graphWidth + 50} y={originY + 5} fill="#8C8E96" fontSize="16" fontFamily="monospace">time</text>
      <text x={originX - 10} y={originY - graphHeight - 50} fill="#8C8E96" fontSize="16" fontFamily="monospace" textAnchor="end">position</text>

      {/* Tangentes de Bézier si courbées */}
      {curveMorph > 0.05 && (
        <>
          <line x1={p0.x} y1={p0.y} x2={p1.x} y2={p1.y} stroke="#1E6BFF" strokeWidth="1.5" strokeDasharray="4 4" />
          <line x1={p3.x} y1={p3.y} x2={p2.x} y2={p2.y} stroke="#1E6BFF" strokeWidth="1.5" strokeDasharray="4 4" />
          <circle cx={p1.x} cy={p1.y} r="5" fill="#1E6BFF" />
          <circle cx={p2.x} cy={p2.y} r="5" fill="#1E6BFF" />
        </>
      )}

      {/* Tracé de la courbe active */}
      <path
        d={`M ${p0.x} ${p0.y} C ${p1.x} ${p1.y}, ${p2.x} ${p2.y}, ${p3.x} ${p3.y}`}
        fill="none"
        stroke={curveMorph > 0.5 ? "#1E6BFF" : "#FF334B"}
        strokeWidth="4"
      />

      {/* Rail horizontal du bas */}
      <line x1={railX} y1={railY} x2={railX + railLength} y2={railY} stroke="#D8D8DC" strokeWidth="2" />

      {/* Carré noir animé */}
      <rect
        x={cubeX - 24}
        y={railY - 24}
        width="48"
        height="48"
        fill="#111215"
      />
    </svg>
  );
};
```

---

## Blueprint 4 : Champ de Répulsion Vectoriel sur Lemniscate (Follow-Through)

### Rôle & Algorithme Physique
1. Trajectoire paramétrique en lemniscate de Gerono pour la particule guide de tête :
   $$x(t) = x_c + A \cos(t), \quad y(t) = y_c + \frac{A}{2} \sin(2t)$$
2. Chaîne de 12 particules suiveuses à inertie amortie (décalage de phase $\Delta t$).
3. Matrice de $16 \times 9$ points de grille perturbée par un champ de potentiel répulsif inversement proportionnel à la distance euclidienne :
   $$\vec{d}_i = \vec{p}_i - \vec{p}_{\text{head}}, \quad \Delta \vec{p}_i = \frac{R^2}{\|\vec{d}_i\|^2 + \epsilon} \cdot \frac{\vec{d}_i}{\|\vec{d}_i\|}$$
4. Transition de couleur locale : virage au rouge `#FF334B` pour les points dans le rayon d'influence immédiat, retour au gris sombre `#26282E` au repos.

### Composant TypeScript (HTML5 Canvas 2D)

```tsx
import React, { useRef, useEffect } from "react";
import { useCurrentFrame } from "remotion";

export const ReactiveParticleField: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const frame = useCurrentFrame();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, 1920, 1080);

    // Centre et amplitude de la lemniscate
    const cx = 960;
    const cy = 540;
    const ampX = 420;
    const ampY = 220;

    // Calcul de la position de tête
    const speed = 0.08;
    const tHead = frame * speed;
    const headX = cx + ampX * Math.cos(tHead);
    const headY = cy + ampY * Math.sin(2 * tHead) * 0.5;

    // Grille matricielle cartésienne (espacement 64px)
    const cols = 28;
    const rows = 16;
    const startX = (1920 - cols * 64) / 2;
    const startY = (1080 - rows * 64) / 2;

    const repulsionRadius = 140;

    for (let i = 0; i < cols; i++) {
      for (let j = 0; j < rows; j++) {
        const basePointX = startX + i * 64;
        const basePointY = startY + j * 64;

        const dx = basePointX - headX;
        const dy = basePointY - headY;
        const dist = Math.sqrt(dx * dx + dy * dy);

        let curX = basePointX;
        let curY = basePointY;
        let pointColor = "#26282E";
        let radius = 2.0;

        if (dist < repulsionRadius && dist > 1) {
          const force = (1 - dist / repulsionRadius) * 45;
          curX += (dx / dist) * force;
          curY += (dy / dist) * force;
          pointColor = dist < 70 ? "#FF334B" : "#1E6BFF";
          radius = 3.5;
        }

        ctx.fillStyle = pointColor;
        ctx.beginPath();
        ctx.arc(curX, curY, radius, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // Traîne de 12 particules suiveuses (Follow-through)
    for (let k = 12; k >= 1; k--) {
      const tFollow = (frame - k * 1.5) * speed;
      const fx = cx + ampX * Math.cos(tFollow);
      const fy = cy + ampY * Math.sin(2 * tFollow) * 0.5;

      ctx.fillStyle = `rgba(30, 107, 255, ${1 - k / 14})`;
      ctx.beginPath();
      ctx.arc(fx, fy, 6 * (1 - k / 18), 0, Math.PI * 2);
      ctx.fill();
    }

    // Particule de tête
    ctx.fillStyle = "#1E6BFF";
    ctx.beginPath();
    ctx.arc(headX, headY, 10, 0, Math.PI * 2);
    ctx.fill();

  }, [frame]);

  return <canvas ref={canvasRef} width="1920" height="1080" style={{ position: "absolute", top: 0, left: 0 }} />;
};
```

---

## Blueprint 5 : Cadran Radial d'Anticipation & Onde de Choc Concentrique

### Rôle & Séquençage
1. Tracé circulaire trigonométrique avec anneau de ticks techniques de 0 à 100%.
2. Compteur monospace défilant avec accélération exponentielle.
3. Pause cinétique stricte de 14 frames à 100% (Hang time).
4. Détonation en onde de choc circulaire (Iris Wipe de transition vers le fond clair).

### Composant TypeScript (Remotion / SVG)

```tsx
import React from "react";
import { useCurrentFrame, interpolate } from "remotion";

export const AnticipationRadialDial: React.FC = () => {
  const frame = useCurrentFrame();

  // Frames relatives au chapitre Anticipation (F336 à F405)
  // Montée : 0 à 38 (F336 - F374)
  // Hang Time figé à 100% : 38 à 52 (F374 - F388)
  // Explosion : 52 à 65 (F388 - F401)

  const radius = 180;
  const circumference = 2 * Math.PI * radius;

  // Calcul de la progression (0 à 100%)
  const rawProgress = interpolate(frame, [0, 38], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: (t) => Math.pow(t, 2.4), // Montée accélérée
  });
  const progressPercent = Math.min(100, Math.floor(rawProgress));

  const strokeDashoffset = circumference - (circumference * progressPercent) / 100;

  // Onde de choc d'explosion (F52+)
  const shockwaveRadius = interpolate(frame, [52, 64], [0, 2400], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: (t) => 1 - Math.pow(1 - t, 4), // Décélération explosive
  });

  return (
    <svg width="1920" height="1080" style={{ position: "absolute", top: 0, left: 0 }}>
      <g transform="translate(960, 540)">
        {/* Anneau de 60 graduations (ticks) */}
        {Array.from({ length: 60 }).map((_, i) => {
          const angle = (i * 360) / 60;
          const isMajor = i % 5 === 0;
          return (
            <line
              key={i}
              x1="0"
              y1={isMajor ? -210 : -205}
              x2="0"
              y2="-198"
              stroke={isMajor ? "#FFFFFF" : "#6E7079"}
              strokeWidth={isMajor ? "2" : "1"}
              transform={`rotate(${angle})`}
            />
          );
        })}

        {/* Cercle de fond inactif */}
        <circle cx="0" cy="0" r={radius} fill="none" stroke="rgba(255, 255, 255, 0.15)" strokeWidth="4" />

        {/* Arc de progression actif blanc */}
        <circle
          cx="0"
          cy="0"
          r={radius}
          fill="none"
          stroke="#FFFFFF"
          strokeWidth="6"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          transform="rotate(-90)"
        />

        {/* Compteur numérique central */}
        <text
          x="0"
          y="18"
          fill="#FFFFFF"
          fontSize="56"
          fontFamily="'JetBrains Mono', monospace"
          fontWeight="700"
          textAnchor="middle"
        >
          {`${progressPercent}%`}
        </text>

        {/* Onde de choc d'explosion finale (Iris Wipe blanc) */}
        {shockwaveRadius > 0 && (
          <circle cx="0" cy="0" r={shockwaveRadius} fill="#F2F2F4" opacity={1} />
        )}
      </g>
    </svg>
  );
};
```

---

## Blueprint 6 : Système de HUD Universel (Timecode & Timeline Scrubber)

### Rôle & Spécifications
Composant permanent superposé à l'ensemble du film (Z-index maximal) :
1. Timecode frame-accurate affiché au format `00:00:SS:FF` en haut à droite.
2. Scrubber de timeline dynamique en bas d'écran avec rail continu, 5 repères en losange aux frontières de sections, tête de lecture triangulaire mobile et label cursif du chapitre actif.

### Composant TypeScript (Remotion / SVG)

```tsx
import React from "react";
import { useCurrentFrame } from "remotion";

export const UniversalHUDOverlay: React.FC<{ isDarkBg?: boolean }> = ({ isDarkBg = false }) => {
  const frame = useCurrentFrame();

  // 1. Calcul du Timecode exact (Base 30 fps)
  const totalSeconds = Math.floor(frame / 30);
  const framePart = frame % 30;
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  const pad = (n: number) => n.toString().padStart(2, "0");
  const timecodeString = `00:${pad(minutes)}:${pad(seconds)}:${pad(framePart)}`;

  // 2. Calcul du Scrubber (452 frames totales)
  const totalFrames = 452;
  const progressRatio = Math.min(1, frame / totalFrames);
  const railStartX = 80;
  const railEndX = 1840;
  const railLength = railEndX - railStartX;
  const needleX = railStartX + progressRatio * railLength;
  const needleY = 1010;

  // Chapitres et labels
  const chapters = [
    { start: 0, label: "spacing" },
    { start: 56, label: "type" },
    { start: 168, label: "easing" },
    { start: 280, label: "follow-through" },
    { start: 336, label: "anticipation" },
    { start: 392, label: "hello" },
  ];

  const currentChapter = [...chapters].reverse().find((c) => frame >= c.start)?.label || "spacing";

  const textColor = isDarkBg ? "#FFFFFF" : "#111215";
  const trackColor = isDarkBg ? "rgba(255, 255, 255, 0.15)" : "rgba(0, 0, 0, 0.08)";
  const diamondColor = isDarkBg ? "#8C8E96" : "#6E7079";

  return (
    <svg width="1920" height="1080" style={{ position: "absolute", top: 0, left: 0, pointerEvents: "none" }}>
      {/* Timecode en haut à droite */}
      <text
        x="1856"
        y="58"
        fill={textColor}
        fontSize="20"
        fontFamily="'JetBrains Mono', monospace"
        fontWeight="500"
        textAnchor="end"
        letterSpacing="0.05em"
      >
        {timecodeString}
      </text>

      {/* Rail de timeline inférieur */}
      <line x1={railStartX} y1={needleY} x2={railEndX} y2={needleY} stroke={trackColor} strokeWidth="2" />

      {/* Losanges de repères de chapitres */}
      {chapters.map((chap, idx) => {
        const markerX = railStartX + (chap.start / totalFrames) * railLength;
        return (
          <polygon
            key={idx}
            points={`${markerX},${needleY - 5} ${markerX + 5},${needleY} ${markerX},${needleY + 5} ${markerX - 5},${needleY}`}
            fill={diamondColor}
          />
        );
      })}

      {/* Tête de lecture (Needle) */}
      <polygon
        points={`${needleX - 6},${needleY - 14} ${needleX + 6},${needleY - 14} ${needleX},${needleY - 4}`}
        fill="#1E6BFF"
      />
      <line x1={needleX} y1={needleY - 4} x2={needleX} y2={needleY + 8} stroke="#1E6BFF" strokeWidth="2" />

      {/* Étiquette cursive du chapitre actif au-dessus de l'aiguille */}
      <text
        x={needleX}
        y={needleY - 22}
        fill="#1E6BFF"
        fontSize="17"
        fontFamily="'Caveat', cursive, sans-serif"
        fontWeight="600"
        textAnchor="middle"
      >
        {currentChapter}
      </text>
    </svg>
  );
};
```

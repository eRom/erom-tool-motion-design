# 03. Blueprints de Fabrication & Recettes de Code

Ce document fournit aux agents développeurs (Remotion, WebGL/Three.js, Canvas 2D, SVG/GSAP) les algorithmes, formules mathématiques et architectures logicielles nécessaires pour ré-implémenter les sept briques visuelles maîtresses de la vidéo MIRR.

---

## 1. Moteur 1 : The Focus Pointer & Kinetic Physics Engine

Utilisé dans : L'introduction (00:00 - 00:04), la navigation entre les 4 cadrans de friction et la convergence centrale.

### Principe Mathématique & Physique
1. **Interpolation de Trajectoire par Ressort Dégénéré (Damped Spring)** : Les coordonnées cibles `(X_target, Y_target)` changent brusquement à chaque étape. La position courante `P(t)` est régie par l'équation différentielle :
   $$\ddot{P} + 2\zeta\omega_0 \dot{P} + \omega_0^2 (P - P_{target}) = 0$$
   avec un facteur d'amortissement $\zeta = 0.85$ (léger dépassement de 8%) et une pulsation $\omega_0 = 18\text{ rad/s}$.
2. **Squash & Stretch Directionnel** : Lors du déplacement, la sphère se déforme en ellipse orientée selon le vecteur vitesse $\vec{v} = (\dot{x}, \dot{y})$ :
   - Angle de rotation : $\theta = \text{atan2}(v_y, v_x)$
   - Élongation dans l'axe du mouvement : $S_\parallel = 1 + \min\left(0.65, \frac{\|\vec{v}\|}{v_{\max}} \times 0.5\right)$
   - Contraction perpendiculaire : $S_\perp = \frac{1}{\sqrt{S_\parallel}}$ (conservation apparente du volume).

### Implémentation de Référence (TypeScript / Remotion + SVG)

```typescript
import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface Point {
  x: number;
  y: number;
}

interface PointerKeyframe {
  frame: number;
  target: Point;
}

const WAYPOINTS: PointerKeyframe[] = [
  { frame: 0, target: { x: 118, y: 169 } },    // Q1: Faktury
  { frame: 45, target: { x: 626, y: 242 } },   // Q2: Zapytania
  { frame: 100, target: { x: 146, y: 470 } },  // Q3: Wyceny
  { frame: 155, target: { x: 659, y: 537 } },  // Q4: Godziny
  { frame: 210, target: { x: 640, y: 360 } },  // Centre convergence
];

export const KineticFocusPointer: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Recherche du segment actif
  let startIdx = 0;
  for (let i = 0; i < WAYPOINTS.length - 1; i++) {
    if (frame >= WAYPOINTS[i].frame) {
      startIdx = i;
    }
  }

  const p0 = WAYPOINTS[startIdx];
  const p1 = WAYPOINTS[Math.min(startIdx + 1, WAYPOINTS.length - 1)];

  const springProgress = spring({
    frame: frame - p0.frame,
    fps,
    config: { damping: 14, stiffness: 160, mass: 0.9 },
  });

  const curX = interpolate(springProgress, [0, 1], [p0.target.x, p1.target.x]);
  const curY = interpolate(springProgress, [0, 1], [p0.target.y, p1.target.y]);

  // Vitesse instantanée (différence finie sur 1 frame)
  const dtProgress = spring({
    frame: Math.max(0, frame - p0.frame - 1),
    fps,
    config: { damping: 14, stiffness: 160, mass: 0.9 },
  });
  const prevX = interpolate(dtProgress, [0, 1], [p0.target.x, p1.target.x]);
  const prevY = interpolate(dtProgress, [0, 1], [p0.target.y, p1.target.y]);

  const vx = curX - prevX;
  const vy = curY - prevY;
  const speed = Math.hypot(vx, vy);
  const angleRad = Math.atan2(vy, vx);

  const stretch = Math.min(1.7, 1 + speed * 0.04);
  const squash = 1 / Math.sqrt(stretch);

  // Rayon de base avec expansion au centre à partir de la frame 210
  const baseRadius = interpolate(frame, [210, 240], [10, 24], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <g transform={`translate(${curX}, ${curY}) rotate(${(angleRad * 180) / Math.PI}) scale(${stretch}, ${squash})`}>
      {/* Halo de bloom additif */}
      <circle r={baseRadius * 1.8} fill="#6FD7CB" opacity={0.25} filter="blur(6px)" />
      {/* Cœur néon */}
      <circle r={baseRadius} fill="#6FD7CB" />
    </g>
  );
};
```

---

## 2. Moteur 2 : Shockwave Circle Burst & 3D Layer Zoom Transition

Utilisé dans : La transition d'ouverture du tableau de bord (00:05.93, frame 350-365).

### Principe Technique
1. **Onde de Choc Circulaire (Shockwave)** : Un anneau SVG dont le rayon croît de $0$ à $1200\text{px}$ en 12 frames selon une courbe exponentielle out (`easeOutExpo`), tandis que l'épaisseur du trait (`stroke-width`) décroît de $8\text{px}$ à $0\text{px}$ et l'opacité s'éteint.
2. **Particules d'Étincelles Radiales** : 24 particules projetées uniformément sur $360^\circ$ depuis le point d'impact central, avec une traînée de vitesse (`radial streaks`).
3. **Décompression d'Échelle 3D** : Le groupe d'éléments du tableau de bord subit simultanément une expansion d'échelle (`scale: 0.15 -> 1.0`) et un recul en profondeur (`translateZ: -800px -> 0px`).

### Implémentation de Référence (Canvas 2D / React)

```typescript
export class ShockwaveBurst {
  private particles: Array<{ angle: number; speed: number; dist: number; len: number }> = [];

  constructor(particleCount = 28) {
    for (let i = 0; i < particleCount; i++) {
      this.particles.push({
        angle: (i / particleCount) * Math.PI * 2 + (Math.random() - 0.5) * 0.1,
        speed: Math.random() * 18 + 12,
        dist: 0,
        len: Math.random() * 14 + 8,
      });
    }
  }

  render(ctx: CanvasRenderingContext2D, progress: number, cx: number, cy: number) {
    // progress in [0, 1] over 14 frames
    const ringRadius = Math.pow(progress, 0.35) * 650;
    const ringOpacity = Math.max(0, 1 - progress);
    const ringStroke = (1 - progress) * 6;

    ctx.save();
    ctx.translate(cx, cy);

    // 1. Anneau d'onde de choc
    ctx.beginPath();
    ctx.arc(0, 0, ringRadius, 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(255, 255, 255, ${ringOpacity * 0.8})`;
    ctx.lineWidth = ringStroke;
    ctx.stroke();

    // 2. Particules radiales cyan
    ctx.strokeStyle = '#6FD7CB';
    ctx.lineWidth = 2;
    ctx.globalCompositeOperation = 'lighter';

    for (const p of this.particles) {
      const currentDist = p.speed * (1 - Math.exp(-progress * 5)) * 25;
      const x1 = Math.cos(p.angle) * currentDist;
      const y1 = Math.sin(p.angle) * currentDist;
      const x2 = Math.cos(p.angle) * (currentDist + p.len * (1 - progress));
      const y2 = Math.sin(p.angle) * (currentDist + p.len * (1 - progress));

      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
    }

    ctx.restore();
  }
}
```

---

## 3. Moteur 3 : 3D Perspective Card Engine with Dynamic Glow & Status Borders

Utilisé dans : Le Dashboard `PULPIT` (00:06), le pipeline Kanban `ZAPYTANIA` (00:10) et la boîte de dialogue Telegram (00:28).

### Principe Technique
- Chaque conteneur de données est rendu comme une surface plane surélevée dans un espace 3D à perspective centrale.
- La bordure d'accentuation (rouge alerte `#EF4141`, ambre `#C6AE3C`, vert `#4B9370`, cyan `#6FD7CB`) est projetée sous forme de liseré gauche (`border-left: 3px solid`) couplé à une ombre interne luminescente (`box-shadow: inset 6px 0 16px -4px <color>`).
- L'élévation d'une carte (ex: prospect `Jakub Kowalski`) applique une translation négative en Z (`translateZ(30px)`) et une multiplication de l'ombre portée portée sur les calques sous-jacents.

### Implémentation de Référence (React / Remotion Style Module)

```typescript
import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface CardProps {
  title: string;
  metric: string;
  subtitle?: string;
  accentColor?: string;
  isActive?: boolean;
  delayFrames?: number;
}

export const IsometricB2BCard: React.FC<CardProps> = ({
  title,
  metric,
  subtitle,
  accentColor = 'rgba(255,255,255,0.1)',
  isActive = false,
  delayFrames = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame: frame - delayFrames,
    fps,
    config: { damping: 16, stiffness: 140, mass: 1 },
  });

  const translateY = interpolate(entrance, [0, 1], [40, 0]);
  const opacity = interpolate(entrance, [0, 1], [0, 1]);

  return (
    <div
      style={{
        width: 380,
        backgroundColor: '#111111',
        borderRadius: 8,
        border: '1px solid rgba(255, 255, 255, 0.07)',
        borderLeft: `3.5px solid ${accentColor}`,
        boxShadow: isActive
          ? `0 20px 40px rgba(0,0,0,0.8), 0 0 24px ${accentColor}40`
          : '0 8px 24px rgba(0,0,0,0.5)',
        transform: `translateY(${translateY}px) ${isActive ? 'scale(1.04) translateZ(25px)' : 'translateZ(0)'}`,
        opacity,
        padding: '20px 24px',
        display: 'flex',
        flexDirection: 'column',
        gap: 8,
        color: '#FFFFFF',
        fontFamily: "'Inter', sans-serif",
      }}
    >
      <div style={{ fontSize: 11, letterSpacing: '0.08em', color: '#8F94A0', textTransform: 'uppercase', fontFamily: "'JetBrains Mono', monospace" }}>
        {title}
      </div>
      <div style={{ fontSize: 32, fontWeight: 700, letterSpacing: '-0.02em', fontFamily: "'JetBrains Mono', monospace" }}>
        {metric}
      </div>
      {subtitle && (
        <div style={{ fontSize: 12, color: '#6A6E78', marginTop: 4 }}>
          {subtitle}
        </div>
      )}
    </div>
  );
};
```

---

## 4. Moteur 4 : Odometer / Rolling Number Counter with Tabular Zero Dotted Formatting

Utilisé dans : Le calcul du devis net (00:15), le chronomètre des ouvriers (00:33) et les flash-cuts (00:38).

### Principe Technique
1. **Tambours Chiffrés Indépendants** : Chaque position décimale dispose d'une colonne verticale comportant les chiffres `0` à `9` en défilement vertical infini (`translateY(-digit * lineHeight)`).
2. **Motion Blur Directionnel par Vélocité** : Lorsque la vitesse de rotation dépasse 15 chiffres/seconde, un filtre de flou vertical `blur(0px, Y px)` proportionnel à la vitesse angulaire est injecté.
3. **Formatage Monétaire Strict** : Espace insécable séparateur de milliers et virgule décimale (`104 582,45 zł`). Le glyphe zéro utilise la police *JetBrains Mono* avec son point central distinctif (`font-feature-settings: 'zero' 1`).

### Implémentation de Référence (TypeScript / React)

```typescript
import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';

interface OdometerDigitProps {
  digit: number;
  progress: number; // 0 à 1
  rotations: number;
  lineHeight: number;
}

export const OdometerColumn: React.FC<OdometerDigitProps> = ({ digit, progress, rotations, lineHeight }) => {
  // Défilement de rotations * 10 + valeur cible
  const totalSteps = rotations * 10 + digit;
  const currentStep = progress * totalSteps;
  const offset = currentStep * lineHeight;
  
  // Vitesse instantanée pour flou de mouvement
  const blurY = progress < 0.9 ? Math.min(8, (1 - progress) * 10) : 0;

  return (
    <div style={{ height: lineHeight, overflow: 'hidden', display: 'inline-block', filter: `blur(0px, ${blurY}px)` }}>
      <div style={{ transform: `translateY(-${offset % (lineHeight * 10)}px)` }}>
        {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0].map((n, idx) => (
          <div key={idx} style={{ height: lineHeight, lineHeight: `${lineHeight}px`, textAlign: 'center' }}>
            {n}
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

## 5. Moteur 5 : Document Scanning Laser Beam & OCR Shutter Viewfinder

Utilisé dans : La numérisation de facture (00:17 - 00:20, séquence 05).

### Principe Technique
1. **Rayon Laser Cyan Évanescent** : Une fine barre horizontale de $2\text{px}$ (`#6FD7CB`) couplée à un dégradé ascendant `linear-gradient(to top, rgba(111,215,203,0.35), transparent 60px)`.
2. **Balayage Temporel Synchronisé** : Progression verticale linéaire $Y(t) = \text{height} \times \frac{t - t_0}{T_{\text{scan}}}$.
3. **Coins de Visée de Caméra Téléphonique** : 4 équerres SVG `[ ]` en `#6FD7CB` entourant la zone de détection, qui se resserrent légèrement (spring damping) sur le document avant le déclenchement du flash.

### Implémentation de Référence (SVG / Remotion)

```typescript
import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';

export const OCRScanLaser: React.FC<{ width: number; height: number; startFrame: number; duration: number }> = ({
  width,
  height,
  startFrame,
  duration,
}) => {
  const frame = useCurrentFrame();
  const scanProgress = interpolate(frame, [startFrame, startFrame + duration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const scanY = scanProgress * height;

  if (frame < startFrame || frame > startFrame + duration) return null;

  return (
    <div style={{ position: 'absolute', top: 0, left: 0, width, height, overflow: 'hidden', pointerEvents: 'none' }}>
      {/* Nappe de lueur laser */}
      <div
        style={{
          position: 'absolute',
          top: scanY - 60,
          left: 0,
          width: '100%',
          height: 60,
          background: 'linear-gradient(to top, rgba(111, 215, 203, 0.4), transparent)',
        }}
      />
      {/* Filet laser net */}
      <div
        style={{
          position: 'absolute',
          top: scanY,
          left: 0,
          width: '100%',
          height: 2,
          backgroundColor: '#6FD7CB',
          boxShadow: '0 0 10px #6FD7CB, 0 0 20px #6FD7CB',
        }}
      />
    </div>
  );
};
```

---

## 6. Moteur 6 : Interactive Stopwatch Timer & Simultaneous Multi-Worker Clock

Utilisé dans : La séquence ouvriers (00:32 - 00:36, séquence 09).

### Principe Technique
1. **Course de Temps Accélérée** : Simulation d'une journée de chantier condensée en 60 frames :
   $$T(t) = T_0 + (T_{\text{final}} - T_0) \times \left(\frac{t}{T_{\text{run}}}\right)^3$$
   permettant de passer de `0:00:09` à `6:16:42` puis `8:30:00`.
2. **Mutation d'État Instantanée sur Trigger Audio** : À l'impact du coup de kick (frame 2040) :
   - Le bouton `STOP` passe de `#EF4141` à un badge statique gris `#242424` marqué `✓ 8,5 H`.
   - Les chiffres du chronomètre basculent de `#FFFFFF` au cyan éclatant `#6FD7CB` avec glow additif.
   - La jauge d'imputation financière inférieure `CZAS PRACY · BUDOWA MICHALSKI` s'anime de $0\%$ à $100\%$.

---

## 7. Moteur 7 : Orbital Particle Core & Logo Dot Snapping

Utilisé dans : La convergence finale et la révélation du logo MIRR (00:40 - 00:48, séquences 12 et 13).

### Principe Mathématique
1. **Mouvement Orbital en 3D Projetée** : 6 satellites paramétrés par un angle orbital $\phi_k(t) = \omega t + \frac{2\pi k}{6}$. Les coordonnées dans le plan écran sont données par :
   $$X_k(t) = C_x + R_x \cos\phi_k(t)$$
   $$Y_k(t) = C_y + R_y \sin\phi_k(t) \cos\alpha$$
   avec un rayon majeur $R_x = 240\text{px}$, un rayon mineur $R_y = 110\text{px}$ et une inclinaison de plan orbital $\alpha = 35^\circ$.
2. **Facteur de Profondeur Z & Échelle** : Le calque $k$ passe derrière la sphère centrale lorsque $\sin\phi_k(t) < 0$ :
   $$\text{scale}_k = 0.8 + 0.3 \times \frac{1 + \sin\phi_k(t)}{2}$$
   $$\text{opacity}_k = 0.4 + 0.6 \times \frac{1 + \sin\phi_k(t)}{2}$$
3. **Effondrement Gravitationnel & Snapping vers le Logo** : À $t = 43.35\text{s}$, le rayon $R(t) \to 0$ en spirale logarithmique $R(t) = R_0 e^{-\lambda t}$ tandis que le centre $C$ converge vers la position du point du logo `MIRR.` en `(x: 915, y: 350)`.

### Implémentation de Référence (Canvas 2D / WebGL)

```typescript
export interface SatelliteBadge {
  id: string;
  iconPath: string;
  phaseOffset: number;
}

export function computeOrbitalPosition(
  timeSeconds: number,
  phaseOffset: number,
  centerX: number,
  centerY: number,
  radiusX = 220,
  radiusY = 90,
  tiltAngleRad = (25 * Math.PI) / 180
) {
  const angularSpeed = 1.2; // rad/s
  const theta = angularSpeed * timeSeconds + phaseOffset;

  const rawX = radiusX * Math.cos(theta);
  const rawY = radiusY * Math.sin(theta);

  // Rotation selon l'inclinaison du plan
  const projX = centerX + rawX;
  const projY = centerY + rawY * Math.cos(tiltAngleRad);
  const depthZ = rawY * Math.sin(tiltAngleRad); // pour z-sorting

  const scale = 0.75 + 0.35 * ((depthZ + radiusY) / (2 * radiusY));
  const opacity = 0.5 + 0.5 * ((depthZ + radiusY) / (2 * radiusY));

  return { x: projX, y: projY, z: depthZ, scale, opacity };
}
```

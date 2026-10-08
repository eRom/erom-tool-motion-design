# 03. Blueprints de Fabrication & Recettes de Code

Ce document fournit les spécifications algorithmiques et le code source complet des six effets majeurs de la vidéo `2Dz1vf5VhJw5zC4D.mp4`.
Tous les composants sont rédigés en TypeScript pour Remotion, Three.js (`@react-three/fiber`) ou Canvas 2D / SVG, prêts à être instanciés directement dans un pipeline de rendu à 60 fps.

---

## Blueprint 01 : Le HUD Télémétrique Frame-Accurate

### Rôle & Principe Géométrique
Un affichage tête haute (HUD) permanent servant d'armature visuelle tout au long de la vidéo :
- **Timecode absolu** formaté en `00:00:SS:FF` sans dérive.
- **Métronome 4 temps** à base de 4 glyphes carrés (`■□□□`, `□■□□`, `□□■□`, `□□□■`) qui change exactement toutes les 25 frames (tempo 144 BPM).
- **Désembrouillage textuel (Text Scramble)** générant des caractères aléatoires avant de se figer sur le libellé de scène cible en 18 frames.
- **Repères de visée Viewfinder** aux quatre angles de l'écran.

### Code Source TypeScript (Remotion)

```tsx
import React, { useMemo } from 'react';
import { useCurrentFrame } from 'remotion';

interface TelemetricHUDProps {
  sceneIndex: number; // Ex: 1 pour SCENE 01
  totalScenes?: number; // 7 par défaut
  categoryLabel: string; // Ex: "IDENTITY / TYPE"
  textColor?: string;
  borderColor?: string;
}

const GLYPH_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_#/*+';

export const TelemetricHUD: React.FC<TelemetricHUDProps> = ({
  sceneIndex,
  totalScenes = 7,
  categoryLabel,
  textColor = '#FFFFFF',
  borderColor = 'rgba(255, 255, 255, 0.4)',
}) => {
  const frame = useCurrentFrame();
  const fps = 60;

  // 1. Calcul du Timecode frame-accurate 00:00:SS:FF
  const timecode = useMemo(() => {
    const totalSeconds = Math.floor(frame / fps);
    const subFrames = frame % fps;
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;

    const pad = (n: number) => n.toString().padStart(2, '0');
    return `${pad(minutes)}:${pad(seconds)}:${pad(subFrames)}`;
  }, [frame, fps]);

  // 2. Métronome 4 temps (1 temps = 25 frames, mesure = 100 frames)
  const currentBeat = Math.floor((frame % 100) / 25); // 0, 1, 2, ou 3
  const metronomeSymbols = useMemo(() => {
    return [0, 1, 2, 3].map((b) => (b === currentBeat ? '■' : '□')).join(' ');
  }, [currentBeat]);

  // 3. Désembrouillage de texte (Text Scramble) sur les 18 premières frames de la mesure
  const localMeasureFrame = frame % 100;
  const scrambledCategory = useMemo(() => {
    const revealProgress = Math.min(1, localMeasureFrame / 18);
    const targetLength = categoryLabel.length;
    const revealedCount = Math.floor(revealProgress * targetLength);

    let result = '';
    for (let i = 0; i < targetLength; i++) {
      if (categoryLabel[i] === ' ' || categoryLabel[i] === '/') {
        result += categoryLabel[i];
      } else if (i < revealedCount) {
        result += categoryLabel[i];
      } else {
        const randIndex = (frame * 17 + i * 31) % GLYPH_CHARS.length;
        result += GLYPH_CHARS[randIndex];
      }
    }
    return result;
  }, [categoryLabel, localMeasureFrame, frame]);

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        pointerEvents: 'none',
        padding: '48px 64px',
        boxSizing: 'border-box',
        fontFamily: 'monospace',
        fontSize: '12px',
        color: textColor,
        letterSpacing: '0.08em',
        zIndex: 90,
      }}
    >
      {/* Repères Viewfinder aux 4 angles */}
      <svg
        style={{
          position: 'absolute',
          inset: '32px 48px',
          width: 'calc(100% - 96px)',
          height: 'calc(100% - 64px)',
          pointerEvents: 'none',
        }}
      >
        <path d="M 0,16 L 0,0 L 16,0" stroke={borderColor} strokeWidth="1.5" fill="none" />
        <path d="M calc(100% - 16px),0 L 100%,0 L 100%,16" stroke={borderColor} strokeWidth="1.5" fill="none" />
        <path d="M 0,calc(100% - 16px) L 0,100% L 16,100%" stroke={borderColor} strokeWidth="1.5" fill="none" />
        <path d="M calc(100% - 16px),100% L 100%,100% L 100%,calc(100% - 16px)" stroke={borderColor} strokeWidth="1.5" fill="none" />
      </svg>

      {/* Coin Supérieur Droit : Scène courante */}
      <div style={{ position: 'absolute', top: 48, right: 64 }}>
        SCENE {sceneIndex.toString().padStart(2, '0')} / {totalScenes.toString().padStart(2, '0')}
      </div>

      {/* Coin Inférieur Gauche : Catégorie désembrouillée */}
      <div style={{ position: 'absolute', bottom: 48, left: 64 }}>
        {scrambledCategory}
      </div>

      {/* Coin Inférieur Droit : Métronome & Timecode */}
      <div
        style={{
          position: 'absolute',
          bottom: 48,
          right: 64,
          display: 'flex',
          gap: '20px',
          alignItems: 'center',
        }}
      >
        <span style={{ letterSpacing: '0.2em' }}>{metronomeSymbols}</span>
        <span style={{ fontVariantNumeric: 'tabular-nums' }}>{timecode}</span>
      </div>
    </div>
  );
};
```

---

## Blueprint 02 : L'Onde Harmonique Stationnaire & Fente Lumineuse (Bar 1)

### Rôle & Principe Physique
Simulation d'une corde vibrante tenue à ses deux extrémités ($x=0$ et $x=L$), oscillant selon la superposition de ses trois premiers modes propres harmoniques :
$$y(x, t) = \sum_{k=1}^3 A_k \sin\left(\frac{k \pi x}{L}\right) \cos(\omega_k t)$$
À la frame 85, l'onde s'élargit verticalement par un facteur d'échelle exponentiel pour créer une bande lumineuse pleine qui assure la transition vers la scène suivante.

### Code Source TypeScript (SVG Canvas / Remotion)

```tsx
import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';

export const HarmonicWaveIntro: React.FC = () => {
  const frame = useCurrentFrame(); // Durée : frames 0 à 99
  const width = 1920;
  const height = 1080;
  const centerY = height / 2;

  // Paramètres physiques de la corde
  const t = frame / 60; // Temps en secondes
  const omega1 = 2 * Math.PI * 2.4; // Pulsation fondamentale (2.4 Hz)

  // Facteur d'amplitude globale : montée en puissance jusqu'à la frame 80
  const baseAmplitude = interpolate(frame, [0, 20, 80], [0, 24, 28], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Facteur d'ouverture en fente lumineuse : frames 85 à 99
  const lightBandHeight = interpolate(frame, [85, 99], [2, height], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const isSaturating = frame >= 85;

  // Génération du tracé SVG à 120 points d'échantillonnage
  const pointsCount = 120;
  const pathD = React.useMemo(() => {
    let d = '';
    for (let i = 0; i <= pointsCount; i++) {
      const x = (i / pointsCount) * width;
      const normalizedX = i / pointsCount;

      // Superposition de 3 harmoniques
      const h1 = baseAmplitude * Math.sin(1 * Math.PI * normalizedX) * Math.cos(omega1 * t);
      const h2 = (baseAmplitude * 0.4) * Math.sin(2 * Math.PI * normalizedX) * Math.cos(2 * omega1 * t + 0.3);
      const h3 = (baseAmplitude * 0.15) * Math.sin(3 * Math.PI * normalizedX) * Math.cos(3 * omega1 * t + 0.7);

      const y = centerY + (h1 + h2 + h3);
      d += i === 0 ? `M ${x.toFixed(1)} ${y.toFixed(1)}` : ` L ${x.toFixed(1)} ${y.toFixed(1)}`;
    }
    return d;
  }, [baseAmplitude, omega1, t, width, centerY]);

  // Position Y du point conducteur central corail (x = 960)
  const dotY = centerY + baseAmplitude * Math.cos(omega1 * t);

  return (
    <div style={{ position: 'relative', width, height, backgroundColor: '#05080D' }}>
      <svg width={width} height={height} style={{ position: 'absolute', inset: 0 }}>
        {/* Tracé de l'onde sinusoïdale */}
        <path d={pathD} stroke="#FFFFFF" strokeWidth="2" fill="none" opacity={isSaturating ? 0.3 : 1} />

        {/* Fente lumineuse s'élargissant entre frames 85 et 99 */}
        {isSaturating && (
          <rect
            x={0}
            y={centerY - lightBandHeight / 2}
            width={width}
            height={lightBandHeight}
            fill="#FFFFFF"
            opacity={interpolate(frame, [85, 99], [0.1, 1])}
          />
        )}

        {/* Puce conductrice corail au centre */}
        {!isSaturating && (
          <circle cx={width / 2} cy={dotY} r={6} fill="#FA4E20" />
        )}
      </svg>
    </div>
  );
};
```

---

## Blueprint 03 : Nappe Isométrique 3D & Sphère Miroir (Bar 3, Scene 02)

### Rôle & Principe Géométrique
Un espace 3D constitué d'une grille régulière de $20 \times 20$ parallélépipèdes arrondis (400 prismes instanciés via `THREE.InstancedMesh`).
Chaque prisme est animé verticalement selon une fonction de vague circulaire progressive :
$$y_{i,j}(t) = A \cdot \sin(\omega t - k \cdot r_{i,j}), \quad \text{avec } r_{i,j} = \sqrt{(x_i - x_c)^2 + (z_j - z_c)^2}$$
La couleur de chaque prisme est calculée en fonction de son élévation par interpolation linéaire entre `#6C3BAA` (creux) et `#FF8A65` (crêtes). Au centre flotte une sphère spéculaire réfléchissante ceinte de deux anneaux orbitaux inclinés.

### Code Source Three.js (React Three Fiber / Remotion Three)

```tsx
import React, { useRef, useMemo, useEffect } from 'react';
import * as THREE from 'three';
import { useCurrentFrame } from 'remotion';

const GRID_SIZE = 20;
const TOTAL_INSTANCES = GRID_SIZE * GRID_SIZE;
const SPACING = 1.2;

const COLOR_LOW = new THREE.Color('#6C3BAA');  // Violet profond
const COLOR_HIGH = new THREE.Color('#FF8A65'); // Saumon vif

export const WaveGrid3D: React.FC = () => {
  const frame = useCurrentFrame(); // frames 200 à 299 (durée relative : 0 à 99)
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const ring1Ref = useRef<THREE.Group>(null);
  const ring2Ref = useRef<THREE.Group>(null);

  const dummy = useMemo(() => new THREE.Object3D(), []);
  const tempColor = useMemo(() => new THREE.Color(), []);

  // Calcul frame-par-frame des transformations matricielles
  useEffect(() => {
    if (!meshRef.current) return;

    const t = (frame % 100) / 60;
    const omega = 2 * Math.PI * 1.5; // Fréquence d'onde
    const k = 0.6; // Nombre d'onde spatial
    const amplitude = 1.4;

    let idx = 0;
    for (let i = 0; i < GRID_SIZE; i++) {
      for (let j = 0; j < GRID_SIZE; j++) {
        const x = (i - (GRID_SIZE - 1) / 2) * SPACING;
        const z = (j - (GRID_SIZE - 1) / 2) * SPACING;
        const distance = Math.sqrt(x * x + z * z);

        // Élévation ondulatoire
        const y = amplitude * Math.sin(omega * t - k * distance);

        dummy.position.set(x, y, z);
        dummy.scale.set(0.85, 0.85, 0.85);
        dummy.updateMatrix();

        meshRef.current.setMatrixAt(idx, dummy.matrix);

        // Interpolation chromatique
        const normalizedY = (y + amplitude) / (2 * amplitude);
        tempColor.copy(COLOR_LOW).lerp(COLOR_HIGH, normalizedY);
        meshRef.current.setColorAt(idx, tempColor);

        idx++;
      }
    }

    meshRef.current.instanceMatrix.needsUpdate = true;
    if (meshRef.current.instanceColor) {
      meshRef.current.instanceColor.needsUpdate = true;
    }
  }, [frame, dummy, tempColor]);

  // Rotation des anneaux orbitaux
  const tRing = frame / 60;

  return (
    <group rotation={[Math.PI / 4, Math.PI / 6 + (frame / 60) * 0.1, 0]}>
      {/* 400 Prismes instanciés */}
      <instancedMesh
        ref={meshRef}
        args={[undefined, undefined, TOTAL_INSTANCES]}
      >
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial roughness={0.3} metalness={0.2} />
      </instancedMesh>

      {/* Sphère chromée spéculaire centrale */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[1.6, 64, 64]} />
        <meshPhysicalMaterial
          color="#FFFFFF"
          roughness={0.05}
          metalness={0.95}
          clearcoat={1.0}
        />
      </mesh>

      {/* Anneaux orbitaux filaires inclinés */}
      <group rotation={[0.6, 0.2, tRing * 1.2]}>
        <mesh>
          <torusGeometry args={[2.8, 0.04, 16, 100]} />
          <meshBasicMaterial color="#FA4E20" />
        </mesh>
      </group>
      <group rotation={[-0.8, -0.4, -tRing * 0.9]}>
        <mesh>
          <torusGeometry args={[3.4, 0.03, 16, 100]} />
          <meshBasicMaterial color="#FFFFFF" />
        </mesh>
      </group>
    </group>
  );
};
```

---

## Blueprint 04 : Moteur Kinetic Typography en 4 Beats (Bar 4, Scene 03)

### Rôle & Principe Géométrique
Un séquenceur typographique découpé en quatre tranches temporelles exactes de 25 frames (un beat musical par état) :
1. **Beat 1** : Masque d'échelle brutale sur `EVERY`.
2. **Beat 2** : Défilement parallaxe de contours filaires pour `SINGLE`.
3. **Beat 3** : Tranchage horizontal du mot `FRAME` en 5 bandes latérales oscillantes.
4. **Beat 4** : Tracé d'arc vectoriel SVG de rature sur la cursive `on purpose.`.

### Code Source TypeScript (Remotion)

```tsx
import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';

export const KineticTypographyScene: React.FC = () => {
  const frame = useCurrentFrame(); // Mesure 4 : frames 300 à 399 (0 à 99 relatives)
  const beatIndex = Math.floor(frame / 25); // 0, 1, 2, ou 3
  const beatFrame = frame % 25; // 0 à 24

  // BEAT 1 : "EVERY" (Fond crème, mot noir)
  if (beatIndex === 0) {
    const scale = interpolate(beatFrame, [0, 4], [0.92, 1.0], { extrapolateRight: 'clamp' });
    return (
      <div style={{ width: 1920, height: 1080, backgroundColor: '#F1F1E7', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <h1 style={{ fontSize: '240px', fontWeight: 900, color: '#060910', transform: `scale(${scale})`, letterSpacing: '-0.06em', margin: 0 }}>
          EVERY
        </h1>
      </div>
    );
  }

  // BEAT 2 : "SINGLE" (Fond noir, mot corail + 4 rangées filaires défilantes)
  if (beatIndex === 1) {
    const shiftX = beatFrame * 12; // Déplacement continu à 12px/frame
    return (
      <div style={{ width: 1920, height: 1080, backgroundColor: '#05080D', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', overflow: 'hidden' }}>
        {/* Rangée filaire haute 1 (vers la gauche) */}
        <div style={{ fontSize: '130px', fontWeight: 900, WebkitTextStroke: '2px rgba(255,255,255,0.3)', color: 'transparent', transform: `translateX(-${shiftX}px)`, whiteSpace: 'nowrap' }}>
          SINGLE SINGLE SINGLE SINGLE SINGLE
        </div>
        {/* Mot central plein corail */}
        <div style={{ fontSize: '220px', fontWeight: 900, color: '#FA4E20', letterSpacing: '-0.05em', margin: '-20px 0' }}>
          SINGLE
        </div>
        {/* Rangée filaire basse 2 (vers la droite) */}
        <div style={{ fontSize: '130px', fontWeight: 900, WebkitTextStroke: '2px rgba(255,255,255,0.3)', color: 'transparent', transform: `translateX(${shiftX}px)`, whiteSpace: 'nowrap' }}>
          SINGLE SINGLE SINGLE SINGLE SINGLE
        </div>
      </div>
    );
  }

  // BEAT 3 : "FRAME" (Fond bleu, mot blanc découpé en 5 bandes)
  if (beatIndex === 2) {
    const slices = [-14, 18, -10, 16, -12]; // Décalages horizontaux par bande
    return (
      <div style={{ width: 1920, height: 1080, backgroundColor: '#314CFF', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ border: '2px solid #FFFFFF', padding: '16px 48px', position: 'relative' }}>
          <div style={{ position: 'relative', height: '180px', width: '800px', overflow: 'hidden' }}>
            {[0, 1, 2, 3, 4].map((i) => {
              const sliceHeight = 180 / 5;
              const offsetY = i * sliceHeight;
              const offsetX = (beatFrame % 4 < 2) ? slices[i] : -slices[i] * 0.5;
              return (
                <div
                  key={i}
                  style={{
                    position: 'absolute',
                    top: offsetY,
                    left: 0,
                    width: '100%',
                    height: sliceHeight,
                    overflow: 'hidden',
                  }}
                >
                  <div
                    style={{
                      position: 'absolute',
                      top: -offsetY,
                      left: offsetX,
                      width: '100%',
                      textAlign: 'center',
                      fontSize: '180px',
                      fontWeight: 900,
                      color: '#FFFFFF',
                      letterSpacing: '-0.04em',
                      lineHeight: '180px',
                    }}
                  >
                    FRAME
                  </div>
                </div>
              );
            })}
          </div>
          <div style={{ position: 'absolute', bottom: -28, right: 0, fontSize: '12px', color: '#FFFFFF', fontFamily: 'monospace' }}>
            1920 x 1080 • 60 FPS
          </div>
        </div>
      </div>
    );
  }

  // BEAT 4 : "on purpose." (Fond corail, cursive noire avec rature SVG)
  const strikeProgress = interpolate(beatFrame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });
  return (
    <div style={{ width: 1920, height: 1080, backgroundColor: '#FA4E20', display: 'flex', justifyContent: 'center', alignItems: 'center', position: 'relative' }}>
      <div style={{ position: 'relative' }}>
        <h2 style={{ fontSize: '160px', fontFamily: 'serif', fontStyle: 'italic', color: '#060910', margin: 0 }}>
          on purpose.
        </h2>
        {/* Arc de rature dynamique SVG */}
        <svg style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none' }}>
          <path
            d="M 10,120 Q 350,60 700,90"
            stroke="#060910"
            strokeWidth="6"
            fill="none"
            strokeDasharray="800"
            strokeDashoffset={800 * (1 - strikeProgress)}
          />
        </svg>
      </div>
    </div>
  );
};
```

---

## Blueprint 05 : Phyllotaxie Dorée & Essaim de 2 400 Particules (Bar 6, Scene 05)

### Rôle & Principe Mathématique
Modélisation de 2 400 particules vectorielles passant d'un état turbulent (bruit tridimensionnel) à un arrangement polaire parfait selon la loi de la phyllotaxie à angle d'or :
$$r_i = c \sqrt{i}, \quad \theta_i = i \times 137.50776^\circ \quad (i \in [1, 2400])$$
L'interpolation progressive entre les coordonnées turbulentes aléatoires et les coordonnées polaires cibles s'effectue en Canvas 2D avec traînées de vélocité.

### Code Source TypeScript (Canvas 2D / Remotion)

```tsx
import React, { useRef, useEffect } from 'react';
import { interpolate, useCurrentFrame } from 'remotion';

interface Particle {
  turbulentX: number;
  turbulentY: number;
  targetX: number;
  targetY: number;
  color: string;
}

const PARTICLE_COUNT = 2400;
const GOLDEN_ANGLE = 137.50776 * (Math.PI / 180); // Radian

export const PhyllotaxisParticles: React.FC = () => {
  const frame = useCurrentFrame(); // frames 500 à 599 (0 à 99 relatives)
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Initialisation déterministe des particules
  const particles = React.useMemo<Particle[]>(() => {
    const list: Particle[] = [];
    const centerX = 1920 / 2;
    const centerY = 1080 / 2;
    const scalingC = 9.2;

    for (let i = 1; i <= PARTICLE_COUNT; i++) {
      // Coordonnées polaires de phyllotaxie
      const r = scalingC * Math.sqrt(i);
      const theta = i * GOLDEN_ANGLE;
      const targetX = centerX + r * Math.cos(theta);
      const targetY = centerY + r * Math.sin(theta);

      // Coordonnées de dispersion turbulente initiale
      const angleTurb = (i * 0.31) % (Math.PI * 2);
      const distTurb = 200 + ((i * 137) % 700);
      const turbulentX = centerX + distTurb * Math.cos(angleTurb);
      const turbulentY = centerY + distTurb * Math.sin(angleTurb);

      // Répartition des couleurs : 70% blanc, 20% corail, 10% cyan
      let color = '#FFFFFF';
      if (i % 10 === 0) color = '#2EE9D8';
      else if (i % 5 === 0) color = '#FA4E20';

      list.push({ turbulentX, turbulentY, targetX, targetY, color });
    }
    return list;
  }, []);

  // Progression de la convergence (frames 0 à 60 de la mesure)
  const morphProgress = interpolate(frame, [10, 65], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Effacement avec traînée de rémanence
    ctx.fillStyle = '#05080D';
    ctx.fillRect(0, 0, 1920, 1080);

    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const p = particles[i];

      // Interpolation linéaire avec amorti cubique
      const t = morphProgress * morphProgress * (3 - 2 * morphProgress);
      const curX = p.turbulentX + (p.targetX - p.turbulentX) * t;
      const curY = p.turbulentY + (p.targetY - p.turbulentY) * t;

      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(curX, curY, 1.8, 0, Math.PI * 2);
      ctx.fill();
    }
  }, [frame, morphProgress, particles]);

  return (
    <div style={{ position: 'relative', width: 1920, height: 1080 }}>
      <canvas ref={canvasRef} width={1920} height={1080} />
      <div
        style={{
          position: 'absolute',
          top: 80,
          left: 80,
          color: '#FFFFFF',
          fontFamily: 'monospace',
          fontSize: '14px',
        }}
      >
        n = 2,400 | φ = 137.508°
      </div>
    </div>
  );
};
```

---

## Blueprint 06 : Morphing Superformula 2D & Métaballes Fluides (Bar 8, Scene 07)

### Rôle & Principe Mathématique
Modélisation d'une forme organique noire fluide animée par la Superformula de Johan Gielis :
$$r(\theta) = \left( \left| \frac{\cos\left(\frac{m \theta}{4}\right)}{a} \right|^{n_2} + \left| \frac{\sin\left(\frac{m \theta}{4}\right)}{b} \right|^{n_3} \right)^{-\frac{1}{n_1}}$$
Le paramètre de symétrie $m$ varie continûment de `0.00` à `8.00`, faisant transiter la forme d'un blob amiboïde vers une étoile à 8 branches. Les métaballes satellites fusionnent avec la masse centrale grâce à un filtre matriciel SVG `feColorMatrix`.

### Code Source TypeScript (SVG Filter & Path Generator)

```tsx
import React, { useMemo } from 'react';
import { interpolate, useCurrentFrame } from 'remotion';

// Calcul du rayon selon la Superformula de Gielis
function superformula(
  theta: number,
  m: number,
  n1: number = 1.0,
  n2: number = 1.0,
  n3: number = 1.0,
  a: number = 1.0,
  b: number = 1.0
): number {
  const part1 = Math.pow(Math.abs(Math.cos((m * theta) / 4) / a), n2);
  const part2 = Math.pow(Math.abs(Math.sin((m * theta) / 4) / b), n3);
  const total = Math.pow(part1 + part2, -1 / n1);
  return isNaN(total) ? 1 : total;
}

export const SuperformulaLiquidScene: React.FC = () => {
  const frame = useCurrentFrame(); // frames 700 à 799 (0 à 99 relatives)
  const centerX = 1920 / 2;
  const centerY = 1080 / 2;

  // Animation du paramètre de symétrie m de 0 à 8
  const m = interpolate(frame, [0, 80], [0.0, 8.0], { extrapolateRight: 'clamp' });
  const scale = interpolate(frame, [80, 99], [220, 8], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  }); // Effondrement terminal

  // Génération des 240 coordonnées du polygone régulier
  const pathD = useMemo(() => {
    const steps = 240;
    let d = '';
    for (let i = 0; i <= steps; i++) {
      const theta = (i / steps) * 2 * Math.PI;
      const r = superformula(theta, m, 1.2, 1.0, 1.0) * scale;
      const x = centerX + r * Math.cos(theta);
      const y = centerY + r * Math.sin(theta);
      d += i === 0 ? `M ${x.toFixed(1)} ${y.toFixed(1)}` : ` L ${x.toFixed(1)} ${y.toFixed(1)}`;
    }
    return d + ' Z';
  }, [m, scale, centerX, centerY]);

  return (
    <div style={{ width: 1920, height: 1080, backgroundColor: '#FA4E20', position: 'relative' }}>
      <svg width={1920} height={1080} style={{ position: 'absolute', inset: 0 }}>
        {/* Filtre SVG de fusion liquide pour métaballes */}
        <defs>
          <filter id="liquid-goo">
            <feGaussianBlur in="SourceGraphic" stdDeviation="12" result="blur" />
            <feColorMatrix
              in="blur"
              mode="matrix"
              values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 24 -9"
              result="goo"
            />
            <feComposite in="SourceGraphic" in2="goo" operator="atop" />
          </filter>
        </defs>

        <g filter="url(#liquid-goo)">
          {/* Forme centrale Superformula */}
          <path d={pathD} fill="#060910" />

          {/* 3 Métaballes satellites en orbite fusionnante */}
          {[0, 1, 2].map((idx) => {
            const angleOrbit = (frame / 20) + (idx * (2 * Math.PI / 3));
            const distOrbit = 180 + Math.sin(frame / 10 + idx) * 40;
            const satX = centerX + distOrbit * Math.cos(angleOrbit);
            const satY = centerY + distOrbit * Math.sin(angleOrbit);
            return <circle key={idx} cx={satX} cy={satY} r={32} fill="#060910" />;
          })}
        </g>
      </svg>

      {/* Cartouche formule mathématique */}
      <div
        style={{
          position: 'absolute',
          bottom: 120,
          left: 64,
          fontFamily: 'monospace',
          fontSize: '13px',
          color: '#FFFFFF',
        }}
      >
        r(θ) = superformula(m={m.toFixed(2)}, n₁=1.2, a=1.0)
      </div>
    </div>
  );
};
```

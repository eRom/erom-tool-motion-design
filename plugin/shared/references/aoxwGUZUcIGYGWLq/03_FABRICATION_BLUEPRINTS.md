# 03. Blueprints de Fabrication & Recettes de Code

Ce guide fournit aux agents développeurs (Remotion, Three.js / WebGL, Canvas 2D, SVG) les algorithmes, équations cinématiques et architectures logicielles nécessaires pour ré-implémenter fidèlement les six briques visuelles maîtresses de la vidéo.

---

## 1. Moteur 1 : Simulation Physique de la Sphère & Squash/Stretch (Physical Ball & Floor Ripple)

Utilisé pour : La chute gravitaire initiale (00:00 - 00:20), les rebonds sur les lettres et le sol (00:20 - 00:58), l'impact sur la grille de voxels (09:26) et le point typographique final (13:21).

### Principe Géométrique & Physique
1. **Équation de chute et rebond amorti** :
   La position verticale $y(t)$ est calculée par intégration d'Euler ou par une fonction fermée par morceaux représentant les arcs de parabole de la gravité $g = 0.85\text{ px/frame}^2$, avec un coefficient de restitution élastique $e = 0.68$.
2. **Squash & Stretch volumétrique** :
   Pour préserver l'illusion de volume incompressible ($\Delta V = 0$), lors de la décélération brutale au point d'impact, le facteur d'échelle vertical se compresse ($\text{scale}_y < 1.0$) tandis que les facteurs horizontaux se dilatent de manière inversement proportionnelle :
   $$\text{scale}_x = \text{scale}_z = \frac{1}{\sqrt{\text{scale}_y}}$$
3. **Onde de choc de Fresnel au sol** :
   À chaque impact ($y = y_{\text{floor}}$), un émetteur d'ondes de choc crée un anneau concentrique plat dont le rayon $R(t)$ croît linéairement tandis que son opacité décroît exponentiellement.

### Implémentation de Référence (TypeScript / React / Remotion + Three.js)

```typescript
import React, { useRef, useMemo } from 'react';
import { useCurrentFrame } from 'remotion';
import * as THREE from 'three';

interface BallPhysicsProps {
  floorY?: number;
  initialY?: number;
  dropFrame?: number;
}

export const PhysicalSphere: React.FC<BallPhysicsProps> = ({
  floorY = 0,
  initialY = 400,
  dropFrame = 16,
}) => {
  const frame = useCurrentFrame();
  const radius = 24;

  // Calcul physique déterministe frame-par-frame sans état mutable
  const { currentY, scaleX, scaleY, rollAngle } = useMemo(() => {
    if (frame < dropFrame) {
      return { currentY: initialY, scaleX: 1, scaleY: 1, rollAngle: 0 };
    }

    const t = frame - dropFrame;
    const g = 1.4; // accélération gravitaire en px/frame^2
    const restitution = 0.62;

    // Simulation discrète rapide pour calculer la position exacte
    let simY = initialY;
    let simV = 0;
    let sX = 1;
    let sY = 1;

    for (let f = 0; f <= t; f++) {
      simV -= g;
      simY += simV;

      if (simY <= floorY + radius) {
        simY = floorY + radius;
        simV = -simV * restitution;

        // Détection de la frame d'impact pour squash
        if (f === t) {
          const impactSpeed = Math.abs(simV);
          const compression = Math.min(0.35, impactSpeed * 0.015);
          sY = 1 - compression;
          sX = 1 + compression * 0.5;
        }
      }
    }

    const rollAngle = (t * 0.08) % (Math.PI * 2);
    return { currentY: simY, scaleX: sX, scaleY: sY, rollAngle };
  }, [frame, dropFrame, floorY, initialY]);

  return (
    <group position={[0, currentY, 0]}>
      {/* Sphère rouge Claude */}
      <mesh scale={[scaleX, scaleY, scaleX]} rotation={[0, 0, rollAngle]}>
        <sphereGeometry args={[radius, 64, 64]} />
        <meshPhysicalMaterial
          color="#EB513F"
          roughness={0.12}
          metalness={0.05}
          clearcoat={1.0}
          clearcoatRoughness={0.08}
        />
      </mesh>
    </group>
  );
};
```

---

## 2. Moteur 2 : Extrusion Typographique Volumétrique Pseudo-3D (Layer-Stacking & Text Shadows)

Utilisé pour : L'apparition et la mise en volume de "EVERY FRAME COUNTS" (03:21 - 04:12) et l'érection des lettres "CLAUDE" en Section 06.

### Principe Géométrique & Algorithmique
Pour obtenir un biseau lourd et un rendu volumétrique brutaliste avec des performances optimales sans le coût d'un maillage 3D complexe, l'effet s'appuie sur la technique du **Layer-Stacking (Multi-Slice Stacking)** couplée à une déformation de perspective CSS 3D :
1. **Translation axiale de tranches successives** : $N$ copies du texte sont superposées le long d'un vecteur de profondeur $V = (\cos(\theta) \cdot d, \sin(\theta) \cdot d)$.
2. **Dégradé d'ombrage d'occlusion (Shading Ramp)** : Les tranches profondes reçoivent une interpolation vers la teinte sombre d'occlusion (`#1A0806`), tandis que la face avant (`slice = 0`) conserve sa couleur nominale saturée.
3. **Plongée Caméra Z-Punch** : À l'impact de transition, un `scale` exponentiel couplé à un `transform: perspective(600px) rotateX(24deg) rotateY(-18deg)` projette le bloc dans la vue.

### Implémentation de Référence (TypeScript / React / CSS-in-JS)

```typescript
import React from 'react';
import { interpolate, useCurrentFrame, spring } from 'remotion';

interface KineticExtrusionProps {
  text: string;
  depth?: number;
  textColor?: string;
  depthColor?: string;
  fontSize?: number;
}

export const Kinetic3DText: React.FC<KineticExtrusionProps> = ({
  text,
  depth = 48,
  textColor = '#09090B',
  depthColor = '#661408',
  fontSize = 180,
}) => {
  const frame = useCurrentFrame();

  // Animation d'extrusion synchronisée avec le beat
  const extrudeProgress = spring({
    frame,
    fps: 30,
    config: { damping: 14, stiffness: 180, mass: 0.8 },
  });

  const effectiveDepth = Math.round(depth * extrudeProgress);
  const layers = Array.from({ length: effectiveDepth }, (_, i) => i);

  return (
    <div
      style={{
        position: 'relative',
        display: 'inline-block',
        fontFamily: '"Neue Haas Grotesk", "Druk Wide", sans-serif',
        fontWeight: 900,
        fontSize: `${fontSize}px`,
        textTransform: 'uppercase',
        letterSpacing: '-0.04em',
        transform: `perspective(1000px) rotateX(16deg) rotateY(-22deg)`,
        transformStyle: 'preserve-3d',
      }}
    >
      {/* Tranches d'extrusion arrière */}
      {layers.map((index) => {
        const factor = index / effectiveDepth;
        return (
          <span
            key={index}
            style={{
              position: 'absolute',
              left: 0,
              top: 0,
              color: factor > 0.8 ? '#150302' : depthColor,
              transform: `translate3d(${-index * 1.2}px, ${index * 1.4}px, ${-index}px)`,
              zIndex: effectiveDepth - index,
              userSelect: 'none',
              filter: `brightness(${1 - factor * 0.6})`,
            }}
          >
            {text}
          </span>
        );
      })}

      {/* Face avant principale */}
      <span
        style={{
          position: 'relative',
          color: textColor,
          zIndex: effectiveDepth + 1,
          display: 'block',
        }}
      >
        {text}
      </span>
    </div>
  );
};
```

---

## 3. Moteur 3 : Système Gyroscopique 3D Multiaxes (Euler Gimbal System & Bloom)

Utilisé pour : La séquence géométrique de la Section 03 `03 FORM` (04:16 - 07:15).

### Principe Géométrique
Un assemblage de trois anneaux toriques concentriques et d'une sphère interne, tournant selon des vitesses angulaires non harmoniques sur les trois degrés de liberté d'Euler :
- **Anneau Extérieur (Titane Chromé)** : Rayon $R_1 = 280\text{px}$, rotation autour de l'axe $X$ à vitesse $\omega_x = 1.25\text{ rad/s}$.
- **Anneau Intermédiaire (Noir Laqué)** : Rayon $R_2 = 230\text{px}$, rotation autour de l'axe $Y$ à vitesse $\omega_y = -0.92\text{ rad/s}$.
- **Anneau Intérieur (Émissif Corail)** : Rayon $R_3 = 180\text{px}$, rotation autour de l'axe $Z$ à vitesse $\omega_z = 2.10\text{ rad/s}$.
- **Phase d'alignement (Frame 211 - 225)** : Une fonction d'interpolation critique force les trois angles d'Euler vers zéro $(\theta_x, \theta_y, \theta_z) \to (0, 0, 0)$ pour créer l'effet d'iris coaxial face à l'objectif.

### Implémentation de Référence (Three.js / WebGL)

```typescript
import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useCurrentFrame } from 'remotion';
import * as THREE from 'three';

export const GimbalGyroscope: React.FC = () => {
  const frame = useCurrentFrame();
  const ring1Ref = useRef<THREE.Mesh>(null);
  const ring2Ref = useRef<THREE.Mesh>(null);
  const ring3Ref = useRef<THREE.Mesh>(null);

  // Alignement coaxial en fin de section (frames 75 à 90 de la composition locale)
  const isAligning = frame > 65;
  const alignProgress = Math.min(1, Math.max(0, (frame - 65) / 20));
  const easeAlign = 1 - Math.pow(1 - alignProgress, 3);

  const t = frame / 30; // temps en secondes

  // Calcul des rotations avec décélération d'alignement
  const rotX = (t * 1.25) * (1 - easeAlign);
  const rotY = (-t * 0.92) * (1 - easeAlign);
  const rotZ = (t * 2.10) * (1 - easeAlign);

  return (
    <group position={[0, 0, 0]}>
      {/* Anneau 1 : Titane chromé poli */}
      <mesh ref={ring1Ref} rotation={[rotX, 0, 0]}>
        <torusGeometry args={[9, 0.45, 32, 100]} />
        <meshStandardMaterial
          color="#F0F0F2"
          metalness={0.92}
          roughness={0.15}
        />
      </mesh>

      {/* Anneau 2 : Noir satiné */}
      <mesh ref={ring2Ref} rotation={[0, rotY, 0]}>
        <torusGeometry args={[7.2, 0.4, 32, 100]} />
        <meshStandardMaterial
          color="#151518"
          metalness={0.7}
          roughness={0.3}
        />
      </mesh>

      {/* Anneau 3 : Néon rouge/corail émissif */}
      <mesh ref={ring3Ref} rotation={[0, 0, rotZ]}>
        <torusGeometry args={[5.5, 0.25, 32, 100]} />
        <meshStandardMaterial
          color="#EB513F"
          emissive="#FF442A"
          emissiveIntensity={2.5}
          roughness={0.2}
        />
      </mesh>

      {/* Cœur central : Sphère rouge */}
      <mesh scale={1 - easeAlign * 0.3}>
        <sphereGeometry args={[2.8, 64, 64]} />
        <meshPhysicalMaterial
          color="#EB513F"
          roughness={0.1}
          metalness={0.1}
          clearcoat={1}
        />
      </mesh>
    </group>
  );
};
```

---

## 4. Moteur 4 : Tunnel Hexagonal Infini & Warp Hyper-Vitesse (Infinite Hex-Portal Warp Engine)

Utilisé pour : La séquence Section 04 `04 VELOCITY` (07:16 - 08:29).

### Principe Géométrique & Algorithmique
1. **Recyclage Modulaire (Infinite Modulo Z-Depth)** :  
   Un ensemble de $K = 28$ anneaux hexagonaux est distribué le long de l'axe $Z$ sur un intervalle $[-D, 0]$. À chaque frame, les hexagones avancent vers la caméra à la vitesse $V(t)$. Lorsqu'un hexagone dépasse la caméra ($Z > 0$), sa position est réinjectée au fond du tunnel ($Z \to Z - D$).
2. **Torsion Angulaire (Helical Twist)** :  
   Chaque hexagone subit une rotation d'angle $\theta(z) = \text{frame} \cdot \omega_{\text{roll}} + z \cdot \kappa$, créant une spirale géométrique en vrille.
3. **Speed Lines Radiales** :  
   Des segments de droite vectoriels partent du point de fuite central $(x_0, y_0)$ avec une longueur proportionnelle à la vitesse de déplacement et un flou de mouvement étiré vers les angles de l'écran.

### Implémentation de Référence (TypeScript / HTML5 Canvas 2D)

```typescript
export class HexWarpEngine {
  private hexCount = 24;
  private tunnelLength = 2400;

  render(ctx: CanvasRenderingContext2D, width: number, height: number, frame: number) {
    const cx = width / 2;
    const cy = height / 2;
    const fov = 400;

    // Accélération exponentielle au fil des frames
    const speed = 35 + Math.pow(frame * 0.45, 1.8);
    const globalRoll = frame * 0.045;

    ctx.save();
    ctx.fillStyle = '#050505';
    ctx.fillRect(0, 0, width, height);

    for (let i = 0; i < this.hexCount; i++) {
      const baseZ = (i / this.hexCount) * this.tunnelLength;
      // Déplacement et recyclage modulo
      const currentZ = ((baseZ - frame * speed) % this.tunnelLength + this.tunnelLength) % this.tunnelLength;

      if (currentZ < 40) continue; // Évite les artefacts de division par zéro

      const scale = fov / currentZ;
      const radius = 320 * scale;
      const angle = globalRoll + (currentZ * 0.002);
      const isWhite = i % 2 === 0;

      // Dessin de l'hexagone
      ctx.beginPath();
      for (let s = 0; s < 6; s++) {
        const a = angle + (s * Math.PI) / 3;
        const hx = cx + Math.cos(a) * radius;
        const hy = cy + Math.sin(a) * radius;
        if (s === 0) ctx.moveTo(hx, hy);
        else ctx.lineTo(hx, hy);
      }
      ctx.closePath();

      // Style et lueur néon
      ctx.lineWidth = Math.max(1.5, 4.5 * scale);
      ctx.strokeStyle = isWhite ? '#FFFFFF' : '#EB513F';
      ctx.shadowColor = isWhite ? '#FFFFFF' : '#FF5533';
      ctx.shadowBlur = Math.min(25, 15 * scale);
      ctx.stroke();
    }

    ctx.restore();
  }
}
```

---

## 5. Moteur 5 : Matrice Voxel Tactile Réactive (Pin Screen & Wave Propagation)

Utilisé pour : La séquence Section 05 `05 SYSTEMS` (09:00 - 12:02).

### Principe Géométrique & Mathématique
Une grille orthogonale de $M \times N = 36 \times 24 = 864$ pavés cubiques instanciés (`InstancedMesh`).
1. **Équation de propagation d'onde** :
   À chaque point d'impact de la sphère $(x_0, z_0)$ survenu à la frame $t_0$, l'élévation d'un voxel en $(x_i, z_i)$ au temps courant $t$ est :
   $$\Delta y_i(t) = A \cdot \exp\left(-\frac{(d_i - v \cdot (t - t_0))^2}{2 \sigma^2}\right) \cdot \exp(-\alpha (t - t_0))$$
   où $d_i = \sqrt{(x_i - x_0)^2 + (z_i - z_0)^2}$ est la distance euclidienne, $v$ la vitesse de propagation de l'onde, et $\sigma$ l'épaisseur de l'anneau de crête.
2. **Morphing Chromatique par Élévation** :
   La matrice d'instance interpole la couleur diffuse du matériau :
   $$\text{Color}_i = \text{lerp}(\#E8E4D8, \#EB513F, \frac{\Delta y_i}{\Delta y_{\max}})$$
3. **Formation Structurée de l'Astérisque** :
   En fin de séquence ($t > t_{\text{lock}}$), les élévations dynamiques s'annulent et sont remplacées par un masque binaire $M_{i} \in \{0, 1\}$ définissant l'étoile à 8 branches. Les cubes appartenant au masque s'élèvent de $+32\text{px}$ et fixent la teinte `#EB513F`.

### Implémentation de Référence (Three.js InstancedMesh)

```typescript
import React, { useRef, useMemo, useEffect } from 'react';
import { useCurrentFrame } from 'remotion';
import * as THREE from 'three';

const COLS = 36;
const ROWS = 24;
const TOTAL = COLS * ROWS;
const SPACING = 16;

export const TactileVoxelGrid: React.FC = () => {
  const frame = useCurrentFrame();
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);
  const baseColor = useMemo(() => new THREE.Color('#E8E4D8'), []);
  const activeColor = useMemo(() => new THREE.Color('#EB513F'), []);

  useEffect(() => {
    if (!meshRef.current) return;

    const impactFrame = 25; // Frame relative d'impact
    const t = Math.max(0, frame - impactFrame);
    const waveSpeed = 8;
    const waveRadius = t * waveSpeed;

    let index = 0;
    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        const x = (c - COLS / 2) * SPACING;
        const z = (r - ROWS / 2) * SPACING;
        const dist = Math.hypot(x, z);

        // Calcul de la crête d'onde gaussienne
        const waveDelta = dist - waveRadius;
        const waveHeight = Math.exp(-Math.pow(waveDelta / 35, 2)) * Math.exp(-t * 0.04) * 45;

        dummy.position.set(x, waveHeight / 2, z);
        dummy.scale.set(1, 1 + waveHeight * 0.1, 1);
        dummy.updateMatrix();

        meshRef.current.setMatrixAt(index, dummy.matrix);

        // Coloration en rouge sur la crête d'onde
        const colorFactor = Math.min(1, waveHeight / 30);
        const voxelColor = baseColor.clone().lerp(activeColor, colorFactor);
        meshRef.current.setColorAt(index, voxelColor);

        index++;
      }
    }

    meshRef.current.instanceMatrix.needsUpdate = true;
    if (meshRef.current.instanceColor) meshRef.current.instanceColor.needsUpdate = true;
  }, [frame, dummy, baseColor, activeColor]);

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, TOTAL]}>
      <boxGeometry args={[14, 14, 14]} />
      <meshStandardMaterial roughness={0.4} metalness={0.05} />
    </instancedMesh>
  );
};
```

---

## 6. Moteur 6 : Instrumentation Télémétrique Frame-Accurate (Diagnostic HUD Engine)

Utilisé pour : Le système HUD permanent présent de la frame 001 à 450.

### Principe de Conception
Le HUD ne doit comporter aucun retard ni lissage : il reflète la réalité mathématique brute du buffer de trame en temps réel.
- **Compteur de Temps** : `timecode = format(frame / 30)`.
- **Compteur de Frames** : `F ${String(frame).padStart(3, '0')} / 450`.
- **Barre de Scan Continue** : Segment `Line(48px, 1040px, 48px + 1824px * (frame / 450), 1040px)`.
- **Inversion Automatique Sombre / Clair** : Le composant écoute l'index de chapitre pour basculer ses tokens de couleur (`#FFFFFF` pour les chapitres 01-04, `#1A1919` pour 05-06).

### Implémentation de Référence (TypeScript / React / SVG)

```typescript
import React from 'react';
import { useCurrentFrame } from 'remotion';

const SECTION_DATA = [
  { start: 1, end: 60, name: '01 IMPACT', isLightBg: false },
  { start: 61, end: 135, name: '02 KINETIC TYPE', isLightBg: false },
  { start: 136, end: 225, name: '03 FORM', isLightBg: false },
  { start: 226, end: 269, name: '04 VELOCITY', isLightBg: false },
  { start: 270, end: 362, name: '05 SYSTEMS', isLightBg: true },
  { start: 363, end: 450, name: '06 SIGN-OFF', isLightBg: true },
];

export const TelemetryHUD: React.FC = () => {
  const frame = useCurrentFrame();

  const currentSection =
    SECTION_DATA.find((s) => frame >= s.start && frame <= s.end) || SECTION_DATA[0];

  const color = currentSection.isLightBg ? '#1A1919' : '#FFFFFF';
  const mutedColor = currentSection.isLightBg
    ? 'rgba(26, 25, 25, 0.45)'
    : 'rgba(255, 255, 255, 0.45)';

  // Formatage frame-accurate
  const seconds = Math.floor(frame / 30);
  const subSeconds = Math.floor(((frame % 30) / 30) * 100);
  const timecode = `${String(seconds).padStart(2, '0')}:${String(subSeconds).padStart(2, '0')}`;
  const frameString = `F ${String(Math.min(450, frame)).padStart(3, '0')} / 450`;

  // Progression de la timeline inférieure
  const progressWidth = (frame / 450) * 1824;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        pointerEvents: 'none',
        fontFamily: '"JetBrains Mono", "SF Mono", monospace',
        fontSize: '15px',
        fontWeight: 600,
        letterSpacing: '+0.10em',
        color,
      }}
    >
      {/* Header */}
      <div style={{ position: 'absolute', top: 48, left: 48 }}>CLAUDE — MOTION REEL</div>
      <div style={{ position: 'absolute', top: 48, right: 48 }}>©2026</div>

      {/* Footer */}
      <div style={{ position: 'absolute', bottom: 56, left: 48 }}>
        <span>{currentSection.name}</span>
      </div>
      <div style={{ position: 'absolute', bottom: 56, right: 48, letterSpacing: '+0.08em' }}>
        <span>{timecode}</span>
        <span style={{ marginLeft: 24 }}>{frameString}</span>
      </div>

      {/* Barre de Scan Inférieure */}
      <div
        style={{
          position: 'absolute',
          bottom: 40,
          left: 48,
          width: 1824,
          height: 1,
          backgroundColor: mutedColor,
        }}
      >
        <div
          style={{
            height: '100%',
            width: `${progressWidth}px`,
            backgroundColor: color,
          }}
        />
      </div>
    </div>
  );
};
```

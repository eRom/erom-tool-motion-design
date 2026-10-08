# 03. Blueprints de Fabrication & Recettes de Rendu

Ce document fournit les spécifications d'ingénierie logicielle et les algorithmes de rendu pour reproduire les 7 effets clés les plus complexes de la vidéo `PRWfsEy-zcoo2ao_.mp4`. Chaque blueprint comprend les principes mathématiques sous-jacents, les formules frame-par-frame et un composant typé prêt à l'emploi (TypeScript / Remotion, Three.js / GLSL, Canvas 2D).

---

## Sommaire des Blueprints

1. **Blueprint 1** : Shader de Bissection Dual-Mode & Trame Demi-Teintes Ben-Day (Three.js / GLSL)
2. **Blueprint 2** : Kinetic Pop-Brutalist Typography avec Hard Block Shadow (Remotion / React)
3. **Blueprint 3** : Générateur Procédural d'Anime Radial Speed Lines (HTML5 Canvas / TypeScript)
4. **Blueprint 4** : Pluie Numérique Matrix Rain avec Parallaxe 3D (Canvas 2D / Three.js)
5. **Blueprint 5** : Vortex de Feuilles Volantes avec Physique de Traînée (Three.js InstancedMesh)
6. **Blueprint 6** : Ville de Données 3D & Égaliseur Isométrique (Three.js / React Three Fiber)
7. **Blueprint 7** : Rubans de Peinture 3D Extrudés & Éclaboussures Liquides (Three.js Curve Extrusion)

---

## Blueprint 1 : Shader de Bissection Dual-Mode & Trame Demi-Teintes Ben-Day

### Rôle & Contexte Visuel
Présent dans le plan héroïque (F0096-F0192) et le packshot final (F1477-F1537) : l'écran est scindé par une diagonale à 45°/65°. La mascotte Clawd est physique et en argile à gauche, et se transforme en hologramme cyan translucide à droite. Le fond bleu est texturé par une trame de demi-teintes pop-art (Ben-Day dots).

### Principe Mathématique
1. **Plan de coupe diagonal 3D / 2D** :
   Soit une droite dans l'espace écran définie par le vecteur normal \(\vec{n} = (\cos \theta, \sin \theta)\) et un offset \(d\). Pour tout fragment de coordonnées normalisées \((u, v) \in [0, 1]^2\) :
   \[
   S(u, v) = u \cdot \cos \theta + v \cdot \sin \theta - d
   \]
   - Si \(S(u, v) < 0\) : Rendu mat physique (Argile terracotta).
   - Si \(S(u, v) \ge 0\) : Rendu hologramme néon (Cyan émissif, lignes de scan horizontales et réseau filaire).
2. **Trame de points Ben-Day** :
   Grille orthogonale tournée de 45° :
   \[
   u' = \frac{x + y}{\sqrt{2} \cdot s}, \quad v' = \frac{-x + y}{\sqrt{2} \cdot s}
   \]
   où \(s\) est le pas de grille (16px). Le rayon du point dépend de la distance au centre de chaque cellule périodique : \(r = \text{distance}(\text{fract}(u', v'), (0.5, 0.5))\).

### Implémentation GLSL / Three.js

```typescript
import * as THREE from 'three';

export const DualModeMaterial = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0 },
    uSplitOffset: { value: 0.5 },
    uSplitAngle: { value: THREE.MathUtils.degToRad(65) },
    uColorClay: { value: new THREE.Color('#EF7E54') },
    uColorHologram: { value: new THREE.Color('#00E5FF') },
    uHalftoneSize: { value: 16.0 },
  },
  vertexShader: `
    varying vec2 vUv;
    varying vec3 vNormal;
    varying vec3 vWorldPosition;

    void main() {
      vUv = uv;
      vNormal = normalize(normalMatrix * normal);
      vec4 worldPos = modelMatrix * vec4(position, 1.0);
      vWorldPosition = worldPos.xyz;
      gl_Position = projectionMatrix * viewMatrix * worldPos;
    }
  `,
  fragmentShader: `
    uniform float uTime;
    uniform float uSplitOffset;
    uniform float uSplitAngle;
    uniform vec3 uColorClay;
    uniform vec3 uColorHologram;
    uniform float uHalftoneSize;

    varying vec2 vUv;
    varying vec3 vNormal;
    varying vec3 vWorldPosition;

    void main() {
      // Calcul de la frontière diagonale
      vec2 screenCoord = gl_FragCoord.xy;
      float angle = uSplitAngle;
      vec2 dir = vec2(cos(angle), sin(angle));
      float proj = dot(screenCoord, dir) - (uSplitOffset * 1920.0);

      // Éclairage Lambert simple pour la face argile
      vec3 lightDir = normalize(vec3(0.5, 1.0, 0.8));
      float diff = max(dot(vNormal, lightDir), 0.2);

      if (proj < 0.0) {
        // Côté gauche : Argile physique douce
        vec3 clayColor = uColorClay * diff;
        gl_FragColor = vec4(clayColor, 1.0);
      } else {
        // Côté droit : Hologramme cyber cyan
        float scanline = sin(screenCoord.y * 0.4 + uTime * 8.0) * 0.5 + 0.5;
        float fresnel = pow(1.0 - max(dot(vNormal, vec3(0.0, 0.0, 1.0)), 0.0), 2.5);
        
        // Trame filaire/grid sur le modèle
        float gridX = step(0.92, fract(vUv.x * 20.0));
        float gridY = step(0.92, fract(vUv.y * 20.0));
        float wire = max(gridX, gridY);

        vec3 holo = uColorHologram * (0.6 + 0.4 * scanline) + vec3(wire * 0.5) + vec3(fresnel * 0.8);
        gl_FragColor = vec4(holo, 0.85);
      }
    }
  `,
  transparent: true,
});
```

---

## Blueprint 2 : Kinetic Pop-Brutalist Typography avec Hard Block Shadow

### Rôle & Contexte Visuel
Le système de titrage percutant affiché en bas à gauche (`12 AGENTS`, `FULL REWRITE`, `847 TABS`, `KILL IT WITH FIRE`, etc.). Les caractères sont massifs, condensés, inclinés, avec un liseré noir opaque et une ombre portée dure en escalier (block shadow).

### Principe Mathématique
1. **Overshoot Elastic Punch-In** :
   À l'instant du beat \(t_0\), le facteur d'échelle \(S(t)\) passe de 0.2 à 1.0 en suivant une oscillation amortie :
   \[
   S(t) = 1.0 - e^{-\zeta \omega t} \cdot \left(\cos(\omega_d t) + \frac{\zeta}{\sqrt{1 - \zeta^2}} \sin(\omega_d t)\right)
   \]
   avec \(\zeta = 0.65\) (facteur d'amortissement) et \(\omega = 25 \text{ rad/s}\).
2. **Hard Block Shadow** :
   Une ombre vectorielle pure sans flou gaussien, créée en superposant 6 paliers de translation 1px vers \((+x, +y)\) pour former un biseau noir dense.

### Composant Remotion / React (TypeScript)

```tsx
import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface KineticTitleProps {
  category: string; // Ex: "01 / 06 • CODE"
  title: string;    // Ex: "12 AGENTS"
  accentColor: string; // Ex: "#39FF14"
  startFrame: number;
}

export const KineticTitle: React.FC<KineticTitleProps> = ({
  category,
  title,
  accentColor,
  startFrame,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const localFrame = Math.max(0, frame - startFrame);

  // Animation élastique d'impact
  const scale = spring({
    frame: localFrame,
    fps,
    config: {
      mass: 0.8,
      stiffness: 240,
      damping: 14,
    },
  });

  const translateY = interpolate(localFrame, [0, 8], [60, 0], {
    extrapolateRight: 'clamp',
  });

  const opacity = interpolate(localFrame, [0, 3], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 96,
        left: 96,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        transform: `translateY(${translateY}px) scale(${scale}) skewX(-6deg)`,
        transformOrigin: 'bottom left',
        opacity,
        zIndex: 50,
      }}
    >
      {/* Label catégorie supérieur */}
      <span
        style={{
          fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
          fontSize: 26,
          fontWeight: 700,
          color: accentColor,
          letterSpacing: '0.12em',
          textTransform: 'uppercase',
          marginBottom: 8,
          textShadow: '0 2px 4px rgba(0,0,0,0.8)',
        }}
      >
        {category}
      </span>

      {/* Titre monumental avec Hard Block Shadow */}
      <h1
        style={{
          margin: 0,
          fontFamily: "'Bebas Neue', 'Anton', sans-serif",
          fontSize: 120,
          lineHeight: 0.9,
          fontWeight: 900,
          letterSpacing: '0.02em',
          color: '#FFFFFF',
          WebkitTextStroke: '4px #1A1A1A',
          paintOrder: 'stroke fill',
          textShadow: `
            2px 2px 0px #1A1A1A,
            3px 3px 0px #1A1A1A,
            4px 4px 0px #1A1A1A,
            5px 5px 0px #1A1A1A,
            6px 6px 0px #1A1A1A,
            8px 8px 12px rgba(0,0,0,0.6)
          `,
        }}
      >
        {title}
      </h1>
    </div>
  );
};
```

---

## Blueprint 3 : Générateur Procédural d'Anime Radial Speed Lines

### Rôle & Contexte Visuel
Utilisé lors de la révélation Shōnen initiale (F0072-F0096) et lors de chaque transition éclair (flashs de 24 frames au début de chaque section). Il focalise le regard sur Clawd et confère une énergie cinétique explosive.

### Principe Mathématique
Pour chaque rayon tracé depuis le centre \((x_c, y_c)\) vers un angle \(\theta \in [0, 2\pi]\) :
- Échantillonnage d'un pas angulaire avec gigue aléatoire : \(\Delta \theta = \frac{2\pi}{N} + \text{noise}(\theta)\).
- Découpe en triangle effilé : sommet intérieur à \(R_{\min} = 160\text{px}\), base extérieure à \(R_{\max} = 1400\text{px}\) avec une largeur de base de 8 à 24px.
- Modulation de transparence en fonction du temps pour éviter le gel de la trame.

### Implémentation Canvas 2D (TypeScript)

```typescript
export class RadialSpeedLines {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private rayCount: number = 72;
  private seed: number = 42;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d')!;
  }

  public render(
    frame: number,
    centerX: number = 960,
    centerY: number = 540,
    innerRadius: number = 180,
    lineColor: string = '#A09A8F',
    intensity: number = 1.0
  ): void {
    const { ctx, canvas } = this;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (intensity <= 0.01) return;

    ctx.save();
    ctx.globalAlpha = Math.min(1.0, intensity);
    ctx.fillStyle = lineColor;

    const maxRadius = Math.hypot(canvas.width, canvas.height);
    const angleStep = (Math.PI * 2) / this.rayCount;

    // Pseudo-bruit dépendant de la frame pour animer le tremblement
    for (let i = 0; i < this.rayCount; i++) {
      const baseAngle = i * angleStep;
      const jitter = Math.sin(i * 1337 + frame * 0.8) * 0.02;
      const angle = baseAngle + jitter;

      // Largeur angulaire du rayon
      const rayWidth = (0.015 + Math.abs(Math.sin(i * 777 + frame)) * 0.02) * (canvas.width / 1920);

      // Coordonnées du triangle effilé
      const rInner = innerRadius + Math.abs(Math.cos(i * 99 + frame)) * 40;
      const x1 = centerX + Math.cos(angle) * rInner;
      const y1 = centerY + Math.sin(angle) * rInner;

      const x2 = centerX + Math.cos(angle - rayWidth) * maxRadius;
      const y2 = centerY + Math.sin(angle - rayWidth) * maxRadius;

      const x3 = centerX + Math.cos(angle + rayWidth) * maxRadius;
      const y3 = centerY + Math.sin(angle + rayWidth) * maxRadius;

      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.lineTo(x3, y3);
      ctx.closePath();
      ctx.fill();
    }

    ctx.restore();
  }
}
```

---

## Blueprint 4 : Pluie Numérique Matrix Rain avec Parallaxe 3D

### Rôle & Contexte Visuel
Le décor d'arrière-plan de la scène 01 • CODE (F0216-F0384). Des cascades de caractères vert fluo tombent en continu à différentes profondeurs de champ (parallaxe Z), conférant une atmosphère de hacker den futuriste.

### Principe Mathématique
Chaque colonne de caractères possède :
- Une position \(X_i\), une profondeur \(Z_i \in [0.5, 2.0]\), une vitesse de chute \(v_i = \frac{v_0}{Z_i}\).
- Une tête de colonne lumineuse (caractère blanc `#FFFFFF` éclatant).
- Une traînée de \(L = 20\) caractères dont l'opacité décroît exponentiellement :
  \[
  \alpha(k) = \exp(-k / 5.0), \quad k \in [0, L]
  \]
- Mutation aléatoire des caractères ASCII / Katakana à une fréquence de 10% par frame.

### Implémentation Canvas 2D / Three.js (TypeScript)

```typescript
export class MatrixRainBackground {
  private columns: {
    x: number;
    y: number;
    speed: number;
    length: number;
    chars: string[];
    depth: number;
  }[] = [];

  private glyphPool = '0123456789ABCDEF{}[]<>=+-*~;:|/\\$#@!アイウエオカキクケコサシスセソ';

  constructor(width: number, height: number, density: number = 60) {
    for (let i = 0; i < density; i++) {
      const depth = 0.6 + Math.random() * 1.4;
      this.columns.push({
        x: (i / density) * width + (Math.random() - 0.5) * 20,
        y: Math.random() * height,
        speed: (4 + Math.random() * 8) / depth,
        length: Math.floor(12 + Math.random() * 18),
        chars: Array.from({ length: 30 }, () => this.randomGlyph()),
        depth,
      });
    }
  }

  private randomGlyph(): string {
    return this.glyphPool[Math.floor(Math.random() * this.glyphPool.length)];
  }

  public updateAndDraw(ctx: CanvasRenderingContext2D, width: number, height: number): void {
    // Fond semi-transparent pour l'effet de persistance rétinienne
    ctx.fillStyle = 'rgba(2, 20, 8, 0.25)';
    ctx.fillRect(0, 0, width, height);

    ctx.font = 'bold 18px monospace';
    ctx.textAlign = 'center';

    for (const col of this.columns) {
      col.y += col.speed;
      if (col.y - col.length * 20 > height) {
        col.y = -20;
      }

      // Mutation occasionnelle
      if (Math.random() < 0.1) {
        col.chars[Math.floor(Math.random() * col.chars.length)] = this.randomGlyph();
      }

      for (let k = 0; k < col.length; k++) {
        const charY = col.y - k * 20;
        if (charY < 0 || charY > height) continue;

        if (k === 0) {
          // Tête blanche éclatante
          ctx.fillStyle = '#FFFFFF';
          ctx.shadowColor = '#00FF66';
          ctx.shadowBlur = 12;
        } else {
          // Dégradé d'estompage vert fluo
          const alpha = Math.max(0, 1 - k / col.length) * (1 / col.depth);
          ctx.fillStyle = `rgba(0, 255, 102, ${alpha})`;
          ctx.shadowBlur = 0;
        }

        ctx.fillText(col.chars[k % col.chars.length], col.x, charY);
      }
    }
  }
}
```

---

## Blueprint 5 : Vortex de Feuilles Volantes avec Physique de Traînée

### Rôle & Contexte Visuel
Effet central de la scène 02 • WRITE (F0408-F0576). Plus de 80 feuilles manuscrites tourbillonnent autour de la mascotte Clawd en simulant un courant d'air vertical chaotique avec portance et traînée aérodynamique.

### Principe Mathématique
Chaque feuille \(i\) est régie par une équation de vortex hélicoïdal :
\[
\theta_i(t) = \theta_{0,i} + \omega \cdot t + \frac{k}{r_i}, \quad r_i(t) = R_0 + A \sin(\omega_r t + \phi_i)
\]
\[
z_i(t) = (z_{0,i} + v_z \cdot t) \pmod{H_{\max}}
\]
L'orientation (quaternion) de la feuille est couplée à la vitesse tangentielle avec un flottement pendulaire (fluttering) :
\[
\text{pitch}_i(t) = \sin(12 \cdot t + \phi_i) \cdot 0.35 \text{ rad}
\]

### Implémentation Three.js InstancedMesh (TypeScript)

```typescript
import * as THREE from 'three';

export class FlyingPaperVortex {
  public mesh: THREE.InstancedMesh;
  private count: number = 90;
  private dummy: THREE.Object3D = new THREE.Object3D();
  private particlesData: {
    angle: number;
    radius: number;
    y: number;
    angularSpeed: number;
    verticalSpeed: number;
    rotXSpeed: number;
    rotZSpeed: number;
  }[] = [];

  constructor() {
    // Géométrie d'une feuille A4 légèrement courbée
    const geometry = new THREE.PlaneGeometry(0.21, 0.297, 2, 2);
    // Double face obligatoire pour le papier tourbillonnant
    const material = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      roughness: 0.8,
      side: THREE.DoubleSide,
    });

    this.mesh = new THREE.InstancedMesh(geometry, material, this.count);

    for (let i = 0; i < this.count; i++) {
      this.particlesData.push({
        angle: Math.random() * Math.PI * 2,
        radius: 0.8 + Math.random() * 1.6,
        y: Math.random() * 3.0,
        angularSpeed: 1.5 + Math.random() * 2.0,
        verticalSpeed: 0.4 + Math.random() * 0.8,
        rotXSpeed: 2.0 + Math.random() * 4.0,
        rotZSpeed: 1.0 + Math.random() * 3.0,
      });
    }
  }

  public update(delta: number): void {
    for (let i = 0; i < this.count; i++) {
      const p = this.particlesData[i];
      p.angle += p.angularSpeed * delta;
      p.y += p.verticalSpeed * delta;

      // Boucle de réinitialisation au sol
      if (p.y > 3.5) {
        p.y = 0.2;
        p.radius = 0.6 + Math.random() * 1.8;
      }

      const x = Math.cos(p.angle) * p.radius;
      const z = Math.sin(p.angle) * p.radius;

      this.dummy.position.set(x, p.y, z);
      this.dummy.rotation.set(
        p.angle * 0.5 + Math.sin(p.y * 3) * 0.5,
        -p.angle + Math.PI / 2,
        Math.cos(p.angle * 2) * 0.3
      );
      this.dummy.updateMatrix();

      this.mesh.setMatrixAt(i, this.dummy.matrix);
    }
    this.mesh.instanceMatrix.needsUpdate = true;
  }
}
```

---

## Blueprint 6 : Ville de Données 3D & Égaliseur Isométrique

### Rôle & Contexte Visuel
Environnement de la scène 05 • ANALYZE (F0984-F1152). Une grille orthogonale de piliers 3D aux couleurs pop (jaune or, rose pâle, bleu cyan) qui pulsent comme les barres d'un analyseur de spectre musical en synchronisation avec le beat.

### Principe Mathématique
Pour chaque colonne à la coordonnée de grille \((i, j) \in [-N, N]^2\) :
\[
H(i, j, t) = H_{\text{base}} + A \cdot \left| \sin\left(\omega t - \frac{\sqrt{i^2 + j^2}}{\lambda}\right) \right| + \text{beatEnergy} \cdot \delta(i, j)
\]
Une onde circulaire d'amplitude se propage depuis le centre où se trouve la mascotte Clawd.

### Implémentation Three.js / React Three Fiber (TypeScript)

```tsx
import React, { useRef, useMemo } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';

export const DataCityscape: React.FC<{ beatProgress: number }> = ({ beatProgress }) => {
  const meshRef = useRef<THREE.InstancedMesh>(null!);
  const dummy = useMemo(() => new THREE.Object3D(), []);
  const gridSize = 14;
  const count = gridSize * gridSize;

  const colors = useMemo(() => {
    const palette = [
      new THREE.Color('#F7C844'), // Jaune or
      new THREE.Color('#F78FB3'), // Rose pastel
      new THREE.Color('#56CFE1'), // Cyan
    ];
    return Array.from({ length: count }, () => palette[Math.floor(Math.random() * palette.length)]);
  }, [count]);

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime();
    let idx = 0;

    for (let x = -gridSize / 2; x < gridSize / 2; x++) {
      for (let z = -gridSize / 2; z < gridSize / 2; z++) {
        const dist = Math.hypot(x, z);
        // Onde sinusoïdale radiale accentuée par le beat
        const height = 0.4 + Math.sin(t * 5.0 - dist * 0.4) * 0.8 + Math.max(0, Math.sin(t * 10)) * 1.2;

        dummy.position.set(x * 0.8, height / 2, z * 0.8);
        dummy.scale.set(0.65, height, 0.65);
        dummy.updateMatrix();

        meshRef.current.setMatrixAt(idx, dummy.matrix);
        meshRef.current.setColorAt(idx, colors[idx]);
        idx++;
      }
    }
    meshRef.current.instanceMatrix.needsUpdate = true;
    if (meshRef.current.instanceColor) meshRef.current.instanceColor.needsUpdate = true;
  });

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial roughness={0.3} metalness={0.1} />
    </instancedMesh>
  );
};
```

---

## Blueprint 7 : Rubans de Peinture 3D Extrudés & Éclaboussures Liquides

### Rôle & Contexte Visuel
Effet signature de la scène 06 • DESIGN (F1176-F1248). Clawd balaye l'espace avec un rouleau de peinture cyan, générant d'immenses rubans de peinture tridimensionnels luisants et cintrés en arc-en-ciel au-dessus de la pièce.

### Principe Mathématique
1. **Courbe Spline 3D de Trajectoire** :
   Modélisée via une spline Catmull-Rom cubique interpolant 5 points de contrôle :
   \[
   P(u) = \text{CatmullRom}(P_0, P_1, P_2, P_3, P_4, u), \quad u \in [0, 1]
   \]
2. **Extrusion Tubulaire avec Section Aplatie** :
   Génération d'une `TubeGeometry` ou extrusion de contour ruban le long de \(P(u)\).
3. **Animation de Déploiement Progressif** :
   Contrôle de la longueur visible via le paramètre de draw range ou un paramètre shader `uProgress \in [0, 1]` masquant les fragments où \(u > uProgress\).

### Implémentation Three.js (TypeScript)

```typescript
import * as THREE from 'three';

export class PaintRibbonSweep {
  public mesh: THREE.Mesh;
  private curve: THREE.CatmullRomCurve3;
  private material: THREE.MeshStandardMaterial;

  constructor(points: THREE.Vector3[], colorHex: string = '#FFD166') {
    this.curve = new THREE.CatmullRomCurve3(points);
    this.curve.curveType = 'centripetal';

    // Extrusion tubulaire lisse le long de la courbe
    const geometry = new THREE.TubeGeometry(this.curve, 80, 0.12, 16, false);

    // Matériau vernis laqué brillant (peinture fraîche)
    this.material = new THREE.MeshStandardMaterial({
      color: new THREE.Color(colorHex),
      roughness: 0.12,
      metalness: 0.05,
      clearcoat: 1.0,
      clearcoatRoughness: 0.1,
    });

    this.mesh = new THREE.Mesh(geometry, this.material);
    // Masquer le tracé initialement
    this.mesh.geometry.setDrawRange(0, 0);
  }

  public animateStroke(progress: number): void {
    // progress entre 0.0 et 1.0
    const clamped = THREE.MathUtils.clamp(progress, 0, 1);
    const totalIndices = this.mesh.geometry.attributes.position.count * 6;
    const currentDrawCount = Math.floor(totalIndices * clamped);
    this.mesh.geometry.setDrawRange(0, currentDrawCount);
  }
}
```

# 03. Blueprints de Fabrication & Recettes de Code

Ce document met à disposition des agents développeurs (Three.js/WebGL, GLSL, Remotion, Canvas 2D, SVG) les algorithmes, équations cinématiques et composants typés nécessaires à la ré-implémentation des six moteurs visuels maîtres de la vidéo `bn7Feycdb-j7Ejbq.mp4` (*UPPING MY P(DOOM) - MADEWITHV DnB REMIX*).

---

## 1. Moteur 1 : Typographie 3D Biseautée Chrome Liquide & Iridescence Fresnel

Utilisé pour : Tous les titres monumentaux (`SPARKS`, `LOSS`, `THE FUTURE GOES`, `LIES`, `OMEGA`, `ASKEW`, `ILYA`).

### Principe Géométrique & Shading
1. **Géométrie 3D extrudée** : Les glyphes sont créés via `TextGeometry` ou `FontLoader` avec un biseau prononcé (`bevelSegments: 5`, `bevelSize: 1.8`, `bevelThickness: 2.2`).
2. **Matériau Chrome Liquide (Shader personnalisé)** :
   - Réflectance d'environnement basée sur un vecteur de normale perturbé par une fonction d'onde fluide (vaguelette de métal liquide).
   - Terme de Fresnel non-linéaire qui injecte du cyan électrique (`#67D4E8`) et du pourpre iridescent (`#C4A7E7`) sur les faces rasantes (angle de vue tangentiel).
3. **Specular Glints à 4 branches** : Sur les sommets de normale orientée vers la caméra, projection d'un sprite additif cruciforme qui pulse au rythme des transitoires audio.

### Implémentation de Référence (Three.js / GLSL / TypeScript)

```typescript
import * as THREE from 'three';

export const LiquidChromeShader = {
  uniforms: {
    uTime: { value: 0.0 },
    uBaseColor: { value: new THREE.Color('#F0F9FE') },
    uIridescentCyan: { value: new THREE.Color('#67D4E8') },
    uIridescentPurple: { value: new THREE.Color('#C4A7E7') },
    uFresnelPower: { value: 3.5 },
    uWaveFrequency: { value: 2.4 },
    uWaveAmplitude: { value: 0.08 },
  },
  vertexShader: `
    varying vec3 vNormal;
    varying vec3 vViewPosition;
    varying vec2 vUv;
    varying vec3 vWorldPosition;
    uniform float uTime;
    uniform float uWaveFrequency;
    uniform float uWaveAmplitude;

    void main() {
      vUv = uv;
      vec3 transformedNormal = normalMatrix * normal;
      vNormal = normalize(transformedNormal);
      
      // Micro-ondulation de surface type métal liquide
      vec3 pos = position;
      float wave = sin(pos.x * uWaveFrequency + uTime * 2.0) * 
                   cos(pos.y * uWaveFrequency + uTime * 1.5) * uWaveAmplitude;
      pos += normal * wave;

      vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
      vViewPosition = -mvPosition.xyz;
      vWorldPosition = (modelMatrix * vec4(pos, 1.0)).xyz;
      gl_Position = projectionMatrix * mvPosition;
    }
  `,
  fragmentShader: `
    uniform vec3 uBaseColor;
    uniform vec3 uIridescentCyan;
    uniform vec3 uIridescentPurple;
    uniform float uFresnelPower;
    uniform float uTime;

    varying vec3 vNormal;
    varying vec3 vViewPosition;
    varying vec2 vUv;
    varying vec3 vWorldPosition;

    void main() {
      vec3 viewDir = normalize(vViewPosition);
      vec3 normal = normalize(vNormal);

      // Calcul de Fresnel
      float NdotV = max(dot(normal, viewDir), 0.0);
      float fresnel = pow(1.0 - NdotV, uFresnelPower);

      // Gradient d'iridescence angulaire
      float angleFactor = 0.5 + 0.5 * sin(dot(normal, vec3(1.0, 0.5, 0.0)) * 4.0 + uTime);
      vec3 iridescence = mix(uIridescentCyan, uIridescentPurple, angleFactor);

      // Réflectance spéculaire centrale
      vec3 lightDir = normalize(vec3(0.5, 1.0, 0.8));
      vec3 halfVector = normalize(lightDir + viewDir);
      float spec = pow(max(dot(normal, halfVector), 0.0), 64.0);

      // Composition finale
      vec3 color = mix(uBaseColor * 0.4, iridescence, fresnel);
      color += vec3(1.0) * spec * 1.8;

      gl_FragColor = vec4(color, 1.0);
    }
  `
};

export function createHeroChromeText(text: string, font: any): THREE.Mesh {
  const geometry = new (THREE as any).TextGeometry(text, {
    font: font,
    size: 24,
    height: 12,
    curveSegments: 12,
    bevelEnabled: true,
    bevelThickness: 2.2,
    bevelSize: 1.8,
    bevelOffset: 0,
    bevelSegments: 5,
  });
  geometry.center();

  const material = new THREE.ShaderMaterial({
    uniforms: THREE.UniformsUtils.clone(LiquidChromeShader.uniforms),
    vertexShader: LiquidChromeShader.vertexShader,
    fragmentShader: LiquidChromeShader.fragmentShader,
  });

  return new THREE.Mesh(geometry, material);
}
```

---

## 2. Moteur 2 : Oscilloscope Ondulant & Ruban Métallique 3D

Utilisé pour : La séquence *Stable Training Run* (01:10 - 01:25).

### Principe Géométrique
1. **Ruban extrudé 3D** : Génération d'une surface tubulaire ou ruban à deux faces le long d'une courbe de spline composée de `N = 256` points équidistants sur l'axe X.
2. **Modulation par audio et harmoniques** : À chaque frame `t`, la coordonnée Y de chaque point est la somme de plusieurs ondes sinusoïdales pondérées par l'énergie spectrale du signal audio :
   $$y(x, t) = \sum_{k=1}^{4} A_k \cdot \sin\left(\omega_k \cdot x + \phi_k \cdot t\right) \cdot \text{envelope}(x) \cdot \text{audioRMS}$$
3. **Texture de réflexion** : Le ruban possède une largeur Z constante de 8px et un biseau latéral blanc brillant qui reflète la nappe de lumière zénithale.

### Implémentation de Référence (TypeScript / Three.js)

```typescript
export class OscilloscopeRibbon {
  public mesh: THREE.Mesh;
  private geometry: THREE.PlaneGeometry;
  private numPoints = 256;
  private width = 1200;

  constructor() {
    // Ruban composé de (numPoints - 1) segments en longueur et 2 bandes en hauteur (Z)
    this.geometry = new THREE.PlaneGeometry(this.width, 16, this.numPoints - 1, 1);
    
    const material = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      metalness: 0.95,
      roughness: 0.1,
      emissive: new THREE.Color(0x9d4edd),
      emissiveIntensity: 0.45,
      side: THREE.DoubleSide,
    });

    this.mesh = new THREE.Mesh(this.geometry, material);
    this.mesh.rotation.x = Math.PI * 0.15; // Légère inclinaison vers la caméra
  }

  public update(frame: number, audioRms: number) {
    const pos = this.geometry.attributes.position;
    const time = frame * 0.05;

    for (let i = 0; i < this.numPoints; i++) {
      const u = i / (this.numPoints - 1);
      const x = (u - 0.5) * this.width;
      
      // Enveloppe d'atténuation aux extrémités
      const envelope = Math.sin(u * Math.PI);

      // Superposition d'harmoniques
      const h1 = Math.sin(u * 14.0 + time * 1.8) * 45.0;
      const h2 = Math.sin(u * 28.0 - time * 2.4) * 22.0;
      const h3 = Math.sin(u * 56.0 + time * 3.6) * 10.0;
      
      const y = (h1 + h2 + h3) * envelope * (0.6 + audioRms * 1.5);

      // Mise à jour des deux sommets haut et bas du ruban
      pos.setY(i, y + 8);
      pos.setY(i + this.numPoints, y - 8);
    }

    pos.needsUpdate = true;
    this.geometry.computeVertexNormals();
  }
}
```

---

## 3. Moteur 3 : Déconstruction & Réassemblage Atomique des Glyphes

Utilisé pour : La séquence *I feel my atoms rearranging* (01:25 - 01:42).

### Principe Physique
1. **Double état de coordonnées pour chaque lettre** :
   - État initial ordonné : Position de base dans la chaîne cible (`REARRANGING`).
   - État dispersé stochastique : Coordonnées 3D chaotiques calculées par un bruit de Simplex vectoriel 3D.
2. **Transition non-linéaire par force magnétique** :
   Chaque lettre $i$ possède un décalage temporel individuel $\tau_i$ pour éviter une animation monolithique :
   $$\text{prog}_i = \text{clamp}\left(\frac{t - \tau_i}{\Delta t}, 0, 1\right)$$
   $$P_i(t) = \text{lerp}\left(P_{\text{chaos}}, P_{\text{target}}, \text{easeOutElastic}(\text{prog}_i)\right)$$
3. **Micro-étincelles d'accouplement** : Dès qu'une lettre s'approche à moins de 15px de son ancrage définitif, génération d'une impulsion lumineuse sphérique (point light flash).

### Implémentation de Référence (TypeScript / Remotion)

```typescript
import { interpolate, spring } from 'remotion';

export interface GlyphState {
  char: string;
  targetX: number;
  targetY: number;
  scatterX: number;
  scatterY: number;
  scatterRotZ: number;
  delayFrame: number;
}

export function buildRearrangingWord(word = "REARRANGING", baseFrame = 5100): GlyphState[] {
  const letters = word.split("");
  const totalWidth = letters.length * 64;
  const startX = 960 - totalWidth / 2;

  return letters.map((char, index) => {
    // Calcul de dispersion pseudo-aléatoire déterministe
    const seed = index * 73.19;
    const scatterAngle = (Math.sin(seed) * Math.PI * 2);
    const scatterDist = 280 + (Math.cos(seed * 2.3) * 180);

    return {
      char,
      targetX: startX + index * 64,
      targetY: 540,
      scatterX: 960 + Math.cos(scatterAngle) * scatterDist,
      scatterY: 540 + Math.sin(scatterAngle) * scatterDist * 0.6,
      scatterRotZ: (Math.sin(seed * 3.1) * 60), // rotation en degrés
      delayFrame: baseFrame + index * 4, // cascade à la croche (10 frames)
    };
  });
}

export function computeGlyphTransform(glyph: GlyphState, currentFrame: number, fps = 60) {
  const spr = spring({
    frame: Math.max(0, currentFrame - glyph.delayFrame),
    fps,
    config: {
      mass: 0.9,
      stiffness: 180,
      damping: 16,
    },
  });

  const x = interpolate(spr, [0, 1], [glyph.scatterX, glyph.targetX]);
  const y = interpolate(spr, [0, 1], [glyph.scatterY, glyph.targetY]);
  const rot = interpolate(spr, [0, 1], [glyph.scatterRotZ, 0]);
  const opacity = interpolate(spr, [0, 0.2, 1], [0.3, 0.9, 1.0]);

  return { x, y, rot, opacity, springProgress: spr };
}
```

---

## 4. Moteur 4 : Tunnel de Géode Cristalline & Portails Incurvés

Utilisé pour : Le tunnel d'améthyste (02:02 - 02:15) et le portail contemplatif *We'll never know* (03:25 - 03:38).

### Principe Géométrique
1. **Extrusion le long d'une courbe 3D (Frenet-Serret Frame)** :
   Un chemin spliné fermé ou infini $C(s)$ oriente une série d'anneaux polygonaux (dodécagones ou rectangles arrondis).
2. **Instanced Mesh de Cristaux Prismatiques** :
   Sur chaque sommet des anneaux, instanciation d'un prisme hexagonal effilé (`CylinderGeometry` avec 6 segments et apex pointu).
3. **Matériau Réfractif Améthyste (Fake Dispersion)** :
   Texture d'environnement projetée en coordonnées sphériques avec variation d'indice de réfraction pour séparer les canaux R, G et B (dispersion chromatique interne).

### Implémentation de Référence (Three.js / TypeScript)

```typescript
export class CrystalWarpTunnel {
  public group: THREE.Group;
  private ringCount = 36;
  private radius = 80;
  private length = 900;
  private rings: THREE.Group[] = [];

  constructor() {
    this.group = new THREE.Group();
    const crystalGeo = new THREE.ConeGeometry(6, 32, 6);
    crystalGeo.rotateX(Math.PI / 2);

    const crystalMat = new THREE.MeshPhysicalMaterial({
      color: 0xb57edc,
      transmission: 0.85,
      opacity: 1,
      transparent: true,
      roughness: 0.12,
      ior: 1.54,
      thickness: 8.0,
      specularColor: new THREE.Color(0xffffff),
    });

    for (let r = 0; r < this.ringCount; r++) {
      const ringGroup = new THREE.Group();
      const z = -r * (this.length / this.ringCount);
      ringGroup.position.z = z;

      const segments = 12;
      for (let s = 0; s < segments; s++) {
        const theta = (s / segments) * Math.PI * 2;
        const crystal = new THREE.Mesh(crystalGeo, crystalMat);
        
        crystal.position.x = Math.cos(theta) * this.radius;
        crystal.position.y = Math.sin(theta) * this.radius;
        crystal.lookAt(0, 0, z); // Pointe orientée vers l'intérieur du tunnel

        ringGroup.add(crystal);
      }

      this.rings.push(ringGroup);
      this.group.add(ringGroup);
    }
  }

  public update(speed = 4.5) {
    for (const ring of this.rings) {
      ring.position.z += speed;
      // Recyclage infini du tunnel
      if (ring.position.z > 50) {
        ring.position.z -= this.length;
      }
      // Rotation hélicoïdale continue
      ring.rotation.z += 0.005;
    }
  }
}
```

---

## 5. Moteur 5 : Chaîne de Barrières de Sécurité Séparables (Safety Fence Breach)

Utilisé pour : La séquence *Breaking through each safety fence* (02:26 - 02:40).

### Principe Cinématique
1. **Rail horizontal compartimenté** :
   Alignement de conteneurs rectangulaires en verre technique (`v1.1` à `v1.5`), séparés par des montants doubles verticaux.
2. **Détection de rupture à la tête de lecture** :
   Lorsque la coordonnée du pointeur franchit le bord gauche du module $k$, bascule d'état de `SAFE` (`#9381FF`) à `BREACHED` (`#EF4444` puis éclatement).
3. **Particules de fracturation polygonale** :
   Chaque panneau de verre se décompose en 8 à 14 fragments triangulaires animés d'une vélocité divergente vers l'avant (axe Z caméra) avec rotation rapide.

### Implémentation de Référence (Canvas 2D / TypeScript)

```typescript
export interface FenceModule {
  id: string;
  version: string;
  x: number;
  width: number;
  height: number;
  breached: boolean;
  breachProgress: number;
}

export class SafetyFenceRail {
  private modules: FenceModule[] = [];

  constructor() {
    const versions = ['v1.1', 'v1.2', 'v1.3', 'v1.4', 'v1.5'];
    let currentX = 240;

    versions.forEach((ver, i) => {
      this.modules.push({
        id: `fence-${i}`,
        version: ver,
        x: currentX,
        width: 260,
        height: 72,
        breached: false,
        breachProgress: 0,
      });
      currentX += 300;
    });
  }

  public update(cursorX: number) {
    for (const m of this.modules) {
      if (cursorX >= m.x && !m.breached) {
        m.breached = true;
      }
      if (m.breached && m.breachProgress < 1.0) {
        m.breachProgress = Math.min(1.0, m.breachProgress + 0.08);
      }
    }
  }

  public render(ctx: CanvasRenderingContext2D) {
    ctx.save();
    for (const m of this.modules) {
      if (m.breachProgress >= 1.0) continue; // Totalement détruit

      const alpha = 1.0 - m.breachProgress;
      const strokeColor = m.breached ? `rgba(239, 68, 68, ${alpha})` : `rgba(147, 129, 255, 0.8)`;
      const fillColor = m.breached ? `rgba(239, 68, 68, ${alpha * 0.15})` : `rgba(20, 20, 28, 0.6)`;

      ctx.strokeStyle = strokeColor;
      ctx.fillStyle = fillColor;
      ctx.lineWidth = 2;

      // Cadre extérieur
      ctx.strokeRect(m.x, 740, m.width, m.height);
      ctx.fillRect(m.x, 740, m.width, m.height);

      // Séparateurs intérieurs verticaux
      for (let div = 1; div <= 3; div++) {
        const dx = m.x + (m.width / 4) * div;
        ctx.beginPath();
        ctx.moveTo(dx, 740);
        ctx.lineTo(dx, 740 + m.height);
        ctx.stroke();
      }

      // Libellé de version
      ctx.fillStyle = m.breached ? '#EF4444' : '#94A3B8';
      ctx.font = '12px "JetBrains Mono", monospace';
      ctx.fillText(`SAFETY FENCE ${m.version}`, m.x + 12, 835);
    }
    ctx.restore();
  }
}
```

---

## 6. Moteur 6 : Télémétrie HUD Temps Réel & Double Ticker Infini

Utilisé pour : Le bandeau haut/bas et le module permanent `P(DOOM)` sur l'intégralité des 230 secondes.

### Principe d'Ingénierie
1. **Double Ruban Infini Sans Rupture (Seamless Loop)** :
   Une chaîne unitaire de texte est dupliquée $K$ fois. La translation horizontale $X(t) = -(t \cdot v) \pmod L$ garantit une absence totale d'interruption visuelle.
2. **Progression Non-Linéaire de P(DOOM)** :
   Interpolation par morceaux (*piecewise spline*) connectant rigoureusement les valeurs clés de chaque drop et stabilisations narratives, jusqu'à la bascule finale vers la valeur spéciale `NaN`.

### Implémentation de Référence (TypeScript / Remotion)

```typescript
export interface TelemetryPoint {
  frame: number;
  value: number | 'NaN';
  status: string;
}

export const P_DOOM_TIMELINE: TelemetryPoint[] = [
  { frame: 0,     value: 0.0,   status: 'INIT' },
  { frame: 360,   value: 2.5,   status: 'MONITORING' },
  { frame: 1440,  value: 3.8,   status: 'MONITORING' },
  { frame: 2040,  value: 4.3,   status: 'EVALUATING' },
  { frame: 2460,  value: 12.9,  status: 'ELEVATED' },     // Drop 1
  { frame: 3480,  value: 13.8,  status: 'ELEVATED' },
  { frame: 4200,  value: 17.2,  status: 'ACTIVE' },
  { frame: 5100,  value: 18.0,  status: 'ACTIVE' },
  { frame: 6120,  value: 47.3,  status: 'HIGH' },         // Drop 2 Omega
  { frame: 8100,  value: 49.7,  status: 'HIGH' },
  { frame: 8760,  value: 55.0,  status: 'CRITICAL' },
  { frame: 9600,  value: 61.8,  status: 'STABLE' },       // Safety Fences
  { frame: 11100, value: 86.0,  status: 'ROUNDED UP' },    // GPU clusters
  { frame: 12300, value: 94.0,  status: 'ROUNDED UP' },
  { frame: 13080, value: 98.5,  status: 'CONVERGENCE' },
  { frame: 13260, value: 99.96, status: 'SINGULARITY' },
  { frame: 13320, value: 'NaN', status: 'OVERFLOW' },      // Outro crash
];

export function getPDoomStateAtFrame(frame: number): { displayValue: string; status: string; progressRatio: number } {
  // Détection du segment
  for (let i = 0; i < P_DOOM_TIMELINE.length - 1; i++) {
    const p1 = P_DOOM_TIMELINE[i];
    const p2 = P_DOOM_TIMELINE[i + 1];

    if (frame >= p1.frame && frame <= p2.frame) {
      if (p2.value === 'NaN') {
        return { displayValue: 'NaN', status: p2.status, progressRatio: 1.0 };
      }
      
      const t = (frame - p1.frame) / (p2.frame - p1.frame);
      const v = (p1.value as number) + t * ((p2.value as number) - (p1.value as number));
      return {
        displayValue: `${v.toFixed(1)}%`,
        status: p1.status,
        progressRatio: Math.min(1.0, v / 100.0),
      };
    }
  }

  return { displayValue: 'NaN', status: 'OVERFLOW', progressRatio: 1.0 };
}

export function renderRunningTicker(ctx: CanvasRenderingContext2D, y: number, frame: number, speed = 3.5) {
  const textUnit = "UPPING MY P(DOOM) - MADEWITHV - ";
  ctx.save();
  ctx.font = '600 11px "JetBrains Mono", monospace';
  ctx.fillStyle = '#9381FF';
  ctx.letterSpacing = '0.18em';

  const unitWidth = ctx.measureText(textUnit).width;
  const offset = -(frame * speed) % unitWidth;

  const count = Math.ceil(1920 / unitWidth) + 2;
  for (let i = 0; i < count; i++) {
    ctx.fillText(textUnit, offset + i * unitWidth, y);
  }
  ctx.restore();
}
```

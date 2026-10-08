# 03. Blueprints de Fabrication & Recettes de Code

Ce document met à disposition des agents de développement (Remotion, WebGL/Three.js, Canvas 2D, SVG/GSAP) les algorithmes, formules mathématiques et architectures logicielles typées pour ré-implémenter les six moteurs visuels les plus sophistiqués de la vidéo `juiGldW_-J9pBs0s.mp4`.

---

## 1. Moteur 1 : Déploiement Cinématique de l'Astérisque Claude & Streak Flare

Utilisé pour : L'ouverture cinématique (00:00 - 00:05), l'apparition des cartes de titre (00:20), le packshot final (01:08) et la rétraction horlogère de clôture (01:14).

### 1.1. Principe Géométrique & Physique
1. **Géométrie des branches** : L'astérisque Anthropic est constitué de 12 branches arrondies réparties tous les $30^\circ$ ($\Delta\theta = \pi / 6$), avec une alternance de longueurs de rayons intérieurs/extérieurs (branches majeures $R_1 \approx 120\text{px}$, branches mineures $R_2 \approx 95\text{px}$).
2. **Cinématique de radar** : En phase d'intro, une aiguille directrice tourne à vitesse angulaire constante $\omega_0$. À chaque fois qu'elle franchit un angle de branche $\theta_k = k \cdot \pi / 6$, la branche correspondante est instanciée et jaillit depuis le centre avec un ressort suramorti (`stiffness: 300, damping: 25`).
3. **Faisceau anamorphique (Streak Flare)** : Un gradient horizontal additif simulant une lentille anamorphique cinématographique, traversant le centre focal et décroissant exponentiellement sur l'axe vertical :
   $$I(x, y) = I_0 \cdot \exp\left(-\frac{|y - y_0|}{\sigma_y}\right) \cdot \left(1 - \frac{|x - x_0|}{W/2}\right)^2$$

### 1.2. Implémentation de Référence (TypeScript / Remotion + Canvas 2D)

```typescript
import React, { useRef, useEffect } from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

interface AsteriskArm {
  angleRad: number;
  length: number;
  width: number;
  targetScale: number;
}

export const ClaudeAsteriskCanvas: React.FC<{
  color?: string;
  glowColor?: string;
  isUnwinding?: boolean;
}> = ({
  color = '#CC7152',
  glowColor = '#E99372',
  isUnwinding = false,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const centerX = width / 2;
  const centerY = height / 2;
  const totalArms = 12;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, width, height);

    // 1. Rendu du Streak Flare anamorphique horizontal
    const flareProgress = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
    const flareGrad = ctx.createLinearGradient(0, centerY, width, centerY);
    flareGrad.addColorStop(0, 'rgba(204, 113, 82, 0)');
    flareGrad.addColorStop(0.3, `rgba(204, 113, 82, ${0.15 * flareProgress})`);
    flareGrad.addColorStop(0.5, `rgba(233, 147, 114, ${0.85 * flareProgress})`);
    flareGrad.addColorStop(0.7, `rgba(204, 113, 82, ${0.15 * flareProgress})`);
    flareGrad.addColorStop(1, 'rgba(204, 113, 82, 0)');

    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    ctx.fillStyle = flareGrad;
    ctx.fillRect(0, centerY - 1.5, width, 3);

    // Halo diffus central
    const radialGlow = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 160);
    radialGlow.addColorStop(0, `rgba(240, 140, 105, ${0.5 * flareProgress})`);
    radialGlow.addColorStop(0.4, `rgba(204, 113, 82, ${0.2 * flareProgress})`);
    radialGlow.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = radialGlow;
    ctx.beginPath();
    ctx.arc(centerX, centerY, 160, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // 2. Rendu des branches de l'astérisque
    ctx.save();
    ctx.translate(centerX, centerY);

    for (let i = 0; i < totalArms; i++) {
      const angle = (i * Math.PI) / 6;
      const isMajor = i % 2 === 0;
      const baseLength = isMajor ? 110 : 88;
      const armWidth = 14;

      // Déclenchement séquentiel frame-accurate par rotation radar
      const armDelayFrames = isUnwinding ? (totalArms - 1 - i) * 6 : i * 6;
      const armSpring = spring({
        frame: frame - armDelayFrames,
        fps,
        config: { damping: 22, stiffness: 280, mass: 0.9 },
      });

      const currentScale = isUnwinding ? 1 - armSpring : armSpring;
      if (currentScale <= 0.001) continue;

      ctx.save();
      ctx.rotate(angle);

      // Branche avec extrémités arrondies (pill shape)
      ctx.beginPath();
      const armLen = baseLength * currentScale;
      ctx.roundRect(-armWidth / 2, -armLen, armWidth, armLen, armWidth / 2);
      ctx.fillStyle = color;
      ctx.fill();

      // Halo additif sur la branche
      ctx.shadowColor = glowColor;
      ctx.shadowBlur = 16 * currentScale;
      ctx.fill();

      ctx.restore();
    }

    // Noyau central
    ctx.beginPath();
    ctx.arc(0, 0, 14, 0, Math.PI * 2);
    ctx.fillStyle = glowColor;
    ctx.fill();

    ctx.restore();
  }, [frame, fps, width, height, color, glowColor, isUnwinding, centerX, centerY]);

  return <canvas ref={canvasRef} width={width} height={height} style={{ width: '100%', height: '100%' }} />;
};
```

---

## 2. Moteur 2 : Vortex de Tokens Orbitaux & Fly-Through 3D (Accretion Disk)

Utilisé pour : La séquence "From question to finished work" (00:11 - 00:20).

### 2.1. Principe Géométrique & Dynamique
1. **Distribution annulaire képlérienne** : $N$ tokens textuels (`refactor`, `build`, `test`, `schema`, `git push`, etc.) sont répartis sur $M=5$ anneaux concentriques de rayons $r_m = r_0 + m \cdot \Delta r$.
2. **Vitesse angulaire différentielle** : Selon les lois de la gravitation de Kepler, la vitesse angulaire diminue avec la distance :
   $$\omega(r) = \omega_0 \cdot \left(\frac{r_0}{r}\right)^{1.2}$$
3. **Plongée caméra en Warp Speed** : La coordonnée caméra $Z_{\text{cam}}$ avance exponentiellement vers le noyau. Les coordonnées 3D projetées sur l'écran 2D suivent la projection perspective standard :
   $$X_{\text{proj}} = \frac{X \cdot f}{Z - Z_{\text{cam}}} + X_{\text{center}}, \quad Y_{\text{proj}} = \frac{Y \cdot f}{Z - Z_{\text{cam}}} + Y_{\text{center}}$$
   Lorsque $Z - Z_{\text{cam}} \to 0$, les tokens subissent un étirement radial le long de leur vecteur de fuite (radial blur / speed streaks).

### 2.2. Implémentation de Référence (TypeScript / Canvas 2D Vectoriel)

```typescript
interface OrbitalToken {
  text: string;
  radius: number;
  initialAngle: number;
  zDepth: number;
  isAccent: boolean;
}

export class AccretionDiskEngine {
  private tokens: OrbitalToken[] = [];
  private tokenVocab = [
    'refactor', 'plan', 'diff', 'build', 'test', 'PR #2841', 'schema',
    'await', 'SELECT', '<div>', 'fn', 'git push', 'Rust', 'PDF',
    'cache', 'invoice', 'Q3', 'contract', 'insight', 'hypothesis'
  ];

  constructor(ringCount = 5, tokensPerRing = 8) {
    for (let ring = 1; ring <= ringCount; ring++) {
      const radius = 120 + ring * 85;
      for (let i = 0; i < tokensPerRing; i++) {
        const text = this.tokenVocab[(ring * tokensPerRing + i) % this.tokenVocab.length];
        this.tokens.push({
          text,
          radius,
          initialAngle: (i * 2 * Math.PI) / tokensPerRing + (ring * 0.4),
          zDepth: (ring - 1) * 60,
          isAccent: (ring + i) % 4 === 0,
        });
      }
    }
  }

  render(ctx: CanvasRenderingContext2D, width: number, height: number, progress: number) {
    const centerX = width * 0.68; // Centré sur le 2/3 droit de l'écran
    const centerY = height * 0.5;
    const fov = 750;

    // Progression de plongée caméra (dolly-in)
    const cameraZ = progress * 600;
    const speedBoost = 1 + progress * 4;

    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    for (const token of this.tokens) {
      // Rotation différentielle
      const angularVelocity = (0.012 * Math.pow(200 / token.radius, 1.1)) * speedBoost;
      const currentAngle = token.initialAngle + angularVelocity * progress * 300;

      const worldX = Math.cos(currentAngle) * token.radius;
      const worldY = Math.sin(currentAngle) * token.radius;
      const worldZ = token.zDepth - cameraZ + 500;

      if (worldZ <= 10) continue; // Derrière la caméra

      const scale = fov / worldZ;
      const screenX = centerX + worldX * scale;
      const screenY = centerY + worldY * scale;

      const alpha = Math.min(1, Math.max(0, (worldZ - 20) / 200)) * (scale > 3 ? Math.max(0, 1 - (scale - 3) / 2) : 1);
      if (alpha <= 0.02) continue;

      ctx.save();
      ctx.translate(screenX, screenY);
      // Rotation tangentielle pour épouser l'orbite
      ctx.rotate(currentAngle + Math.PI / 2);

      const fontSize = Math.max(8, 14 * scale);
      ctx.font = `${token.isAccent ? '600' : '400'} ${fontSize}px "Berkeley Mono", monospace`;
      ctx.fillStyle = token.isAccent
        ? `rgba(204, 113, 82, ${alpha * 0.95})`
        : `rgba(243, 239, 230, ${alpha * 0.75})`;

      // Étirement radial en fin de warp
      if (progress > 0.6) {
        const streakLength = (progress - 0.6) * 2.5 * scale;
        ctx.scale(1, 1 + streakLength);
      }

      ctx.fillText(token.text, 0, 0);
      ctx.restore();
    }

    ctx.restore();
  }
}
```

---

## 3. Moteur 3 : Fenêtre 3D en Perspective & Curseur Automate (Computer Use)

Utilisé pour : La démonstration interactive du benchmark OSWorld 2.0 (00:28 - 00:30).

### 3.1. Principe de Projection & Animation d'Action
1. **Transformation spatiale 3D** :
   ```css
   transform: perspective(1200px) rotateY(-11deg) rotateX(4deg) translateZ(0);
   transform-style: preserve-3d;
   ```
2. **Trajectoire du curseur (Cubic Bézier Interpolation)** : Le curseur se déplace entre des cibles discrètes (point repos $\to$ champ `Tax ID` $\to$ bouton `Save & send`) en suivant une courbe de Bézier avec inertie et tremblement micro-humain.
3. **Labels d'intention d'agent** : Une bulle d'état attachée au curseur (`typing: tax id`) s'affiche pendant la phase de frappe avec fondu d'opacité `cubic-bezier(0.16, 1, 0.3, 1)`.

### 3.2. Implémentation de Référence (React / Remotion + Styled CSS)

```tsx
import React from 'react';
import { useCurrentFrame, interpolate, spring, useVideoConfig } from 'remotion';

export const ComputerUseShowcase: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 1. Animation d'entrée de la fenêtre (snap-in depuis la droite)
  const windowSpring = spring({
    frame,
    fps,
    config: { damping: 20, stiffness: 220, mass: 1 },
  });
  const windowTranslateX = interpolate(windowSpring, [0, 1], [400, 0]);
  const windowOpacity = interpolate(windowSpring, [0, 1], [0, 1]);

  // 2. Trajectoire du curseur de souris
  // Frame 20-45 : déplacement vers le champ Tax ID (X: 380, Y: 180)
  // Frame 45-75 : frappe du texte
  // Frame 75-100 : déplacement vers le bouton Save & send (X: 180, Y: 320)
  // Frame 100-110 : clic
  const cursorX = interpolate(frame, [20, 45, 75, 100], [500, 380, 380, 180], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const cursorY = interpolate(frame, [20, 45, 75, 100], [400, 180, 180, 320], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const isTyping = frame >= 45 && frame <= 75;
  const typedCharsCount = Math.floor(interpolate(frame, [45, 72], [0, 13], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const fullTaxId = 'US-84-1900733';
  const displayedTaxId = fullTaxId.slice(0, typedCharsCount);

  const isClicked = frame >= 100 && frame <= 108;

  return (
    <div
      style={{
        position: 'relative',
        width: 860,
        height: 540,
        transform: `perspective(1200px) rotateY(-11deg) rotateX(4deg) translateX(${windowTranslateX}px)`,
        opacity: windowOpacity,
        borderRadius: 16,
        backgroundColor: '#F5F2EB',
        boxShadow: '0 30px 60px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(204, 113, 82, 0.25)',
        overflow: 'hidden',
        fontFamily: '"Favorit", sans-serif',
      }}
    >
      {/* Barre de titre macOS */}
      <div style={{ height: 36, backgroundColor: '#EBE7DE', display: 'flex', alignItems: 'center', padding: '0 14px' }}>
        <div style={{ display: 'flex', gap: 6 }}>
          <div style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: '#FF5F56' }} />
          <div style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: '#FFBD2E' }} />
          <div style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: '#27C93F' }} />
        </div>
        <span style={{ marginLeft: 16, fontSize: 11, color: '#7A756D', fontFamily: 'monospace' }}>
          Claude • computer use — erp.company.com
        </span>
      </div>

      {/* Contenu Formulaire ERP */}
      <div style={{ padding: 32, color: '#1A1917' }}>
        <h2 style={{ fontSize: 24, fontWeight: 700, margin: '0 0 24px 0' }}>Nowa faktura</h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
          <div>
            <label style={{ fontSize: 11, color: '#7A756D', display: 'block', marginBottom: 6 }}>Customer</label>
            <div style={{ background: '#FFF', border: '1px solid #D6D1C7', borderRadius: 8, padding: '10px 14px', fontSize: 14 }}>
              Grain Coffee Co.
            </div>
          </div>

          <div>
            <label style={{ fontSize: 11, color: '#7A756D', display: 'block', marginBottom: 6 }}>Tax ID</label>
            <div
              style={{
                background: '#FFF',
                border: isTyping ? '2px solid #CC7152' : '1px solid #D6D1C7',
                borderRadius: 8,
                padding: '9px 13px',
                fontSize: 14,
                fontFamily: 'monospace',
                minHeight: 20,
              }}
            >
              {displayedTaxId}
              {isTyping && <span style={{ color: '#CC7152', animation: 'blink 0.8s infinite' }}>|</span>}
            </div>
          </div>
        </div>

        <button
          style={{
            marginTop: 28,
            backgroundColor: isClicked ? '#A85238' : '#CC7152',
            color: '#FFF',
            border: 'none',
            borderRadius: 8,
            padding: '12px 24px',
            fontSize: 14,
            fontWeight: 600,
            transform: isClicked ? 'scale(0.96)' : 'scale(1)',
          }}
        >
          Save & send
        </button>
      </div>

      {/* Curseur de souris dynamique avec étiquette d'action */}
      <div
        style={{
          position: 'absolute',
          left: cursorX,
          top: cursorY,
          pointerEvents: 'none',
          transition: 'transform 0.05s linear',
        }}
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
          <path d="M4 2L20 12L12 14L8 22L4 2Z" fill="#111" stroke="#FFF" strokeWidth="2" strokeLinejoin="round" />
        </svg>

        {isTyping && (
          <div
            style={{
              position: 'absolute',
              left: 20,
              top: 10,
              backgroundColor: '#CC7152',
              color: '#FFF',
              fontSize: 11,
              fontFamily: 'monospace',
              padding: '2px 8px',
              borderRadius: 4,
              whiteSpace: 'nowrap',
            }}
          >
            typing: tax id
          </div>
        )}
      </div>
    </div>
  );
};
```

---

## 4. Moteur 4 : Matrice de Migration Diagonale en 432 Tuiles

Utilisé pour : La visualisation de conversion massive Python $\to$ Rust (00:48 - 00:51).

### 4.1. Algorithme de Front d'Onde Diagonal
1. **Topologie de la grille** : Matrice $24 \times 18 = 432$ tuiles (représentant `432 files`).
2. **Distance au front d'onde** : Pour chaque tuile de coordonnées $(c, r)$ avec $c \in [0, 23]$ et $r \in [0, 17]$ :
   $$d(c, r) = \frac{c}{24} + \frac{r}{18} + \text{noise}(c, r) \cdot 0.15$$
3. **Fonction de bascule (Flip 3D)** :
   À l'instant $t$, le front avance de $0$ à $2.2$ :
   $$\text{phase}(c, r, t) = \text{clamp}\left(\frac{t - d(c, r)}{\Delta t_{\text{flip}}}, 0, 1\right)$$
   L'angle de rotation 3D est $\theta = \text{phase} \cdot 180^\circ$.
   - Pour $\theta < 90^\circ$ : Face avant visible (Python, teinte corail/brique `#CC7152`).
   - Pour $\theta \ge 90^\circ$ : Face arrière visible (Rust, teinte ivoire/bleu `#F3EFE6`).

### 4.2. Implémentation de Référence (TypeScript / React)

```tsx
import React, { useMemo } from 'react';
import { useCurrentFrame, interpolate } from 'remotion';

const COLS = 24;
const ROWS = 18;
const TOTAL_TILES = COLS * ROWS; // 432

export const CodeMigrationMatrix: React.FC<{ progress: number }> = ({ progress }) => {
  // Génération déterministe du bruit de front d'onde
  const tileDelays = useMemo(() => {
    const delays: number[] = [];
    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        const normDist = (c / COLS) * 0.6 + (r / ROWS) * 0.4;
        const pseudoNoise = ((Math.sin(c * 12.9898 + r * 78.233) * 43758.5453) % 1) * 0.12;
        delays.push(normDist + pseudoNoise);
      }
    }
    return delays;
  }, []);

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${COLS}, 14px)`,
        gridTemplateRows: `repeat(${ROWS}, 14px)`,
        gap: 3,
        perspective: 800,
      }}
    >
      {tileDelays.map((delay, idx) => {
        // Progression de rotation de la tuile spécifique
        const tileProgress = interpolate(progress, [delay, delay + 0.15], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });

        const rotateY = tileProgress * 180;
        const isFlipped = tileProgress >= 0.5;

        return (
          <div
            key={idx}
            style={{
              width: 14,
              height: 14,
              borderRadius: 2,
              transform: `rotateY(${rotateY}deg)`,
              transformStyle: 'preserve-3d',
              backgroundColor: isFlipped ? '#F3EFE6' : '#CC7152',
              boxShadow: isFlipped ? '0 0 6px rgba(243, 239, 230, 0.4)' : 'none',
              transition: 'background-color 0.05s',
            }}
          />
        );
      })}
    </div>
  );
};
```

---

## 5. Moteur 5 : Jauge de Thinking Budget & Mascotte Pixel Suiveuse

Utilisé pour : Le curseur de pensée "You decide how hard it thinks" (00:54 - 00:58).

### 5.1. Principe de Sprite & Magnétisme des Paliers
1. **Matrice de pixels de la mascotte (11x8)** :
   ```
   . . x x x x x x x . .
   . x x x x x x x x x .
   x x x . x x x . x x x
   x x x . x x x . x x x
   x x x x x x x x x x x
   . x x x x x x x x x .
   . x . x . . . x . x .
   . x . x . . . x . x .
   ```
2. **Course non-linéaire avec arrêts magnétiques** :
   Le curseur progresse de `LOW` ($0\%$) à `HIGH` ($50\%$) puis `XHIGH` ($75\%$).
   À chaque cran, amortissement prononcé et surbrillance du texte correspondant.
3. **Aura énergétique (Thinking Halo)** : À partir du niveau `HIGH`, une ondulation sinusoïdale de lueur radiale corail enveloppe la mascotte :
   $$R_{\text{glow}}(t) = R_0 + 6\text{px} \cdot \sin(2\pi \cdot f_{\text{pulse}} \cdot t)$$

### 5.2. Implémentation de Référence (TypeScript / SVG + React)

```tsx
import React from 'react';
import { useCurrentFrame, interpolate, spring, useVideoConfig } from 'remotion';

// Matrice binaire du sprite 11x8
const MASCOT_PIXELS = [
  [0,0,1,1,1,1,1,1,1,0,0],
  [0,1,1,1,1,1,1,1,1,1,0],
  [1,1,1,0,1,1,1,0,1,1,1],
  [1,1,1,0,1,1,1,0,1,1,1],
  [1,1,1,1,1,1,1,1,1,1,1],
  [0,1,1,1,1,1,1,1,1,1,0],
  [0,1,0,1,0,0,0,1,0,1,0],
  [0,1,0,1,0,0,0,1,0,1,0],
];

const TIERS = ['LOW', 'MEDIUM', 'HIGH', 'XHIGH', 'MAX'];

export const ThinkingBudgetSlider: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Trajectoire frame-accurate : Frame 0-30 à LOW, 30-70 vers HIGH, 80-120 vers XHIGH
  const sliderPercent = interpolate(frame, [20, 60, 80, 115], [0, 0.5, 0.5, 0.75], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const trackWidth = 720;
  const currentHandleX = sliderPercent * trackWidth;

  // Animation de pulsation de l'aura de réflexion
  const pulse = Math.sin((frame / fps) * Math.PI * 4) * 0.5 + 0.5;
  const glowOpacity = interpolate(sliderPercent, [0.3, 0.6], [0, 0.8], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <div style={{ position: 'relative', width: trackWidth, margin: '0 auto', userSelect: 'none' }}>
      {/* Rail du Slider */}
      <div style={{ position: 'relative', width: '100%', height: 4, backgroundColor: 'rgba(255, 255, 255, 0.2)', borderRadius: 2 }}>
        {/* Rail actif rempli */}
        <div style={{ width: currentHandleX, height: '100%', backgroundColor: '#CC7152', borderRadius: 2 }} />

        {/* Bouton du Slider */}
        <div
          style={{
            position: 'absolute',
            left: currentHandleX,
            top: '50%',
            transform: 'translate(-50%, -50%)',
            width: 14,
            height: 14,
            borderRadius: '50%',
            backgroundColor: '#FFF',
            boxShadow: '0 0 10px rgba(204, 113, 82, 0.8)',
          }}
        />

        {/* Mascotte Pixel perchée sur le bouton */}
        <div
          style={{
            position: 'absolute',
            left: currentHandleX,
            top: -46,
            transform: 'translateX(-50%)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          {/* Halo d'aura incandescente */}
          <div
            style={{
              position: 'absolute',
              width: 64,
              height: 64,
              borderRadius: '50%',
              background: `radial-gradient(circle, rgba(204, 113, 82, ${glowOpacity * (0.4 + 0.3 * pulse)}) 0%, transparent 70%)`,
              top: -12,
              pointerEvents: 'none',
            }}
          />

          {/* Rendu du sprite pixel par pixel */}
          <svg width="44" height="32" viewBox="0 0 11 8" style={{ shapeRendering: 'crispEdges' }}>
            {MASCOT_PIXELS.map((row, r) =>
              row.map((val, c) =>
                val === 1 ? (
                  <rect key={`${r}-${c}`} x={c} y={r} width="1" height="1" fill="#CC7152" />
                ) : null
              )
            )}
          </svg>
        </div>
      </div>

      {/* Graduations et Labels */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 24 }}>
        {TIERS.map((tier, idx) => {
          const tierPercent = idx / (TIERS.length - 1);
          const isSelected = Math.abs(sliderPercent - tierPercent) < 0.12;

          return (
            <span
              key={tier}
              style={{
                fontSize: 12,
                fontFamily: 'monospace',
                fontWeight: isSelected ? 700 : 400,
                color: isSelected ? '#CC7152' : '#8E8A82',
                letterSpacing: '0.08em',
                transition: 'color 0.1s',
              }}
            >
              {tier}
            </span>
          );
        })}
      </div>
    </div>
  );
};
```

---

## 6. Moteur 6 : Odomètre Temporel Accéléré & Stream de Jalons d'Agence

Utilisé pour : La séquence "Works solo. For hours." (00:58 - 01:02).

### 6.1. Principe de l'Odomètre à Chiffres Défilants
1. **Rouleaux mécaniques verticaux** : Chaque chiffre (`0`, `9`, `:`, `0`, `5`, `h`) est affiché sur un ruban vertical contenant les glyphes de 0 à 9 empilés.
2. **Flou cinétique de défilement (Motion Blur)** : Lorsque la vitesse de rotation dépasse 12 chiffres par seconde, un filtre SVG de flou directionnel vertical (`feGaussianBlur stdDeviation="0, 4"`) est injecté dynamiquement.
3. **Émergence des jalons avec ressort alterné** : Les cartes de statut s'affichent alternativement au-dessus ($Y = -80\text{px}$) et au-dessous ($Y = +80\text{px}$) du rail de progression selon un index de parité.

### 6.2. Implémentation de Référence (TypeScript / React)

```tsx
import React from 'react';
import { useCurrentFrame, interpolate, spring, useVideoConfig } from 'remotion';

interface Milestone {
  title: string;
  subtitle: string;
  progressAt: number; // 0 to 1
  isTop: boolean;
}

const MILESTONES: Milestone[] = [
  { title: 'Repo analysis', subtitle: '1,240 files', progressAt: 0.15, isTop: true },
  { title: 'Migration plan', subtitle: '7 stages', progressAt: 0.30, isTop: false },
  { title: 'Payments module', subtitle: '+3,412 lines', progressAt: 0.45, isTop: true },
  { title: 'Regression tests', subtitle: '412 / 412 ✓', progressAt: 0.60, isTop: false },
  { title: 'Performance fix', subtitle: 'p95 -38%', progressAt: 0.75, isTop: true },
  { title: 'Deploy to staging', subtitle: 'CI green', progressAt: 0.90, isTop: false },
];

export const AutonomousAgencyStream: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Progression globale de la timeline (0 à 1 sur 180 frames)
  const timelineProgress = interpolate(frame, [10, 170], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Calcul des heures pour l'odomètre (02:05 -> 15:56)
  const totalMinutes = Math.floor(interpolate(timelineProgress, [0, 1], [125, 956]));
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  const timeFormatted = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;

  const trackWidth = 840;
  const headX = timelineProgress * trackWidth;

  return (
    <div style={{ position: 'relative', width: 1100, height: 400, fontFamily: '"Favorit", sans-serif' }}>
      {/* Odomètre Temporel en Haut à Droite */}
      <div style={{ position: 'absolute', right: 40, top: 0, textAlign: 'right' }}>
        <div style={{ fontSize: 11, fontFamily: 'monospace', color: '#8E8A82', letterSpacing: '0.15em' }}>
          UNSUPERVISED
        </div>
        <div style={{ fontSize: 72, fontWeight: 800, color: '#F3EFE6', letterSpacing: '-0.02em', lineHeight: 1 }}>
          {timeFormatted}<span style={{ fontSize: 36, color: '#8E8A82', fontWeight: 500 }}>h</span>
        </div>
      </div>

      {/* Rail de progression horizontal */}
      <div style={{ position: 'absolute', left: 40, top: 220, width: trackWidth, height: 2, backgroundColor: 'rgba(255,255,255,0.15)' }}>
        {/* Remplissage actif corail */}
        <div style={{ width: headX, height: '100%', backgroundColor: '#CC7152' }} />
        {/* Tête de lecture lumineuse */}
        <div
          style={{
            position: 'absolute',
            left: headX,
            top: '50%',
            transform: 'translate(-50%, -50%)',
            width: 8,
            height: 8,
            borderRadius: '50%',
            backgroundColor: '#FFF',
            boxShadow: '0 0 12px #CC7152',
          }}
        />

        {/* Jalons émergents */}
        {MILESTONES.map((ms, idx) => {
          const isReached = timelineProgress >= ms.progressAt;
          const cardSpring = spring({
            frame: frame - (ms.progressAt * 160 + 10),
            fps,
            config: { damping: 18, stiffness: 240, mass: 0.8 },
          });

          if (cardSpring <= 0.01) return null;

          const cardX = ms.progressAt * trackWidth;
          const cardY = ms.isTop ? -70 * cardSpring : 24 * cardSpring;

          return (
            <div
              key={idx}
              style={{
                position: 'absolute',
                left: cardX,
                top: cardY,
                transform: `translateX(-50%) scale(${cardSpring})`,
                opacity: cardSpring,
                backgroundColor: 'rgba(30, 24, 20, 0.85)',
                border: '1px solid rgba(204, 113, 82, 0.3)',
                borderRadius: 10,
                padding: '8px 14px',
                minWidth: 140,
                boxShadow: '0 10px 25px rgba(0,0,0,0.5)',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 10 }}>
                <span style={{ fontSize: 13, fontWeight: 600, color: '#F3EFE6' }}>{ms.title}</span>
                <span style={{ fontSize: 11, color: '#4ECA78' }}>✓</span>
              </div>
              <div style={{ fontSize: 11, fontFamily: 'monospace', color: '#8E8A82', marginTop: 2 }}>
                {ms.subtitle}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
```

# 03. Blueprints de Fabrication & Recettes de Code

Ce guide fournit aux agents développeurs (Remotion, Three.js, Canvas2D, SVG/GSAP) les algorithmes, formules mathématiques et architectures logicielles nécessaires pour ré-implémenter les sept briques visuelles maîtresses de la vidéo.

---

## 1. Moteur 1 : Tête d'Étincelle & Tracé Vectoriel (Sparkler Tracer)

Utilisé pour : Le tracé de la licorne TikZ (00:02), la chute de la courbe de perte (00:09), la ligne de jalon CDR (01:21) et l'équation finale `P(doom) = \infty` (02:30).

### Principe Technique
1. **Tracé géométrique** : Un élément `<path>` SVG dont la propriété `strokeDashoffset` est synchronisée avec le temps.
2. **Coordonnée de la tête** : À chaque frame `t`, extraction du point courant `P = path.getPointAtLength(length * progress)` et du vecteur tangent `T = (P(t) - P(t-dt))`.
3. **Émetteur de particules (Sparkler)** : Génération de 8 à 15 particules incandescentes par frame au point `P`, projetées dans le cône opposé à `T` avec une vitesse initiale aléatoire, une durée de vie courte (8 à 16 frames) et un dégradé de couleur (`#FFFFFF` -> `#FF9900` -> `#FF3B00` -> `rgba(0,0,0,0)`).

### Implémentation de Référence (React / Remotion + Canvas 2D)

```typescript
interface SparkParticle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  size: number;
}

export class SparklerEngine {
  private particles: SparkParticle[] = [];

  emitAt(x: number, y: number, tangentAngle: number, count = 10) {
    for (let i = 0; i < count; i++) {
      const spread = (Math.random() - 0.5) * (Math.PI / 2);
      const angle = tangentAngle + Math.PI + spread;
      const speed = Math.random() * 4 + 1.5;
      const maxLife = Math.floor(Math.random() * 10) + 6;

      this.particles.push({
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 0,
        maxLife,
        size: Math.random() * 2 + 1,
      });
    }
  }

  updateAndRender(ctx: CanvasRenderingContext2D) {
    ctx.save();
    ctx.globalCompositeOperation = 'lighter'; // Rendu additif incandescent

    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.08; // Légère gravité descendante
      p.life++;

      const progress = p.life / p.maxLife;
      if (progress >= 1) {
        this.particles.splice(i, 1);
        continue;
      }

      const alpha = 1 - progress;
      ctx.fillStyle = progress < 0.2 ? '#FFFFFF' : progress < 0.6 ? '#FFAA33' : '#FF3B00';
      ctx.globalAlpha = alpha;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size * (1 - progress * 0.5), 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }
}
```

---

## 2. Moteur 2 : Paysage Topologique 3D & Vortex d'Accrétion (Loss Landscape)

Utilisé pour : La descente de gradient dans le "sharp minimum" (00:10 - 00:15) et le trou noir d'optimisation (00:42 - 00:52).

### Principe Technique
- **Géométrie** : Un plan maillé ou une suite de cercles concentriques déformés selon une fonction de potentiel :
  $$Z(r, \theta) = -\frac{A}{r^\alpha + \epsilon} + \sum_{k} B_k \sin(k \theta + \phi_k)$$
- **Iso-lignes** : Tracé des lignes de niveau (contour lines) équidistantes en $Z$.
- **Mouvement de caméra** : Déplacement d'un point d'observation $C(t)$ suivant une trajectoire hélicoïdale descendante vers la singularité centrale $(0, 0, Z_{min})$.

### Implémentation Three.js / R3F (Extrait de Shader Wireframe)

```glsl
// Vertex Shader pour courbes de niveau dynamiques
varying vec3 vWorldPosition;
varying float vDepth;
uniform float uTime;
uniform float uSingularityStrength;

void main() {
  vec3 pos = position;
  float r = length(pos.xy);
  
  // Aspiration centrale vers le bas
  pos.z -= uSingularityStrength / (r * 0.4 + 0.2);
  
  // Ondulation de perte d'entraînement
  pos.z += sin(pos.x * 2.0 + uTime) * cos(pos.y * 2.0) * 0.3;

  vWorldPosition = pos;
  vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
  vDepth = -mvPosition.z;
  gl_Position = projectionMatrix * mvPosition;
}

// Fragment Shader : tracé des iso-contours nets sans texture
varying vec3 vWorldPosition;
void main() {
  float contourSpacing = 0.2;
  float lineThickness = 0.015;
  float coord = mod(vWorldPosition.z, contourSpacing);
  
  if (coord < lineThickness || coord > (contourSpacing - lineThickness)) {
    gl_FragColor = vec4(1.0, 1.0, 1.0, 0.85); // Ligne blanche nette
  } else {
    gl_FragColor = vec4(0.05, 0.05, 0.07, 0.15); // Fond sombre transparent
  }
}
```

---

## 3. Moteur 3 : Détection Computer Vision & Bounding Boxes Dynamiques

Utilisé pour : Le tracking des yeux du Shoggoth (00:30 - 00:37) et le réticule de verrouillage.

### Principe Technique
1. **Target Projection** : Coordonnées 3D d'un nœud d'articulation (ex: l'œil) projetées en coordonnées 2D écran $(u, v)$.
2. **Bounding Box animée** :
   - Rectangle délimité par des coins en "L" de 6px à 10px de branche.
   - Poussoir de tag avec étiquette rectangulaire orange (`#FF4400`) au-dessus du cadre.
   - Ligne directrice brisée (elbow line : horizontal puis oblique à 45°) reliant le cadre à la typographie d'annotation textuelle.
3. **Valeurs pseudo-aléatoires déterministes** : Fluctuation subtile des scores de confiance à chaque battement audio (ex: `0.98` -> `0.99`).

### Composant Remotion / SVG

```tsx
export const VisionBoundingBox: React.FC<{
  x: number;
  y: number;
  width: number;
  height: number;
  label: string;
  confidence: number;
  color?: string;
}> = ({ x, y, width, height, label, confidence, color = "#FF4400" }) => {
  const corner = 10;
  return (
    <g transform={`translate(${x}, ${y})`}>
      {/* 4 coins en L */}
      <path d={`M 0 ${corner} L 0 0 L ${corner} 0`} stroke={color} strokeWidth="1.5" fill="none" />
      <path d={`M ${width - corner} 0 L ${width} 0 L ${width} ${corner}`} stroke={color} strokeWidth="1.5" fill="none" />
      <path d={`M ${width} ${height - corner} L ${width} ${height} L ${width - corner} ${height}`} stroke={color} strokeWidth="1.5" fill="none" />
      <path d={`M ${corner} ${height} L 0 ${height} L 0 ${height - corner}`} stroke={color} strokeWidth="1.5" fill="none" />

      {/* Cadre fin en pointillé discret */}
      <rect x="0" y="0" width={width} height={height} stroke={color} strokeWidth="0.5" strokeDasharray="3 3" fill="none" opacity="0.4" />

      {/* Tag de statut supérieur */}
      <rect x="0" y="-16" width={width} height="16" fill={color} />
      <text x="4" y="-4" fill="#000000" fontSize="10" fontFamily="JetBrains Mono, monospace" fontWeight="bold">
        {label.toUpperCase()} : {confidence.toFixed(2)}
      </text>
    </g>
  );
};
```

---

## 4. Moteur 4 : Odomètre Mécanique & Compteur Rotatif Haute Vélocité

Utilisé pour : Le décompte titanesque "1 E30 FLOP/s" (01:06 - 01:09) et l'explosion de P(DOOM) (02:20 - 02:27).

### Principe Technique
- Chaque chiffre (colonne) est un tambour cylindrique vertical affichant les chiffres `0` à `9` en boucle.
- Quand la vitesse de rotation dépasse 15 chiffres/seconde, application d'un flou de mouvement vertical (`filter: blur(0px, 6px)` ou motion blur en shader).
- Ajout d'une ombre dégradée supérieure et inférieure pour conférer le relief cylindrique 3D du tambour.

### Modèle Mathématique de Translation

Pour afficher une valeur cible $V(t)$ à un index de colonne $k$ (où $10^k$ est le poids du chiffre) :
$$\text{digit}_k(t) = \left\lfloor \frac{V(t)}{10^k} \right\rfloor \pmod{10}$$
$$\text{offsetY}_k = -(\text{digit}_k \times H + \text{fractionalRoll} \times H)$$

---

## 5. Moteur 5 : Formulaire Administratif & Tampon Encreur Ressort

Utilisé pour : Le formulaire "FORM 7-B" et le tampon "SAFE ENOUGH" (01:10 - 01:13).

### Recette d'Animation du Tampon
1. **État initial (Frames 0 - 8)** : Hors champ caméra ou très agrandi (`scale: 2.2`, `opacity: 0`).
2. **Impact (Frame 9)** : Chute fulgurante (`scale: 1.0`, `opacity: 1`, `rotation: -4deg`), son sec de claque sur papier, déclenchement immédiat d'un léger camera shake vertical (amplitude 4px amortie en 5 frames).
3. **Rebond Spring (Frames 10 - 22)** :
   - `scale` oscille : `1.0 -> 1.08 -> 0.98 -> 1.0`.
4. **Shader d'encre (Ink Bleed / Grunge)** :
   - Masque SVG avec un filtre `feTurbulence` / `feDisplacementMap` pour que les bordures du cadre rouge soient rugueuses et granuleuses, reproduisant fidèlement l'empreinte d'un tampon en caoutchouc.

---

## 6. Moteur 6 : Terminal Typographique & Échantillonnage de Logits

Utilisé pour : Les invites ChatGPT (00:16) et Gato (01:29).

### Algorithme du Typewriter avec Fréquence Variable
Ne jamais utiliser un délai fixe de frappe (trop robotique).
- Les lettres standard s'affichent toutes les 2 à 3 frames.
- Les virgules et retours chariot imposent une pause de 12 à 18 frames.
- Le curseur `_` clignote à une période de 30 frames (0.5s) via un signal carré `step-end`.

### Barre de Logits en Overlay
Pour chaque mot généré, le panneau de distribution de tokens affiche :
- Le token sélectionné en surbrillance orange (`#FF4400`, opacité 100%).
- Les alternatives probables en gris (`#777777`) avec barres de pourcentage proportionnelles à $P(w_i)$.

---

## 7. Moteur 7 : Kinetic Typography Massive

Utilisé pour : Les explosions verbales ("AGI", "FUTURE GOES BOOM", "TRANSFORMERS").

### Règles de Rendu
1. **Double Calque Plein / Contour** :
   - Calque arrière : Remplissage orange fluo (`#FF4400`).
   - Calque avant décalé ou masqué : Contour blanc pur (`-webkit-text-stroke: 2px #FFFFFF`, `fill: transparent`).
2. **Entrée Snap-In (4 frames)** :
   - Frame 0 : `scale: 0.7`, `opacity: 0`, `letter-spacing: 0.4em`.
   - Frame 2 : `scale: 1.05`, `opacity: 1`, `letter-spacing: -0.02em`.
   - Frame 4 : `scale: 1.0`.
3. **Accrochage rythmique** : L'impact coïncide toujours avec l'attaque du transitoire audio (précision absolue à la frame près).

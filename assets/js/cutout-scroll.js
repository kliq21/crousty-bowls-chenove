/*
  Crousty Cutout Scroll — module réutilisable
  - Attache un canvas Three.js à une section
  - Rend un plat isolé (PNG cutout) avec displacement 3D et post-effects
  - Anime la caméra selon la progression scroll de la section

  Dépendances globales attendues : THREE (via CDN), gsap, ScrollTrigger
*/
(function () {
  const instances = [];

  function createCutout(opts) {
    const {
      canvas,
      photo,
      section,
      preset = 'pushIn',
      steamAmount = 0.6,
      depthStrength = 0.55,
      autoRender = true,
    } = opts;

    if (!window.THREE) {
      console.warn('[cutout] THREE not loaded');
      return null;
    }
    const T = window.THREE;

    const scene = new T.Scene();
    const camera = new T.PerspectiveCamera(50, 1, 0.1, 100);
    camera.position.set(0, 0, 2.6);

    const renderer = new T.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const vs = `
      uniform sampler2D depthMap;
      uniform float depthStrength;
      uniform float depthCurve;
      uniform float breath;
      varying vec2 vUv;
      varying float vDepth;
      void main() {
        vUv = uv;
        float d = texture2D(depthMap, uv).r;
        d = pow(d, depthCurve);
        vDepth = d;
        vec3 pos = position;
        pos.z += d * depthStrength;
        pos *= 1.0 + breath * 0.004;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
      }
    `;
    const fs = `
      uniform sampler2D colorMap;
      uniform float exposure;
      uniform float time;
      uniform float sauceWave;
      uniform float shimmer;
      varying vec2 vUv;
      varying float vDepth;
      float hash(vec2 p) {
        p = fract(p * vec2(123.34, 456.21));
        p += dot(p, p + 45.32);
        return fract(p.x * p.y);
      }
      void main() {
        vec2 uv = vUv;
        vec4 base = texture2D(colorMap, uv);
        if (base.a < 0.06) discard;
        float redness = base.r - (base.g + base.b) * 0.5;
        float sauceMask = smoothstep(0.05, 0.25, redness);
        vec2 waveUV = uv;
        waveUV.x += sin(uv.y * 40.0 + time * 1.6) * 0.002 * sauceMask * sauceWave;
        waveUV.y += cos(uv.x * 40.0 + time * 1.2) * 0.002 * sauceMask * sauceWave;
        vec4 sampled = texture2D(colorMap, waveUV);
        vec3 col = sampled.rgb;
        float lum = dot(col, vec3(0.299, 0.587, 0.114));
        float highlightMask = smoothstep(0.62, 0.92, lum);
        float shimNoise = hash(uv * 512.0 + vec2(time * 3.0)) - 0.5;
        col += vec3(shimNoise) * highlightMask * shimmer;
        col *= exposure;
        col *= 1.0 + (vDepth - 0.4) * 0.10;
        col += sauceMask * vec3(0.03, -0.005, -0.008);
        float alpha = smoothstep(0.06, 0.4, sampled.a);
        gl_FragColor = vec4(col, alpha);
      }
    `;

    let mesh = null;
    let steam = null;
    const loader = new T.TextureLoader();

    function makeMesh(colorTex, depthTex) {
      const imgW = colorTex.image.naturalWidth || colorTex.image.width;
      const imgH = colorTex.image.naturalHeight || colorTex.image.height;
      const aspect = imgW / imgH;
      const planeH = 2.0;
      const planeW = planeH * aspect;

      const geo = new T.PlaneGeometry(planeW, planeH, 160, 160);
      const mat = new T.ShaderMaterial({
        vertexShader: vs,
        fragmentShader: fs,
        transparent: true,
        side: T.DoubleSide,
        uniforms: {
          colorMap: { value: colorTex },
          depthMap: { value: depthTex },
          depthStrength: { value: depthStrength },
          depthCurve: { value: 1.15 },
          breath: { value: 0 },
          exposure: { value: 1.06 },
          time: { value: 0 },
          sauceWave: { value: 1.0 },
          shimmer: { value: 0.10 },
        },
      });
      mesh = new T.Mesh(geo, mat);
      scene.add(mesh);
      return { planeW, planeH };
    }

    function buildSteam(planeW, planeH) {
      const N = 180;
      const geo = new T.BufferGeometry();
      const positions = new Float32Array(N * 3);
      const seeds = new Float32Array(N);
      for (let i = 0; i < N; i++) {
        positions[i*3+0] = (Math.random() - 0.5) * planeW * 0.5;
        positions[i*3+1] = -planeH * 0.15 + Math.random() * planeH * 0.05;
        positions[i*3+2] = 0.15 + Math.random() * 0.4;
        seeds[i] = Math.random();
      }
      geo.setAttribute('position', new T.BufferAttribute(positions, 3));
      geo.setAttribute('seed', new T.BufferAttribute(seeds, 1));
      const mat = new T.ShaderMaterial({
        transparent: true, depthWrite: false, blending: T.AdditiveBlending,
        uniforms: {
          time: { value: 0 },
          size: { value: 56 * steamAmount },
          color:{ value: new T.Color(0xffffff) },
        },
        vertexShader: `
          attribute float seed;
          uniform float time, size;
          varying float vAlpha;
          void main() {
            vec3 pos = position;
            float t = mod(time * 0.13 + seed, 1.0);
            pos.y += t * 1.35;
            pos.x += sin(time * 0.5 + seed * 12.0) * 0.06 * t;
            vAlpha = smoothstep(0.0, 0.15, t) * smoothstep(1.0, 0.55, t) * 0.32;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
            gl_PointSize = size * (1.0 + t * 1.5) * (300.0 / -gl_Position.z);
          }
        `,
        fragmentShader: `
          uniform vec3 color;
          varying float vAlpha;
          void main() {
            vec2 c = gl_PointCoord - 0.5;
            float d = length(c);
            if (d > 0.5) discard;
            float soft = smoothstep(0.5, 0.0, d);
            gl_FragColor = vec4(color, vAlpha * soft);
          }
        `,
      });
      return new T.Points(geo, mat);
    }

    // ---------- Presets caméra pour scroll progress 0..1 ----------
    const PRESETS = {
      pushIn:      { from: { x: 0, y: 0, z: 3.2, fov: 50 }, to:   { x: 0, y: 0, z: 1.6, fov: 50 } },
      pullOut:     { from: { x: 0, y: 0, z: 1.6, fov: 50 }, to:   { x: 0, y: 0, z: 3.5, fov: 50 } },
      dollyZoom:   { from: { x: 0, y: 0, z: 3.6, fov: 30 }, to:   { x: 0, y: 0, z: 1.5, fov: 78 } },
      parallax:    { from: { x: -0.5, y: 0.05, z: 2.4, fov: 50 }, to: { x: 0.5, y: -0.05, z: 2.4, fov: 50 } },
      orbit:       { kind: 'orbit', from: { angle: -0.35, distance: 2.6, y: 0.02, fov: 50 }, to: { angle: 0.35, distance: 2.6, y: 0.02, fov: 50 } },
      archSlow:    { kind: 'orbit', from: { angle: -0.25, distance: 2.8, y: -0.10, fov: 46 }, to: { angle: 0.25, distance: 2.4, y: 0.08, fov: 52 } },
    };

    let scrollProgress = 0;

    function applyPreset(t) {
      const p = PRESETS[preset] || PRESETS.pushIn;
      const s = {};
      for (const k of Object.keys(p.from)) {
        s[k] = p.from[k] + (p.to[k] - p.from[k]) * t;
      }
      if (p.kind === 'orbit') {
        const cx = Math.sin(s.angle) * s.distance;
        const cz = Math.cos(s.angle) * s.distance;
        camera.position.set(cx, s.y, cz);
      } else {
        camera.position.set(s.x, s.y, s.z);
      }
      camera.lookAt(0, 0, 0);
      if (s.fov !== undefined) {
        camera.fov = s.fov;
        camera.updateProjectionMatrix();
      }
    }

    function resize() {
      const rect = canvas.getBoundingClientRect();
      renderer.setSize(rect.width, rect.height, false);
      camera.aspect = rect.width / rect.height;
      camera.updateProjectionMatrix();
    }
    resize();
    window.addEventListener('resize', resize);

    // Load textures
    const base = '/assets/img/nobg/';
    let ready = false;
    const colorTex = loader.load(base + photo + '.png', () => {
      const depthTex = loader.load(base + photo + '-depth.png', () => {
        colorTex.colorSpace = T.SRGBColorSpace;
        colorTex.minFilter = T.LinearFilter;
        colorTex.magFilter = T.LinearFilter;
        depthTex.minFilter = T.LinearFilter;
        depthTex.magFilter = T.LinearFilter;
        const { planeW, planeH } = makeMesh(colorTex, depthTex);
        if (steamAmount > 0) {
          steam = buildSteam(planeW, planeH);
          scene.add(steam);
        }
        ready = true;
        applyPreset(0);
      });
    });

    // ScrollTrigger
    if (window.gsap && window.ScrollTrigger && section) {
      window.ScrollTrigger.create({
        trigger: section,
        start: 'top bottom',
        end: 'bottom top',
        scrub: 0.8,
        onUpdate: (self) => { scrollProgress = self.progress; },
      });
    }

    // Render loop
    const clock = new T.Clock();
    let breathT = 0, lastT = performance.now();
    function tick() {
      requestAnimationFrame(tick);
      const now = performance.now();
      const dt = (now - lastT) / 1000;
      lastT = now;
      breathT += dt;

      const elapsed = clock.getElapsedTime();
      if (mesh) {
        mesh.material.uniforms.breath.value = Math.sin(breathT * 1.4) * 0.5 + 0.5;
        mesh.material.uniforms.time.value = elapsed;
      }
      if (steam) steam.material.uniforms.time.value = elapsed;

      if (ready) applyPreset(scrollProgress);
      renderer.render(scene, camera);
    }
    if (autoRender) tick();

    const instance = {
      canvas, scene, camera, renderer,
      setProgress: (p) => { scrollProgress = p; },
      dispose: () => {
        renderer.dispose();
        if (mesh) { mesh.geometry.dispose(); mesh.material.dispose(); }
        if (steam) { steam.geometry.dispose(); steam.material.dispose(); }
      },
    };
    instances.push(instance);
    return instance;
  }

  window.CroustyCutout = { create: createCutout, instances };
})();

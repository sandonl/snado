"use client";

import { useEffect, useRef } from "react";

const vertexShaderSource = `
  attribute vec2 a_position;
  void main() {
    gl_Position = vec4(a_position, 0.0, 1.0);
  }
`;

const fragmentShaderSource = `
  precision highp float;
  uniform vec2 u_resolution;
  uniform float u_time;

  // Simplex-style noise helpers
  vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec3 permute(vec3 x) { return mod289(((x * 34.0) + 1.0) * x); }

  float snoise(vec2 v) {
    const vec4 C = vec4(
      0.211324865405187,   // (3.0-sqrt(3.0))/6.0
      0.366025403784439,   // 0.5*(sqrt(3.0)-1.0)
     -0.577350269189626,   // -1.0 + 2.0 * C.x
      0.024390243902439    // 1.0 / 41.0
    );

    vec2 i  = floor(v + dot(v, C.yy));
    vec2 x0 = v - i + dot(i, C.xx);

    vec2 i1;
    i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
    vec4 x12 = x0.xyxy + C.xxzz;
    x12.xy -= i1;

    i = mod289(i);
    vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0));

    vec3 m = max(0.5 - vec3(dot(x0, x0), dot(x12.xy, x12.xy), dot(x12.zw, x12.zw)), 0.0);
    m = m * m;
    m = m * m;

    vec3 x = 2.0 * fract(p * C.www) - 1.0;
    vec3 h = abs(x) - 0.5;
    vec3 ox = floor(x + 0.5);
    vec3 a0 = x - ox;

    m *= 1.79284291400159 - 0.85373472095314 * (a0 * a0 + h * h);

    vec3 g;
    g.x = a0.x * x0.x + h.x * x0.y;
    g.yz = a0.yz * x12.xz + h.yz * x12.yw;

    return 130.0 * dot(m, g);
  }

  float fbm(vec2 p) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    for (int i = 0; i < 5; i++) {
      value += amplitude * snoise(p * frequency);
      frequency *= 2.0;
      amplitude *= 0.5;
    }
    return value;
  }

  void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution;
    float aspect = u_resolution.x / u_resolution.y;
    vec2 p = vec2(uv.x * aspect, uv.y);

    float t = u_time * 0.08;

    // Domain warping for organic flow
    float n1 = fbm(p * 1.8 + vec2(t * 0.7, t * 0.5));
    float n2 = fbm(p * 2.2 + vec2(n1 * 0.6, t * 0.3 + n1 * 0.4));
    float n3 = fbm(p * 1.5 + vec2(n2 * 0.5 + t * 0.2, n1 * 0.3));

    // Color palette — deep blues, indigo, subtle warm
    vec3 col1 = vec3(0.04, 0.06, 0.10);  // near black blue
    vec3 col2 = vec3(0.08, 0.12, 0.22);  // deep navy
    vec3 col3 = vec3(0.14, 0.16, 0.32);  // indigo
    vec3 col4 = vec3(0.10, 0.28, 0.38);  // teal
    vec3 col5 = vec3(0.35, 0.20, 0.12);  // warm amber (subtle)

    float blend = n3 * 0.5 + 0.5;
    vec3 color = mix(col1, col2, smoothstep(0.0, 0.35, blend));
    color = mix(color, col3, smoothstep(0.3, 0.55, blend));
    color = mix(color, col4, smoothstep(0.5, 0.75, blend));
    color = mix(color, col5, smoothstep(0.7, 0.95, blend) * 0.3);

    // Add subtle bright highlights
    float highlight = smoothstep(0.6, 0.9, n2 * 0.5 + 0.5);
    color += vec3(0.06, 0.10, 0.18) * highlight;

    // Subtle vignette
    float vignette = 1.0 - length((uv - 0.5) * 1.3);
    vignette = smoothstep(0.0, 0.7, vignette);
    color *= mix(0.6, 1.0, vignette);

    // Bottom fade to match site background (#1b1b1b)
    vec3 bgColor = vec3(0.106, 0.106, 0.106);
    float bottomFade = smoothstep(0.0, 0.25, uv.y);
    color = mix(bgColor, color, bottomFade);

    // Top fade
    float topFade = smoothstep(1.0, 0.85, uv.y);
    color = mix(bgColor, color, topFade * bottomFade + (1.0 - bottomFade) * (1.0 - topFade));

    gl_FragColor = vec4(color, 1.0);
  }
`;

function createShader(
  gl: WebGLRenderingContext,
  type: number,
  source: string
): WebGLShader | null {
  const shader = gl.createShader(type);
  if (!shader) return null;
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    console.error("Shader compile error:", gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
    return null;
  }
  return shader;
}

export default function ShaderHero() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const gl = canvas.getContext("webgl", {
      alpha: false,
      antialias: false,
      preserveDrawingBuffer: false,
    });
    if (!gl) return;

    const vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
    const fragmentShader = createShader(
      gl,
      gl.FRAGMENT_SHADER,
      fragmentShaderSource
    );
    if (!vertexShader || !fragmentShader) return;

    const program = gl.createProgram();
    if (!program) return;
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);

    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      console.error("Program link error:", gl.getProgramInfoLog(program));
      return;
    }

    gl.useProgram(program);

    // Full-screen quad
    const positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(
      gl.ARRAY_BUFFER,
      new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]),
      gl.STATIC_DRAW
    );

    const positionLocation = gl.getAttribLocation(program, "a_position");
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

    const resolutionLocation = gl.getUniformLocation(program, "u_resolution");
    const timeLocation = gl.getUniformLocation(program, "u_time");

    function resize() {
      if (!canvas) return;
      const dpr = Math.min(window.devicePixelRatio, 2);
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      gl!.viewport(0, 0, canvas.width, canvas.height);
    }

    resize();
    window.addEventListener("resize", resize);

    const startTime = performance.now();

    function render() {
      const elapsed = (performance.now() - startTime) / 1000;
      gl!.uniform2f(resolutionLocation, canvas!.width, canvas!.height);
      gl!.uniform1f(timeLocation, elapsed);
      gl!.drawArrays(gl!.TRIANGLES, 0, 6);
      animationRef.current = requestAnimationFrame(render);
    }

    render();

    return () => {
      window.removeEventListener("resize", resize);
      cancelAnimationFrame(animationRef.current);
      gl.deleteProgram(program);
      gl.deleteShader(vertexShader);
      gl.deleteShader(fragmentShader);
      gl.deleteBuffer(positionBuffer);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="w-full h-[400px] block"
      style={{ background: "#1b1b1b" }}
    />
  );
}

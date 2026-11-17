import { useEffect, useRef } from 'react'

export type HeroField = 'horizon' | 'rim' | 'ribbon'
const fieldIndex = { horizon: 0, rim: 1, ribbon: 2 } satisfies Record<HeroField, number>

const vertexSource = `
attribute vec2 position;
void main() { gl_Position = vec4(position, 0.0, 1.0); }
`
const fragmentSource = `
precision highp float;
uniform vec2 resolution;
uniform vec2 pointer;
uniform float time;
uniform int field;
void main() {
  vec2 pixel = vec2(gl_FragCoord.x, resolution.y - gl_FragCoord.y);
  // A rotated print screen, measured in CSS pixels, keeps the dots crisp.
  mat2 rotation = mat2(.9781, .2079, -.2079, .9781);
  vec2 grid = rotation * pixel / 9.0;
  vec2 centre = (floor(grid) + .5) * 9.0;
  vec2 sampleUV = mat2(.9781, -.2079, .2079, .9781) * centre / resolution;
  float x = sampleUV.x + pointer.x * .014;
  float y = sampleUV.y + pointer.y * .009;
  float drift = sin(x * 5.0 + time * .2) * .012;
  float distanceToField;
  if (field == 0) {
    float curve = .81 + .85 * (x - .5) * (x - .5) + drift;
    distanceToField = y - curve;
  } else if (field == 1) {
    float centreX = resolution.x < 700.0 ? 1.77 : 1.35;
    vec2 ellipse = (vec2(x, y) - vec2(centreX, .85)) / vec2(.82, 1.18);
    distanceToField = (length(ellipse) - 1.0) * .46 + drift * .3;
  } else {
    float curve = .30 - .19 * sin(x * 4.5 - 1.05) + drift;
    distanceToField = y - curve;
  }
  float core = exp(-pow(distanceToField / .027, 2.0));
  float halo = exp(-pow((distanceToField + .038) / .078, 2.0));
  float strength = max(core, halo * .35);
  float radius = .43 * smoothstep(.015, .32, strength);
  float mask = 1.0 - smoothstep(radius - .055, radius, length(fract(grid) - .5));
  vec3 ink = vec3(.0431, .0824, .0706);
  vec3 color = mix(vec3(.10, .24, .19), vec3(.94, .54, .43), smoothstep(.18, .7, core));
  color = mix(color, vec3(1.0, .843, .769), smoothstep(.7, 1.0, core));
  float grain = fract(sin(dot(pixel, vec2(12.9898, 78.233))) * 43758.5453) - .5;
  vec3 background = ink + halo * vec3(.008, .028, .019) + grain * .012;
  gl_FragColor = vec4(mix(background, color, mask * smoothstep(.01, .12, strength)), 1.0);
}
`

function compile(gl: WebGLRenderingContext, type: number, source: string) {
  const shader = gl.createShader(type)
  if (!shader) return null
  gl.shaderSource(shader, source); gl.compileShader(shader)
  if (gl.getShaderParameter(shader, gl.COMPILE_STATUS)) return shader
  gl.deleteShader(shader)
  return null
}

export default function ShaderHero({ field }: { field: HeroField }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const selectedField = useRef(field)
  useEffect(() => { selectedField.current = field }, [field])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const gl = canvas.getContext('webgl', { alpha: false, antialias: false })
    if (!gl) return
    const vertex = compile(gl, gl.VERTEX_SHADER, vertexSource)
    const fragment = compile(gl, gl.FRAGMENT_SHADER, fragmentSource)
    if (!vertex || !fragment) {
      if (vertex) gl.deleteShader(vertex)
      if (fragment) gl.deleteShader(fragment)
      return
    }
    const program = gl.createProgram()
    if (!program) { gl.deleteShader(vertex); gl.deleteShader(fragment); return }
    gl.attachShader(program, vertex); gl.attachShader(program, fragment); gl.linkProgram(program)
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      gl.deleteProgram(program); gl.deleteShader(vertex); gl.deleteShader(fragment); return
    }
    const buffer = gl.createBuffer()
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer)
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW)
    gl.useProgram(program)
    const position = gl.getAttribLocation(program, 'position')
    gl.enableVertexAttribArray(position); gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0)
    const resolution = gl.getUniformLocation(program, 'resolution')
    const time = gl.getUniformLocation(program, 'time')
    const mode = gl.getUniformLocation(program, 'field')
    const pointer = gl.getUniformLocation(program, 'pointer')
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)')
    const parent = canvas.parentElement
    let pointerX = 0, pointerY = 0, isVisible = true, frame = 0, lastFrame = 0
    const started = performance.now()
    const move = (event: PointerEvent) => {
      const rect = canvas.getBoundingClientRect()
      pointerX = (event.clientX - rect.left) / rect.width - .5
      pointerY = (event.clientY - rect.top) / rect.height - .5
    }
    function leave() { pointerX = 0; pointerY = 0 }
    const resize = new ResizeObserver(() => {
      // Decorative print needs only one pixel per CSS pixel, even on retina screens.
      canvas.width = Math.round(canvas.clientWidth); canvas.height = Math.round(canvas.clientHeight)
      gl.viewport(0, 0, canvas.width, canvas.height)
    })
    resize.observe(canvas)
    const visibility = new IntersectionObserver(([entry]) => { isVisible = entry.isIntersecting })
    visibility.observe(canvas)
    if (parent) { parent.addEventListener('pointermove', move); parent.addEventListener('pointerleave', leave) }
    const render = (now: number) => {
      frame = requestAnimationFrame(render)
      if (!isVisible || document.hidden || now - lastFrame < 1000 / 30) return
      lastFrame = now
      gl.uniform2f(resolution, canvas.width, canvas.height)
      gl.uniform1f(time, reducedMotion.matches ? 0 : (now - started) / 1000)
      gl.uniform1i(mode, fieldIndex[selectedField.current])
      gl.uniform2f(pointer, reducedMotion.matches ? 0 : pointerX, reducedMotion.matches ? 0 : pointerY)
      gl.drawArrays(gl.TRIANGLES, 0, 6)
      canvas.style.opacity = '1'
    }
    frame = requestAnimationFrame(render)
    return () => {
      cancelAnimationFrame(frame); resize.disconnect(); visibility.disconnect()
      if (parent) { parent.removeEventListener('pointermove', move); parent.removeEventListener('pointerleave', leave) }
      gl.deleteBuffer(buffer); gl.deleteProgram(program); gl.deleteShader(vertex); gl.deleteShader(fragment)
    }
  }, [])

  return <canvas ref={canvasRef} className="portfolio-hero-field" aria-hidden="true" />
}

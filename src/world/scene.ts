import * as THREE from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js'
import { discoveries, moveThroughWorld, obstacles, spawn, cafeRoom, type DiscoveryId } from './world-data'
import { watercolourMaterial } from './watercolour'

export type MoveAction = 'forward' | 'backward' | 'left' | 'right'
type Callbacks = {
  onNearby: (id: DiscoveryId | null) => void
  onDiscover: (id: DiscoveryId) => void
}
export type WorldController = ReturnType<typeof createWorld>

export function createWorld(canvas: HTMLCanvasElement, callbacks: Callbacks) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75))
  renderer.outputColorSpace = THREE.SRGBColorSpace
  const scene = new THREE.Scene()
  scene.background = new THREE.Color('#d7e0df')
  scene.fog = new THREE.Fog('#d7e0df', 32, 110)
  const camera = new THREE.PerspectiveCamera(55, 1, .12, 200)
  const timer = new THREE.Timer()
  timer.connect(document)
  const draco = new DRACOLoader().setDecoderPath('/decoders/')
  const loader = new GLTFLoader().setDRACOLoader(draco)
  let disposed = false
  let paused = false
  let loaded = false
  let nearby: DiscoveryId | null = null
  const keys = new Set<string>()
  const actions = new Set<MoveAction>()
  const modelMeshes: THREE.Mesh[] = []
  const palette = new Map<string, THREE.Material>()
  const pencil = new THREE.LineBasicMaterial({ color: '#4b5657', transparent: true, opacity: .23, depthWrite: false })

  function painted(hex: string) {
    const existing = palette.get(hex)
    if (existing) return existing
    const material = watercolourMaterial(new THREE.Color(hex))
    palette.set(hex, material)
    return material
  }
  function mesh(geometry: THREE.BufferGeometry, color: string, parent: THREE.Object3D, position: [number, number, number]) {
    const value = new THREE.Mesh(geometry, painted(color))
    value.position.set(...position)
    parent.add(value)
    return value
  }
  mesh(new THREE.PlaneGeometry(600, 600), '#b3b8a3', scene, [0, -.4, 0]).rotation.x = -Math.PI / 2
  const avatar = new THREE.Group()
  scene.add(avatar)
  avatar.position.set(spawn.x, -.015, spawn.z)
  mesh(new THREE.BoxGeometry(.43, .52, .25), '#556772', avatar, [0, 1, 0])
  mesh(new THREE.IcosahedronGeometry(.17, 2), '#c5a18a', avatar, [0, 1.47, 0])
  const hair = mesh(new THREE.IcosahedronGeometry(.172, 2), '#3b3b38', avatar, [0, 1.55, -.025])
  hair.scale.set(1, .62, 1)
  const limbs: THREE.Group[] = []
  for (const side of [-1, 1]) {
    const leg = new THREE.Group(); leg.position.set(side * .12, .73, 0); avatar.add(leg)
    mesh(new THREE.BoxGeometry(.15, .6, .18), '#b7a07c', leg, [0, -.3, 0])
    mesh(new THREE.BoxGeometry(.17, .1, .25), '#3d4a4b', leg, [0, -.63, .045])
    limbs.push(leg)
    const arm = new THREE.Group(); arm.position.set(side * .29, 1.2, 0); avatar.add(arm)
    mesh(new THREE.BoxGeometry(.12, .43, .15), '#556772', arm, [0, -.19, 0])
    mesh(new THREE.IcosahedronGeometry(.065, 1), '#c5a18a', arm, [0, -.43, 0])
    limbs.push(arm)
  }
  const shadow = new THREE.Mesh(new THREE.CircleGeometry(.32, 24), new THREE.MeshBasicMaterial({ color: '#485553', transparent: true, opacity: .12, depthWrite: false }))
  shadow.rotation.x = -Math.PI / 2; scene.add(shadow)
  for (const place of discoveries) {
    const marker = new THREE.Mesh(new THREE.RingGeometry(.28, .31, 32), new THREE.MeshBasicMaterial({ color: '#b49b58', side: THREE.DoubleSide, transparent: true, opacity: .65 }))
    marker.rotation.x = -Math.PI / 2; marker.position.set(place.x, .095, place.z); scene.add(marker)
  }

  async function loadNeighbourhood() {
    const asset = await loader.loadAsync('/models/neighbourhood.glb')
    const root = asset.scene
    root.traverse(node => {
      if (!(node instanceof THREE.Mesh)) return
      const original = Array.isArray(node.material) ? node.material : [node.material]
      const replacements = original.map(material => {
        if (!(material instanceof THREE.MeshStandardMaterial)) return material
        const key = material.name
        const cached = palette.get(key)
        if (cached) { material.dispose(); return cached }
        let replacement: THREE.Material
        if (key.startsWith('text/')) replacement = new THREE.MeshBasicMaterial({ color: material.color })
        else if (key.startsWith('glass/')) replacement = new THREE.MeshBasicMaterial({ color: material.color, transparent: true, opacity: .16, side: THREE.DoubleSide, depthWrite: false })
        else replacement = watercolourMaterial(material.color.clone())
        if (key.toLowerCase().includes('foliage')) replacement.side = THREE.DoubleSide
        palette.set(key, replacement)
        material.dispose()
        return replacement
      })
      node.material = Array.isArray(node.material) ? replacements : replacements[0]
      const isSolidSurface = original.every(material => !material.name.startsWith('text/') && !material.name.startsWith('glass/'))
      if (isSolidSurface) {
        // Scenery and paving stay out of camera ray tests. Their distant merged
        // geometry should not consume the walking camera's frame budget.
        let ancestor: THREE.Object3D | null = node
        while (ancestor) {
          if (ancestor.userData.cameraCollision === true) { modelMeshes.push(node); break }
          ancestor = ancestor.parent
        }
        if (original.some(material => /foliage|scenery/i.test(material.name))) return
        const edges = new THREE.EdgesGeometry(node.geometry, 50)
        const positions = edges.getAttribute('position')
        // A tiny stable variation gives the pencil trace a human edge, without
        // animated noise that would shimmer as the player walks.
        for (let index = 0; index < positions.count; index++) {
          const x = positions.getX(index), y = positions.getY(index), z = positions.getZ(index)
          positions.setXYZ(index, x + Math.sin(y * 17 + z * 7) * .0015, y + Math.sin(x * 11 + z * 13) * .0015, z)
        }
        const lines = new THREE.LineSegments(edges, pencil)
        lines.renderOrder = 1
        node.add(lines)
      }
    })
    scene.add(root)
    if (disposed) releaseScene()
  }
  const ready = loadNeighbourhood().then(() => {
    if (disposed) return
    loaded = true
    scene.updateMatrixWorld(true)
  })

  let yaw = 0
  let pitch = .25
  let dragging = false
  let lastPointerX = 0
  let lastPointerY = 0
  let stride = 0
  const focus = new THREE.Vector3()
  const desired = new THREE.Vector3()
  const offset = new THREE.Vector3()
  const forward = new THREE.Vector3()
  const rayDirection = new THREE.Vector3()
  const ray = new THREE.Raycaster()
  const cameraPosition = new THREE.Vector3()
  let snapCamera = true

  const resize = new ResizeObserver(() => {
    const width = canvas.clientWidth, height = canvas.clientHeight
    if (!width || !height) return
    renderer.setSize(width, height, false)
    camera.aspect = width / height; camera.updateProjectionMatrix()
  })
  resize.observe(canvas)
  const keyDown = (event: KeyboardEvent) => {
    if (paused || event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) return
    if (event.target instanceof HTMLElement && event.target !== canvas && event.target.closest('button,a,dialog,summary,select')) return
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(event.key)) event.preventDefault()
    keys.add(event.key.toLowerCase())
    if (event.key.toLowerCase() === 'e' && nearby) callbacks.onDiscover(nearby)
  }
  const keyUp = (event: KeyboardEvent) => { keys.delete(event.key.toLowerCase()) }
  const clearKeys = () => { keys.clear(); actions.clear(); dragging = false }
  const pointerDown = (event: PointerEvent) => {
    dragging = true; lastPointerX = event.clientX; lastPointerY = event.clientY
    canvas.setPointerCapture(event.pointerId)
  }
  const pointerMove = (event: PointerEvent) => {
    if (!dragging || paused) return
    yaw -= (event.clientX - lastPointerX) * .005
    pitch = THREE.MathUtils.clamp(pitch + (event.clientY - lastPointerY) * .003, -.3, .9)
    lastPointerX = event.clientX; lastPointerY = event.clientY
  }
  const pointerUp = () => { dragging = false }
  window.addEventListener('keydown', keyDown)
  window.addEventListener('keyup', keyUp)
  window.addEventListener('blur', clearKeys)
  canvas.addEventListener('pointerdown', pointerDown)
  canvas.addEventListener('pointermove', pointerMove)
  canvas.addEventListener('pointerup', pointerUp)
  canvas.addEventListener('pointercancel', pointerUp)

  renderer.setAnimationLoop(() => {
    timer.update()
    const dt = Math.min(timer.getDelta(), .05)
    if (disposed) return
    if (loaded && !paused) {
      const horizontal = Number(keys.has('d') || keys.has('arrowright') || actions.has('right')) - Number(keys.has('a') || keys.has('arrowleft') || actions.has('left'))
      const vertical = Number(keys.has('s') || keys.has('arrowdown') || actions.has('backward')) - Number(keys.has('w') || keys.has('arrowup') || actions.has('forward'))
      forward.set(horizontal, 0, vertical)
      if (forward.lengthSq() > 0) {
        forward.normalize().applyAxisAngle(THREE.Object3D.DEFAULT_UP, yaw)
        const speed = keys.has('shift') ? 4.5 : 2.7
        const next = moveThroughWorld(avatar.position, { x: forward.x * speed * dt, z: forward.z * speed * dt }, obstacles)
        const distance = Math.hypot(next.x - avatar.position.x, next.z - avatar.position.z)
        avatar.position.x = next.x; avatar.position.z = next.z
        const heading = Math.atan2(forward.x, forward.z)
        avatar.rotation.y += Math.atan2(Math.sin(heading - avatar.rotation.y), Math.cos(heading - avatar.rotation.y)) * (1 - Math.exp(-12 * dt))
        stride += distance * 8
        limbs.forEach((limb, index) => { limb.rotation.x = Math.sin(stride + (index === 0 || index === 3 ? 0 : Math.PI)) * .35 })
      } else limbs.forEach(limb => { limb.rotation.x *= Math.exp(-12 * dt) })
      let closest: DiscoveryId | null = null
      let closestDistance = 1.9
      for (const place of discoveries) {
        const distance = Math.hypot(place.x - avatar.position.x, place.z - avatar.position.z)
        if (distance < closestDistance) { closest = place.id; closestDistance = distance }
      }
      if (closest !== nearby) { nearby = closest; callbacks.onNearby(nearby) }
    }
    const insideCafe = avatar.position.x > cafeRoom.minX && avatar.position.x < cafeRoom.maxX && avatar.position.z > cafeRoom.minZ && avatar.position.z < cafeRoom.maxZ
    // The café floor has a shallow threshold above the shared lane.
    avatar.position.y = insideCafe ? .065 : -.015
    focus.copy(avatar.position); focus.y += 1.15
    const followDistance = insideCafe ? 2.7 : 6.8
    offset.set(Math.sin(yaw) * Math.cos(pitch), Math.sin(pitch), Math.cos(yaw) * Math.cos(pitch)).multiplyScalar(followDistance)
    // Looking up is useful beneath the rafters; keep the camera above ground.
    offset.y = Math.max(offset.y, .35 - focus.y)
    ray.set(focus, rayDirection.copy(offset).normalize())
    ray.far = offset.length()
    const obstruction = ray.intersectObjects(modelMeshes, false)[0]
    if (obstruction) offset.setLength(Math.max(1.15, obstruction.distance - .25))
    desired.copy(focus).add(offset)
    if (snapCamera) { cameraPosition.copy(desired); snapCamera = false }
    else cameraPosition.lerp(desired, 1 - Math.exp(-9 * dt))
    camera.position.copy(cameraPosition); camera.lookAt(focus)
    shadow.position.set(avatar.position.x, insideCafe ? .117 : .043, avatar.position.z)
    renderer.render(scene, camera)
  })

  function releaseScene() {
    const geometries = new Set<THREE.BufferGeometry>()
    const materials = new Set<THREE.Material>()
    scene.traverse(node => {
      if (node instanceof THREE.Mesh || node instanceof THREE.LineSegments) {
        geometries.add(node.geometry)
        for (const material of Array.isArray(node.material) ? node.material : [node.material]) materials.add(material)
      }
    })
    geometries.forEach(value => value.dispose()); materials.forEach(value => value.dispose())
  }
  return {
    ready,
    setAction(action: MoveAction, active: boolean) { if (active) actions.add(action); else actions.delete(action) },
    setPaused(value: boolean) { paused = value; clearKeys() },
    dispose() {
      disposed = true; renderer.setAnimationLoop(null); resize.disconnect(); timer.dispose(); draco.dispose()
      window.removeEventListener('keydown', keyDown); window.removeEventListener('keyup', keyUp); window.removeEventListener('blur', clearKeys)
      canvas.removeEventListener('pointerdown', pointerDown); canvas.removeEventListener('pointermove', pointerMove)
      canvas.removeEventListener('pointerup', pointerUp); canvas.removeEventListener('pointercancel', pointerUp)
      releaseScene(); renderer.dispose()
    },
  }
}

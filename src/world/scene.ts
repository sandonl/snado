import * as THREE from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js'
import { discoveries, moveThroughWorld, obstacles, spawn, cafeRoom, rooms, seats, residents, type Seat, type SeatId, type DiscoveryId } from './world-data'
import { watercolourMaterial } from './watercolour'
import { loadWalker, characterPalettes, type Walker, type CharacterPaletteId } from './character'
import { advanceJump, groundedJump, startJump, type JumpState } from './jump'
import { createBarista } from './barista'

export type MoveAction = 'forward' | 'backward' | 'left' | 'right'
export type Activity = 'walking' | 'seated' | 'transitioning'
export type MouseLook = 'click' | 'locked' | 'drag'
type Posture = { kind: 'walking' } | { kind: 'sittingDown' | 'standingUp'; seat: Seat; elapsed: number; from: THREE.Vector3; fromYaw: number } | { kind: 'seated'; seat: Seat; elapsed: number }
type Callbacks = {
  onNearby: (id: DiscoveryId | null) => void
  onDiscover: (id: DiscoveryId) => void
  onNearbySeat: (id: SeatId | null) => void
  onActivity: (activity: Activity) => void
  onMouseLook: (mode: MouseLook) => void
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
  let nearbySeat: Seat | null = null
  let posture: Posture = { kind: 'walking' }
  let jumpState: JumpState = groundedJump
  const people: { walker: Walker; offset: number }[] = []
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
  let walker: Walker | null = null
  let barista: ReturnType<typeof createBarista> | null = null
  const characterReady = loadWalker(loader).then(value => {
    walker = value
    avatar.add(value.root)
    barista = createBarista(value)
    scene.add(barista.root)
    for (const resident of residents) {
      const person = value.clone()
      const palette = characterPalettes.find(value => value.id === resident.palette)
      if (!palette) throw new Error(`Unknown resident palette: ${resident.palette}`)
      person.setPalette(palette.id)
      person.root.position.set(resident.x, resident.surfaceY - person.hipBottom, resident.z)
      person.root.rotation.y = resident.yaw
      scene.add(person.root)
      people.push({ walker: person, offset: resident.offset })
    }
    if (disposed) releaseScene()
  })
  // Soft character lighting; the neighbourhood keeps its painted materials.
  scene.add(new THREE.HemisphereLight('#fff3d7', '#71858b', 1.65))
  const characterSun = new THREE.DirectionalLight('#fff1da', 2.1)
  characterSun.position.set(-3, 6, 4); scene.add(characterSun)
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
  const ready = Promise.all([loadNeighbourhood(), characterReady]).then(() => {
    if (disposed) return
    loaded = true
    scene.updateMatrixWorld(true)
  })

  let yaw = 0
  let pitch = .25
  let dragging = false
  let dragDistance = 0
  let mouseLockAvailable = typeof canvas.requestPointerLock === 'function'
  let requestingMouseLock = false
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
    if (event.key === 'Escape' && document.pointerLockElement === canvas) {
      releaseMouse()
      return
    }
    if (event.target instanceof HTMLElement && event.target !== canvas && event.target.closest('button,a,dialog,summary,select')) return
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(event.key)) event.preventDefault()
    keys.add(event.key.toLowerCase())
    if (event.repeat) return
    if (event.code === 'Space') jump()
    if (event.key.toLowerCase() === 'e') {
      if (posture.kind === 'seated') stand()
      else if (posture.kind === 'walking' && nearbySeat) sit()
      else if (posture.kind === 'walking' && nearby) callbacks.onDiscover(nearby)
    }
    if (event.key === 'Escape' && posture.kind === 'seated') stand()
  }
  const keyUp = (event: KeyboardEvent) => { keys.delete(event.key.toLowerCase()) }
  const clearKeys = () => { keys.clear(); actions.clear(); dragging = false }
  const releaseMouse = () => {
    if (document.pointerLockElement === canvas) document.exitPointerLock()
  }
  const mouseLockChanged = () => {
    requestingMouseLock = false
    clearKeys()
    const isLocked = document.pointerLockElement === canvas
    if (isLocked && paused) releaseMouse()
    callbacks.onMouseLook(isLocked ? 'locked' : mouseLockAvailable ? 'click' : 'drag')
  }
  const mouseLockFailed = () => {
    if (!requestingMouseLock) return
    requestingMouseLock = false
    mouseLockAvailable = false
    if (!disposed) callbacks.onMouseLook('drag')
  }
  const captureMouse = async (event: MouseEvent) => {
    if (paused || !loaded || dragDistance > 4 || !mouseLockAvailable || requestingMouseLock ||
        document.pointerLockElement === canvas || ('pointerType' in event && event.pointerType !== 'mouse')) return
    canvas.focus({ preventScroll: true })
    requestingMouseLock = true
    try {
      await canvas.requestPointerLock()
      if (disposed || paused) releaseMouse()
    } catch {
      mouseLockFailed()
    }
  }
  const look = (horizontal: number, vertical: number) => {
    yaw -= horizontal * .005
    pitch = THREE.MathUtils.clamp(pitch + vertical * .003, -.3, .9)
  }
  const mouseMove = (event: MouseEvent) => {
    if (!paused && document.pointerLockElement === canvas) look(event.movementX, event.movementY)
  }
  const pointerDown = (event: PointerEvent) => {
    if (paused || event.button !== 0 || document.pointerLockElement === canvas) return
    dragDistance = 0
    dragging = true; lastPointerX = event.clientX; lastPointerY = event.clientY
    canvas.setPointerCapture(event.pointerId)
  }
  const pointerMove = (event: PointerEvent) => {
    if (!dragging || paused || document.pointerLockElement === canvas) return
    const horizontal = event.clientX - lastPointerX
    const vertical = event.clientY - lastPointerY
    dragDistance += Math.abs(horizontal) + Math.abs(vertical)
    look(horizontal, vertical)
    lastPointerX = event.clientX; lastPointerY = event.clientY
  }
  const pointerUp = () => { dragging = false }
  window.addEventListener('keydown', keyDown)
  window.addEventListener('keyup', keyUp)
  window.addEventListener('blur', clearKeys)
  document.addEventListener('pointerlockchange', mouseLockChanged)
  document.addEventListener('pointerlockerror', mouseLockFailed)
  canvas.addEventListener('click', captureMouse)
  canvas.addEventListener('mousemove', mouseMove)
  canvas.addEventListener('pointerdown', pointerDown)
  canvas.addEventListener('pointermove', pointerMove)
  canvas.addEventListener('pointerup', pointerUp)
  canvas.addEventListener('pointercancel', pointerUp)
  callbacks.onMouseLook(mouseLockAvailable ? 'click' : 'drag')

  function roomAt(x: number, z: number) {
    return rooms.find(room => x > room.minX && x < room.maxX && z > room.minZ && z < room.maxZ)
  }
  function floorHeight(x: number, z: number) {
    const room = roomAt(x, z)
    return room === cafeRoom ? .065 : room ? .02 : -.015
  }
  function jump() {
    if (loaded && !paused && posture.kind === 'walking') jumpState = startJump(jumpState)
  }
  function sit() {
    if (!loaded || paused || !walker || !nearbySeat || posture.kind !== 'walking' || jumpState.phase !== 'grounded') return
    posture = { kind: 'sittingDown', seat: nearbySeat, elapsed: 0, from: avatar.position.clone(), fromYaw: avatar.rotation.y }
    clearKeys(); callbacks.onActivity('transitioning')
  }
  function stand() {
    if (paused || posture.kind !== 'seated') return
    posture = { kind: 'standingUp', seat: posture.seat, elapsed: 0, from: avatar.position.clone(), fromYaw: avatar.rotation.y }
    clearKeys(); callbacks.onActivity('transitioning')
  }

  renderer.setAnimationLoop(() => {
    timer.update()
    const dt = Math.min(timer.getDelta(), .05)
    if (disposed) return
    let isWalking = false
    if (loaded && !paused && posture.kind === 'walking') {
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
        isWalking = distance > .0001
      }
      let closest: DiscoveryId | null = null
      let closestDistance = 1.9
      for (const place of discoveries) {
        const distance = Math.hypot(place.x - avatar.position.x, place.z - avatar.position.z)
        if (distance < closestDistance) { closest = place.id; closestDistance = distance }
      }
      if (closest !== nearby) { nearby = closest; callbacks.onNearby(nearby) }
      let nextSeat: Seat | null = null
      let seatDistance = 1.2
      for (const seat of seats) {
        const distance = Math.hypot(seat.approach.x - avatar.position.x, seat.approach.z - avatar.position.z)
        if (distance < seatDistance) { nextSeat = seat; seatDistance = distance }
      }
      if (nextSeat !== nearbySeat) { nearbySeat = nextSeat; callbacks.onNearbySeat(nextSeat ? nextSeat.id : null) }
      jumpState = advanceJump(jumpState, dt)
      avatar.position.y = floorHeight(avatar.position.x, avatar.position.z) + jumpState.height

    }
    const room = roomAt(avatar.position.x, avatar.position.z)
    if (walker) {
      if (posture.kind === 'walking') walker.animate({ kind: 'standing', stride, isWalking, airborne: jumpState.phase === 'airborne' }, dt, timer.getElapsed())
      else {
        if (!paused) posture.elapsed += dt
        let amount = 1
        if (posture.kind !== 'seated') {
          const isSitting = posture.kind === 'sittingDown'
          const progress = Math.min(1, posture.elapsed / (isSitting ? .9 : .65))
          const eased = THREE.MathUtils.smoothstep(progress, 0, 1)
          const seat = posture.seat
          const target = isSitting ? new THREE.Vector3(seat.x, seat.surfaceY - walker.hipBottom, seat.z) : new THREE.Vector3(seat.approach.x, floorHeight(seat.approach.x, seat.approach.z), seat.approach.z)
          avatar.position.lerpVectors(posture.from, target, eased)
          const turn = Math.atan2(Math.sin(seat.yaw - posture.fromYaw), Math.cos(seat.yaw - posture.fromYaw))
          avatar.rotation.y = posture.fromYaw + turn * eased
          amount = isSitting ? eased : 1 - eased
          if (progress === 1) {
            if (isSitting) { posture = { kind: 'seated', seat, elapsed: 0 }; callbacks.onActivity('seated') }
            else { posture = { kind: 'walking' }; callbacks.onActivity('walking') }
          }
        }
        walker.animate({ kind: 'seated', elapsed: posture.kind === 'seated' ? posture.elapsed : 0, amount }, dt, timer.getElapsed())
      }
    }
    for (const person of people) person.walker.animate({ kind: 'seated', elapsed: timer.getElapsed() + person.offset, amount: 1 }, dt, timer.getElapsed() + person.offset)
    barista?.animate(timer.getElapsed(), dt)
    focus.copy(avatar.position); focus.y += 1.15
    const isSeated = posture.kind !== 'walking'
    const followDistance = room ? 2.7 : isSeated ? 3.8 : 6.8
    // Look across the table when seated, so the opposite chair doesn't hide the player.
    const cameraYaw = yaw + (isSeated ? .5 : 0)
    offset.set(Math.sin(cameraYaw) * Math.cos(pitch), Math.sin(pitch), Math.cos(cameraYaw) * Math.cos(pitch)).multiplyScalar(followDistance)
    // Looking up is useful beneath the rafters; keep the camera above ground.
    offset.y = Math.max(offset.y, .35 - focus.y)
    ray.set(focus, rayDirection.copy(offset).normalize())
    ray.far = offset.length()
    const obstruction = ray.intersectObjects(modelMeshes, false)[0]
    if (obstruction) offset.setLength(Math.max(.25, obstruction.distance - .18))
    desired.copy(focus).add(offset)
    if (snapCamera || (obstruction && cameraPosition.distanceTo(focus) > offset.length())) { cameraPosition.copy(desired); snapCamera = false }
    else cameraPosition.lerp(desired, 1 - Math.exp(-9 * dt))
    camera.position.copy(cameraPosition); camera.lookAt(focus)
    // Tight corners become a clear first-person view instead of the inside of a head.
    avatar.visible = camera.position.distanceTo(focus) > 1.25
    shadow.position.set(avatar.position.x, room === cafeRoom ? .117 : room ? .075 : .043, avatar.position.z)
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
    jump, sit, stand,
    setCharacterPalette(id: CharacterPaletteId) { if (walker) walker.setPalette(id) },
    setAction(action: MoveAction, active: boolean) { if (active) actions.add(action); else actions.delete(action) },
    setPaused(value: boolean) { paused = value; clearKeys(); if (value) releaseMouse() },
    dispose() {
      disposed = true; renderer.setAnimationLoop(null); resize.disconnect(); timer.dispose(); draco.dispose()
      document.removeEventListener('pointerlockchange', mouseLockChanged)
      document.removeEventListener('pointerlockerror', mouseLockFailed)
      canvas.removeEventListener('click', captureMouse); canvas.removeEventListener('mousemove', mouseMove)
      releaseMouse()
      window.removeEventListener('keydown', keyDown); window.removeEventListener('keyup', keyUp); window.removeEventListener('blur', clearKeys)
      canvas.removeEventListener('pointerdown', pointerDown); canvas.removeEventListener('pointermove', pointerMove)
      canvas.removeEventListener('pointerup', pointerUp); canvas.removeEventListener('pointercancel', pointerUp)
      releaseScene(); renderer.dispose()
    },
  }
}

import * as THREE from 'three'
import type { Walker } from './character'
import layout from './layout.json'

const cycleLength = 16
const brewStart = 7.2
const brewEnd = 10.1
const collectAt = 10.65
const serveAt = 13
const groupHead = new THREE.Vector3(-2.625, 1.316, -16.88 + layout.counterShiftZ)
const dripTray = new THREE.Vector3(-2.625, 1.167, -16.925 + layout.counterShiftZ)
const servingSpot = new THREE.Vector3(-1.41, 1.085, -16.86 + layout.counterShiftZ)
const filterOffset = new THREE.Vector3(-.035, .018, .09)
const counterHeight = .065

// Hand positions are calibrated to the back of the existing espresso machine.
const stations = [
  { time: 0, x: -2.38, z: -17.22, hand: [-2.04, 1.20, -16.95] },
  { time: 2.4, x: -2.38, z: -17.22, hand: [-2.04, 1.20, -16.95] },
  { time: 3.5, x: -2.65, z: -17.22, hand: [-2.31, 1.15, -16.94] },
  { time: 5.0, x: -2.65, z: -17.22, hand: [-2.31, 1.15, -16.94] },
  { time: 6.3, x: -2.95, z: -17.20, hand: [-2.585, 1.32, -17.03] },
  { time: 6.8, x: -2.95, z: -17.19, hand: [-2.61, 1.48, -16.92] },
  { time: 7.2, x: -2.95, z: -17.19, hand: [-2.61, 1.48, -16.92] },
  { time: 8.1, x: -2.96, z: -17.29, hand: [-2.62, .85, -17.27] },
  { time: 9.95, x: -2.96, z: -17.29, hand: [-2.62, .85, -17.27] },
  { time: collectAt, x: -2.96, z: -17.22, hand: [-2.63, 1.22, -16.94] },
  { time: 11.35, x: -2.80, z: -17.30, hand: [-2.46, 1.28, -17.02] },
  { time: 12.65, x: -1.75, z: -17.24, hand: [-1.41, 1.22, -16.88] },
  { time: serveAt, x: -1.75, z: -17.23, hand: [-1.41, 1.15, -16.86] },
  { time: 13.65, x: -1.75, z: -17.26, hand: [-1.41, .85, -17.20] },
  { time: 14.7, x: -1.75, z: -17.26, hand: [-1.41, .85, -17.20] },
  { time: cycleLength, x: -2.38, z: -17.22, hand: [-2.04, 1.20, -16.95] },
] as const

function armRig(walker: Walker, side: 'left' | 'right') {
  function joint(name: string) {
    const node = walker.root.getObjectByName(side + name)
    if (!node) throw new Error(`Missing barista joint ${side + name}`)
    return node
  }
  const arm = joint('Arm')
  const parent = arm.parent
  if (!parent) throw new Error(`Missing shoulder parent for ${side} barista arm`)
  const forearm = joint('ForeArm')
  const hand = joint('Hand')
  const shoulder = new THREE.Vector3()
  const elbow = new THREE.Vector3()
  const direction = new THREE.Vector3()
  const bend = new THREE.Vector3()
  const parentRotation = new THREE.Quaternion()
  const restArm = forearm.position.clone().normalize()
  const restForearm = hand.position.clone().normalize()
  const first = forearm.position.length() * walker.root.scale.x
  const second = hand.position.length() * walker.root.scale.x
  const sideSign = Math.sign(arm.position.x)

  return {
    hand,
    reach(target: THREE.Vector3) {
      arm.getWorldPosition(shoulder)
      direction.copy(target).sub(shoulder)
      const distance = THREE.MathUtils.clamp(direction.length(), .02, first + second - .001)
      direction.normalize()
      // Bend away from the torso so tight station work still reads from the doorway.
      bend.set(sideSign * .7, -.8, -.2).addScaledVector(direction, -bend.dot(direction)).normalize()
      const along = (first * first - second * second + distance * distance) / (2 * distance)
      const height = Math.sqrt(Math.max(0, first * first - along * along))
      elbow.copy(shoulder).addScaledVector(direction, along).addScaledVector(bend, height)
      parent.getWorldQuaternion(parentRotation).invert()
      bend.copy(elbow).sub(shoulder).normalize().applyQuaternion(parentRotation)
      arm.quaternion.setFromUnitVectors(restArm, bend)
      arm.getWorldQuaternion(parentRotation).invert()
      bend.copy(shoulder).addScaledVector(direction, distance).sub(elbow).normalize().applyQuaternion(parentRotation)
      forearm.quaternion.setFromUnitVectors(restForearm, bend)
    },
  }
}

export function createBarista(source: Walker) {
  const walker = source.clone()
  const root = new THREE.Group()
  root.name = 'Working barista'
  root.add(walker.root)
  walker.setPalette('clay')
  walker.root.scale.setScalar(1.16)
  walker.root.traverse(node => {
    if (/^(canvasBackpack|backpack)/.test(node.name)) node.visible = false
  })
  const apron = new THREE.BufferGeometry()
  apron.setAttribute('position', new THREE.Float32BufferAttribute([
    -.16,.88,.151, .16,.88,.151, -.235,.63,.171, .235,.63,.171,
    -.19,.34,.125, .19,.34,.125,
  ], 3))
  apron.setIndex([0,2,1,1,2,3,2,4,3,3,4,5])
  apron.computeVertexNormals()
  const apronMaterial = new THREE.MeshStandardMaterial({ color: '#3f5555', side: THREE.DoubleSide, roughness: 1 })
  walker.root.getObjectByName('upperBody')?.add(new THREE.Mesh(apron, apronMaterial))
  const right = armRig(walker, 'right')
  const left = armRig(walker, 'left')
  const rightTarget = new THREE.Vector3()
  const leftTarget = new THREE.Vector3()
  const handPoint = new THREE.Vector3()

  function prop(parent: THREE.Object3D, geometry: THREE.BufferGeometry, material: THREE.Material, x = 0, y = 0, z = 0) {
    const object = new THREE.Mesh(geometry, material)
    object.position.set(x, y, z)
    parent.add(object)
    return object
  }
  const chrome = new THREE.MeshStandardMaterial({ color: '#bac6bd', roughness: .32, metalness: .35 })
  const rubber = new THREE.MeshStandardMaterial({ color: '#414544', roughness: .91 })
  const espresso = new THREE.MeshStandardMaterial({ color: '#8c532d', roughness: .53 })
  const glass = new THREE.Group()
  glass.name = 'Barista’s serving glass'
  root.add(glass)
  const clear = new THREE.MeshPhysicalMaterial({ color: '#bde5db', transparent: true, opacity: .3, depthWrite: false, side: THREE.DoubleSide, roughness: .24 })
  prop(glass, new THREE.CylinderGeometry(.046, .034, .103, 12, 1, true), clear, 0, .052)
  prop(glass, new THREE.TorusGeometry(.044, .0026, 6, 24), chrome, 0, .103).rotation.x = Math.PI / 2
  prop(glass, new THREE.CylinderGeometry(.034, .034, .01, 12), clear, 0, .005)
  const liquid = prop(glass, new THREE.CylinderGeometry(.038, .03, .071, 16), espresso)
  const portafilter = new THREE.Group()
  root.add(portafilter)
  prop(portafilter, new THREE.CylinderGeometry(.047, .041, .025, 20), chrome)
  prop(portafilter, new THREE.CylinderGeometry(.013, .014, .14, 10), rubber, .035, -.008, -.09).rotation.x = Math.PI / 2
  const tamper = new THREE.Group()
  root.add(tamper)
  prop(tamper, new THREE.CylinderGeometry(.019, .016, .045, 12), rubber, 0, -.018)
  prop(tamper, new THREE.CylinderGeometry(.029, .029, .009, 16), chrome, 0, -.044)
  const stream = prop(root, new THREE.CylinderGeometry(.003, .004, .068, 8), espresso,
    dripTray.x, 1.25, dripTray.z)

  function animate(elapsed: number, dt: number) {
    const time = elapsed % cycleLength
    const next = stations.findIndex(station => station.time > time)
    const from = stations[next - 1]
    const to = stations[next]
    const progress = THREE.MathUtils.smoothstep(time, from.time, to.time)
    const interpolate = (start: number, end: number) => THREE.MathUtils.lerp(start, end, progress)
    const x = interpolate(from.x, to.x)
    const z = interpolate(from.z, to.z)
    walker.root.position.set(x, counterHeight, z + layout.counterShiftZ)
    const isMoving = Math.abs(to.x - from.x) > .12 && time > from.time && time < to.time
    walker.animate({ kind: 'standing', stride: x * 26, isWalking: isMoving, airborne: false }, dt, elapsed)

    rightTarget.set(interpolate(from.hand[0], to.hand[0]), interpolate(from.hand[1], to.hand[1]),
      interpolate(from.hand[2], to.hand[2]) + layout.counterShiftZ)
    right.reach(rightTarget)
    const isTamping = time >= 3.4 && time < 5.35
    tamper.visible = isTamping
    if (isTamping) {
      const press = Math.sin((time - 3.4) * 7) ** 2
      leftTarget.set(rightTarget.x - .035, 1.24 - press * .06, rightTarget.z + .025)
      left.reach(leftTarget)
      left.hand.getWorldPosition(tamper.position)
    }
    right.hand.getWorldPosition(handPoint)

    portafilter.position.copy(groupHead)
    if (time < 6.3) portafilter.position.copy(handPoint).add(filterOffset)
    glass.position.copy(dripTray)
    if (time >= collectAt && time < serveAt) {
      glass.position.copy(handPoint)
      glass.position.y = Math.max(servingSpot.y, handPoint.y - .053)
      glass.position.z += .023
    } else if (time >= serveAt) glass.position.copy(servingSpot)
    const fill = THREE.MathUtils.clamp((time - brewStart) / (brewEnd - brewStart), 0, 1)
    liquid.visible = fill > .005
    liquid.scale.y = fill
    liquid.position.y = .01 + fill * .0355
    stream.visible = time >= brewStart && time < brewEnd
    stream.scale.x = stream.scale.z = 1 + Math.sin(time * 24) * .22
  }

  return { root, animate }
}

import * as THREE from 'three'
import type { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'

export const characterPalettes = [
  { id: 'fern', label: 'Fern', cap: '#547c68', top: '#e4dec7', bottom: '#6e7a70', shoes: '#d8c9aa', bag: '#ae8d62' },
  { id: 'clay', label: 'Clay', cap: '#bb8b75', top: '#778f83', bottom: '#515f63', shoes: '#dfd0b5', bag: '#aa8b69' },
  { id: 'ink', label: 'Ink', cap: '#617787', top: '#cbb998', bottom: '#536965', shoes: '#d7ceb7', bag: '#9e886e' },
] as const
export type CharacterPaletteId = (typeof characterPalettes)[number]['id']
export type WalkerPose = { kind: 'standing'; stride: number; isWalking: boolean; airborne: boolean } | { kind: 'seated'; elapsed: number; amount: number }
export type Walker = {
  root: THREE.Object3D
  hipBottom: number
  clone: () => Walker
  setPalette: (id: CharacterPaletteId) => void
  animate: (pose: WalkerPose, dt: number, elapsed: number) => void
}

export async function loadWalker(loader: GLTFLoader) {
  const asset = await loader.loadAsync('/models/cafe-walker.glb')
  return prepareWalker(asset.scene)
}

function prepareWalker(root: THREE.Object3D): Walker {
  function part(name: string) {
    const value = root.getObjectByName(name)
    if (!value) throw new Error(`Character is missing its ${name} joint.`)
    return value
  }
  const upperBody = part('upperBody'), head = part('head')
  const arms = [part('leftArm'), part('rightArm')]
  const forearms = [part('leftForeArm'), part('rightForeArm')]
  const legs = [part('leftLeg'), part('rightLeg')].map((joint, index) => ({ joint, knee: part(index === 0 ? 'leftLowerLeg' : 'rightLowerLeg'), shoe: part(index === 0 ? 'leftShoe' : 'rightShoe'), restHeight: joint.position.y }))
  const eyes = [part('leftEye'), part('rightEye')]
  const hand = part('rightHand'), cup = part('heldCup')
  cup.visible = false
  root.updateMatrixWorld(true)
  const bounds = new THREE.Box3()
  const rootPosition = new THREE.Vector3(), handPosition = new THREE.Vector3(), cupPosition = new THREE.Vector3()
  const rootRotation = new THREE.Quaternion(), handRotation = new THREE.Quaternion()
  const soleHeight = bounds.setFromObject(legs[0].shoe).min.y
  const hipBottom = bounds.setFromObject(part('trouserHips')).min.y
  const materials = new Set<THREE.MeshStandardMaterial>()
  root.traverse(node => {
    if (!(node instanceof THREE.Mesh)) return
    for (const material of Array.isArray(node.material) ? node.material : [node.material]) {
      if (material instanceof THREE.MeshStandardMaterial) materials.add(material)
    }
  })
  function smooth(value: number) { return THREE.MathUtils.smoothstep(value, 0, 1) }
  return {
    root, hipBottom,
    clone(): Walker {
      const copy = root.clone(true)
      const copiedMaterials = new Map<THREE.Material, THREE.Material>()
      copy.traverse(node => {
        if (!(node instanceof THREE.Mesh)) return
        const duplicate = (material: THREE.Material) => {
          const existing = copiedMaterials.get(material)
          if (existing) return existing
          const value = material.clone(); copiedMaterials.set(material, value); return value
        }
        node.material = Array.isArray(node.material) ? node.material.map(duplicate) : duplicate(node.material)
      })
      return prepareWalker(copy)
    },
    setPalette(id: CharacterPaletteId) {
      const palette = characterPalettes.find(value => value.id === id)
      if (!palette) return
      const colors = new Map([
        ['Walker · cap', palette.cap], ['Walker · top', palette.top], ['Walker · bottom', palette.bottom],
        ['Walker · shoes', palette.shoes], ['Walker · bag', palette.bag],
      ])
      for (const material of materials) {
        const color = colors.get(material.name)
        if (color) material.color.set(color)
      }
    },
    animate(pose: WalkerPose, dt: number, elapsed: number) {
      const blend = 1 - Math.exp(-14 * dt)
      const seated = pose.kind === 'seated'
      const amount = seated ? pose.amount : 0
      const cycle = seated ? pose.elapsed % 7 : 0
      const sip = seated ? (smooth((cycle - 1.6) / 1) - smooth((cycle - 3.3) / 1)) * amount : 0
      const moving = pose.kind === 'standing' && pose.isWalking
      const airborne = pose.kind === 'standing' && pose.airborne
      arms.forEach((arm, index) => {
        let target = moving && pose.kind === 'standing' ? Math.sin(pose.stride + index * Math.PI) * .42 : 0
        if (airborne) target = -.25
        if (seated) target = index === 1 ? THREE.MathUtils.lerp(-.35, -1.05, sip) * amount : -.3 * amount
        arm.rotation.x = THREE.MathUtils.lerp(arm.rotation.x, target, blend)
        arm.rotation.y = THREE.MathUtils.lerp(arm.rotation.y, index === 1 ? -1.15 * sip : 0, blend)
        arm.rotation.z = THREE.MathUtils.lerp(arm.rotation.z, airborne ? (index === 0 ? .25 : -.25) : 0, blend)
        const forearm = seated ? (index === 1 ? THREE.MathUtils.lerp(-1.1, -1.75, sip) : -.6) * amount : (airborne ? -.35 : 0)
        forearms[index].rotation.x = THREE.MathUtils.lerp(forearms[index].rotation.x, forearm, blend)
      })
      root.getWorldPosition(rootPosition)
      legs.forEach(({ joint, knee, shoe, restHeight }, index) => {
        const phase = pose.kind === 'standing' ? pose.stride + index * Math.PI : 0
        const target = seated ? -1.25 * amount : airborne ? -.25 : moving ? -Math.sin(phase) * .42 : 0
        joint.rotation.x = THREE.MathUtils.lerp(joint.rotation.x, target, blend)
        knee.rotation.x = THREE.MathUtils.lerp(knee.rotation.x, seated ? 1.25 * amount : airborne ? .75 : 0, blend)
        joint.position.y = restHeight
        if (!seated && !airborne) {
          root.updateWorldMatrix(true, true)
          const floorCorrection = rootPosition.y + soleHeight - bounds.setFromObject(shoe).min.y
          joint.position.y += floorCorrection + (moving ? Math.max(0, Math.sin(phase)) * .055 : 0)
        }
      })
      upperBody.rotation.x = THREE.MathUtils.lerp(upperBody.rotation.x, seated ? .035 * amount : 0, blend)
      upperBody.rotation.z = seated ? 0 : moving && pose.kind === 'standing' ? Math.sin(pose.stride) * .025 : Math.sin(elapsed * 1.3) * .009
      head.rotation.y = THREE.MathUtils.lerp(head.rotation.y, .13 * sip, blend)
      const blinkPhase = elapsed % 4.8
      const eyeHeight = blinkPhase > 4.6 ? 1 - Math.sin((blinkPhase - 4.6) / .2 * Math.PI) * .9 : 1
      eyes.forEach(eye => { eye.scale.y = eyeHeight })
      cup.visible = seated && amount > .3
      if (cup.visible) {
        root.updateWorldMatrix(true, true)
        root.getWorldQuaternion(rootRotation);hand.getWorldQuaternion(handRotation);hand.getWorldPosition(handPosition)
        cupPosition.set(-.045, .03, .14).applyQuaternion(rootRotation).add(handPosition)
        cup.position.copy(hand.worldToLocal(cupPosition))
        cup.quaternion.copy(handRotation).invert().multiply(rootRotation)
        cup.rotateX(.18 * sip)
      }
    },
  }
}

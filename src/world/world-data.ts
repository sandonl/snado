import layout from './layout.json'

export type Point = { x: number; z: number }
export type Obstacle = { minX: number; maxX: number; minZ: number; maxZ: number }

export const discoveries = [
  {
    id: 'coffee', title: 'Coffee & cafés', origin: 'Melbourne cafés', ...layout.points.coffee,
    body: 'I’m Sandon, a software engineer living in Melbourne. I enjoy coffee and visiting cafés. This neighbourhood brings together the Melbourne laneways and Seoul workshops that inspired this site.',
    href: '/', linkLabel: 'More about me',
  },
  {
    id: 'writing', title: 'Writing', origin: 'The laneway bookshop', ...layout.points.writing,
    body: 'Notes on building software, working with AI, and what I’m learning along the way.',
    href: '/posts', linkLabel: 'Read my writing',
  },
  {
    id: 'building', title: 'What I build', origin: 'Mullae workshop café', ...layout.points.building,
    body: 'I work on AI and software at Tilt Legal, building tools for legal professionals. Here’s one example: using Effect to review thousands of agreements.',
    href: '/posts/how-we-used-effect-ts-to-review-1000s-of-agreements', linkLabel: 'Read the project story',
  },
] as const

export type Discovery = (typeof discoveries)[number]
export type DiscoveryId = Discovery['id']

// Simple gameplay footprints are independent of the detailed visual mesh.
export const obstacles: readonly Obstacle[] = layout.obstacles
export const worldBounds = layout.bounds
export const spawn = layout.spawn
export const cafeRoom = layout.rooms.cafe

export function moveThroughWorld(position: Point, movement: Point, barriers: readonly Obstacle[], radius = .26): Point {
  let x = position.x + movement.x
  let z = position.z
  for (const obstacle of barriers) {
    if (z <= obstacle.minZ - radius || z >= obstacle.maxZ + radius) continue
    if (movement.x > 0 && position.x <= obstacle.minX - radius && x > obstacle.minX - radius) x = obstacle.minX - radius
    if (movement.x < 0 && position.x >= obstacle.maxX + radius && x < obstacle.maxX + radius) x = obstacle.maxX + radius
  }
  z += movement.z
  for (const obstacle of barriers) {
    if (x <= obstacle.minX - radius || x >= obstacle.maxX + radius) continue
    if (movement.z > 0 && position.z <= obstacle.minZ - radius && z > obstacle.minZ - radius) z = obstacle.minZ - radius
    if (movement.z < 0 && position.z >= obstacle.maxZ + radius && z < obstacle.maxZ + radius) z = obstacle.maxZ + radius
  }
  return {
    x: Math.max(worldBounds.minX + radius, Math.min(worldBounds.maxX - radius, x)),
    z: Math.max(worldBounds.minZ + radius, Math.min(worldBounds.maxZ - radius, z)),
  }
}

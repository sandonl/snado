import layout from './layout.json'

export type Point = { x: number; z: number }
export type Obstacle = { minX: number; maxX: number; minZ: number; maxZ: number }

export const discoveries = [
  { id: 'coffee', title: 'Coffee & cafés', origin: 'Melbourne cafés', body: 'I’m Sandon, a software engineer living in Melbourne. I enjoy coffee and visiting cafés. This neighbourhood brings together the Melbourne laneways and Seoul workshops that inspired this site.', href: '/', linkLabel: 'More about me', ...layout.points.coffee },
  { id: 'writing', title: 'Writing', origin: 'The laneway bookshop', body: 'Notes on building software, working with AI, and what I’m learning along the way.', href: '/posts', linkLabel: 'Read my writing', ...layout.points.writing },
  { id: 'building', title: 'What I build', origin: 'Mullae workshop café', body: 'I work on AI and software at Tilt Legal, building tools for legal professionals. Here’s one example: using Effect to review thousands of agreements.', href: '/posts/how-we-used-effect-ts-to-review-1000s-of-agreements', linkLabel: 'Read the project story', ...layout.points.building },
] as const

export type Discovery = (typeof discoveries)[number]
export type DiscoveryId = Discovery['id']

// Simple gameplay footprints are independent of the detailed visual mesh.
export const obstacles: readonly Obstacle[] = layout.obstacles
export const worldBounds = layout.bounds
export const spawn = layout.spawn
export const cafeRoom = layout.rooms.cafe

export const playerRadius = .38
export const walkableAreas: readonly Obstacle[] = layout.walkableAreas
export const seats = layout.seats
export type Seat = (typeof seats)[number]
export type SeatId = Seat['id']
export const residents = layout.residents

// Clamp to the connected public area at this cross-section. Overlapping zones
// leave a generous connection between the lane, courtyard and café entrance.
function constrainAxis(start: number, target: number, cross: number, axis: 'x' | 'z', areas: readonly Obstacle[], radius: number) {
  const intervals = areas.flatMap(area => {
    const crossMin = axis === 'x' ? area.minZ : area.minX
    const crossMax = axis === 'x' ? area.maxZ : area.maxX
    if (cross < crossMin + radius || cross > crossMax - radius) return []
    return [{ min: (axis === 'x' ? area.minX : area.minZ) + radius, max: (axis === 'x' ? area.maxX : area.maxZ) - radius }]
  }).sort((a, b) => a.min - b.min)
  const merged: { min: number; max: number }[] = []
  for (const interval of intervals) {
    const last = merged[merged.length - 1]
    if (last && interval.min <= last.max) last.max = Math.max(last.max, interval.max)
    else merged.push({ ...interval })
  }
  const room = merged.find(interval => start >= interval.min - .0001 && start <= interval.max + .0001)
  if (!room) return start
  return Math.max(room.min, Math.min(room.max, target))
}

export function moveThroughWorld(position: Point, movement: Point, barriers: readonly Obstacle[], radius = playerRadius, areas = walkableAreas): Point {
  let x = position.x + movement.x
  let z = position.z
  for (const obstacle of barriers) {
    if (z <= obstacle.minZ - radius || z >= obstacle.maxZ + radius) continue
    if (movement.x > 0 && position.x <= obstacle.minX - radius && x > obstacle.minX - radius) x = obstacle.minX - radius
    if (movement.x < 0 && position.x >= obstacle.maxX + radius && x < obstacle.maxX + radius) x = obstacle.maxX + radius
  }
  x = constrainAxis(position.x, x, z, 'x', areas, radius)
  z += movement.z
  for (const obstacle of barriers) {
    if (x <= obstacle.minX - radius || x >= obstacle.maxX + radius) continue
    if (movement.z > 0 && position.z <= obstacle.minZ - radius && z > obstacle.minZ - radius) z = obstacle.minZ - radius
    if (movement.z < 0 && position.z >= obstacle.maxZ + radius && z < obstacle.maxZ + radius) z = obstacle.maxZ + radius
  }
  z = constrainAxis(position.z, z, x, 'z', areas, radius)
  return {
    x: Math.max(worldBounds.minX + radius, Math.min(worldBounds.maxX - radius, x)),
    z: Math.max(worldBounds.minZ + radius, Math.min(worldBounds.maxZ - radius, z)),
  }
}

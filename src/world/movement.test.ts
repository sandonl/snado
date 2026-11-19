import { describe, expect, test } from 'bun:test'
import { discoveries, moveThroughWorld, obstacles, playerRadius, spawn } from './world-data'

const wall = { minX: 1, maxX: 3, minZ: -2, maxZ: 2 }

describe('walking through the neighbourhood', () => {
  test('a long frame cannot carry the player through a building', () => {
    const result = moveThroughWorld({ x: 0, z: 0 }, { x: 5, z: 0 }, [wall])
    expect(result.x).toBeCloseTo(.62)
  })
  test('the player slides along a wall instead of losing diagonal movement', () => {
    const result = moveThroughWorld({ x: .62, z: 0 }, { x: .3, z: -.5 }, [wall])
    expect(result.x).toBeCloseTo(.62)
    expect(result.z).toBeCloseTo(-.5)
  })
  test('the space between two building rows stays walkable', () => {
    const rows = [
      { minX: -6, maxX: -1.9, minZ: -8, maxZ: 6 },
      { minX: 1.9, maxX: 6, minZ: -8, maxZ: 6 },
    ]
    expect(moveThroughWorld({ x: 0, z: 5 }, { x: 0, z: -4 }, rows)).toEqual({ x: 0, z: 1 })
  })
  test('the lane continues into the courtyard without an old end-wall barrier', () => {
    let position = { ...spawn }
    for (let step = 0; step < 150; step++) position = moveThroughWorld(position, { x: 0, z: -.12 }, obstacles)
    expect(position.z).toBeCloseTo(-9.2)
  })
  test('the writing discovery is reachable through the print yard off the lane', () => {
    const printRoom = discoveries.find(place => place.id === 'writing')
    if (!printRoom) throw new Error('Writing discovery is missing')
    const junction = moveThroughWorld(spawn, { x: 0, z: printRoom.z - spawn.z }, obstacles)
    const yard = moveThroughWorld(junction, { x: printRoom.x, z: 0 }, obstacles)
    expect(yard.x).toBeCloseTo(printRoom.x)
    expect(yard.z).toBeCloseTo(printRoom.z)

    const wall = moveThroughWorld(yard, { x: 3, z: 0 }, obstacles)
    expect(wall.x).toBeGreaterThan(yard.x)
    expect(wall.x + playerRadius).toBeCloseTo(5.73)
    expect(moveThroughWorld(yard, { x: -printRoom.x, z: 0 }, obstacles)).toEqual(junction)
  })
  test('the workshop bay is enterable and its counter stops the player', () => {
    const inside = moveThroughWorld({ x: -2.8, z: -12 }, { x: 0, z: -2 }, obstacles)
    expect(inside.z).toBeCloseTo(-14)
    const atCounter = moveThroughWorld(inside, { x: 0, z: -3 }, obstacles)
    expect(atCounter.z).toBeCloseTo(-15.74)
  })
  test.each([
    { shop: 'restaurant', entranceZ: 2.39, insideX: -4.25, roomZ: 3.5 },
    { shop: 'market', entranceZ: 4.58, insideX: 4.25, roomZ: 3.65 },
    { shop: 'ceramics studio', entranceZ: -.31, insideX: -4.15, roomZ: .35 },
  ])('the $shop doorway connects the lane and a walkable interior', ({ entranceZ, insideX, roomZ }) => {
    const lane = { x: 0, z: entranceZ }
    const inside = moveThroughWorld(lane, { x: insideX, z: 0 }, obstacles)
    expect(inside.x).toBeCloseTo(insideX)
    const room = moveThroughWorld(inside, { x: 0, z: roomZ - entranceZ }, obstacles)
    expect(room.z).toBeCloseTo(roomZ)
    const againstWall = moveThroughWorld(room, { x: -insideX, z: 0 }, obstacles)
    expect(Math.abs(againstWall.x)).toBeGreaterThan(2)
    const aligned = moveThroughWorld(room, { x: 0, z: entranceZ - roomZ }, obstacles)
    expect(moveThroughWorld(aligned, { x: -insideX, z: 0 }, obstacles).x).toBeCloseTo(lane.x)
  })
  test('the interior aisle connects the entrance to the tiled seating room', () => {
    const inside = moveThroughWorld({ x: -2.8, z: -13.5 }, { x: 0, z: -2 }, obstacles)
    expect(inside.z).toBeCloseTo(-15.5)
    const seating = moveThroughWorld(inside, { x: 5.6, z: 0 }, obstacles)
    expect(seating.x).toBeCloseTo(2.8)
  })
  test('the wider arrival footway connects back to the lane and stops at the kerb', () => {
    const kerb = moveThroughWorld(spawn, { x: 0, z: 4 }, obstacles)
    expect(kerb.z).toBeCloseTo(9.22)
    for (const direction of [-1, 1]) {
      const edge = moveThroughWorld(kerb, { x: direction * 40, z: 0 }, obstacles)
      expect(Math.abs(edge.x)).toBeCloseTo(4.97)
      const entrance = moveThroughWorld(edge, { x: -edge.x, z: 0 }, obstacles)
      const lane = moveThroughWorld(entrance, { x: 0, z: -8 }, obstacles)
      expect(lane.z).toBeCloseTo(1.22)
    }
  })

  test('the street tree stops the player at its planting bed', () => {
    const forecourt = moveThroughWorld(spawn, { x: 0, z: -.65 }, obstacles)
    const tree = moveThroughWorld(forecourt, { x: -5, z: 0 }, obstacles)
    expect(tree.x).toBeCloseTo(-3.04)
  })
})

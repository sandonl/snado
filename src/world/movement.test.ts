import { describe, expect, test } from 'bun:test'
import { moveThroughWorld, obstacles, spawn } from './world-data'

const wall = { minX: 1, maxX: 3, minZ: -2, maxZ: 2 }

describe('walking through the neighbourhood', () => {
  test('a long frame cannot carry the player through a building', () => {
    const result = moveThroughWorld({ x: 0, z: 0 }, { x: 5, z: 0 }, [wall])
    expect(result.x).toBeCloseTo(.74)
  })
  test('the player slides along a wall instead of losing diagonal movement', () => {
    const result = moveThroughWorld({ x: .74, z: 0 }, { x: .3, z: -.5 }, [wall])
    expect(result.x).toBeCloseTo(.74)
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
  test('the workshop bay is enterable and its counter stops the player', () => {
    const inside = moveThroughWorld({ x: -2.8, z: -12 }, { x: 0, z: -2 }, obstacles)
    expect(inside.z).toBeCloseTo(-14)
    const atCounter = moveThroughWorld(inside, { x: 0, z: -3 }, obstacles)
    expect(atCounter.z).toBeCloseTo(-15.86)
  })
  test('the interior aisle connects the entrance to the tiled seating room', () => {
    const inside = moveThroughWorld({ x: -2.8, z: -13.5 }, { x: 0, z: -2 }, obstacles)
    expect(inside.z).toBeCloseTo(-15.5)
    const seating = moveThroughWorld(inside, { x: 5.6, z: 0 }, obstacles)
    expect(seating.x).toBeCloseTo(2.8)
  })
  test('both perimeter paths allow walking behind the buildings', () => {
    for (const x of [-11.5, 11.9]) {
      expect(moveThroughWorld({ x, z: 8.8 }, { x: 0, z: -35 }, obstacles).z).toBeCloseTo(-26.2)
    }
  })
})

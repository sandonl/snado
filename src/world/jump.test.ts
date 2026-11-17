import { expect, test } from 'bun:test'
import { advanceJump, groundedJump, startJump } from './jump'

test('a short jump rises and returns to the floor at different frame rates', () => {
  for (const dt of [1 / 60, 1 / 30]) {
    let jump = startJump(groundedJump)
    let apex = 0
    let minimum = 0
    for (let frame = 0; frame < 1 / dt; frame++) {
      jump = advanceJump(jump, dt)
      apex = Math.max(apex, jump.height)
      minimum = Math.min(minimum, jump.height)
    }
    expect(minimum).toBeGreaterThanOrEqual(0)
    expect(apex).toBeGreaterThan(.38)
    expect(apex).toBeLessThan(.42)
    expect(jump.phase).toBe('grounded')
  }
})

test('pressing jump again in the air cannot reset the upward impulse', () => {
  const airborne = advanceJump(startJump(groundedJump), .12)
  const repeated = startJump(airborne)
  expect(repeated.velocity).toBe(airborne.velocity)
  expect(repeated.height).toBe(airborne.height)
})

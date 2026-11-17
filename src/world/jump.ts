export type JumpState = { phase: 'grounded'; height: 0; velocity: 0 } | { phase: 'airborne'; height: number; velocity: number }
export const groundedJump: JumpState = { phase: 'grounded', height: 0, velocity: 0 }

export function startJump(state: JumpState): JumpState {
  if (state.phase === 'airborne') return state
  return { phase: 'airborne', height: 0, velocity: 3.2 }
}

export function advanceJump(state: JumpState, dt: number): JumpState {
  if (state.phase === 'grounded') return state
  const velocity = state.velocity - 12.8 * dt
  const height = state.height + (state.velocity + velocity) * .5 * dt
  if (height <= 0 && velocity < 0) return groundedJump
  return { phase: 'airborne', height: Math.max(0, height), velocity }
}

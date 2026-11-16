import { useEffect, useRef, useState } from 'react'
import { discoveries, type DiscoveryId } from './world-data'
import type { MoveAction, WorldController } from './scene'

type LoadState = { phase: 'loading' } | { phase: 'ready' } | { phase: 'error'; message: string }

export default function PortfolioWorld() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const controllerRef = useRef<WorldController | null>(null)
  const dialogRef = useRef<HTMLDialogElement>(null)
  const [load, setLoad] = useState<LoadState>({ phase: 'loading' })
  const [nearby, setNearby] = useState<DiscoveryId | null>(null)
  const [selected, setSelected] = useState<DiscoveryId | null>(null)
  const [showPlaces, setShowPlaces] = useState(false)
  const place = discoveries.find(value => value.id === selected)
  const nearbyPlace = discoveries.find(value => value.id === nearby)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    let disposed = false
    void import('./scene').then(({ createWorld }) => {
      if (disposed) return
      const controller = createWorld(canvas, { onNearby: setNearby, onDiscover: setSelected })
      controllerRef.current = controller
      return controller.ready.then(() => { if (!disposed) setLoad({ phase: 'ready' }) })
    }).catch((error: unknown) => {
      if (!disposed) setLoad({ phase: 'error', message: error instanceof Error ? error.message : 'The scene could not load.' })
    })
    return () => {
      disposed = true
      const controller = controllerRef.current
      if (controller) controller.dispose()
      controllerRef.current = null
    }
  }, [])

  useEffect(() => {
    const dialog = dialogRef.current
    const controller = controllerRef.current
    if (selected) {
      if (controller) controller.setPaused(true)
      if (dialog && !dialog.open) dialog.showModal()
    } else {
      if (dialog && dialog.open) dialog.close()
      if (controller) controller.setPaused(false)
    }
  }, [selected])

  function move(action: MoveAction, active: boolean) {
    const controller = controllerRef.current
    if (controller) controller.setAction(action, active)
  }

  return (
    <main className="portfolio-world">
      <canvas ref={canvasRef} className="world-canvas" aria-label="Walk through Melbourne and Seoul. Use W A S D or arrow keys to move, drag to look, and E to open a nearby place." tabIndex={0} />
      <header className="world-header">
        <div className="world-identity"><h1><a href="/">Sandon Lai</a></h1><span>The neighbourhood</span></div>
        <nav aria-label="World navigation">
          <button type="button" onClick={() => setShowPlaces(value => !value)} aria-expanded={showPlaces}>Places</button>
          <a href="/">Read portfolio <span aria-hidden="true">↗</span></a>
        </nav>
      </header>

      {showPlaces && <section className="world-places" aria-label="Places to explore">
        <p className="world-eyebrow">Along the lane</p>
        <p className="world-route-note">Walk through the cafés into the workshop courtyard. The side streets continue around the buildings.</p>
        <p className="world-eyebrow">Read directly</p>
        {discoveries.map(value => <button className="world-place-link" key={value.id} onClick={() => { setSelected(value.id); setShowPlaces(false) }}>{value.title}<span aria-hidden="true">↗</span></button>)}
      </section>}

      {load.phase === 'loading' && <div className="world-status" role="status"><span className="world-loading-mark" aria-hidden="true" /><h2>Loading the neighbourhood</h2><p>Melbourne laneways & Mullae workshops.</p></div>}
      {load.phase === 'error' && <div className="world-status" role="alert"><h2>The neighbourhood couldn’t load</h2><p>You can still read everything in the portfolio.</p><a href="/">Read about Sandon ↗</a><details><summary>Loading details</summary><p>{load.message}</p></details></div>}

      {load.phase === 'ready' && <>
        <div className="world-caption"><span>Cafés, workshops & laneways</span><p>Walk the lane. Follow the side streets.</p></div>
        <div className="world-help"><span><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> walk</span><span>drag to look</span><span><kbd>shift</kbd> run</span></div>
        {nearbyPlace && <button className="world-discover" onClick={() => setSelected(nearbyPlace.id)}><kbd>E</kbd><span>{nearbyPlace.title}</span><span aria-hidden="true">↗</span></button>}
        <div className="world-touch-controls" aria-label="Movement controls">
          {(['forward', 'left', 'backward', 'right'] as const).map((action, index) => <button key={action} aria-label={`Walk ${action}`} className={`world-move-${action}`} onPointerDown={event => { event.preventDefault(); event.currentTarget.setPointerCapture(event.pointerId); move(action, true) }} onPointerUp={() => move(action, false)} onPointerCancel={() => move(action, false)} onLostPointerCapture={() => move(action, false)}>{['↑', '←', '↓', '→'][index]}</button>)}
        </div>
      </>}

      <dialog className="world-dialog" ref={dialogRef} onClose={() => setSelected(null)} onCancel={() => setSelected(null)} aria-labelledby="world-discovery-title">
        {place && <><button className="world-dialog-close" onClick={() => setSelected(null)} aria-label="Close discovery">×</button><p className="world-eyebrow">{place.origin}</p><h2 id="world-discovery-title">{place.title}</h2><p>{place.body}</p><a className="world-story-link" href={place.href}>{place.linkLabel} <span aria-hidden="true">↗</span></a><button className="world-keep-walking" onClick={() => setSelected(null)}>Keep walking</button></>}
      </dialog>
    </main>
  )
}

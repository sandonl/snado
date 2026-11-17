import { useState } from 'react'
import { Link } from '@tanstack/react-router'
import '@fontsource/fraunces/300-italic.css'
import ShaderHero, { type HeroField } from './shader-hero'
import './portfolio-hero.css'

const fields = [
  { id: 'horizon', label: 'Horizon' },
  { id: 'rim', label: 'Rim' },
  { id: 'ribbon', label: 'Ribbon' },
] as const

export default function PortfolioHero() {
  const [field, setField] = useState<HeroField>('horizon')
  return <section className="portfolio-hero" data-field={field} aria-labelledby="portfolio-introduction">
    <ShaderHero field={field} />
    <div className="portfolio-hero-copy">
      <p className="portfolio-hero-label">Sandon Lai · Melbourne</p>
      <h1 id="portfolio-introduction">{field === 'ribbon' ? 'Sandon Lai.' : <>Software, AI &amp;<br />small experiments.</>}</h1>
      <p className="portfolio-hero-description">I’m Sandon, an engineer in Melbourne. I build AI tools at Tilt Legal and make things on the side.</p>
      <div className="portfolio-hero-links"><a className="portfolio-hero-primary" href="#portfolio">View portfolio <span aria-hidden="true">↓</span></a><Link to="/posts">Read my writing <span aria-hidden="true">↗</span></Link></div>
    </div>
    <div className="portfolio-hero-footer">
      <div className="portfolio-field-picker" role="group" aria-label="Hero artwork">
        {fields.map((value, index) => <button key={value.id} aria-pressed={field === value.id} onClick={() => setField(value.id)}><span aria-hidden="true">0{index + 1}</span> {value.label}</button>)}
      </div>
      <span className="portfolio-hero-note">Portfolio · Writing · Experiments</span>
    </div>
  </section>
}

// Run through Figma's connected use_figma tool. The field remains editable vectors.
const page = figma.currentPage
if (page.children.some(node => node.name === '01 — Horizon')) return { status: 'Studies already exist; edit the existing frames.' }
const fonts = [{ family: 'Fraunces', style: 'Light Italic' }, { family: 'Geist', style: 'Regular' }, { family: 'Geist Mono', style: 'Regular' }]
await Promise.all(fonts.map(font => figma.loadFontAsync(font)))
const created = []
function remember(node) { created.push(node.id); return node }
function color(hex) { return { r: parseInt(hex.slice(0,2),16)/255, g: parseInt(hex.slice(2,4),16)/255, b: parseInt(hex.slice(4,6),16)/255 } }
const colors = { ink:'0B1512', mist:'E3F5EC', muted:'9DBFAF', mint:'7FE0B4', coral:'F08A6E' }
const collection = figma.variables.createVariableCollection('Portfolio / Counterform')
const variables = {}
for (const [name,hex] of Object.entries(colors)) {
  const variable = figma.variables.createVariable(name,collection,'COLOR')
  variable.scopes=['FRAME_FILL','SHAPE_FILL','TEXT_FILL','STROKE_COLOR']
  variable.setValueForMode(collection.modes[0].modeId,color(hex)); variables[name]=variable
}
function paint(role) { return figma.variables.setBoundVariableForPaint({type:'SOLID',color:color(colors[role])},'color',variables[role]) }
function row(parent,name,gap=24) { const node=remember(figma.createAutoLayout('HORIZONTAL'));node.name=name;node.itemSpacing=gap;node.fills=[];node.counterAxisAlignItems='CENTER';parent.appendChild(node);return node }
function column(parent,name,gap=26) {const node=remember(figma.createAutoLayout('VERTICAL'));node.name=name;node.itemSpacing=gap;node.fills=[];parent.appendChild(node);return node}
function text(parent,content,size,role='mist',font=fonts[1],line=size*1.35,width) {
 const node=remember(figma.createText());node.fontName=font;node.fontSize=size;node.lineHeight={unit:'PIXELS',value:line};node.characters=content;node.fills=[paint(role)];parent.appendChild(node)
 if(width){node.textAutoResize='HEIGHT';node.resize(width,node.height)}
 return node
}
const foundation=remember(figma.createAutoLayout('VERTICAL'));foundation.name='Local components';foundation.x=100;foundation.y=1050;foundation.itemSpacing=24;foundation.fills=[]
function makeLink(name,label,primary) {
 const component=remember(figma.createComponent());component.name=name;component.layoutMode='HORIZONTAL';component.primaryAxisSizingMode='AUTO';component.counterAxisSizingMode='AUTO';component.counterAxisAlignItems='CENTER';component.fills=primary?[paint('coral')]:[];component.cornerRadius=999
 if(primary){component.paddingLeft=24;component.paddingRight=24;component.paddingTop=14;component.paddingBottom=14}
 const node=text(component,label,15,primary?'ink':'mist');const property=component.addComponentProperty('Label','TEXT',label);node.componentPropertyReferences={characters:property};foundation.appendChild(component);return {component,property}
}
const navigation=makeLink('Navigation link','Home',false)
const primary=makeLink('Primary link','View portfolio ↓',true)
const secondary=makeLink('Text link','Read my writing ↗',false)
function instance(parent,source,label) {const node=remember(source.component.createInstance());parent.appendChild(node);node.setProperties({[source.property]:label});return node}
function fieldSvg(mode) {
 const paths=Array.from({length:16},()=>[])
 for(let iy=-40;iy<140;iy++)for(let ix=-30;ix<190;ix++) {
  const gx=(ix+.5)*9,gy=(iy+.5)*9;const px=.9781*gx-.2079*gy,py=.2079*gx+.9781*gy
  if(px < -5||px>1445||py < -5||py>905)continue
  const x=px/1440,y=py/900
  let d=y-(.81+.85*(x-.5)**2+Math.sin(x*5)*.012)
  if(mode===1)d=(Math.hypot((x-1.35)/.82,(y-.85)/1.18)-1)*.46
  if(mode===2)d=y-(.30-.19*Math.sin(x*4.5-1.05))
  const core=Math.exp(-Math.pow(d/.027,2)),halo=Math.exp(-Math.pow((d+.038)/.078,2)),strength=Math.max(core,halo*.35)
  if(strength<.025)continue
  const bucket=Math.min(15,Math.floor(core*15));const radius=3.85*Math.min(1,strength/.25)
  const r=radius.toFixed(2),start=(px-radius).toFixed(2),yy=py.toFixed(2),diameter=(radius*2).toFixed(2)
  paths[bucket].push(`M${start},${yy}a${r},${r} 0 1 0 ${diameter},0a${r},${r} 0 1 0 -${diameter},0`)
 }
 const groups=paths.map((parts,i)=>{const a=i/15;const t=Math.min(1,a*1.5);const rgb=[26+(240-26)*t,61+(138-61)*t,48+(110-48)*t];if(a>.7){const t=(a-.7)/.3;rgb[0]+=(255-rgb[0])*t;rgb[1]+=(215-rgb[1])*t;rgb[2]+=(196-rgb[2])*t}return `<path fill="rgb(${rgb.map(Math.round).join(',')})" d="${parts.join('')}"/>`}).join('')
 return `<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="900" viewBox="0 0 1440 900">${groups}</svg>`
}
const studies=[]
for(const [mode,name] of ['Horizon','Glass rim','Ribbon'].entries()) {
 const wrapper=remember(figma.createFrame());wrapper.name=`0${mode+1} — ${name}`;wrapper.resize(1440,900);wrapper.x=100+mode*1540;wrapper.y=0;wrapper.fills=[paint('ink')];wrapper.clipsContent=true
 const field=figma.createNodeFromSvg(fieldSvg(mode));wrapper.appendChild(field);field.name='Halftone field / editable vectors';field.x=0;field.y=0;created.push(field.id,...field.findAll(()=>true).map(node=>node.id))
 const nav=row(wrapper,'Navigation',32);nav.resize(1328,32);nav.primaryAxisSizingMode='FIXED';nav.primaryAxisAlignItems='SPACE_BETWEEN';nav.x=56;nav.y=36
 text(nav,'sandon lai',26,'mist',fonts[0],32)
 const links=row(nav,'Pages',32);for(const label of ['Home','Posts','Explore'])instance(links,navigation,label)
 const copy=column(wrapper,'Personal introduction');copy.x=mode===0?220:56;copy.y=mode===0?178:mode===1?282:450;copy.resize(mode===0?1000:640,100);copy.layoutSizingVertical='HUG';copy.counterAxisAlignItems=mode===0?'CENTER':'MIN'
 text(copy,'SANDON LAI · MELBOURNE',13,'mint',fonts[2],16)
 const heading=text(copy,mode===2?'Sandon Lai.':'Software, AI &\nsmall experiments.',mode===2?132:104,'mist',fonts[0],mode===2?130:102);heading.letterSpacing={unit:'PERCENT',value:-3.5};heading.textAlignHorizontal=mode===0?'CENTER':'LEFT'
 const body=text(copy,'I’m Sandon, an engineer in Melbourne. I build AI tools at Tilt Legal and make things on the side.',19,'muted',fonts[1],28,530);body.textAlignHorizontal=mode===0?'CENTER':'LEFT'
 const actions=row(copy,'Actions',24);instance(actions,primary,'View portfolio ↓');instance(actions,secondary,'Read my writing ↗')
 const footer=row(wrapper,'Footer',24);footer.resize(1328,32);footer.primaryAxisSizingMode='FIXED';footer.primaryAxisAlignItems='SPACE_BETWEEN';footer.x=56;footer.y=832;text(footer,`0${mode+1} / ${name.toUpperCase()}`,12,'muted',fonts[2],18);text(footer,'PORTFOLIO · WRITING · EXPERIMENTS',12,'muted',fonts[2],18)
 studies.push({id:wrapper.id,name:wrapper.name,width:wrapper.width,height:wrapper.height,descendants:wrapper.findAll(()=>true).length})
}
return {createdNodeIds:created,studies,variableIds:Object.values(variables).map(v=>v.id),collectionId:collection.id,fonts:fonts.map(f=>f.family),images:0}

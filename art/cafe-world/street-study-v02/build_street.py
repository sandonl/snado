"""Seoul street corner, revised toward inked 3D illustration and photographic proportions.

Builds a new Blender scene. Reuses only the primitive helpers from the first study.
The camera is at walking height; no miniature plinth or orthographic presentation.
"""
from pathlib import Path
helper_source = Path(__file__).resolve().parents[1] / 'build_cafes.py'
exec(helper_source.read_text().split('# Shared ground:')[0], globals())
import bmesh

scene.name = 'Sandon · Seoul street · illustrated v02'
seoul.name = '01 · Seoul corner café'
melbourne.name = '02 · Neighbouring buildings'
street.name = '03 · Pavement and street furniture'
rig.name = '04 · Illustration lighting and cameras'
random.seed(43)

# Sharper architecture and much smaller edge radii than the miniature study.
def bevel(obj, width=.006, segments=1):
    if width:
        modifier = obj.modifiers.new('Very small architectural edge', 'BEVEL')
        modifier.width = min(width,.008)
        modifier.segments = 1
    return obj

def recolour(mat, hex_value, roughness=1):
    mat.diffuse_color=(*colour(hex_value),1)
    shader=mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value=mat.diffuse_color
    shader.inputs['Roughness'].default_value=roughness
    shader.inputs['Metallic'].default_value=0
    shader.inputs['Specular IOR Level'].default_value=.08

for mat,hex_value in [(cream,'D8CCB2'),(ivory,'E4DEC9'),(trim,'B7B1A0'),(green,'52665D'),(sage,'919782'),(dark,'3E4749'),(ink,'4B4A4F'),(brick_mortar,'B6836E'),(terracotta,'BD836A'),(wood,'8A715A'),(light_wood,'B79C79'),(glass,'899F9D'),(glass_light,'B5C8BF'),(glow,'DAC7A5')]:
    recolour(mat,hex_value)
for mat,hex_value in zip(bricks,['B38570','BC8F78','AD7E6B','C29A83','B78A78']):recolour(mat,hex_value)
asphalt=material('street asphalt','7D8A91',1)
concrete=material('old concrete','B3B5AA',1)
plaster=material('faded peach plaster','D5BEAA',1)
wall_shadow=material('recessed shop interior','676E67',1)
line_mat=material('drawn detail','51565D',1)
paper=material('aged paper','DED6BC',1)
red=material('faded red plastic','A96754',1)
sky_blue=material('distant blue plaster','A3B4B0',1)
roof_grey=material('roof concrete','A6ACA5',1)
soil=material('planter soil','6B6B5A',1)

def stroke(name,points,radius=.003):
    return curve(name,points,radius,line_mat)

def front_window(name,x,y,z,w,h,frame=dark,warm=False):
    box(name+' thin frame',(x,y,z),(w+.08,.09,h+.08),frame,.005)
    box(name+' recessed glazing',(x,y-.048,z),(w,.016,h),glow if warm else glass,.002)
    box(name+' centre mullion',(x,y-.077,z),(.035,.035,h),frame,.003)
    box(name+' low rail',(x,y-.079,z-h*.24),(w,.035,.033),frame,.002)
    box(name+' concrete sill',(x,y-.07,z-h/2-.045),(w+.16,.18,.07),trim,.006)
    # Restrained planar reflections, as in a hand-coloured architectural drawing.
    mesh=bpy.data.meshes.new(name+' reflection')
    mesh.from_pydata([(x-w*.43,y-.061,z+h*.43),(x-w*.24,y-.061,z+h*.43),(x+w*.2,y-.061,z-h*.42),(x+.01,y-.061,z-h*.42)],[],[(0,1,2,3)])
    link_object(name+' reflection',mesh,glass_light)
    if warm:
        box(name+' interior shelf',(x,y-.073,z-.2),(w-.05,.023,.045),wood,.002)
        for offset in [-w*.3,0,w*.31]:
            box(name+' silhouetted cup',(x+offset,y-.095,z-.11),(.1,.023,.13),ivory,.005)

def side_window(name,x,y,z,w,h,frame=dark):
    box(name+' frame',(x,y,z),(.09,w+.08,h+.08),frame,.005)
    box(name+' glazing',(x+.048,y,z),(.016,w,h),glass,.002)
    box(name+' mullion',(x+.077,y,z),(.035,.035,h),frame,.002)
    box(name+' lower rail',(x+.079,y,z-h*.24),(.035,w,.033),frame,.002)
    box(name+' sill',(x+.07,y,z-h/2-.045),(.18,w+.16,.07),trim,.005)

def rough_patch(name,x,y,z,width,height,mat):
    points=[]
    for i in range(10):
        angle=i*math.tau/10
        points.append((x+math.cos(angle)*width*(.4+random.random()*.1),y,z+math.sin(angle)*height*(.4+random.random()*.1)))
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(points,[],[tuple(range(len(points)))])
    return link_object(name,mesh,mat)

def brick_lines(front_x,front_y,bottom,width,height,skip):
    # Brick courses are sparse ink and shallow faces, rather than inflated rounded blocks.
    for row in range(int(height/.12)):
        z=bottom+row*.12
        for col in range(int(width/.31)):
            x=front_x-width/2+col*.31+(row%2)*.155
            if skip(x,z):continue
            if random.random()<.25:
                box('Variation in brick face',(x,front_y-.003,z),(.28,.008,.095),random.choice(bricks),0)
            if random.random()<.65:
                stroke('Brick horizontal joint',[(x-.14,front_y-.015,z-.053),(x+.145,front_y-.015,z-.053)],.0021)
            if random.random()<.4:
                stroke('Brick vertical joint',[(x+.145,front_y-.015,z-.053),(x+.145,front_y-.015,z+.05)],.0021)

active_collection=street
box('Street continuing beyond frame',(0,-5,-.12),(80,65,.2),asphalt,.005)
box('Raised concrete sidewalk',(0,.1,.015),(24,10,.27),concrete,.005)
box('Neighbourhood road edge',(0,-4.93,.04),(24,.18,.3),trim,.005)
for i in range(38):
    x=-11.5+i*.62
    stroke('Kerb stone joint',[(x,-5.03,-.02),(x,-5.03,.18),(x,-4.83,.18)],.004)
for ix in range(25):
    for iy in range(10):
        x=-12+ix
        y=-4.4+iy*.9
        stroke('Concrete slab joint',[(x,y,.155),(x+.96,y,.155)],.003)
        stroke('Concrete slab joint',[(x,y,.155),(x,y+.86,.155)],.003)
for i in range(7):
    box('Worn pedestrian crossing stripe',(1.8+i*.7,-6.2,-.006),(.39,2.35,.012),ivory,.001)
for x,y in [(-2.3,-4.58),(6.8,-4.58)]:
    box('Drain grate',(x,y,.159),(.6,.37,.015),dark,.002)
    for i in range(9):
        box('Drain grate opening',(x-.25+i*.06,y,.17),(.025,.28,.012),asphalt,0)

active_collection=seoul
cx=0; front=-1.1; side=3.3
box('Ground floor mass',(cx,1.3,1.65),(6.6,4.8,3),brick_mortar,.008)
box('Upper brick storey',(cx,1.3,4.75),(6.6,4.8,3.15),brick_mortar,.008)
box('Thin ground floor lintel',(cx,1.3,3.18),(6.72,4.92,.14),trim,.005)
box('Concrete roof overhang',(cx,1.3,6.4),(6.85,5.05,.18),trim,.005)
box('Flat roof',(cx,1.3,6.52),(6.55,4.75,.1),roof_grey,.005)
for x in [-2.09,0,2.09]:
    front_window('Upstairs café glazing',x,front-.035,4.78,1.88,1.93,wood)
for y in [-.22,1.57,3.02]:
    side_window('Corner upper glazing',side+.035,y,4.78,1.47 if y<2 else 1.08,1.93,wood)
brick_lines(cx,front-.012,.27,6.6,6.05,lambda x,z: (3.74<z<5.83 and any(abs(x-wx)<1.02 for wx in [-2.09,0,2.09])) or (.7<z<2.8))

# Deep green ground-level joinery with tall glazing and a single side-hinged door.
box('Streetfront timber surround',(0,front-.075,1.65),(6.42,.12,2.79),green,.006)
for x,w in [(-2.28,1.42),(.28,2.75),(2.35,1.15)]:
    front_window('Ground café shop window',x,front-.16,1.77,w,2.1,green,True)
box('Recessed café doorway',(-1.12,front-.225,1.49),(1.03,.08,2.61),dark,.005)
box('Timber glazed door',(-1.12,front-.28,1.5),(.87,.055,2.43),green,.005)
box('Door glazing',(-1.12,front-.317,1.69),(.7,.012,1.72),glass,.002)
rod('Brass door pull',(-.81,front-.37,1.2),(-.81,front-.37,1.53),.012,yellow,8)
box('Stone entry step',(-1.12,front-.4,.23),(1.2,.63,.16),trim,.005)
for y in [-.21,1.52,3.03]:
    side_window('Side ground café window',side+.045,y,1.73,1.5 if y<2 else 1,2.07,green)
box('Simple faded fabric canopy',(0,front-.4,2.96),(6.64,.8,.045),plaster,.004)
box('Canopy front canvas hem',(0,front-.8,2.86),(6.64,.035,.16),plaster,.002)
for x in [-3.02,3.02]:
    rod('Narrow awning bracket',(x,front,2.54),(x,front-.75,2.91),.017,dark,8)
box('Old timber café name board',(.32,front-.11,3.46),(3.42,.16,.39),wood,.005)
text('Korean café name','골목 커피',(.32,front-.205,3.47),.27,ivory,korean=True)
box('Vertical lightbox',(side+.25,front-.08,4.85),(.46,.22,1.6),paper,.006)
text('Lightbox Hangul','커\n피',(side+.25,front-.205,4.84),.31,green,korean=True)
rod('Lightbox top bracket',(side-.08,front+.03,5.67),(side+.44,front+.03,5.67),.022,dark,8)
text('Small upstairs lettering','COFFEE  /  ROOFTOP',(1.43,front-.096,5.49),.095,ivory)
text('Shopfront door sign','OPEN',(-1.12,front-.335,2.14),.12,ivory)

# Rooftop railing, practical furniture, plants and utilities echo the original photo.
for x in [-3.15+i*.56 for i in range(12)]:
    rod('Thin roof railing post',(x,front+.03,6.55),(x,front+.03,7.55),.014,ivory,6)
for z in [6.9,7.54]:
    rod('Roof front handrail',(-3.15,front+.03,z),(3.15,front+.03,z),.018,ivory,8)
for y in [-1.05+i*.55 for i in range(9)]:
    rod('Roof side railing post',(side-.1,y,6.55),(side-.1,y,7.55),.014,ivory,6)
for z in [6.9,7.54]:
    rod('Roof side handrail',(side-.1,-1.05,z),(side-.1,3.55,z),.018,ivory,8)
box('Roof stair enclosure',(-1.83,2.85,7.05),(1.55,1.35,1.12),plaster,.006)
box('Roof stair sheet metal cap',(-1.83,2.85,7.64),(1.7,1.5,.055),dark,.003)
for x,y in [(-2.48,-.4),(2.53,.03),(2.6,2.9)]:
    pot('Roof planter',x,y,6.57,.22)
before=set(seoul.objects)
cafe_table('Rooftop coffee table',.45,1.25)
chair('Rooftop metal chair',-.3,1.25,math.pi/2,wood,dark)
chair('Rooftop metal chair',1.19,1.25,-math.pi/2,wood,dark)
for obj in set(seoul.objects)-before:obj.location.z+=6.27
box('Outdoor air conditioner',(side+.22,2.52,3.38),(.35,.87,.54),ivory,.005)
fan=cylinder('Air conditioner fan',(side+.405,2.52,3.38),.19,.018,dark,20)
fan.rotation_euler.y=math.pi/2
for i in range(6):
    rod('Air conditioner grille',(side+.425,2.36+i*.064,3.24),(side+.425,2.36+i*.064,3.52),.006,trim,6)
curve('Exposed painted drainpipe',[(side+.13,3.42,6.42),(side+.13,3.42,3.3),(side+.24,3.42,3.14),(side+.24,3.42,.3)],.038,ivory)
curve('Exposed front conduit',[(-2.86,front-.12,3.24),(-2.86,front-.14,2.6),(-2.73,front-.14,2.48),(-2.73,front-.14,.28)],.021,ivory)
box('Electric meter box',(-2.88,front-.19,1.68),(.24,.12,.39),trim,.005)
for x in [-2.45,-.45,1.55,2.75]:
    rod('Wall light arm',(x,front-.12,3.83),(x,front-.38,3.79),.017,dark,8)
    shade=cylinder('Small wall lamp shade',(x,front-.38,3.76),.11,.07,dark,12,top_radius=.035)
    cylinder('Wall lamp diffuser',(x,front-.38,3.72),.075,.01,lamp_glow,12)

# Flanking buildings form an actual street rather than an isolated display base.
active_collection=melbourne
box('Left older plaster building',(-6.08,1.55,4.1),(5.52,5.3,7.95),cream,.006)
box('Left plaster building cornice',(-6.08,1.55,8.12),(5.65,5.42,.14),trim,.005)
for x in [-7.75,-5.65,-3.96]:
    front_window('Neighbour upstairs window',x,-1.16,6.49,.95,1.5,dark)
    front_window('Neighbour middle window',x,-1.16,4.34,1.02,1.43,dark)
box('Neighbour rolling metal shutter',(-6.64,-1.15,1.63),(3.7,.09,2.9),sky_blue,.004)
for i in range(26):
    stroke('Metal shutter slat',[(-8.46,-1.21,.29+i*.107),(-4.82,-1.21,.29+i*.107)],.0028)
box('Neighbour faded shop sign',(-6.7,-1.24,3.32),(3.76,.13,.39),paper,.005)
text('Neighbour shop lettering','사진관',(-6.7,-1.32,3.34),.27,green,korean=True)
box('Neighbour doorway',(-4.15,-1.18,1.57),(.83,.1,2.64),wood,.004)
front_window('Neighbour door glass',-4.15,-1.27,1.75,.59,1.63,dark)
for x,z,w,h in [(-8.44,3.8,.44,1.1),(-4.87,7.5,.62,.35),(-5.47,3.75,.46,.29),(-7.1,5.2,.9,.28)]:
    rough_patch('Uneven aged plaster',x,-1.118,z,w,h,plaster)
for i in range(14):
    x=random.uniform(-8.7,-3.4);z=random.uniform(.35,7.6)
    if any(abs(x-wx)<.7 and abs(z-wz)<1 for wx in [-7.75,-5.65,-3.96] for wz in [6.49,4.34]):continue
    stroke('Small plaster crack',[(x,-1.125,z),(x+.06,-1.125,z-.15),(x+.02,-1.125,z-.26)],.002)

box('Across the side alley building',(9.1,3.6,4.9),(5.1,8.8,9.5),plaster,.008)
box('Opposite shop base',(9.1,-.81,1.5),(5.1,.16,2.6),green,.005)
for x in [7.52,9.1,10.68]:
    for z in [4.2,6.55,8.65]:
        front_window('Across-alley window',x,-.84,z,.95,1.48,dark)
text('Across-alley shop sign','서울 상회',(9.1,-.92,2.99),.32,green,korean=True)
# Side-alley depth terminates with a much older, smaller block.
box('Distant alley building',(4.88,10.4,3.48),(3.1,2.1,6.7),sky_blue,.005)
for x in [4.15,5.65]:
    for z in [2.1,4.8]:front_window('Distant alley window',x,9.33,z,.81,1.2,dark)

active_collection=street
# Ground-level seating is more modest and asymmetrical than the first study.
cafe_table('Pavement café table',1.75,-2.6)
chair('Pavement café chair',.96,-2.58,math.pi/2,wood,dark)
chair('Pavement café chair',2.55,-2.58,-math.pi/2,wood,dark)
menu('Handwritten menu',-.48,-2.06)
for x,y in [(-2.8,-1.72),(3.73,-1.54),(3.72,2.05)]:pot('Street plant',x,y,.16,.24)
for i in range(3):
    x=4.02+i*.47
    cylinder('Red pavement stool seat',(x,-2.4,.56),.19,.065,red,14)
    for angle in [0,math.tau/3,math.tau*2/3]:
        rod('Red pavement stool leg',(x+math.cos(angle)*.16,-2.4+math.sin(angle)*.16,.18),(x+math.cos(angle)*.12,-2.4+math.sin(angle)*.12,.53),.018,red,7)
box('Stacked delivery crate',(-3.8,-2.05,.37),(.57,.41,.42),green,.004)
for i in range(5):
    box('Delivery crate opening',(-4.01+i*.1,-2.263,.4),(.05,.009,.19),wall_shadow,0)

# Utility pole and relaxed wire curves are key cues from the Seoul references.
px,py=5.6,-1.72
cylinder('Concrete utility pole',(px,py,4.28),.12,8.5,concrete,14,top_radius=.082)
for z in [1.1,1.42,1.74]:
    cylinder('Utility pole safety band',(px,py,z),.125,.16,yellow,14)
box('Utility pole cross arm',(px,py,7.62),(2.05,.13,.12),dark,.004)
for x in [px-.86,px-.28,px+.3,px+.87]:
    cylinder('Porcelain wire insulator',(x,py,7.77),.06,.21,ivory,8)
box('Pole transformer',(px+.23,py,6.89),(.43,.47,.82),trim,.004)
for i in range(4):
    y=py+(i-1.5)*.18
    stroke('Overhead utility cable',[(-12,y+.7,9.2),(-4,y+.2,7.14),(px,y,7.91),(11,y+.8,8.5)],.009)
for z in [6.65,6.88]:
    stroke('Alley building connection',[(px,py,z),(4.52,2,z-.48),(3.55,4.5,z-.12)],.007)
curve('Street lamp arm',[(px,py,6.5),(px,py-.45,6.8),(px,py-1.17,6.8)],.035,dark)
box('Street lamp head',(px,py-1.2,6.77),(.22,.43,.08),dark,.006)

# A natural, irregular street tree uses individual flat leaves rather than bubble clusters.
tx,ty=-8.2,-1.82
rod('Street tree trunk',(tx,ty,.16),(tx+.13,ty,5.6),.16,wood,10)
tips=[]
for i in range(10):
    angle=i*2.4
    tip=(tx+math.cos(angle)*(1.15+(i%3)*.25),ty+math.sin(angle)*1.1,5.2+(i%4)*.45)
    rod('Street tree branch',(tx+.06,ty,3.9+(i%2)*.7),tip,.035,wood,7)
    tips.append(tip)
for shade_index in range(4):
    vertices=[];faces=[]
    for i in range(160):
        tip=tips[i%len(tips)]
        x=tip[0]+random.uniform(-.7,.7);y=tip[1]+random.uniform(-.65,.65);z=tip[2]+random.uniform(-.55,.6)
        a=random.uniform(0,math.tau);length=random.uniform(.11,.23);width=length*.52
        start=len(vertices)
        vertices.extend([(x-math.cos(a)*length,y-math.sin(a)*length,z),(x-math.sin(a)*width,y+math.cos(a)*width,z+.035),(x+math.cos(a)*length,y+math.sin(a)*length,z+.06),(x+math.sin(a)*width,y-math.cos(a)*width,z+.025)])
        faces.append((start,start+1,start+2,start+3))
    mesh=bpy.data.meshes.new('Street tree leaves')
    mesh.from_pydata(vertices,[],faces)
    link_object('Fine street tree foliage',mesh,leaf[shade_index])

# Selectively drawn joints and wear add human scale without photographic texture noise.
for points in [[(-2,-4.2,.158),(-1.7,-4.03,.158),(-1.62,-3.7,.158)],[(5.2,-3.8,.158),(5.36,-3.57,.158),(5.32,-3.26,.158)],[(.1,-6.3,-.005),(.5,-6.1,-.005),(.75,-6.15,-.005)]]:
    stroke('Pavement hairline crack',points,.003)

active_collection=rig
world=bpy.data.worlds.new('Pale blue illustrated daylight')
world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(*colour('C4D3DC'),1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
scene.world=world
sun_data=bpy.data.lights.new('Broad afternoon sun','SUN')
sun_data.energy=1.8
sun_data.angle=math.radians(3)
sun_obj=link_object('Broad afternoon sun',sun_data)
sun_obj.rotation_euler=(math.radians(26),math.radians(-27),math.radians(-32))
fill_data=bpy.data.lights.new('Soft open-sky fill','AREA')
fill_data.energy=550
fill_data.size=15
fill_obj=link_object('Soft open-sky fill',fill_data)
fill_obj.location=(0,-9,12)
fill_obj.rotation_euler=(Vector((0,0,3))-fill_obj.location).to_track_quat('-Z','Y').to_euler()
camera_data=bpy.data.cameras.new('Street-level perspective')
camera_obj=link_object('Street-level perspective',camera_data)
camera_obj.location=(10,-16,2.65)
camera_obj.rotation_euler=(Vector((.25,.1,3.8))-camera_obj.location).to_track_quat('-Z','Y').to_euler()
camera_data.type='PERSP'
camera_data.lens=39
camera_data.clip_end=160
scene.camera=camera_obj
scene.render.engine='CYCLES'
scene.cycles.samples=32
scene.cycles.use_denoising=True
scene.render.resolution_x=1680
scene.render.resolution_y=1120
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(OUTPUT/'seoul-illustrated-v02.png')
scene.view_settings.view_transform='Standard'
scene.view_settings.look='Medium High Contrast' if 'Medium High Contrast' in [item.name for item in scene.view_settings.bl_rna.properties['look'].enum_items] else 'None'
scene.view_settings.exposure=0
scene.view_settings.gamma=1

# Use two colour bands based on surface direction. This removes the glossy/clay
# gradients of the first study while retaining a little light for contact shadows.
def illustrated_materials():
    used={mat for obj in scene.objects if obj.type in {'MESH','CURVE','FONT'} for mat in obj.data.materials if mat}
    for mat in used:
        nodes=mat.node_tree.nodes
        links=mat.node_tree.links
        output=next(node for node in nodes if node.type=='OUTPUT_MATERIAL')
        normal=nodes.new('ShaderNodeNewGeometry')
        direction=nodes.new('ShaderNodeVectorMath')
        direction.operation='DOT_PRODUCT'
        direction.inputs[1].default_value=(-.48,-.55,.72)
        links.new(normal.outputs['Normal'],direction.inputs[0])
        threshold=nodes.new('ShaderNodeMath')
        threshold.operation='GREATER_THAN'
        threshold.inputs[1].default_value=.24
        links.new(direction.outputs['Value'],threshold.inputs[0])
        colours=nodes.new('ShaderNodeMixRGB')
        colours.blend_type='MIX'
        base=mat.diffuse_color
        colours.inputs[1].default_value=(base[0]*.74,base[1]*.77,base[2]*.85,1)
        colours.inputs[2].default_value=base
        links.new(threshold.outputs[0],colours.inputs[0])
        emission=nodes.new('ShaderNodeEmission')
        emission.inputs['Strength'].default_value=1
        links.new(colours.outputs[0],emission.inputs['Color'])
        diffuse=nodes.new('ShaderNodeBsdfDiffuse')
        links.new(colours.outputs[0],diffuse.inputs['Color'])
        mix=nodes.new('ShaderNodeMixShader')
        mix.inputs[0].default_value=.12
        links.new(emission.outputs[0],mix.inputs[1])
        links.new(diffuse.outputs[0],mix.inputs[2])
        links.new(mix.outputs[0],output.inputs['Surface'])

illustrated_materials()

# Freestyle is the Blender art-review equivalent of the runtime outline pass.
scene.render.use_freestyle=True
scene.render.line_thickness=1
settings=scene.view_layers[0].freestyle_settings
settings.crease_angle=math.radians(120)
line_set=settings.linesets[0] if len(settings.linesets) else settings.linesets.new('Fine architectural ink')
line_set.select_silhouette=True
line_set.select_border=True
line_set.select_crease=True
line_set.select_material_boundary=False
line_set.select_external_contour=True
line_set.linestyle.color=colour('414C59')
line_set.linestyle.thickness=.72
line_set.linestyle.alpha=.8

for obj in bpy.context.selected_objects:obj.select_set(False)
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_perspective='CAMERA'
        area.spaces.active.overlay.show_overlays=False
        area.spaces.active.shading.type='MATERIAL'
scene['style']='Moebius-inspired illustrated 3D / architectural ink and flat colour'
scene['revision']='v02: photographic building proportions, street-level perspective, fine linework, restrained edges, lived-in details; no miniature plinth.'
scene['reference']='User supplied Seoul corner café photographs and https://x.com/javpixel_art/status/2119232534592590158'
scene['runtimeNote']='Blender uses fine Freestyle lines and two-band directional materials. Three.js will need an equivalent outline/toon-material pass; this is an art target, not a browser-ready shader export.'
for loaded_font in [font,korean_font]:
    if not loaded_font.packed_file:loaded_font.pack()
bpy.data.libraries.write(str(OUTPUT/'seoul-street-v02.blend'),{scene},fake_user=True,compress=True)
result={'scene':scene.name,'objects':len(scene.objects),'source':str(OUTPUT/'seoul-street-v02.blend')}

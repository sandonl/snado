"""Editable café art study. Run in Blender; adds a new scene without changing existing objects.

Z is up, metres are world units, storefronts face -Y. GLB export converts to Y-up.
No external textures: coloured geometry and standard Principled materials travel to glTF.
"""

import bpy
import math
import random
from pathlib import Path
from mathutils import Vector

OUTPUT = Path(__file__).resolve().parent
random.seed(14)
scene = bpy.data.scenes.new("Sandon · Melbourne & Seoul · café study")
bpy.context.window.scene = scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1

def collection(name):
    value = bpy.data.collections.new(name)
    scene.collection.children.link(value)
    return value

melbourne = collection("01 · Melbourne · Little Lane Coffee")
seoul = collection("02 · Seoul · Golmok Coffee")
street = collection("03 · Shared laneway & café furniture")
rig = collection("04 · Preview cameras & lighting · excluded from GLB")
active_collection = street

def colour(hex_value):
    rgb = [int(hex_value[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v < .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb)

def material(name, hex_value, roughness=.75, metal=0, glow=0):
    value = bpy.data.materials.new("Café · " + name)
    value.diffuse_color = (*colour(hex_value), 1)
    value.use_nodes = True
    shader = value.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = value.diffuse_color
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Metallic"].default_value = metal
    if glow:
        shader.inputs["Emission Color"].default_value = value.diffuse_color
        shader.inputs["Emission Strength"].default_value = glow
    return value

cream = material("oat plaster", "EBD9B4")
ivory = material("porcelain", "FFF0CF")
trim = material("sandstone edges", "C9B58E")
green = material("eucalyptus paint", "3C6555")
sage = material("awning sage", "718A65")
dark = material("deep forest metal", "233D37", .48, .15)
ink = material("coffee charcoal", "303936")
brick_mortar = material("warm brick mortar", "9B6450")
bricks = [material("clay brick %d" % i, h) for i,h in enumerate(["AA6045", "B87555", "C0815B", "A85E43", "BC6E4D"])]
terracotta = material("terracotta", "C96B45")
rust = material("awning persimmon", "BB583E")
wood = material("honey timber", "A96F3F")
light_wood = material("table oak", "D8A260")
coffee = material("espresso", "563827")
glass = material("stylised blue green glazing", "557A79", .28, .12)
glass_light = material("sky reflected in glass", "9CB8AD", .4)
glow = material("honey window light", "FFD68E", .55, glow=.35)
lamp_glow = material("warm lanterns", "FFE2A3", .5, glow=2)
chalk = material("chalkboard", "28453E")
yellow = material("street ochre", "D8B35C")
leaf = [material("foliage %d" % i, h) for i,h in enumerate(["47694F", "638455", "88A266", "ABAF6C"])]
stone = [material("bluestone %d" % i, h) for i,h in enumerate(["707D79", "7C8780", "8C9489", "647571"])]
grout = material("paving grout", "535F59")
base_mat = material("diorama base", "B9AD8E")
backdrop = material("studio sand", "D9CEB4")

def link_object(name, data, mat=None):
    obj = bpy.data.objects.new(name, data)
    active_collection.objects.link(obj)
    if mat:
        data.materials.append(mat)
    return obj

def bevel(obj, width=.035, segments=2):
    mod = obj.modifiers.new("Soft toy-like edges", "BEVEL")
    mod.width = width
    mod.segments = segments
    mod = obj.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    mod.keep_sharp = True
    return obj

def box(name, pos, size, mat, edge=.025):
    x,y,z = [v/2 for v in size]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([(-x,-y,-z),(-x,-y,z),(-x,y,-z),(-x,y,z),(x,-y,-z),(x,-y,z),(x,y,-z),(x,y,z)], [], [(2,6,4,0),(5,7,3,1),(4,5,1,0),(3,7,6,2),(1,3,2,0),(6,7,5,4)])
    mesh.update()
    obj = link_object(name, mesh, mat)
    obj.location = pos
    if edge:
        bevel(obj, min(edge,min(size)/3))
    return obj

def sphere(name, pos, scale, mat, subdivisions=1):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1, location=pos)
    obj = bpy.context.object
    for value in list(obj.users_collection):
        value.objects.unlink(obj)
    active_collection.objects.link(obj)
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat)
    return obj

def cylinder(name, pos, radius, depth, mat, vertices=16, top_radius=None):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius, radius2=radius if top_radius is None else top_radius, depth=depth, location=pos)
    obj = bpy.context.object
    for value in list(obj.users_collection):
        value.objects.unlink(obj)
    active_collection.objects.link(obj)
    obj.name = name
    obj.data.materials.append(mat)
    bevel(obj, .016, 2)
    return obj

def rod(name, start, end, radius, mat, vertices=10):
    start,end=Vector(start),Vector(end)
    obj = cylinder(name, (start+end)/2, radius, (end-start).length, mat, vertices)
    obj.rotation_euler = (end-start).to_track_quat('Z','Y').to_euler()
    return obj

def curve(name, points, radius, mat):
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = '3D'
    data.resolution_u = 12
    data.bevel_depth = radius
    data.bevel_resolution = 2
    spline = data.splines.new("BEZIER")
    spline.bezier_points.add(len(points)-1)
    for point, co in zip(spline.bezier_points, points):
        point.co = co
        point.handle_left_type = point.handle_right_type = 'AUTO'
    return link_object(name,data,mat)

font = bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf')
korean_font = bpy.data.fonts.load('/System/Library/Fonts/AppleSDGothicNeo.ttc')

def text(name, body, pos, size, mat=ivory, rotation=(math.pi/2,0,0), korean=False):
    data = bpy.data.curves.new(name, 'FONT')
    data.body = body
    data.font = korean_font if korean else font
    data.size = size
    data.align_x = 'CENTER'
    data.align_y = 'CENTER'
    data.extrude = .002
    # Letter bevels add thousands of invisible faces at this viewing distance.
    data.bevel_depth = 0
    data.resolution_u = 3
    obj = link_object(name, data, mat)
    obj.location = pos
    obj.rotation_euler = rotation
    return obj

def panel_window(name, x, y, z, width, height, frame=green, side=False):
    # Layered opaque panes retain their illustrated look without transparency sorting.
    if not side:
        box(name+' outer frame',(x,y,z),(width+.16,.15,height+.16),frame,.035)
        box(name+' pane',(x,y-.085,z),(width,.025,height),glass,.008)
        box(name+' mullion',(x,y-.12,z),(.065,.07,height),frame,.012)
        box(name+' rail',(x,y-.13,z-height*.15),(width,.07,.06),frame,.012)
        box(name+' sill',(x,y-.12,z-height/2-.1),(width+.28,.3,.12),ivory,.035)
        box(name+' reflection',(x-width*.28,y-.105,z+.06),(.085,.015,height*.65),glass_light,.015)
    else:
        box(name+' outer frame',(x,y,z),(.15,width+.16,height+.16),frame,.035)
        box(name+' pane',(x+.085,y,z),(.025,width,height),glass,.008)
        box(name+' mullion',(x+.12,y,z),(.07,.065,height),frame,.012)
        box(name+' rail',(x+.13,y,z-height*.15),(.07,width,.06),frame,.012)
        box(name+' sill',(x+.12,y,z-height/2-.1),(.3,width+.28,.12),ivory,.035)
        box(name+' reflection',(x+.105,y-width*.28,z+.06),(.015,.085,height*.65),glass_light,.01)

def pot(name,x,y,z,size=.35):
    cylinder(name+' clay pot',(x,y,z+size*.48),size*.62,size*.96,terracotta,12,top_radius=size*.82)
    cylinder(name+' rim',(x,y,z+size*.92),size*.86,size*.16,terracotta,12)
    cylinder(name+' soil',(x,y,z+size),size*.69,.03,coffee,12)
    for i in range(6):
        angle=i*math.tau/6
        rod(name+' stem',(x,y,z+size),(x+math.cos(angle)*size*.5,y+math.sin(angle)*size*.5,z+size*(2.1+(i%2)*.4)),.022,leaf[0],7)
        sphere(name+' leaf',(x+math.cos(angle)*size*.55,y+math.sin(angle)*size*.55,z+size*(2.1+(i%2)*.4)),(size*.32,size*.17,size*.62),leaf[i%4],1)

def cup(name,x,y,z,scale=1):
    cylinder(name+' saucer',(x,y,z+.015*scale),.14*scale,.025*scale,ivory,20)
    cylinder(name+' porcelain',(x,y,z+.09*scale),.075*scale,.14*scale,ivory,20,top_radius=.1*scale)
    cylinder(name+' coffee',(x,y,z+.163*scale),.083*scale,.007*scale,coffee,20)
    cylinder(name+' crema',(x-.018*scale,y,z+.169*scale),.037*scale,.006*scale,light_wood,16)
    points=[(x+.08*scale,y,z+.14*scale),(x+.15*scale,y,z+.14*scale),(x+.15*scale,y,z+.06*scale),(x+.08*scale,y,z+.05*scale)]
    curve(name+' handle',points,.018*scale,ivory)

def chair(name,x,y,angle=0,seat=wood,metal=dark):
    # Local coordinates make each chair's facing easy to change.
    def p(a,b,c):
        return (x+a*math.cos(angle)-b*math.sin(angle),y+a*math.sin(angle)+b*math.cos(angle),c)
    cylinder(name+' seat',p(0,0,.84),.29,.1,seat,16)
    for a in [-.21,.21]:
        for b in [-.18,.18]:
            rod(name+' leg',p(a*1.35,b*1.35,.33),p(a,b,.83),.032,metal)
    curve(name+' bent back',[p(-.25,.18,.82),p(-.28,.24,1.33),p(0,.27,1.49),p(.28,.24,1.33),p(.25,.18,.82)],.038,metal)
    for a in [-.14,0,.14]:
        rod(name+' back spindle',p(a,.25,.89),p(a,.25,1.37),.023,metal)

def cafe_table(name,x,y,style='round'):
    z=1.1
    if style=='round':
        cylinder(name+' top',(x,y,z),.52,.11,light_wood,24)
    else:
        box(name+' top',(x,y,z),(1,.72,.1),light_wood,.055)
    cylinder(name+' pedestal',(x,y,.71),.065,.7,dark,12)
    for a in [0,math.tau/3,math.tau*2/3]:
        rod(name+' foot',(x,y,.43),(x+math.cos(a)*.38,y+math.sin(a)*.38,.34),.04,dark)
    cup(name+' flat white',x-.13,y-.08,z+.06)
    cup(name+' espresso',x+.2,y+.1,z+.06,.78)

def menu(name,x,y):
    board=box(name+' frame',(x,y,1),( .69,.12,1.1),wood,.045)
    board.rotation_euler.x=math.radians(-9)
    box(name+' chalk face',(x,y-.075,1),(.56,.03,.9),chalk,.012)
    text(name+' title','COFFEE',(x,y-.105,1.23),.11)
    text(name+' line one','ESPRESSO',(x,y-.107,1.02),.065)
    text(name+' line two','FILTER / MILK',(x,y-.107,.85),.058)
    rod(name+' back leg',(x,y+.42,.32),(x,y,1.45),.035,wood)
    rod(name+' front left',(x-.27,y-.1,.32),(x-.27,y,1.45),.035,wood)
    rod(name+' front right',(x+.27,y-.1,.32),(x+.27,y,1.45),.035,wood)

def awning(name,x,y,z,width,projection,mat):
    for i in range(12):
        stripe=box(name+' canvas stripe',(x-width/2+width/12*(i+.5),y-projection/2,z),(width/12-.008,projection,.1),ivory if i%2 else mat,.018)
        stripe.rotation_euler.x=math.radians(12)
        box(name+' scalloped valance',(x-width/2+width/12*(i+.5),y-projection,z-.2),(width/12-.009,.08,.25),ivory if i%2 else mat,.065)
    for offset in [-width/2+.12,width/2-.12]:
        rod(name+' brace',(x+offset,y+.05,z-.7),(x+offset,y-projection+.05,z-.15),.027,dark)

# Shared ground: clear flat walking area; miniature base is only presentation framing.
box('Rounded neighbourhood plinth',(0,0,-.22),(18.5,11.7,.7),base_mat,.27)
box('Bluestone mortar bed',(0,-.15,.145),(18.15,11.3,.12),grout,.12)
for row in range(20):
    y=-5.4+row*.55
    for column in range(27):
        x=-8.8+column*.67+(row%2)*.28
        if x>9: continue
        box('Shared lane · bluestone paver',(x,y,.23),(.62,.51,.09),random.choice(stone),.018)
for x in [-8.75,8.75]:
    for y in [-4.7+i*.65 for i in range(15)]:
        box('Kerb stone',(x,y,.3),(.23,.6,.22),trim,.03)
box('Melbourne city plaque',(-4.6,-5.84,-.14),(5.3,.05,.36),green,.035)
text('Melbourne city name','M E L B O U R N E',(-4.6,-5.88,-.14),.22)
box('Seoul city plaque',(4.6,-5.84,-.14),(5.3,.05,.36),rust,.035)
text('Seoul city name','S E O U L   /   서울',(4.6,-5.88,-.14),.22,korean=True)

# MELBOURNE: tall cream laneway café, exaggerated cornices and green joinery.
active_collection=melbourne
mx=-4.6
front=-.9
box('Melbourne ground slab',(mx,1.2,.38),(5.4,4.45,.28),trim,.06)
box('Melbourne upper storey',(mx,1.2,4.32),(5.25,4.25,2.45),cream,.07)
box('Melbourne rear ground wall',(mx,3.25,1.72),(5.25,.2,2.7),cream,.05)
box('Melbourne west wall',(mx-2.55,1.2,1.72),(.2,4.25,2.7),cream,.05)
box('Melbourne east wall',(mx+2.55,1.2,1.72),(.2,4.25,2.7),cream,.05)
for x in [mx-2.5,mx-1,mx+1,mx+2.5]:
    box('Melbourne shopfront pier',(x,front,1.75),(.19,.28,2.65),green,.025)
    box('Pier plinth',(x,front-.05,.55),(.29,.35,.35),green,.025)
box('Melbourne front fascia',(mx,front-.03,2.94),(5.42,.32,.52),green,.04)
text('Little Lane lettering','LITTLE LANE',(mx,front-.207,2.98),.37)
box('Melbourne fascia top lip',(mx,front-.08,3.24),(5.57,.4,.12),ivory,.025)
for x,w in [(mx-1.77,1.27),(mx+1.77,1.27)]:
    box('Shop window lower panelling',(x,front, .75),(w,.2,.65),green,.02)
    box('Shop window warm recess',(x,front+.18,1.78),(w,.04,1.42),glow,.025)
    for dx in [-w*.28,w*.28]:
        rod('Window mullion',(x+dx,front-.02,1.06),(x+dx,front-.02,2.48),.026,green)
    box('Shop window sill',(x,front-.15,1.06),(w+.08,.34,.1),ivory,.02)
    box('Shop transom',(x,front-.02,2.22),(w,.1,.065),green,.01)
box('Door shadow',(mx,front+.15,1.63),(1.75,.08,2.3),dark,.025)
for dx in [-.43,.43]:
    box('Double timber door',(mx+dx,front-.02,1.63),(.81,.11,2.28),green,.025)
    box('Door glass',(mx+dx,front-.087,1.9),(.61,.025,1.32),glass,.012)
    box('Door bottom panel',(mx+dx,front-.095,.82),(.6,.035,.43),sage,.015)
    rod('Door brass pull',(mx+dx*.25,front-.17,1.3),(mx+dx*.25,front-.17,1.62),.023,yellow)
text('Door opening hours','OPEN',(mx,front-.16,2.3),.13)
box('Doorstep',(mx,front-.34,.43),(2.05,.7,.2),trim,.045)
awning('Melbourne striped awning',mx,front-.13,2.56,5.12,.92,sage)
for x in [mx-1.65,mx,mx+1.65]:
    panel_window('Melbourne upper sash',x,front-.04,4.37,1.02,1.47)
    box('Sash header',(x,front-.09,5.19),(1.27,.22,.15),ivory,.04)
for y in [.2,1.8]:
    panel_window('Melbourne laneway sash',mx+2.67,y,4.36,1.05,1.4,side=True)
    panel_window('Melbourne laneway shop',mx+2.68,y,1.72,1.1,1.6,side=True)
for z,w,d,h in [(5.55,5.45,4.45,.16),(5.76,5.66,4.6,.19),(6.0,5.48,4.35,.29)]:
    box('Melbourne stepped cornice',(mx,1.2,z),(w,d,h),ivory,.035)
box('Melbourne central parapet',(mx,front+.03,6.24),(2.7,.32,.66),cream,.06)
box('Melbourne parapet cap',(mx,front+.01,6.59),(2.9,.43,.14),ivory,.04)
text('Melbourne parapet lettering','COFFEE DAILY',(mx,front-.15,6.29),.16,green)
for x in [mx-2.4,mx+2.4]:
    cylinder('Parapet urn base',(x,front+.1,6.25),.18,.28,trim,12)
    sphere('Parapet urn',(x,front+.1,6.48),(.22,.22,.25),ivory,2)
for row in range(8):
    for column in range(5):
        # Sparse plaster blocks read at walking distance without a noisy brick texture.
        x=mx-2.3+column*.96+(row%2)*.18
        if x>mx+2.4: continue
        z=3.25+row*.28
        if any(abs(x-wx)<.69 and abs(z-4.37)<.9 for wx in [mx-1.65,mx,mx+1.65]): continue
        box('Melbourne plaster block',(x,front-.035,z),(.64,.025,.15),trim,.012)

# Projecting cup sign: orientation toward front; bracket grows from the east corner.
rod('Cup sign wall bracket',(mx+2.45,front,3.95),(mx+3.14,front-.05,3.95),.045,dark)
rod('Cup sign chain',(mx+3.08,front-.04,3.93),(mx+3.08,front-.04,3.58),.022,dark)
disk=cylinder('Round hanging coffee sign',(mx+3.08,front-.05,3.27),.43,.12,green,32)
disk.rotation_euler.x=math.pi/2
box('Cup sign porcelain relief',(mx+3.04,front-.13,3.27),(.25,.028,.2),ivory,.035)
curve('Cup sign handle relief',[(mx+3.16,front-.15,3.35),(mx+3.26,front-.15,3.32),(mx+3.24,front-.15,3.23),(mx+3.16,front-.15,3.23)],.025,ivory)
rod('Cup sign saucer relief',(mx+2.87,front-.15,3.12),(mx+3.22,front-.15,3.12),.018,ivory)
curve('Cup sign steam relief',[(mx+3.04,front-.15,3.44),(mx+3.01,front-.15,3.5),(mx+3.06,front-.15,3.56)],.012,ivory)

# Interior coffee-making details sit in the window bays.
box('Melbourne interior counter',(mx-1.74,front+.25,1.2),(1.15,.5,.16),wood,.03)
box('Melbourne espresso machine',(mx-1.78,front+.12,1.48),(.63,.24,.39),ivory,.055)
box('Melbourne espresso machine inset',(mx-1.78,front-.02,1.46),(.48,.035,.16),dark,.01)
for dx in [-.16,.16]:
    rod('Melbourne portafilter',(mx-1.78+dx,front-.06,1.43),(mx-1.78+dx,front-.22,1.43),.025,dark)
pot('Melbourne window fern',mx+1.76,front-.03,1.15,.22)

# SEOUL: rounded brick corner café with glazing, rooftop seating and handmade signs.
active_collection=seoul
sx=4.4
sf=-1.25
right=sx+2.5
box('Seoul foundation',(sx,.9,.39),(5.25,4.65,.3),trim,.06)
box('Seoul upper storey',(sx,.9,4.05),(5.1,4.4,2.3),brick_mortar,.095)
box('Seoul ground back wall',(sx,3.03,1.64),(5.1,.21,2.65),brick_mortar,.04)
box('Seoul ground west wall',(sx-2.45,.9,1.64),(.2,4.4,2.65),brick_mortar,.04)
for x in [sx-2.42,sx-1.13,sx+1.15,sx+2.43]:
    box('Seoul timber shop pier',(x,sf,1.69),(.18,.25,2.7),wood,.025)
box('Seoul floor fascia',(sx,.9,2.93),(5.3,4.58,.2),trim,.035)
box('Seoul ground lower brick band',(sx,sf,.67),(5,.2,.55),brick_mortar,.04)
for x,w in [(sx-1.78,1.04),(sx+.0,1.99),(sx+1.82,1.06)]:
    panel_window('Seoul ground café window',x,sf-.06,1.81,w,1.65,wood)
    box('Seoul lower window warmth',(x,sf-.162,1.64),(w-.12,.012,.52),glow,.01)
box('Seoul café door frame',(sx-1.16,sf-.19,1.59),(.88,.14,2.34),dark,.035)
box('Seoul café door glazing',(sx-1.16,sf-.27,1.76),(.63,.03,1.64),glass,.015)
rod('Seoul door handle',(sx-.94,sf-.33,1.2),(sx-.94,sf-.33,1.55),.023,yellow)
box('Seoul entry step',(sx-1.16,sf-.38,.44),(1.25,.72,.2),trim,.04)
box('Seoul coffee fascia',(sx,sf-.12,2.69),(5.3,.2,.5),green,.04)
text('Golmok Korean café name','골목 커피',(sx-.48,sf-.235,2.71),.36,ivory,korean=True)
text('Golmok English café name','GOLMOK',(sx+1.61,sf-.235,2.72),.16)
for x in [sx-1.3,sx+1.3]:
    panel_window('Seoul upstairs picture window',x,sf-.08,4.03,2.14,1.5,wood)
    box('Seoul upstairs lamp glow',(x,sf-.183,3.84),(1.91,.012,.48),glow,.02)
    for dx in [-.64,.64]:
        box('Seoul upstairs glass mullion',(x+dx,sf-.22,4.03),(.045,.06,1.5),wood,.009)
for y in [-.38,1.46]:
    panel_window('Seoul corner upstairs window',right+.07,y,4.03,1.5,1.5,wood,True)
    panel_window('Seoul corner downstairs window',right+.07,y,1.75,1.5,1.55,wood,True)

# Selective individual bricks form proper geometry on both street-facing elevations.
for row in range(27):
    z=.52+row*.17
    for col in range(11):
        x=sx-2.32+col*.46+(row%2)*.23
        if x>sx+2.44: continue
        if z>3.12 and z<4.89 and any(abs(x-wx)<1.19 for wx in [sx-1.3,sx+1.3]): continue
        if .98<z<2.97: continue
        box('Seoul façade clay brick',(x,sf-.119,z),(.425,.07,.135),random.choice(bricks),.012)
    for col in range(9):
        y=-1.07+col*.47+(row%2)*.23
        if y>2.99:continue
        if any(abs(y-wy)<.9 for wy in [-.38,1.46]) and ((.89<z<2.62) or (3.15<z<4.9)):continue
        box('Seoul corner clay brick',(right+.085,y,z),(.07,.43,.135),random.choice(bricks),.012)

box('Seoul roof slab',(sx,.9,5.29),(5.5,4.72,.23),trim,.07)
box('Seoul rooftop timber deck',(sx,.9,5.44),(5.2,4.4,.12),wood,.02)
for i in range(15):
    box('Rooftop deck board',(sx-2.43+i*.347,.9,5.515),(.32,4.3,.035),light_wood,.006)
for x in [sx-2.5,sx-1.25,sx,sx+1.25,sx+2.5]:
    rod('Roof front railing upright',(x,sf-.01,5.5),(x,sf-.01,6.27),.031,ivory)
for y in [-1.25,-.2,.85,1.9,3.05]:
    rod('Roof side railing upright',(right+.03,y,5.5),(right+.03,y,6.27),.031,ivory)
rod('Roof front top rail',(sx-2.5,sf-.01,6.27),(sx+2.5,sf-.01,6.27),.036,ivory)
rod('Roof front middle rail',(sx-2.5,sf-.01,5.83),(sx+2.5,sf-.01,5.83),.026,ivory)
rod('Roof side top rail',(right+.03,sf,6.27),(right+.03,3.05,6.27),.036,ivory)
rod('Roof side middle rail',(right+.03,sf,5.83),(right+.03,3.05,5.83),.026,ivory)
for x in [sx-2,sx+2]:
    for y in [.15,2.68]:
        rod('Rooftop pergola upright',(x,y,5.48),(x,y,7.05),.065,green)
for y in [.15,2.68]:
    box('Rooftop pergola crossbeam',(sx,y,7.04),(4.45,.16,.18),green,.025)
for i in range(7):
    box('Rooftop pergola slat',(sx-2.05+i*.68,1.42,7.15),(.13,3.1,.12),sage,.025)
# A rooftop table uses local geometry translated upward as one semantic group.
before=set(seoul.objects)
cafe_table('Seoul rooftop table',sx+.3,1.3)
chair('Seoul rooftop chair',sx-.45,1.3,math.pi/2,ivory,green)
chair('Seoul rooftop chair',sx+1.05,1.3,-math.pi/2,ivory,green)
for obj in set(seoul.objects)-before: obj.location.z += 5.2
pot('Rooftop garden',sx-1.7,2.1,5.53,.35)
pot('Rooftop garden',sx+1.7,2.1,5.53,.4)

# Side sign, roll-down awning and recognisable Seoul street details.
box('Seoul vertical projecting sign',(right+.36,sf+.06,4.45),(.58,.28,1.74),rust,.065)
text('Seoul vertical coffee lettering','커\n피',(right+.36,sf-.095,4.47),.41,ivory,korean=True)
awning('Seoul short striped canopy',sx+1.07,sf-.17,2.36,2.32,.64,rust)
box('Seoul external air conditioner',(right+.22,2.45,3.17),(.4,1,.62),ivory,.05)
fan=cylinder('Seoul AC fan',(right+.44,2.45,3.17),.225,.025,dark,20)
fan.rotation_euler.y=math.pi/2
for angle in [0,math.pi/2]:
    start=(right+.47,2.45+math.cos(angle)*.19,3.17+math.sin(angle)*.19)
    end=(right+.47,2.45-math.cos(angle)*.19,3.17-math.sin(angle)*.19)
    rod('AC fan grille',start,end,.015,trim)
curve('Seoul painted drainpipe',[(right+.17,2.95,5.3),(right+.17,2.95,3),(right+.27,3.04,2.8),(right+.27,3.04,.5)],.048,green)
for i in range(4):
    x=sx-1.7+i*1.1
    rod('Seoul lantern cord',(x,sf-.28,3.12),(x,sf-.28,2.91),.012,dark)
    sphere('Seoul paper lantern',(x,sf-.28,2.84),(.12,.12,.15),lamp_glow,2)

# Shared furniture and plants: coffee is the main activity in this neighbourhood.
active_collection=street
for name,x,y in [('Melbourne pavement table',-5.9,-3.26),('Melbourne laneway table',-2.65,-3.8),('Seoul pavement table',5.65,-3.38)]:
    cafe_table(name,x,y)
    chair(name+' chair',x-.84,y,math.pi/2,wood,green if x<0 else dark)
    chair(name+' chair',x+.84,y,-math.pi/2,wood,green if x<0 else dark)
menu('Melbourne daily menu',-4.15,-2.5)
menu('Seoul daily menu',3.4,-2.75)
for name,x,y,size in [('Melbourne entrance pot',-6.9,-1.8,.36),('Melbourne entrance pot',-3.25,-1.85,.3),('Seoul entrance pot',2.1,-1.95,.32),('Seoul corner pot',7.15,-1.75,.38)]:
    pot(name,x,y,.3,size)

# Café umbrella with an exaggerated scalloped eight-sided canopy.
ux,uy=-5.9,-3.26
cylinder('Umbrella weighted foot',(ux,uy,.37),.3,.12,trim,16)
rod('Umbrella timber pole',(ux,uy,.35),(ux,uy,3.5),.045,wood)
vertices=[(ux,uy,3.65)]
for z,radius in [(3.38,.64),(3.04,1.38)]:
    for i in range(8):
        a=i*math.tau/8
        vertices.append((ux+math.cos(a)*radius,uy+math.sin(a)*radius,z))
faces=[]
for i in range(8):
    j=(i+1)%8
    faces.extend([(0,1+i,1+j),(1+i,9+i,9+j,1+j)])
mesh=bpy.data.meshes.new('Umbrella fabric')
mesh.from_pydata(vertices,[],faces)
mesh.materials.append(green);mesh.materials.append(sage)
for polygon in mesh.polygons: polygon.material_index=(polygon.index//2)%2
link_object('Melbourne octagonal umbrella',mesh)
for i in range(8):
    a=i*math.tau/8
    rod('Umbrella rib',(ux,uy,3.61),(ux+math.cos(a)*1.38,uy+math.sin(a)*1.38,3.04),.015,ivory)

# A tree and string lights frame the join between cities without closing the lane.
tx,ty=-.2,3.15
box('Tree planter',(tx,ty,.47),(1.25,1.25,.4),cream,.09)
cylinder('Tree soil',(tx,ty,.7),.48,.05,coffee,16)
rod('Laneway tree trunk',(tx,ty,.65),(tx-.12,ty,4.6),.16,wood,9)
for a in [0,2,4]:
    rod('Tree branch',(tx-.05,ty,3.2),(tx+math.cos(a)*.8,ty+math.sin(a)*.7,4.6),.08,wood,7)
for i in range(13):
    angle=i*2.4
    sphere('Rounded tree canopy',(tx+math.cos(angle)*(.5+(i%3)*.25),ty+math.sin(angle)*(.5+(i%3)*.2),4.55+(i%4)*.37),(.8,.72,.85),leaf[i%4],2)
curve('Laneway festoon cable',[(-1.9,-.15,4.1),(0,-.15,3.63),(1.85,-.15,4.1)],.018,dark)
for i in range(7):
    x=-1.55+i*.52
    z=3.64+.12*x*x
    rod('Festoon pendant',(x,-.15,z),(x,-.15,z-.13),.016,dark,8)
    sphere('Festoon bulb',(x,-.15,z-.19),(.08,.08,.105),lamp_glow,2)
for x in [-1.05,.55]:
    for y in [-4.8,-1.7]:
        cylinder('Lane bollard foot',(x,y,.37),.16,.13,dark,12)
        cylinder('Lane bollard',(x,y,.78),.067,.8,green,12)
        sphere('Lane bollard cap',(x,y,1.2),(.09,.09,.09),yellow,2)

# Minimal road markings are inlaid geometry, not a photographic ground texture.
for y in [-4.5,-3.45,-2.4,-1.35,.0,1.1]:
    box('Laneway centre inlay',(-.05,y,.283),(.07,.42,.01),ivory,.006)
for i in range(6):
    box('Seoul pedestrian crossing',(2.0+i*.62,-4.85,.283),(.38,.58,.012),ivory,.015)

# Semantic anchors are exported for future Three.js discovery interactions.
for target_collection,name,position,slug in [(melbourne,'discover-melbourne-cafe',(mx,front-.8,.3),'about/coffee'),(seoul,'discover-seoul-cafe',(sx-1.16,sf-.8,.3),'about/seoul')]:
    anchor=bpy.data.objects.new(name,None)
    target_collection.objects.link(anchor)
    anchor.location=position
    anchor.empty_display_type='CIRCLE'
    anchor.empty_display_size=.4
    anchor['contentSlug']=slug
    anchor['role']='discovery-anchor'

# Combine repeated static detail per material to keep the exported prototype manageable.
# Named café parts, furniture families and semantic anchors remain distinct/editable.
batch_prefixes=('Shared lane ·','Seoul façade clay brick','Seoul corner clay brick','Rooftop deck board','Melbourne plaster block')
for source_collection in (melbourne,seoul,street):
    for prefix in batch_prefixes:
        objects=[obj for obj in source_collection.objects if obj.type=='MESH' and obj.name.startswith(prefix)]
        if len(objects)<2:continue
        for obj in bpy.context.selected_objects:obj.select_set(False)
        for obj in objects:obj.select_set(True)
        bpy.context.view_layer.objects.active=objects[0]
        # Apply each small bevel before joining so it doesn't affect touching pavers.
        for obj in objects:
            bpy.context.view_layer.objects.active=obj
            for mod in list(obj.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.context.view_layer.objects.active=objects[0]
        bpy.ops.object.join()
        objects[0].name=prefix+' · batched detail'

active_collection=rig
box('Studio ground · preview only',(0,0,-.63),(200,200,.1),backdrop,.01)
world=bpy.data.worlds.new('Café study · warm daylight')
world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(*colour('D9E4DC'),1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
scene.world=world

def light(name,position,power,size,hex_value):
    data=bpy.data.lights.new(name,'AREA')
    data.energy=power
    data.shape='DISK'
    data.size=size
    data.color=colour(hex_value)
    obj=link_object(name,data)
    obj.location=position
    obj.rotation_euler=(Vector((0,0,2))-obj.location).to_track_quat('-Z','Y').to_euler()
    return obj

light('Large warm key',(-8,-9,16),2400,9,'FFE1B0')
light('Soft sky fill',(10,-3,12),1700,9,'DBE8F3')
light('Rooftop rim',(2,9,14),2300,7,'FFE0A9')

def camera(name,position,target,scale):
    data=bpy.data.cameras.new(name)
    data.type='ORTHO';data.ortho_scale=scale
    obj=link_object(name,data)
    obj.location=position
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
    data.lens=45
    return obj

hero=camera('Camera · both worlds',(15,-24,18),(0,.0,2.6),22)
camera('Camera · Melbourne',(-12,-17,12),(mx,-.05,2.95),11.1)
camera('Camera · Seoul',(15,-16,13),(sx,.0,3.05),11.4)
camera('Camera · street level',(0,-13,4.2),(0,.7,2.6),18.6)
scene.camera=hero
scene.render.engine='CYCLES'
scene.cycles.samples=40
scene.cycles.use_denoising=True
scene.render.resolution_x=1720
scene.render.resolution_y=1220
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'

for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_perspective='CAMERA'
        area.spaces.active.overlay.show_overlays=False
        area.spaces.active.shading.type='MATERIAL'

for obj in bpy.context.selected_objects: obj.select_set(False)
bpy.context.view_layer.objects.active=None
scene['artDirection']='Rounded storybook miniatures; oat, forest, clay and honey; geometry-only shared materials.'
scene['status']='Art exploration. Not yet integrated, collision-tested or performance-tuned in Three.js.'
scene['sourceReferences']='User-provided Seoul corner brick café and Melbourne café laneway photographs. Original interpretation, fictional café names.'
scene['worldScale']='Metres. Storefronts face -Y in Blender. Ground paving top Z=0.275.'

# Write only this scene and its dependencies; the user's previously open file is untouched.
blend_path=OUTPUT/'melbourne-seoul-cafes.blend'
bpy.data.libraries.write(str(blend_path),{scene},fake_user=True,compress=True)

for obj in scene.objects:obj.select_set(False)
for source_collection in (melbourne,seoul,street):
    for obj in source_collection.objects:obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUTPUT/'melbourne-seoul-cafes.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_extras=True,export_cameras=False,export_lights=False,export_animations=False)
for obj in scene.objects:obj.select_set(False)

result={'scene':scene.name,'objects':len(scene.objects),'blend':str(blend_path),'glb':str(OUTPUT/'melbourne-seoul-cafes.glb')}

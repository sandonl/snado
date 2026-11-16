"""Warehouse café interior from Sandon's three supplied interior photographs.

Warm timber counter / exposed rafters and plaster (photos 1 and 3), with a
quieter terracotta-tiled room and low partition (photo 2). A clear entrance
connects the bar and seating; measurements below also generate collision boxes.
Executed by build_neighbourhood.py in its modelling context.
"""
active_collection=seoul
# Replace the shallow display counter with a real room, keeping the approved façade.
replace_prefixes=('Visible warm inner rear wall','Reused industrial workbench top','Workbench original steel legs','Workbench steel stretcher','Counter espresso machine','Espresso machine','Counter coffee cup','Coffee grinder','Workshop wall repurposed shelf','Coffee bags on old shelf','Industrial pendant','Old enamel industrial lamp shade','Industrial lamp warm diffuser')
for obj in list(melbourne.objects):
    source_name=obj.name.removeprefix('Workshop · ')
    if obj.name.startswith('Workshop · ') and source_name.startswith(replace_prefixes):
        bpy.data.objects.remove(obj,do_unlink=True)
    elif obj.name.startswith('Workshop · ') and ('Retained small-pane timber shopfront dark inset' in obj.name or 'Corner retained workshop windows dark inset' in obj.name):
        bpy.data.objects.remove(obj,do_unlink=True)

bar_wood=material('Interior smoked honey timber','986A43',1)
bar_edge=material('Interior end grain','BE986A',1)
ceiling_wood=material('Interior old roof timber','92724F',1)
steel_dark=material('Interior roof steel','514B43',1)
plaster_warm=material('Interior warm repaired plaster','C7B79B',1)
plaster_pale=material('Interior pale lime patch','D6C9AF',1)
plaster_old=material('Interior old plaster shadow','B4A58E',1)
interior_tile=material('Interior terracotta tile','C69A6D',1)
tile_light=material('Interior pale terracotta tile','D0AB80',1)
leather=material('Interior cognac leather','95694B',1)
steel_silver=material('Interior espresso brushed steel','AFB4AA',.75)
glassware=material('Interior glassware','C1CDC1',.5)
bottle_green=material('Interior green bottles','5D7053',.65)
interior_footprints=[]

# A matte concrete entry leads into a terracotta dining floor, all at one level.
box('Interior concrete walking floor',(-1.9,15.65,.087),(4.85,5.3,.018),concrete,.001)
box('Interior tiled room grout',(2.1,15.7,.087),(4.25,5.25,.02),bar_wood,.001)
for row in range(27):
    for col in range(20):
        box('Interior narrow terracotta floor tile',(.08+col*.209,13.13+row*.193,.102),(.198,.182,.014),tile_light if (row*7+col)%9==0 else interior_tile,.001)
box('Interior rear lime plaster lining',(0,18.325,2.02),(8.8,.04,3.78),plaster_warm,.002)
random.seed(103)
for i in range(20):
    x=random.uniform(-4.2,4.1);z=random.uniform(.35,3.6)
    points=[(x-.31,18.297,z-.18),(x+.23,18.297,z-.16),(x+.36,18.297,z+.09),(x+.11,18.297,z+.27),(x-.28,18.297,z+.19)]
    mesh=bpy.data.meshes.new('Interior plaster repair')
    mesh.from_pydata(points,[],[(0,1,2,3,4)])
    link_object('Interior irregular lime repair',mesh,plaster_pale if i%3 else plaster_old)
for x in [-3.8,-1.9,1.0,3.5]:
    curve('Interior retained electrical conduit',[(x,18.26,3.7),(x,18.26,2.6),(x+.12,18.26,2.45),(x+.12,18.26,1.6)],.012,steel_dark)

# The roof is enclosed outside; real timber boards and cross-braced beams face in.
for i in range(20):
    y=13.0+i*.274
    roof_z=4.01+math.sin(.045)*(y-15.71)
    plank=box('Interior roof timber board',(0,y,roof_z),(8.9,.26,.045),ceiling_wood if i%4 else bar_edge,.001)
    plank.rotation_euler.x=.045
for y in [13.45,15.65,17.9]:
    box('Interior exposed cross beam',(0,y,3.76),(8.95,.12,.17),steel_dark,.002)
    for x in [-4.3,0,4.3]:
        rod('Interior diagonal roof brace',(x,y,3.73),(x+(.55 if x<4 else -.55),y,3.96),.025,steel_dark,7)
for x in [-3.9,-1.1,1.6,4.1]:box('Interior long roof rafter',(x,15.7,3.91),(.1,5.5,.14),ceiling_wood,.002)

# The bar is behind the entry, rather than blocking the doorway.
box('Interior timber bar carcass',(-1.6,16.65,.55),(4.35,.82,.92),bar_wood,.004)
box('Interior timber bar overhanging top',(-1.6,16.65,1.04),(4.55,1.02,.09),bar_edge,.004)
box('Interior bar toe recess',(-1.6,16.205,.16),(4.2,.04,.13),steel_dark,.002)
for x in [-3.18,-2.13,-1.08,-.03]:
    # Routed arch panels follow the joinery in reference 1, without floating decals.
    outline=[(x-.47,16.229,.24),(x-.47,16.229,.77),(x-.27,16.229,.91),(x,16.229,.97),(x+.27,16.229,.91),(x+.47,16.229,.77),(x+.47,16.229,.24)]
    curve('Interior routed counter arch',outline,.007,bar_edge)
interior_footprints.append((-3.88,.68,16.12,17.19))
rod('Interior counter brass foot rail',(-3.5,15.99,.28),(.25,15.99,.28),.017,bar_edge,9)
for x in [-3.4,-1.6,.15]:rod('Interior foot rail bracket',(x,16.2,.17),(x,15.99,.28),.013,steel_dark,8)

# Equipment controls and dispensing hardware face the staff aisle (+Y).
exec(compile((OUTPUT/'coffee_equipment.py').read_text(),str(OUTPUT/'coffee_equipment.py'),'exec'),globals())
build_coffee_equipment(scene,seoul,rig)

def tumbler(name,x,y,z,r=.045,h=.105):
    vertices=[]
    for radius,level in [(r,z),(r,z+h),(r-.006,z+h),(r-.006,z+.008)]:
        vertices.extend((x+radius*math.cos(i*math.tau/12),y+radius*math.sin(i*math.tau/12),level) for i in range(12))
    faces=[]
    for ring in range(3):
        for i in range(12):faces.append((ring*12+i,ring*12+(i+1)%12,(ring+1)*12+(i+1)%12,(ring+1)*12+i))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces)
    return link_object(name,mesh,glassware)
for row in range(3):
    for col in range(5):tumbler('Interior rinsed counter glass',-1.15+col*.14,16.44+row*.14,1.09)
for x in [-.13,.09,.31]:
    cylinder('Interior bottle body',(x,16.8,1.22),.057,.27,bottle_green,12)
    cylinder('Interior bottle shoulder',(x,16.8,1.38),.057,.07,bottle_green,12,top_radius=.023)
    cylinder('Interior bottle neck',(x,16.8,1.47),.023,.13,bottle_green,10)
    cylinder('Interior bottle cork',(x,16.8,1.54),.022,.025,bar_edge,10)
    box('Interior paper bottle label',(x,16.738,1.22),(.075,.008,.13),paper,.001)
box('Interior folded linen cloth',(-1.7,16.42,1.098),(.27,.21,.02),ivory,.002)
for x in [-3.9,-2.0]:
    box('Interior service back cabinet',(x,17.99,.55),(1.6,.51,.92),bar_wood,.003)
    box('Interior service back worktop',(x,17.95,1.04),(1.68,.62,.055),steel_silver,.002)
for z in [1.68,2.24]:
    box('Interior rear floating shelf',(-2.85,18.1,z),(2.9,.32,.045),bar_edge,.002)
    for i in range(7):
        if z<2: cup('Interior shelf stacked cup',-4.05+i*.38,18.06,z+.025,.56)
        else:box('Interior bean bag',(-4.05+i*.38,18.12,z+.17),(.23,.13,.29),paper if i%2 else plaster_old,.002)
box('Interior narrow cloth hanging',(.2,18.255,2.5),(.48,.012,1.28),paper,.001)
text('Interior quiet cloth calligraphy','平\n和',(.2,18.24,2.52),.31,steel_dark,korean=True)
rod('Interior cloth top rail',(-.08,18.23,3.17),(.48,18.23,3.17),.014,bar_edge,8)

# The second reference supplies a low partition, tiled floor and long calm seating.
box('Interior low seating partition',(.94,17.2,.67),(.1,2.2,1.15),plaster_pale,.002)
interior_footprints.append((.87,1.02,16.1,18.3))
box('Interior long banquette base',(3.94,15.9,.3),(.58,3.85,.4),bar_wood,.003)
box('Interior long leather seat',(3.83,15.9,.54),(.7,3.85,.13),leather,.006)
box('Interior banquette leather back',(4.22,15.9,.87),(.12,3.85,.66),leather,.006)
interior_footprints.append((3.45,4.32,13.9,17.9))
for y in [14.6,16.45]:
    box('Interior square cafe table top',(2.96,y,.82),(.82,.73,.045),bar_edge,.004)
    box('Interior table steel base',(2.96,y,.14),(.43,.4,.04),steel_dark,.002)
    cylinder('Interior table pedestal',(2.96,y,.48),.028,.65,steel_dark,10)
    cup('Interior dining coffee',2.98,y,.85,.65)
    box('Interior dining book',(2.74,y+.16,.86),(.17,.24,.025),paper,.001)
    box('Interior leather stool',(2.12,y,.34),(.44,.44,.48),leather,.004)
    interior_footprints.append((1.87,3.4,y-.42,y+.42))
box('Interior round water station base',(1.54,14.05,.4),(.16,.4,.62),plaster_pale,.003)
cylinder('Interior water station oval table',(1.54,14.05,.84),.44,.055,plaster_pale,24)
for x in [1.3,1.48,1.66]:tumbler('Interior water station glasses',x,14.02,.87)
interior_footprints.append((1.08,1.99,13.57,14.54))
# Tall, fine-leaf bamboo beside the window, rather than oversized round toy foliage.
cylinder('Interior bamboo concrete planter',(-4.05,13.76,.29),.23,.38,plaster_old,14)
random.seed(44)
for i in range(9):
    x=-4.05+random.uniform(-.17,.17);y=13.76+random.uniform(-.17,.17);height=random.uniform(1.65,2.55)
    rod('Interior bamboo cane',(x,y,.47),(x+.08,y,height),.009,bar_edge,7)
    for z in [.8,1.2,1.6,2.0]:
        if z>height:continue
        for side in [-1,1]:
            end=(x+side*.18,y+.06,z+.12)
            rod('Interior bamboo fine branch',(x,y,z),end,.004,leaf[1],5)
            blade=sphere('Interior bamboo narrow leaf',end,(.12,.025,.022),leaf[(i+1)%4],1)
            blade.rotation_euler.z=side*.6
# Warm suspended diffusers match the reference's long strip above the bar.
for x,y,length in [(-1.65,16.6,4.7),(2.3,15.8,2.1)]:
    for dx in [-length*.36,length*.36]:rod('Interior suspended light wire',(x+dx,y,3.8),(x+dx,y,2.85),.006,steel_dark,6)
    box('Interior warm linear lamp shade',(x,y,2.85),(length,.2,.16),bar_edge,.002)
    box('Interior warm linear lamp diffuser',(x,y,2.76),(length-.1,.17,.012),lamp_glow,.001)

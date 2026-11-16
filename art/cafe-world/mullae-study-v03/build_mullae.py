"""Mullae-dong art study: a café occupying an old, low industrial workshop.

Source direction: user's first and third street photographs. This is an original
interpretation of their architecture and atmosphere, not an identified real business.
Keeps the illustrated materials of v02 while replacing its generic shop architecture.
"""
from pathlib import Path
style_source=Path(__file__).resolve().parents[1]/'street-study-v02'/'build_street.py'
style_code=style_source.read_text()
exec(style_code.split('active_collection=street')[0],globals())
scene.name='Sandon · Mullae workshop café · v03'
seoul.name='01 · Converted industrial café'
melbourne.name='02 · Working sheds and rear buildings'
street.name='03 · Narrow shared street'
rig.name='04 · Illustrated street cameras and lighting'
random.seed(61)

raw_wall=material('weathered grey workshop render','A39C8C',1)
old_wood=material('weathered timber signboards','655D4F',1)
wood_edge=material('worn timber edges','948575',1)
rusted_steel=material('old oxidised steel','756959',1)
roof_sheet=material('faded corrugated metal','858D82',1)
roof_dark=material('old roof edge','59645F',1)
teal=material('faded blue green tarpaulin','688C83',1)
ochre=material('old yellow factory sign','C8BE87',1)
stain=material('old water stain','807C6C',1)
plaster_chip=material('pale exposed render','C1B8A1',1)
patch_dark=material('deep worn plaster','6C7065',1)
steel=material('workshop cut steel','64736F',1)
door_glass=material('small old glass panes','8A9D8C',1)
interior_wall=material('café interior plaster','BDAD8D',1)
interior_shadow=material('café interior shade','797C66',1)
warm_timber=material('reused brown door joinery','826444',1)
soft_red=material('plastic stool red','AC6553',1)
faded_green=material('old painted factory doors','68806B',1)
brick_dark=material('older dark brickwork','946F5C',1)

def face_patch(name,x,y,z,width,height,mat,side=False):
    # Irregular chipped outlines, not repeated circular decoration.
    corners=[(-.5,-.5),(-.18,-.46),(.1,-.5),(.48,-.33),(.44,-.1),(.5,.14),(.24,.39),(-.05,.5),(-.38,.38),(-.5,.05)]
    points=[]
    for a,b in corners:
        a+=random.uniform(-.07,.07);b+=random.uniform(-.06,.06)
        points.append((x,y+a*width,z+b*height) if side else (x+a*width,y,z+b*height))
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(points,[],[tuple(range(len(points)))])
    return link_object(name,mesh,mat)

def corrugated_canopy(name,x,y,z,width,depth,mat,slope=.05):
    plate=box(name+' sheet',(x,y,z),(width,depth,.027),mat,.002)
    plate.rotation_euler.x=slope
    count=int(width/.17)
    for i in range(count):
        offset=-width/2+.08+i*.17
        rod(name+' corrugation',(x+offset,y-depth/2,z-math.sin(slope)*depth/2+.024),(x+offset,y+depth/2,z+math.sin(slope)*depth/2+.024),.014,mat,6)
    box(name+' uneven fascia',(x,y-depth/2,z-math.sin(slope)*depth/2-.075),(width,.055,.16),mat,.002)

def grid_front(name,x,y,z,w,h,columns=3,rows=3,frame=warm_timber):
    box(name+' dark inset',(x,y+.025,z),(w+.07,.07,h+.07),dark,.003)
    box(name+' muted glass',(x,y-.018,z),(w,.015,h),door_glass,.001)
    for i in range(columns+1):
        box(name+' fine vertical joinery',(x-w/2+i*w/columns,y-.045,z),(.035,.055,h+.04),frame,.003)
    for i in range(rows+1):
        box(name+' fine horizontal joinery',(x,y-.048,z-h/2+i*h/rows),(w,.055,.033),frame,.002)
    # A few small uneven glints replace v02's repeated diagonal glass stripes.
    for i in range(max(1,columns-1)):
        gx=x-w*.37+i*w/columns
        stroke(name+' glass glint',[(gx,y-.031,z+h*.31),(gx+.045,y-.031,z+h*.08)],.004)

def grid_side(name,x,y,z,w,h,columns=3,rows=3):
    box(name+' dark inset',(x-.025,y,z),(.07,w+.07,h+.07),dark,.003)
    box(name+' glass',(x+.018,y,z),(.015,w,h),door_glass,.001)
    for i in range(columns+1):
        box(name+' fine vertical joinery',(x+.045,y-w/2+i*w/columns,z),(.055,.035,h+.04),warm_timber,.003)
    for i in range(rows+1):
        box(name+' fine horizontal joinery',(x+.048,y,z-h/2+i*h/rows),(.055,w,.033),warm_timber,.002)

def timber_fascia(name,x,y,z,width,height,lettering):
    box(name+' rough backing',(x,y,z),(width,.16,height),old_wood,.003)
    boards=int(width/.57)
    for i in range(boards):
        bx=x-width/2+(i+.5)*width/boards
        box(name+' reclaimed vertical board',(bx,y-.09,z+random.uniform(-.022,.022)),(width/boards-.014,.055,height-random.uniform(0,.045)),old_wood if i%3 else wood_edge,.002)
        for k in range(2):
            gx=bx+random.uniform(-.17,.17)
            stroke(name+' wood split',[(gx,y-.122,z-height*.36),(gx+.02,y-.122,z+.02),(gx-.012,y-.122,z+height*.31)],.002)
    text(name+' retained workshop lettering',lettering,(x,y-.135,z+.04),.37,ivory,korean=True)

def small_bulb(name,x,y,z):
    rod(name+' flex',(x,y,z+.14),(x,y,z+.025),.008,dark,6)
    sphere(name+' warm bulb',(x,y,z),(.085,.085,.105),lamp_glow,2)

# The street is narrow and shared, with very little raised footpath.
active_collection=street
box('Continuous old street',(0,0,-.14),(70,70,.2),asphalt,.002)
box('Thin uneven café apron',(0,1.7,-.012),(21,8,.16),concrete,.003)
box('Low kerb outside workshops',(0,-2.36,-.005),(21,.16,.17),trim,.002)
for i in range(30):
    x=-10+i*.7
    stroke('Low kerb joints',[(x,-2.45,-.07),(x,-2.45,.08),(x,-2.25,.08)],.003)
for i in range(7):
    x=random.uniform(-8,8);y=random.uniform(-5.5,-2.65)
    # Worn tar patches are irregular planes, not a regular tiled plaza.
    vertices=[(x-.6,y-.34,-.034),(x+.26,y-.46,-.034),(x+.8,y-.1,-.034),(x+.5,y+.25,-.034),(x-.4,y+.38,-.034)]
    mesh=bpy.data.meshes.new('Asphalt repair')
    mesh.from_pydata(vertices,[],[(0,1,2,3,4)])
    link_object('Old asphalt patch',mesh,concrete if i%3==0 else roof_grey)
for y in [-5.15,-4,-2.9]:
    box('Faded narrow yellow road edge',(-6.15,y,-.028),(.055,.77,.008),yellow,0)
for x in [-8.8+i*.44 for i in range(7)]:
    for y in [-1.75+j*.3 for j in range(9)]:
        box('Small surviving brick apron',(x,y,.076),(.415,.28,.022),brick_dark,.002)
for points in [[(-1.5,-3.6,-.027),(-1.2,-3.4,-.027),(-.9,-3.46,-.027),(-.7,-3.2,-.027)],[(4.8,-1.95,.07),(4.9,-1.72,.07),(5.15,-1.68,.07)],[(.2,-1.9,.07),(.5,-1.65,.07),(.4,-1.45,.07)]]:
    stroke('Street crack',points,.003)

active_collection=seoul
front=-1.05; side=4.55
# Wall shell leaves a real open bay, with interior space behind the street frontage.
box('Former workshop back wall',(0,4.44,1.91),(9.1,.18,3.76),raw_wall,.006)
box('Former workshop west wall',(-4.49,1.7,1.91),(.18,5.5,3.76),raw_wall,.006)
box('Workshop concrete floor',(0,1.7,.045),(9.1,5.5,.09),trim,.003)
for x in [-4.48,-1.12,1.18,4.48]:
    box('Old rough concrete front pier',(x,front,1.82),(.2,.31,3.63),raw_wall,.004)
    box('Pier base repair',(x,front-.023,.3),(.24,.35,.49),patch_dark,.003)
# The east corner has two small-pane timber window assemblies, like reference 1.
for y in [.18,2.55]:
    box('East wall lower concrete',(side,y,.34),(.18,2.16,.65),raw_wall,.004)
    grid_side('Corner retained workshop windows',side+.03,y,1.78,2.13,2.21,4,3)
box('Corner rear wall strip',(side,3.99,1.84),(.18,.81,3.68),raw_wall,.004)
for x,w in [(.02,2.03),(2.83,3.03)]:
    box('Timber shopfront base',(x,front,.37),(w,.12,.68),warm_timber,.003)
    grid_front('Retained small-pane timber shopfront',x,front-.03,1.83,w,2.23,4 if w>2.2 else 3,3)
box('Workshop lintel',(0,front,3.2),(9.1,.22,.24),rusted_steel,.003)
timber_fascia('Weathered long warehouse fascia',0,front-.09,3.68,9.2,.78,'문 래   작 업 실')
box('Small modern café addition sign',(-2.88,front-.261,3.56),(1.18,.045,.22),ochre,.002)
text('Small coffee lettering','커피 · COFFEE',(-2.88,front-.29,3.56),.105,green,korean=True)
# The workshop's big sliding steel doors are retained and parked to either side.
for x in [-4.07,-1.45]:
    box('Parked original green steel door',(x,front+.05,1.58),(.58,.09,2.82),faded_green,.003)
    for z in [.48,1.6,2.7]:
        box('Workshop door pressed rib',(x,front-.007,z),(.49,.028,.035),rusted_steel,.002)
    rod('Workshop door old pull',(x+.18,front-.03,1.25),(x+.18,front-.03,1.5),.013,rusted_steel,7)
rod('Exposed sliding-door rail',(-4.49,front-.16,3.13),(-1.08,front-.16,3.13),.025,rusted_steel,8)
corrugated_canopy('Thin rust-red fabric and metal awning',.13,front-.49,3.09,8.9,.8,wood_edge,.12)
# Old bent arms support the shallow awning rather than an oversized decorative canopy.
for x in [-4.22,-1,1.28,4.28]:
    rod('Awning diagonal support',(x,front,2.55),(x,front-.83,3.03),.015,rusted_steel,7)
# A low corrugated roof and overlapping rear extension retain an industrial silhouette.
corrugated_canopy('Old low workshop roof',-.1,1.71,4.16,9.52,5.9,roof_sheet,.045)
box('Rusting roof side edge',(4.69,1.72,4.12),(.085,5.9,.18),roof_dark,.002)
for x in [-4.2,-1.15,1.25,4.2]:
    rod('Visible interior roof truss bottom',(x,-.8,3.65),(x,4.2,3.65),.038,rusted_steel,8)
    rod('Visible interior roof truss rise',(x,-.8,3.65),(x,1.8,4.05),.03,rusted_steel,8)
    rod('Visible interior roof truss fall',(x,1.8,4.05),(x,4.2,3.65),.03,rusted_steel,8)

# The open industrial bay reveals a reused workbench coffee counter and warm lamps.
box('Visible warm inner rear wall',(-2.78,3.84,1.61),(2.8,.08,2.9),interior_wall,.002)
box('Reused industrial workbench top',(-2.79,.72,.99),(2.13,.72,.105),light_wood,.003)
for x in [-3.65,-1.94]:
    for y in [.45,.98]:
        rod('Workbench original steel legs',(x,y,.1),(x,y,.95),.033,steel,8)
rod('Workbench steel stretcher',(-3.65,.73,.36),(-1.94,.73,.36),.026,steel,8)
box('Counter espresso machine',(-2.89,.63,1.25),(.75,.41,.43),ivory,.006)
box('Espresso machine black front',(-2.89,.411,1.23),(.64,.018,.16),dark,.002)
for x in [-3.06,-2.72]:
    rod('Espresso machine portafilter',(x,.38,1.17),(x,.2,1.17),.018,dark,7)
    cup('Counter coffee cup',x,.29,1.047,.67)
cylinder('Coffee grinder base',(-1.99,.7,1.19),.1,.3,dark,12)
cylinder('Coffee grinder hopper',(-1.99,.7,1.45),.115,.23,glass,12,top_radius=.08)
for z in [1.66,2.2]:
    box('Workshop wall repurposed shelf',(-2.75,3.74,z),(2.4,.24,.045),wood,.002)
    for i in range(7):
        box('Coffee bags on old shelf',(-3.76+i*.31,3.73,z+.14),(.17,.12,.23),paper if i%2 else ochre,.003)
for x,y in [(-3.6,.62),(-1.75,1.78),(.45,1.5)]:
    rod('Industrial pendant flex',(x,y,3.98),(x,y,2.8),.008,dark,6)
    cylinder('Old enamel industrial lamp shade',(x,y,2.77),.24,.15,green,16,top_radius=.05)
    cylinder('Industrial lamp warm diffuser',(x,y,2.69),.19,.01,lamp_glow,16)

# Material wear follows roof runoff and bottom-of-wall damage, not decorative patterns.
for x in [-4.46,-1.14,1.18,4.48]:
    for z in [1.0,2.45]:
        face_patch('Pier worn render',x,front-.163,z,.19,.69,plaster_chip)
for i in range(14):
    y=random.uniform(-.5,4.25);z=random.uniform(.2,3.4)
    if y<3.6 and z>.7:continue
    face_patch('Corner wall rain damage',side+.098,y,z,.36,.68,stain,True)
for x in [-4.3,-.4,1.3,4.3]:
    stroke('Dirty roof runoff',[(x,front-.193,4.03),(x+.013,front-.193,3.87),(x-.02,front-.193,3.58)],.008)
for i in range(21):
    x=random.uniform(-4.4,4.4)
    face_patch('Irregular age on fascia boards',x,front-.219,random.uniform(3.48,3.98),random.uniform(.13,.38),random.uniform(.1,.27),stain if i%3 else wood_edge)
curve('Old exposed corner drainpipe',[(side+.2,4.35,4.2),(side+.2,4.35,1.1),(side+.32,4.35,.85),(side+.32,4.35,.1)],.032,ivory)
box('Small corner lightbox',(side+.25,front+.01,3.61),(.32,.18,.93),paper,.003)
text('Coffee corner lightbox','커\n피',(side+.25,front-.095,3.61),.23,green,korean=True)
for x in [-4.12,-2.4,-.5,1.3,3.2,4.24]:
    small_bulb('Old shop eave lantern',x,front-.31,4.12)
curve('Uneven eave lighting cable',[(-4.43,front-.28,4.26),(-.3,front-.28,4.12),(4.48,front-.28,4.27)],.007,dark)

# Crowded, taller rear blocks break up the skyline, as in the original street photo.
active_collection=melbourne
box('Older rear red brick building',(-1.25,6.3,4.31),(6.25,3.7,8.55),brick_dark,.005)
box('Rear brick building roof lip',(-1.25,6.3,8.64),(6.4,3.82,.16),trim,.003)
for x in [-3.28,-1.2,.77]:
    grid_front('Rear factory window',x,4.405,6.66,1.04,1.39,2,3,frame=dark)
box('Rear building narrow vertical old sign',(.96,4.3,7.07),(.63,.18,3.2),paper,.003)
text('Rear building old Hangul','문\n래\n철\n공',(.96,4.19,7.08),.29,old_wood,korean=True)
for row in range(11):
    z=5.25+row*.27
    for col in range(10):
        x=-4.25+col*.6+(row%2)*.27
        if any(abs(x-wx)<.67 and abs(z-6.66)<.83 for wx in [-3.28,-1.2,.77]):continue
        if x>1.8:continue
        stroke('Sparse rear brick courses',[(x,4.439,z),(x+.48,4.439,z)],.0025)
box('Additional raw brick rooftop block',(-3.1,6.5,9.07),(2.1,1.8,.85),brick_dark,.003)
for x in [-3.75,-3.34,-2.91]:
    rod('Old roof antenna mast',(x,6.65,8.7),(x,6.65,10.35),.014,dark,7)
    rod('Old antenna crossbar',(x-.4,6.65,10.1),(x+.4,6.65,10.1),.008,dark,6)

# Adjacent shed is still a workshop: its old sign and shutter remain in place.
lx=-7.1
box('Low adjoining workshop back',(lx,3.5,1.79),(4.88,.16,3.51),raw_wall,.004)
for x in [-9.5,-4.68]:
    box('Low adjoining workshop jamb',(x,1.32,1.79),(.16,4.5,3.51),raw_wall,.004)
box('Old neighbouring workshop fascia',(lx,-.98,3.43),(4.97,.19,.66),ochre,.003)
text('Retained factory sign','문래 철공소',(lx,-1.087,3.46),.37,green,korean=True)
text('Small old sign subline','절단 · 용접 · 제작',(lx,-1.09,3.2),.11,old_wood,korean=True)
box('Partially raised green metal shutter',(lx,-.99,2.75),(4.51,.08,.65),faded_green,.003)
for i in range(8):
    stroke('Rolled workshop shutter slat',[(lx-2.19,-1.039,2.48+i*.075),(lx+2.19,-1.039,2.48+i*.075)],.003)
corrugated_canopy('Neighbour workshop corrugated roof',lx,1.33,3.86,5.2,4.95,roof_dark,.1)
box('Workshop shadowed interior back',(lx,3.39,1.29),(4.5,.06,2.4),interior_shadow,.002)
box('Workshop cutting table',(lx,1.4,.94),(2.8,.84,.16),steel,.003)
for x in [lx-1.2,lx+1.2]:
    for y in [1.1,1.7]:rod('Steel cutting bench legs',(x,y,.08),(x,y,.9),.032,dark,8)
for i in range(7):
    box('Steel stock stacked outside',(lx+1.1,-1.24,.15+i*.075),(1.7,.26,.055),steel,.002)
for x in [lx-1.45,lx-1.08]:
    cylinder('Workshop gas cylinder',(x,-.35,.75),.135,1.24,green,12)
    sphere('Workshop gas cylinder shoulder',(x,-.35,1.36),(.135,.135,.13),green,2)
    rod('Workshop cylinder valve',(x,-.35,1.4),(x,-.35,1.53),.024,yellow,7)

# Faded mixed-height blocks on the side lane replace the clean uniform v02 neighbours.
box('Old two-storey side-lane plaster block',(9.3,4.35,3.77),(3.55,6.8,7.45),cream,.004)
for z in [4.73,6.39]:
    for x in [8.35,9.89]:
        grid_front('Side-lane old window',x,.905,z,.85,1.15,2,2,frame=dark)
for x,z,w,h in [(8.1,5.8,.55,.76),(10.2,6.4,.57,1.0),(9.1,7.1,1.1,.31),(10.5,4.5,.62,1.6)]:
    face_patch('Peeling side-lane plaster',x,.939,z,w,h,stain)
for x,z,w,h in [(7.79,3.82,.35,.63),(10.62,5.12,.42,.9),(8.98,6.1,.4,.75),(9.24,4.54,.4,.52),(10.54,7.12,.62,.31)]:
    face_patch('Lighter flaking old paint',x,.934,z,w,h,plaster_chip)
box('Older side-lane closed shop shutter',(9.3,.9,1.64),(3.1,.12,2.6),sky_blue,.003)
for i in range(23):
    stroke('Side shop shutter slat',[(7.82,.825,.4+i*.108),(10.78,.825,.4+i*.108)],.0025)
box('Faded old general shop sign',(9.3,.8,3.13),(3.5,.12,.47),paper,.003)
text('Old side-lane shop Hangul','동네 잡화',(9.3,.726,3.14),.3,green,korean=True)
box('Distant side-lane shed',(6.0,11.1,2.55),(3.2,2,5.0),roof_grey,.004)
grid_front('Distant shed steel door',6,10.06,1.4,2.4,2.6,3,2,frame=green)

active_collection=street
# Informal street seating follows reference 3: plastic chairs and a small red table.
def plastic_chair(name,x,y,angle):
    def p(a,b,c):return(x+a*math.cos(angle)-b*math.sin(angle),y+a*math.sin(angle)+b*math.cos(angle),c)
    seat=box(name+' plastic seat',p(0,0,.52),(.42,.4,.048),ivory,.006)
    seat.rotation_euler.z=angle
    for a in [-.16,.16]:
        for b in [-.15,.15]:rod(name+' narrow leg',p(a*1.2,b*1.2,.08),p(a,b,.51),.018,ivory,7)
    for a in [-.18,.18]:rod(name+' back edge',p(a,.16,.52),p(a,.18,1.03),.022,ivory,8)
    rod(name+' back top',p(-.18,.18,1.03),p(.18,.18,1.03),.027,ivory,8)
    for a in [-.09,0,.09]:rod(name+' slotted back',p(a,.175,.64),p(a,.18,.97),.018,ivory,7)

cylinder('Small red street table top',(.15,-1.81,.8),.45,.055,soft_red,20)
cylinder('Small red street table leg',(.15,-1.81,.44),.048,.68,soft_red,10)
for angle in [0,math.tau/3,math.tau*2/3]:
    rod('Red street table foot',(.15,-1.81,.19),(.15+math.cos(angle)*.3,-1.81+math.sin(angle)*.3,.08),.026,soft_red,8)
plastic_chair('Reused white plastic chair',-.51,-1.79,math.pi/2)
plastic_chair('Reused white plastic chair',.83,-1.84,-math.pi/2)
cup('Street coffee cup',-.01,-1.83,.836,.7)
cup('Street second coffee cup',.35,-1.76,.836,.62)
for i in range(3):
    x=3.0+i*.41
    cylinder('Low red pavement stool',(x,-1.87,.47),.16,.045,soft_red,12)
    for angle in [0,math.tau/3,math.tau*2/3]:
        rod('Pavement stool thin leg',(x+math.cos(angle)*.14,-1.87+math.sin(angle)*.14,.08),(x+math.cos(angle)*.1,-1.87+math.sin(angle)*.1,.45),.014,soft_red,6)
for x,y in [(-1.17,-1.52),(4.78,-.92)]:pot('Modest entrance plant',x,y,.07,.2)
for i in range(3):
    box('Blue delivery crate stack',(-4.77,-1.52,.24+i*.34),(.55,.4,.31),sky_blue,.003)
    for j in range(4):box('Crate vent',(-4.95+j*.12,-1.728,.24+i*.34),(.068,.008,.16),dark,0)
box('Small café sandwich board',(-1.28,-1.6,.61),(.38,.045,.91),paper,.003)
text('Small café board coffee','커피',(-1.28,-1.633,.83),.14,green,korean=True)
text('Small café board hours','OPEN',(-1.28,-1.633,.58),.09,green)
text('Small café board menu','FILTER / MILK',(-1.28,-1.633,.4),.045,green)
rod('Sandwich board support',(-1.28,-1.33,.07),(-1.28,-1.58,1.05),.016,wood,7)

# Pole clutter, transformers and sagging cables are part of the street silhouette.
px,py=5.65,-.55
cylinder('Older concrete utility pole',(px,py,4.28),.115,8.5,concrete,14,top_radius=.077)
for z in [.7,1.05,1.4]:cylinder('Old utility safety band',(px,py,z),.119,.16,yellow,14)
box('Short utility cross arm',(px,py,7.5),(1.72,.11,.1),dark,.002)
for x in [px-.68,px-.22,px+.22,px+.68]:
    cylinder('Cable porcelain insulator',(x,py,7.65),.045,.19,ivory,8)
box('Old pole transformer',(px+.19,py,6.49),(.37,.41,.72),trim,.003)
box('Small junction box on pole',(px-.13,py-.07,4.1),(.23,.16,.33),roof_sheet,.003)
for i in range(5):
    y=py+(i-2)*.11
    curve('Sagging overhead power cable',[(-12,y+.4,9.5),(-5,y+.1,7.07),(px,y,7.78),(12,y+.4,8.1)],.007,dark)
for i in range(3):
    curve('Layered lower service wires',[(-10,-1.4+i*.1,6.4),(-2,-1.2+i*.1,5.2),(px,py+i*.1,6.17),(10,2,7)],.005,dark)
curve('Workshop exterior service cable',[(-4.4,-1.28,4.05),(-4.6,-1.35,2.8),(-4.6,-1.4,1.7)],.012,dark)
curve('Street lamp old bent arm',[(px,py,6.25),(px,py-.4,6.54),(px,py-1.08,6.52)],.024,dark)
box('Utility street lamp head',(px,py-1.1,6.5),(.17,.34,.075),dark,.003)

# Brief geometry notes remain in the editable source for the next modelling pass.
scene['style']='Illustrated 3D with fine ink lines; restrained two-band colour'
scene['placeDirection']='Mullae-dong: old low workshops converted into cafés, with working industrial neighbours.'
scene['referenceMapping']='Photo 1: long low weathered sign fascia, timber pane grid, shallow eaves, rear brick block, dense wires. Photo 3: faded workshop signage, small apron, reused plastic chairs and red table.'
scene['interpretation']='Original composite environment from the supplied photos; not a reconstruction of a named real café.'
scene['runtimeNote']='Blender Freestyle and two-band materials are an art target. Browser shaders and gameplay integration remain separate.'

active_collection=rig
world=bpy.data.worlds.new('Mullae pale afternoon sky')
world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(*colour('BACBD4'),1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
scene.world=world
sun_data=bpy.data.lights.new('Mullae afternoon sun','SUN')
sun_data.energy=1.6;sun_data.angle=math.radians(4)
sun_obj=link_object('Mullae afternoon sun',sun_data)
sun_obj.rotation_euler=(math.radians(26),math.radians(-27),math.radians(-32))
camera_data=bpy.data.cameras.new('Mullae corner at walking height')
camera_obj=link_object('Mullae corner at walking height',camera_data)
camera_obj.location=(9.8,-13.7,2.0)
camera_obj.rotation_euler=(Vector((-.55,1.0,3.15))-camera_obj.location).to_track_quat('-Z','Y').to_euler()
camera_data.type='PERSP';camera_data.lens=45;camera_data.clip_end=140
scene.camera=camera_obj
scene.render.engine='CYCLES'
scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.render.resolution_x=1720;scene.render.resolution_y=1120
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(OUTPUT/'mullae-workshop-v03.png')
scene.view_settings.view_transform='Standard'
scene.view_settings.look='None'
scene.view_settings.exposure=0;scene.view_settings.gamma=1
exec(style_code[style_code.index('def illustrated_materials():'):style_code.index('# Freestyle is the Blender')],globals())
scene.render.use_freestyle=True;scene.render.line_thickness=1
settings=scene.view_layers[0].freestyle_settings
settings.crease_angle=math.radians(120)
line_set=settings.linesets[0] if len(settings.linesets) else settings.linesets.new('Fine workshop ink')
line_set.select_silhouette=True;line_set.select_border=True;line_set.select_crease=True
line_set.select_material_boundary=False;line_set.select_external_contour=True
line_set.linestyle.color=colour('414C59');line_set.linestyle.thickness=.64;line_set.linestyle.alpha=.8
for obj in bpy.context.selected_objects:obj.select_set(False)
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_perspective='CAMERA'
        area.spaces.active.overlay.show_overlays=False
        area.spaces.active.shading.type='MATERIAL'
for loaded_font in [font,korean_font]:
    if not loaded_font.packed_file:loaded_font.pack()
bpy.data.libraries.write(str(OUTPUT/'mullae-workshop-v03.blend'),{scene},fake_user=True,compress=True)
result={'scene':scene.name,'objects':len(scene.objects),'source':str(OUTPUT/'mullae-workshop-v03.blend')}

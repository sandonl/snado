"""Melbourne café lane: low, varied façades, iron sign brackets, deep awnings and bluestone.
Original interpretation of the user's Melbourne laneway photographs.
"""
from pathlib import Path
style_path=Path(__file__).resolve().parents[1]/'street-study-v02'/'build_street.py'
style_code=style_path.read_text()
exec(style_code.split('active_collection=street')[0],globals())
from mathutils import Matrix
scene.name='Sandon · Melbourne café lane'
melbourne.name='01 · Melbourne façades'
seoul.name='02 · Lane end and street details'
street.name='03 · Bluestone and café seating'
rig.name='04 · Illustration preview rig'
random.seed(28)
font=bpy.data.fonts.load('/System/Library/Fonts/Helvetica.ttc')
stone_blue=material('Melbourne bluestone','737E83',1)
burgundy=material('oxblood canvas','785C53',1)
iron=material('wrought iron','465253',1)
ochre_wall=material('aged ochre plaster','C4B393',1)
paint_blue=material('mural blue','758E98',1)
paint_rust=material('mural rust','AD7A6B',1)

def fitted_text(name,body,position,size,mat,width):
    obj=text(name,body,position,size,mat)
    obj.data.font=font
    bpy.context.view_layer.update()
    if obj.dimensions.x>width:obj.scale*=width/obj.dimensions.x
    return obj

active_collection=street
box('Lane paving bed',(0,1.4,-.08),(12.4,17,.14),grout,.003)
for row in range(32):
    y=-6.5+row*.5
    for col in range(7):
        x=-1.66+col*.54+(row%2)*.12
        box('Melbourne bluestone block',(x,y,.015),(.515,.475,.045),stone_blue if (row+col)%3 else concrete,.004)
for x in [-1.8,1.8]:
    box('Lane drainage channel',(x,1.3,.045),(.11,16.8,.035),iron,.001)
    for i in range(40):box('Drain channel slots',(x,-6.7+i*.42,.065),(.07,.15,.008),stone_blue,0)

active_collection=melbourne
def frontage(side,y,width,height,wall,name,canvas):
    before=set(melbourne.objects)
    box(name+' building mass',(0,2.15,height/2),(width,4.3,height),wall,.006)
    box(name+' shop plinth',(0,-.04,.3),(width,.16,.56),iron,.004)
    box(name+' shop surround',(0,-.06,1.55),(width-.12,.14,2.6),iron,.004)
    for x in [-width*.27,width*.27]:
        front_window(name+' street glazing',x,-.15,1.63,width*.4,2.1,iron,True)
    box(name+' glazed entry',(0,-.22,1.4),(.77,.055,2.5),green,.004)
    box(name+' entry pane',(0,-.254,1.6),(.61,.013,1.83),glass,.002)
    rod(name+' entry handle',(.25,-.29,1.3),(.25,-.29,1.56),.012,ivory,7)
    box(name+' shop sign',(0,-.15,2.93),(width-.1,.17,.36),iron,.003)
    fitted_text(name+' shop lettering',name.upper(),(0,-.25,2.93),.205,ivory,width-.5)
    awn=box(name+' deep canvas awning',(0,-.61,2.71),(width+.12,1.14,.045),canvas,.003)
    awn.rotation_euler.x=.1
    box(name+' canvas valance',(0,-1.18,2.59),(width+.12,.035,.13),canvas,.002)
    for x in [-width/2+.12,width/2-.12]:
        rod(name+' canopy brace',(x,-.08,2.08),(x,-1.14,2.65),.016,iron,8)
    for z in [4.25,6.42,8.55]:
        if z+1>height:continue
        for x in [-width*.27,width*.27]:
            front_window(name+' upper sash',x,-.06,z,.91,1.35,iron)
            box(name+' sash header',(x,-.1,z+.78),(1.12,.15,.1),ivory,.004)
        box(name+' floor string course',(0,-.02,z-.94),(width+.08,.2,.1),trim,.004)
    box(name+' upper cornice',(0,2.15,height+.02),(width+.22,4.5,.16),trim,.004)
    # The oval projecting signs and curved brackets are the main cue from photo 5.
    bx=width/2-.34
    curve(name+' curved iron bracket',[(bx,-.07,3.95),(bx,-.55,4.12),(bx,-1.08,3.88),(bx,-1.1,3.67)],.018,iron)
    disc=cylinder(name+' oval hanging sign',(bx,-1.1,3.31),.34,.055,iron,24)
    disc.rotation_euler.x=math.pi/2
    disc.scale.x=.78;disc.scale.y=1.2
    fitted_text(name+' hanging sign initials',name[:1].upper(),(bx,-1.139,3.31),.25,ivory,.35)
    for x in [-width*.4,width*.4]:
        curve(name+' old rainwater pipe',[(x,-.12,height),(x,-.12,3.2),(x+.07,-.19,3.05),(x+.07,-.19,.08)],.025,trim)
    # A small number of café tables leave a clear central walking route.
    furniture_before=set(melbourne.objects)
    cafe_table(name+' outdoor table',-.77,-.62)
    chair(name+' outdoor chair',-1.4,-.62,math.pi/2,wood,iron)
    chair(name+' outdoor chair',-.13,-.62,-math.pi/2,wood,iron)
    furniture_height=Matrix.Translation((0,0,.055))@Matrix.Diagonal((1,1,.9,1))@Matrix.Translation((0,0,-.3))
    for obj in set(melbourne.objects)-furniture_before:obj.matrix_world=furniture_height@obj.matrix_basis.copy()
    transform=Matrix.Translation((side*1.92,y,0))@Matrix.Rotation(-side*math.pi/2,4,'Z')
    for obj in set(melbourne.objects)-before:obj.matrix_world=transform@obj.matrix_basis.copy()

for side,y,width,height,wall,name,canvas in [
    (-1,-3.5,4.2,5.35,cream,'Morrow',green),
    (-1,.9,4.35,6.25,plaster,'Editions',burgundy),
    (-1,5.35,4.25,4.35,brick_mortar,'North',iron),
    (1,-3.5,4.2,4.8,ochre_wall,'Coda',burgundy),
    (1,.9,4.35,6.45,cream,'Market',sage),
    (1,5.35,4.25,4.55,plaster,'Studio',iron),
]:frontage(side,y,width,height,wall,name,canvas)

active_collection=seoul
box('Lane end heritage building',(0,10.5,5.4),(12.5,2.1,10.8),plaster,.005)
for z in [2.1,4.8,7.2,9.4]:
    for x in [-4.1,-2.05,0,2.05,4.1]:front_window('Lane end window',x,9.405,z,.95,1.4,iron)
box('Lane end cornice',(0,10.5,10.88),(12.8,2.3,.18),ivory,.005)
box('Lane end ground doorway',(0,9.3,1.52),(1.5,.09,2.95),iron,.004)
# Simple painted wall art, without invented slogans.
for i in range(11):
    box('Small painted mural stroke',(-1.78,6.9+i*.07,1.1+i*.06),(.015,.065,.66-i*.023),paint_blue if i%2 else paint_rust,.001)

active_collection=street
for y in [-3.1,2,6.5]:
    curve('Lane festoon cable',[(-1.8,y,3.95),(0,y,3.55),(1.8,y,3.95)],.009,iron)
    for x in [-1.2,-.6,0,.6,1.2]:
        z=3.56+.14*x*x
        rod('Festoon short flex',(x,y,z),(x,y,z-.1),.006,iron,6)
        sphere('Lane festoon bulb',(x,y,z-.13),(.043,.043,.06),lamp_glow,1)
for x,y in [(-1.44,-5.7),(1.44,-5.7),(-1.45,7.5),(1.45,7.5)]:
    cylinder('Melbourne slim bollard',(x,y,.54),.052,1.05,iron,10)
    cylinder('Bollard brass collar',(x,y,.92),.057,.08,yellow,10)
for side,y in [(-1,-1.65),(1,2.8),(-1,7.2)]:pot('Lane plant',side*1.45,y,.04,.18)

active_collection=rig
world=bpy.data.worlds.new('Melbourne pale afternoon')
world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(*colour('BACBD4'),1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
scene.world=world
sun=bpy.data.lights.new('Lane afternoon light','SUN');sun.energy=1.8;sun.angle=.07
sun_obj=link_object('Lane afternoon light',sun);sun_obj.rotation_euler=(.45,-.5,-.55)
camera=bpy.data.cameras.new('Melbourne walking view')
camera_obj=link_object('Melbourne walking view',camera)
camera_obj.location=(.2,-10.6,2.0)
camera_obj.rotation_euler=(Vector((0,3.9,2.5))-camera_obj.location).to_track_quat('-Z','Y').to_euler()
camera.lens=25
scene.camera=camera_obj
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.render.resolution_x=1500;scene.render.resolution_y=1120;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUTPUT/'melbourne-lane.png')
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
exec(style_code[style_code.index('def illustrated_materials():'):style_code.index('# Freestyle is the Blender')],globals())
scene.render.use_freestyle=True
settings=scene.view_layers[0].freestyle_settings;settings.crease_angle=math.radians(120)
line_set=settings.linesets[0] if len(settings.linesets) else settings.linesets.new('Lane ink')
line_set.select_silhouette=True;line_set.select_border=True;line_set.select_crease=True
line_set.linestyle.color=colour('414C59');line_set.linestyle.thickness=.6;line_set.linestyle.alpha=.75
letters=bpy.data.collections.new('05 · Lane lettering');scene.collection.children.link(letters)
for obj in scene.objects:
    if obj.type=='FONT':letters.objects.link(obj)
line_set.select_by_collection=True;line_set.collection=letters;line_set.collection_negation='EXCLUSIVE'
for loaded_font in [font,korean_font]:
    if not loaded_font.packed_file:loaded_font.pack()
scene['reference']='User Melbourne café laneway photographs: low, varied façades, hanging oval signs, narrow seating, bluestone and overhead fixtures.'
scene['status']='First Melbourne art pass; fictional shop names.'
scene['runtimeNote']='Matches the approved Mullae illustration palette and directional flat shading.'
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.data.libraries.write(str(OUTPUT/'melbourne-lane.blend'),{scene},fake_user=True,compress=True)
result={'scene':scene.name,'file':str(OUTPUT/'melbourne-lane.blend'),'objects':len(scene.objects)}

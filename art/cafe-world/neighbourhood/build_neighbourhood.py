"""One walkable neighbourhood, with fully modelled building exteriors.

The Melbourne lane opens directly into the Mullae workshop courtyard. Buildings
retain their approved street fronts and gain backs, exposed end walls and roofs.
All collision coordinates are generated with the same assembly, in glTF Y-up.
"""
from pathlib import Path
style_path=Path(__file__).resolve().parents[1]/'street-study-v02'/'build_street.py'
style_code=style_path.read_text()
exec(style_code.split('active_collection=street')[0],globals())
from mathutils import Matrix
import bmesh
import json

scene.name='Sandon · One neighbourhood · Melbourne and Mullae'
melbourne.name='01 · Street fronts and existing structure'
seoul.name='02 · Complete rear façades and roof structure'
street.name='03 · Shared lane and workshop courtyard'
rig.name='04 · Watercolour preview rig'
font=bpy.data.fonts.load('/System/Library/Fonts/Helvetica.ttc')
iron=material('Neighbourhood iron','495658',1)
rear_brick=material('Neighbourhood aged brick','9B7C69',1)
render_wall=material('Neighbourhood patched render','B6AE98',1)
roof_metal=material('Neighbourhood roof zinc','89958E',1)
shift_y=14.0

def copy_study(relative_path,offset,omit_lane_end=False):
    with bpy.data.libraries.load(str(OUTPUT.parent/relative_path),link=False) as (available,loaded):
        loaded.scenes=[next(name for name in available.scenes if name.startswith('Sandon ·'))]
    original_scene=loaded.scenes[0]
    # Library-loaded objects do not have evaluated world transforms until their
    # source scene has a dependency graph. Reading them earlier piles pieces at 0.
    bpy.context.window.scene=original_scene
    bpy.context.view_layer.update()
    seen=set()
    for group in list(original_scene.collection.children)[:3]:
        for original in group.objects:
            if original.as_pointer() in seen:continue
            seen.add(original.as_pointer())
            if original.hide_render or original.hide_viewport or original.type not in {'MESH','CURVE','FONT'}:continue
            if original.name.startswith(('Continuous old street','Thin uneven café apron','Lane paving bed')):continue
            if omit_lane_end and original.name.startswith('Lane end'):continue
            obj=original.copy()
            obj.name=('Lane · ' if omit_lane_end else 'Workshop · ')+original.name
            melbourne.objects.link(obj)
            obj.matrix_world=Matrix.Translation(offset)@original.matrix_world
            if obj.type=='MESH' and 'reflection' in original.name:
                obj.data=original.data.copy()
                for polygon in obj.data.polygons:polygon.flip()
                obj.data.update()
    bpy.context.window.scene=scene
    bpy.context.view_layer.update()
    return original_scene

copy_study('melbourne-lane/melbourne-lane.blend',(0,0,0),True)
copy_study('mullae-lettering-v05/mullae-lettering-v05.blend',(0,shift_y,0))
active_collection=seoul

def wall_window(name,x,y,z,width,height,yaw=0,frame=iron):
    before=set(seoul.objects)
    front_window(name,0,0,z,width,height,frame)
    transform=Matrix.Translation((x,y,0))@Matrix.Rotation(yaw,4,'Z')
    for obj in set(seoul.objects)-before:
        # These are freshly created objects: use their local transform directly,
        # rather than a world matrix that has not yet been evaluated.
        obj.matrix_world=transform@obj.matrix_basis.copy()
        if obj.type=='MESH' and 'reflection' in obj.name:
            for polygon in obj.data.polygons:polygon.flip()
            obj.data.update()

def service_door(name,x,y,yaw=0,width=.82):
    before=set(seoul.objects)
    box(name+' metal frame',(0,-.04,1.13),(width+.1,.08,2.18),iron,.003)
    box(name+' painted panel',(0,-.086,1.13),(width,.018,2.07),green,.003)
    for z in [.45,1.82]:box(name+' pressed metal seam',(0,-.099,z),(width-.13,.014,.025),iron,.001)
    rod(name+' handle',(width*.3,-.12,1.02),(width*.3,-.12,1.25),.011,ivory,7)
    transform=Matrix.Translation((x,y,0))@Matrix.Rotation(yaw,4,'Z')
    for obj in set(seoul.objects)-before:obj.matrix_world=transform@obj.matrix_basis.copy()

def tapered_wall(name,x0,x1,y0,y1,bottom,top0,top1,mat):
    vertices=[(x0,y0,bottom),(x1,y0,bottom),(x1,y1,bottom),(x0,y1,bottom),(x0,y0,top0),(x1,y0,top0),(x1,y1,top1),(x0,y1,top1)]
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(vertices,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
    normals=bmesh.new();normals.from_mesh(mesh);bmesh.ops.recalc_face_normals(normals,faces=list(normals.faces));normals.to_mesh(mesh);normals.free()
    return link_object(name,mesh,mat)

# Exposed backs of all six lane buildings, with doors, windows and roof equipment.
frontages=[(-1,-3.5,4.2,5.35),(-1,.9,4.35,6.25),(-1,5.35,4.25,4.35),(1,-3.5,4.2,4.8),(1,.9,4.35,6.45),(1,5.35,4.25,4.55)]
for index,(side,y,width,height) in enumerate(frontages):
    back_x=side*6.24
    yaw=side*math.pi/2 # outward normal on the service lane, opposite the café front
    service_door('Lane rear service door '+str(index),back_x,y,yaw)
    for window_y in [y-width*.27,y+width*.27]:
        for z in [2.05,4.25,6.42,8.55]:
            if z+.82>height:continue
            wall_window('Lane rear sash '+str(index),back_x,window_y,z,.83,1.3,yaw)
    box('Lane roof west parapet',(side*4.06-width/2,y,height+.2),(.12,width,.36),trim,.003)
    box('Lane roof east parapet',(side*4.06+width/2,y,height+.2),(.12,width,.36),trim,.003)
    box('Lane roof rear parapet',(side*6.16,y,height+.2),(.12,width,.36),trim,.003)
    box('Lane roof plant enclosure',(side*4.55,y+.6,height+.29),(.9,.72,.52),roof_metal,.004)
    for i in range(5):box('Roof plant ventilation slit',(side*4.55-.31+i*.15,y+.23,height+.29),(.07,.015,.28),iron,0)
    curve('Lane rear rainwater pipe',[(back_x+side*.07,y+width*.4,height),(back_x+side*.07,y+width*.4,.4),(back_x+side*.15,y+width*.4,.12)],.024,trim)

# Street-facing end walls and courtyard-facing ends are actual façades too.
for side in [-1,1]:
    for y,yaw in [(-5.65,0),(7.52,math.pi)]:
        height=next(height for building_side,building_y,width,height in frontages if building_side==side and building_y==(-3.5 if y<0 else 5.35))
        for x in [side*3.0,side*5.05]:
            for z in [1.62,4.24,6.4]:
                if z+.75<height:wall_window('Lane exposed end sash',x,y,z,.92,1.35,yaw)
        service_door('Lane corner service entry',side*4.05,y,yaw)
    for y in [-1.34,3.15]:
        height=min(height for building_side,building_y,width,height in frontages if building_side==side and abs(building_y-y)<2.6)
        box('Sealed lane party wall gap',(side*4.08,y,height/2),(4.32,.17,height),render_wall,.002)

# Close the warehouse's eave gaps with proper wall headers beneath the sloping roof.
def cafe_roof(y):return 4.16+math.sin(.045)*(y-1.71)-.025
tapered_wall('Café east full window header',4.46,4.64,12.95,18.45,2.9,cafe_roof(-1.05),cafe_roof(4.45),render_wall)
tapered_wall('Café west roof closure',-4.58,-4.4,12.95,18.45,3.7,cafe_roof(-1.05),cafe_roof(4.45),render_wall)
box('Café rear roof closure',(0,18.44,4.01),(9.1,.2,.55),render_wall,.003)
for y,width in [(12.98,.17),(15.36,.24),(17.73,.18),(18.43,.16)]:
    box('Café east structural pier',(4.55,y,1.5),(.18,width,3.0),render_wall,.003)
service_door('Café rear delivery door',3.54,18.57,math.pi,.9)
wall_window('Café rear high window',2.1,18.57,2.95,.78,.62,math.pi)
box('Café rear gutter',(0,18.64,4.28),(9.47,.12,.1),roof_metal,.002)
curve('Café rear gutter downpipe',[(4.67,18.65,4.28),(4.67,18.65,.32),(4.77,18.65,.12)],.033,trim)

def shed_roof(y):return 3.86+math.sin(.1)*(y-1.33)-.025
tapered_wall('Workshop west roof closure',-9.58,-9.42,13.07,17.57,3.5,shed_roof(-.93),shed_roof(3.57),render_wall)
tapered_wall('Workshop east roof closure',-4.76,-4.6,13.07,17.57,3.5,shed_roof(-.93),shed_roof(3.57),render_wall)
box('Workshop rear roof closure',(-7.1,17.5,3.8),(4.9,.2,.65),render_wall,.003)
service_door('Workshop rear steel door',-7.05,17.62,math.pi,1.02)
for x in [-8.65,-5.58]:wall_window('Workshop rear clerestory',x,17.62,2.7,.8,.65,math.pi)
for y in [14.3,16.3]:wall_window('Workshop outer side window',-9.6,y,2.45,.85,.85,-math.pi/2)

# Fully finish the taller buildings behind the café and on the side street.
for x in [-3.2,-1.2,.75]:
    for z in [2.0,4.2,6.65]:
        if x==-1.2 and z==2.0:continue
        wall_window('Rear brick block back window',x,22.22,z,.95,1.3,math.pi)
service_door('Rear brick block back door',-1.2,22.22,math.pi)
for x,yaw in [(-4.43,-math.pi/2),(1.93,math.pi/2)]:
    for y in [19.5,21.2]:
        for z in [2.05,4.3,6.65]:wall_window('Rear brick block side window',x,y,z,.82,1.23,yaw)
box('Rear block roof parapet',(-1.25,22.14,8.84),(6.4,.13,.35),rear_brick,.002)
curve('Rear brick block drainpipe',[(1.94,22.19,8.65),(1.94,22.19,.13)],.027,trim)
for x,yaw in [(7.47,-math.pi/2),(11.13,math.pi/2)]:
    for y in [16.4,18.7,20.6]:
        for z in [2.2,4.73,6.4]:wall_window('Side-lane building full side window',x,y,z,.86,1.16,yaw)
for x in [8.1,10.15]:
    for z in [2.1,4.73,6.4]:wall_window('Side-lane building rear window',x,21.83,z,.85,1.15,math.pi)
service_door('Side-lane building rear entry',9.1,21.83,math.pi)
box('Side-lane roof parapet',(9.3,21.76,7.68),(3.65,.13,.35),trim,.002)
curve('Side-lane exposed rear pipe',[(11.17,21.8,7.5),(11.17,21.8,.1)],.024,trim)
for x,yaw in [(4.34,-math.pi/2),(7.66,math.pi/2)]:
    for z in [1.8,3.8]:wall_window('Far workshop side window',x,25.1,z,.78,.95,yaw)
service_door('Far workshop back door',6.0,26.18,math.pi)
wall_window('Far workshop back window',6.0,26.18,3.7,1.2,.85,math.pi)

# Reference-led interior is built inside the existing warehouse shell.
exec(compile((OUTPUT/'interior.py').read_text(),str(OUTPUT/'interior.py'),'exec'),globals())

# One shared ground, with the lane opening into the courtyard, plus service paths
# around the outside. No plinths, isolated city islands or teleport entrances.
active_collection=street
box('Continuous neighbourhood foundation',(0,9.4,-.08),(27,42,.16),asphalt,.002)
box('Workshop courtyard paving',(0,10.4,.01),(23.5,5.8,.035),concrete,.002)
for x in [-11.6,12.1]:box('Perimeter service footpath',(x,10,.005),(1.6,39,.025),concrete,.002)
box('Rear service footpath',(0,28.2,.005),(25.5,2.2,.025),concrete,.002)
for y in [8.1,9.4,10.7,11.9]:
    for x in [-10.8,-7.4,-4,-.6,2.8,6.2,9.6]:
        stroke('Courtyard slab joint',[(x,y,.032),(x+3.12,y,.032)],.0025)
for x in [-7.4,-4.0,-.6,2.8,6.2,9.6]:stroke('Shared courtyard cross joint',[(x,7.6,.032),(x,12.8,.032)],.0025)
for x in [-1.7,1.7]:
    curve('Lane lights continue into courtyard',[(x,6.5,3.95),(x,9.4,3.6),(x,12.7,4.22)],.009,iron)
    for y in [8.0,9.4,10.8]:sphere('Shared courtyard light',(x,y,3.6+abs(y-9.4)*.075),(.043,.043,.06),lamp_glow,1)
for x,y in [(-6.7,8.5),(6.6,9.0),(-10.6,20),(11.8,24.5)]:pot('Neighbourhood planter',x,y,.035,.26)

exec(compile((OUTPUT/'street_life.py').read_text(),str(OUTPUT/'street_life.py'),'exec'),globals())
exec(compile((OUTPUT/'utilities.py').read_text(),str(OUTPUT/'utilities.py'),'exec'),globals())
install_utilities(scene,street)
exec(compile((OUTPUT/'scenery.py').read_text(),str(OUTPUT/'scenery.py'),'exec'),globals())

layout={'spawn':{'x':0,'z':8.8},'bounds':{'minX':-12.5,'maxX':13,'minZ':-29,'maxZ':10.5},'points':{'coffee':{'x':-.4,'z':3.8},'writing':{'x':.4,'z':-.9},'building':{'x':-2.5,'z':-15.0}},'obstacles':[]}
def barrier(x0,x1,y0,y1):layout['obstacles'].append({'minX':x0,'maxX':x1,'minZ':-y1,'maxZ':-y0})
barrier(-6.3,-1.92,-5.65,7.53);barrier(1.92,6.3,-5.65,7.53)
barrier(-4.6,-4.39,12.95,18.53);barrier(-4.6,4.66,18.32,18.62);barrier(4.45,4.72,12.95,18.53)
barrier(-1.18,4.62,12.78,13.1);barrier(-4.38,-3.75,12.88,13.04);barrier(-1.76,-1.12,12.88,13.04)
for footprint in interior_footprints:barrier(*footprint)
for footprint in street_footprints:barrier(*footprint)
barrier(-9.6,-9.4,13.02,17.65);barrier(-4.78,-4.6,13.02,17.65);barrier(-9.6,-4.6,17.42,17.65)
barrier(-8.5,-5.6,14.98,15.9)
barrier(-4.44,1.94,18.4,22.22);barrier(7.47,11.16,14.84,21.84);barrier(4.34,7.66,24.05,26.2)
barrier(-.38,.7,11.65,12.7);barrier(2.8,4.0,11.9,12.4)
for side,y,width,height in frontages:
    if side<0:barrier(-1.8,-.85,y-1.7,y+.17)
    else:barrier(.85,1.8,y+.13,y+1.7)
layout['rooms']={'cafe':{'minX':-4.3,'maxX':4.3,'minZ':-18.3,'maxZ':-13.05}}
layout_path=OUTPUT.parents[2]/'src'/'world'/'layout.json'
layout_path.write_text(json.dumps(layout,indent=2)+'\n')

active_collection=rig
world=bpy.data.worlds.new('Shared neighbourhood sky');world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(*colour('BACBD4'),1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8;scene.world=world
sun=bpy.data.lights.new('Shared afternoon sun','SUN');sun.energy=1.7;sun.angle=.07
sun_obj=link_object('Shared afternoon sun',sun);sun_obj.rotation_euler=(.45,-.5,-.55)
def camera(name,position,target,lens):
    data=bpy.data.cameras.new(name);data.lens=lens
    obj=link_object(name,data);obj.location=position;obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
    return obj
scene.camera=camera('Lane into workshop courtyard',(.15,-9.1,2.1),(0,14,2.55),24)
camera('Rear building inspection',(12,29.1,2.4),(0,17,4.2),28)
camera('Café interior at eye level',(-2.7,13.9,1.66),(-.6,17.2,1.75),22)
camera('Quiet tiled seating',(3.4,14.0,1.64),(.3,17.2,1.6),22)
scenery_view=camera('Street and distant scenery',(-11,-8,2.2),(-14,20,4.3),28)
overview=camera('Neighbourhood overview',(25,-22,31),(0,10,1.8),40)
overview.data.type='ORTHO';overview.data.ortho_scale=47
scene.render.engine='CYCLES';scene.cycles.samples=28;scene.cycles.use_denoising=True
scene.render.resolution_x=1500;scene.render.resolution_y=1050;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
# New back-side materials get the same illustration treatment as the existing fronts.
exec(style_code[style_code.index('def illustrated_materials():'):style_code.index('# Freestyle is the Blender')],globals())
# Unlike the old opaque façade studies, these panes can be seen through from
# both inside and outside. The solid mullions and wall shell remain separate.
for mat in bpy.data.materials:
    if 'small old glass panes' not in mat.name:continue
    nodes=mat.node_tree.nodes;links=mat.node_tree.links
    output=next(node for node in nodes if node.type=='OUTPUT_MATERIAL')
    clear=nodes.new('ShaderNodeBsdfTransparent');clear.inputs['Color'].default_value=(.91,.96,.92,1)
    tint=nodes.new('ShaderNodeBsdfDiffuse');tint.inputs['Color'].default_value=(*colour('9DB6A6'),1)
    mix=nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.12
    links.new(clear.outputs[0],mix.inputs[1]);links.new(tint.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],output.inputs['Surface'])
scene.render.use_freestyle=True
settings=scene.view_layers[0].freestyle_settings;settings.crease_angle=math.radians(120)
lines=settings.linesets[0] if len(settings.linesets) else settings.linesets.new('Pencil contours')
lines.select_silhouette=True;lines.select_border=True;lines.select_crease=True
lines.linestyle.color=colour('555C5C');lines.linestyle.thickness=.55;lines.linestyle.alpha=.65
letters=bpy.data.collections.new('05 · Lettering');scene.collection.children.link(letters)
for obj in scene.objects:
    if obj.type=='FONT':letters.objects.link(obj)
lines.select_by_collection=True;lines.collection=letters;lines.collection_negation='EXCLUSIVE'
scene['layout']='One lane and courtyard, with walkable perimeter service streets. Melbourne and Mullae architecture share the same physical block.'
scene['buildingScope']='Fully modelled exteriors and roof enclosures. Workshop café includes an enterable bar and tiled seating area; other closed buildings have complete exteriors.'
for other in list(bpy.data.scenes):
    if other!=scene:bpy.data.scenes.remove(other)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT/'neighbourhood.blend'),compress=True)
audit_path=OUTPUT/'audit_geometry.py'
exec(compile(audit_path.read_text(),str(audit_path),'exec'),{'__file__':str(audit_path),'__name__':'__main__'})
print('CONTINUOUS_NEIGHBOURHOOD_SAVED '+str(OUTPUT/'neighbourhood.blend'),flush=True)

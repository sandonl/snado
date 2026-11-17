"""Original café walker: soft proportions, expressive face and a jointed object rig.
Metres; Blender Z-up, facing -Y. glTF converts this to Y-up, facing +Z.
"""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
folder=Path(__file__).resolve().parent
project=folder.parents[2]
scene=bpy.data.scenes.new('Sandon · Café walker character')
bpy.context.window.scene=scene
scene.unit_settings.system='METRIC'
model=bpy.data.collections.new('01 · Editable walker');scene.collection.children.link(model)
rig=bpy.data.collections.new('02 · Preview rig');scene.collection.children.link(rig)
origins={}

def material(role,hex_color):
    mat=bpy.data.materials.new('Walker · '+role)
    rgb=[int(hex_color[i:i+2],16)/255 for i in (0,2,4)]
    mat.diffuse_color=tuple(v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in rgb)+(1,)
    mat.use_nodes=True
    shader=mat.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=mat.diffuse_color
    shader.inputs['Roughness'].default_value=.88
    shader.inputs['Specular IOR Level'].default_value=.18
    return mat
cap=material('cap','547C68');shirt=material('top','E4DEC7');pants=material('bottom','6E7A70')
shoe=material('shoes','D8C9AA');bag=material('bag','AE8D62');skin=material('skin','CB9B74')
hair=material('hair','4A4035');eye=material('eyes','332F29');white=material('eye light','F2E9D1')
seam=material('seams','7C8170');sole=material('soles','7D8175');blush=material('cheeks','C78A72')

def group(name,parent,origin):
    obj=bpy.data.objects.new(name,None);model.objects.link(obj)
    obj.parent=parent
    obj.location=Vector(origin)-(origins[parent] if parent else Vector())
    origins[obj]=Vector(origin)
    return obj
root=group('cafeWalker',None,(0,0,0));upper=group('upperBody',root,(0,0,0));head=group('head',upper,(0,0,1.22))

def attach(obj,name,parent,position,mat):
    for collection in list(obj.users_collection):collection.objects.unlink(obj)
    model.objects.link(obj);obj.name=name;obj.parent=parent
    obj.location=Vector(position)-origins[parent];origins[obj]=Vector(position)
    obj.data.materials.append(mat)
    return obj

def blob(name,parent,position,scale,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16)
    obj=bpy.context.object
    for vertex in obj.data.vertices:
        vertex.co.x*=scale[0];vertex.co.y*=scale[1];vertex.co.z*=scale[2]
    for polygon in obj.data.polygons:polygon.use_smooth=True
    obj.data.update()
    return attach(obj,name,parent,position,mat)

def mesh(name,parent,vertices,faces,mat):
    data=bpy.data.meshes.new(name)
    data.from_pydata([Vector(v)-origins[parent] for v in vertices],[],faces);data.update()
    normals=bmesh.new();normals.from_mesh(data);bmesh.ops.recalc_face_normals(normals,faces=list(normals.faces));normals.to_mesh(data);normals.free()
    obj=bpy.data.objects.new(name,data);model.objects.link(obj);obj.parent=parent;obj.data.materials.append(mat)
    origins[obj]=origins[parent].copy()
    for polygon in data.polygons:polygon.use_smooth=True
    return obj

def line(name,parent,points,radius,mat):
    data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.resolution_u=6;data.bevel_depth=radius;data.bevel_resolution=2;data.use_fill_caps=True
    spline=data.splines.new('BEZIER');spline.bezier_points.add(len(points)-1)
    for point,co in zip(spline.bezier_points,points):point.co=Vector(co)-origins[parent];point.handle_left_type=point.handle_right_type='AUTO'
    obj=bpy.data.objects.new(name,data);model.objects.link(obj);obj.parent=parent;data.materials.append(mat)
    return obj

# A soft, tapered pullover, instead of a rectangular torso.
vertices=[]
sections=[(.55,.19,.12),(.58,.235,.15),(.67,.25,.155),(.85,.235,.14),(.94,.19,.12),(.98,.105,.075)]
for z,rx,ry in sections:
    vertices.extend((math.cos(i*math.tau/32)*rx,math.sin(i*math.tau/32)*ry,z) for i in range(32))
faces=[tuple(reversed(range(32))),tuple(range((len(sections)-1)*32,len(sections)*32))]
for row in range(len(sections)-1):
    faces.extend((row*32+i,row*32+(i+1)%32,(row+1)*32+(i+1)%32,(row+1)*32+i) for i in range(32))
mesh('softPullover',upper,vertices,faces,shirt)
blob('neck',upper,(0,0,.98),(.07,.075,.1),skin)
line('shirtHem',upper,[(math.cos(i*math.tau/16)*.234,math.sin(i*math.tau/16)*.15,.588) for i in range(17)],.005,seam)
line('collar',upper,[(-.085,-.063,.964),(0,-.084,.946),(.085,-.063,.964)],.012,shirt)
blob('trouserHips',root,(0,.015,.57),(.205,.13,.12),pants)

# Short rounded limbs, with real shoulder/hip pivots and separate feet.
for side,label in [(-1,'left'),(1,'right')]:
    leg=group(label+'Leg',root,(side*.12,0,.56))
    blob(label+'Thigh',leg,(side*.12,.006,.455),(.106,.12,.137),pants)
    lower=group(label+'LowerLeg',leg,(side*.12,0,.335))
    blob(label+'Shin',lower,(side*.12,.006,.245),(.094,.112,.122),pants)
    blob(label+'Shoe',lower,(side*.12,-.045,.135),(.112,.18,.085),shoe)
    blob(label+'Sole',lower,(side*.12,-.043,.081),(.112,.178,.031),sole)
    for offset in [-.024,.005,.034]:line(label+'ShoeLace',lower,[(side*.12-.045,-.074+offset,.202),(side*.12,-.09+offset,.207),(side*.12+.045,-.074+offset,.202)],.0035,white)
    arm=group(label+'Arm',upper,(side*.285,0,.9))
    sleeve=blob(label+'UpperSleeve',arm,(side*.295,.01,.833),(.091,.105,.112),shirt)
    sleeve.rotation_euler.y=side*.1
    forearm=group(label+'ForeArm',arm,(side*.30,-.005,.755))
    blob(label+'LowerSleeve',forearm,(side*.304,.0,.705),(.079,.091,.089),shirt)
    blob(label+'Cuff',forearm,(side*.305,-.005,.655),(.075,.084,.047),shirt)
    hand=blob(label+'Hand',forearm,(side*.307,-.005,.587),(.067,.076,.08),skin)
    blob(label+'Thumb',forearm,(side*.263,-.063,.602),(.032,.035,.041),skin)
    if label=='right':right_hand=hand

# Enlarged head and a readable face, authored with actual geometry.
blob('roundedHead',head,(0,0,1.22),(.34,.30,.33),skin)
for side,label in [(-1,'left'),(1,'right')]:
    blob(label+'Ear',head,(side*.337,.002,1.205),(.057,.048,.073),skin)
    blob(label+'EarInset',head,(side*.361,-.028,1.211),(.02,.012,.037),blush)
    blob(label+'Sideburn',head,(side*.294,.002,1.263),(.063,.082,.104),hair)
    eye_x=side*.118;eye_z=1.245
    surface_y=-.30*math.sqrt(1-(eye_x/.34)**2-((eye_z-1.22)/.33)**2)
    pupil=blob(label+'Eye',head,(eye_x,surface_y-.009,eye_z),(.029,.017,.043),eye)
    blob(label+'EyeGlint',pupil,(eye_x-.006,surface_y-.025,eye_z+.015),(.006,.004,.008),white)
    line(label+'Eyebrow',head,[(side*.074,-.274,1.319),(side*.119,-.28,1.33),(side*.158,-.266,1.321)],.009,hair)
blob('buttonNose',head,(0,-.301,1.192),(.036,.037,.035),skin)
line('smallSmile',head,[(-.037,-.283,1.116),(0,-.289,1.105),(.037,-.283,1.116)],.0045,eye)
# Close the back half of the hair mass; sideburns tuck under the cap.
blob('backHair',head,(0,.083,1.297),(.315,.248,.246),hair)

# Closed cap crown and a curved, thick visor. No flat billboard components.
segments=32;rings=12;theta_max=1.94
vertices=[(0,0,1.65)]
for row in range(1,rings+1):
    theta=theta_max*row/rings
    vertices.extend((.365*math.sin(theta)*math.cos(i*math.tau/segments),.325*math.sin(theta)*math.sin(i*math.tau/segments),1.39+.26*math.cos(theta)) for i in range(segments))
faces=[(0,1+i,1+(i+1)%segments) for i in range(segments)]
for row in range(rings-1):
    a=1+row*segments;b=a+segments
    faces.extend((a+i,b+i,b+(i+1)%segments,a+(i+1)%segments) for i in range(segments))
faces.append(tuple(reversed(range(1+(rings-1)*segments,1+rings*segments))))
mesh('capCrown',head,vertices,faces,cap)
angles=[-math.pi/2+i*math.pi/24 for i in range(25)]
outline=[(.34*math.sin(a),-.21-.32*math.cos(a),1.342+.018*math.cos(a)) for a in angles]
outline +=[(.30*math.sin(a),-.19-.04*math.cos(a),1.36) for a in reversed(angles)]
count=len(outline);vertices=outline+[(x,y,z-.023) for x,y,z in outline]
faces=[tuple(range(count)),tuple(reversed(range(count,count*2)))]
faces.extend((i,i+count,(i+1)%count+count,(i+1)%count) for i in range(count))
mesh('curvedCapVisor',head,vertices,faces,cap)
blob('capTopButton',head,(0,0,1.647),(.023,.023,.014),cap)
for angle in [0,math.pi/2,math.pi,math.pi*1.5]:
    points=[]
    for i in range(9):
        theta=.09+i*1.78/8
        points.append((.366*math.sin(theta)*math.cos(angle),.326*math.sin(theta)*math.sin(angle),1.39+.261*math.cos(theta)))
    line('capPanelSeam',head,points,.0025,seam)
# A small canvas backpack gives the rear silhouette some character too.
blob('canvasBackpack',upper,(0,.167,.767),(.17,.095,.21),bag)
blob('backpackPocket',upper,(0,.245,.733),(.131,.033,.112),bag)
for side in [-1,1]:line('backpackShoulderStrap',upper,[(side*.135,.17,.93),(side*.175,-.07,.903),(side*.178,-.137,.76),(side*.14,-.102,.625)],.015,bag)
line('backpackPocketStitch',upper,[(-.09,.275,.76),(0,.282,.775),(.09,.275,.76)],.003,seam)

# A real cup travels with the hand for the sitting/drinking action.
cup_mat=material('cup','E4DEC9');coffee_mat=material('coffee','5E4A34')
cup_origin=(.262,-.145,.627)
held_cup=group('heldCup',right_hand,cup_origin)
cup_start=set(model.objects)
rings=[(.035,0),(.052,.10),(.046,.10),(.030,.009)];count=24
vertices=[(cup_origin[0]+r*math.cos(i*math.tau/count),cup_origin[1]+r*math.sin(i*math.tau/count),cup_origin[2]+z) for r,z in rings for i in range(count)]
faces=[]
for ring in range(3):faces.extend((ring*count+i,ring*count+(i+1)%count,(ring+1)*count+(i+1)%count,(ring+1)*count+i) for i in range(count))
faces.extend([tuple(reversed(range(count))),tuple(range(count*3,count*4))])
mesh('cupBody',held_cup,vertices,faces,cup_mat)
blob('cupCoffee',held_cup,(cup_origin[0],cup_origin[1],cup_origin[2]+.087),(.042,.042,.002),coffee_mat)
line('cupHandle',held_cup,[(cup_origin[0]+.044,cup_origin[1],cup_origin[2]+.078),(cup_origin[0]+.084,cup_origin[1],cup_origin[2]+.077),(cup_origin[0]+.084,cup_origin[1],cup_origin[2]+.028),(cup_origin[0]+.038,cup_origin[1],cup_origin[2]+.028)],.006,cup_mat)
cup_parts=set(model.objects)-cup_start

bpy.context.view_layer.update()
# Validate the actual rig and mesh, not just the beauty render.
mesh_objects=[obj for obj in model.objects if obj.type=='MESH']
points=[obj.matrix_world@Vector(corner) for obj in mesh_objects for corner in obj.bound_box]
minimum=[min(p[i] for p in points) for i in range(3)];maximum=[max(p[i] for p in points) for i in range(3)]
required=['leftArm','rightArm','leftLeg','rightLeg','leftShoe','rightShoe','leftEye','rightEye','upperBody','leftLowerLeg','rightLowerLeg','leftForeArm','rightForeArm','rightHand','heldCup']
assert all(scene.objects.get(name) for name in required),'The walking rig lost a required part'
assert .049<minimum[2]<.051,'Soles must meet the existing walking floor'
assert 1.5<maximum[2]<1.7,'Character no longer fits the street scale'
for obj in mesh_objects:
    assert all(math.isfinite(value) for vertex in obj.data.vertices for value in vertex.co),'Non-finite geometry'
report={'passed':True,'heightMetres':round(maximum[2]-minimum[2],3),'soleHeightMetres':round(minimum[2],3),'meshCount':len(mesh_objects),'rigParts':required,'frontDirection':'Blender -Y → glTF +Z','stage':'First playable character experiment from the user-supplied reference; original geometry and materials.'}
(folder/'character-audit.json').write_text(json.dumps(report,indent=2)+'\n')
# Authoring preview is separate from the exported character collection.
world=bpy.data.worlds.new('Warm paper studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.69,.65,1);world.node_tree.nodes['Background'].inputs[1].default_value=.6;scene.world=world
for name,location,energy,size in [('Key',(-3,-4,5),420,4),('Fill',(3,-1,3),170,3)]:
    light=bpy.data.lights.new(name,'AREA');light.energy=energy;light.shape='DISK';light.size=size
    obj=bpy.data.objects.new(name,light);rig.objects.link(obj);obj.location=location;obj.rotation_euler=(Vector((0,0,.9))-obj.location).to_track_quat('-Z','Y').to_euler()
cam=bpy.data.cameras.new('Walker portrait');camera=bpy.data.objects.new('Walker portrait',cam);rig.objects.link(camera);camera.location=(2.35,-4.1,2.05);camera.rotation_euler=(Vector((0,0,.85))-camera.location).to_track_quat('-Z','Y').to_euler();cam.type='ORTHO';cam.ortho_scale=2.12;scene.camera=camera
scene.render.engine='CYCLES';scene.cycles.samples=40;scene.cycles.use_denoising=True;scene.render.resolution_x=1000;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=True;scene.view_settings.view_transform='AgX'
for other in list(bpy.data.scenes):
    if other!=scene:bpy.data.scenes.remove(other)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'cafe-walker.blend'),compress=True)
# Convert curved seams in the isolated export selection; the editable file stays intact.
bpy.ops.object.select_all(action='DESELECT')
for obj in model.objects:
    obj.select_set(True)
    if obj.type=='CURVE':obj.data.resolution_u=4;obj.data.bevel_resolution=1
bpy.context.view_layer.objects.active=root
runtime=project/'public/models/cafe-walker.glb'
bpy.ops.export_scene.gltf(filepath=str(runtime),export_format='GLB',use_selection=True,export_apply=True,export_animations=False,export_extras=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
for obj in cup_parts:obj.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'cafe-walker.blend'),compress=True)
scene.render.filepath=str(folder/'cafe-walker.png');bpy.ops.render.render(write_still=True)
print('CAFE_WALKER_BUILT '+json.dumps(report),flush=True)

"""Compact public walking area, usable seats, and matching resident previews.
The outer streets stay as scenery. Runtime residents share the player's GLB.
"""
import bpy,bmesh,math,json
from mathutils import Vector,Matrix


def install_play_area(scene,street,folder):
    for obj in list(scene.objects):
        if obj.name.startswith(('Play area · ','Preview resident · ','Lane reader')):
            bpy.data.objects.remove(obj,do_unlink=True)
        elif obj.name.startswith('Courtyard coffee visitor') and not any(part in obj.name for part in [' seat','chair leg']):
            bpy.data.objects.remove(obj,do_unlink=True)
    # Bring the existing courtyard bench into the pocket courtyard.
    for obj in scene.objects:
        if obj.name.startswith('Courtyard timber bench seat'):obj.location.x=4.8;obj.location.y=9.3
        elif obj.name.startswith('Courtyard bench steel leg'):
            obj.location.x=4.15 if obj.location.x<6.4 else 5.45;obj.location.y=9.3

    def material(name,hex_color):
        name='Play area · '+name
        existing=bpy.data.materials.get(name)
        if existing:return existing
        mat=bpy.data.materials.new(name)
        rgb=[int(hex_color[i:i+2],16)/255 for i in (0,2,4)]
        mat.diffuse_color=tuple(v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in rgb)+(1,)
        mat.use_nodes=True
        nodes=mat.node_tree.nodes;links=mat.node_tree.links
        normal=nodes.new('ShaderNodeNewGeometry');dot=nodes.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.48,-.55,.72)
        links.new(normal.outputs['Normal'],dot.inputs[0])
        ramp=nodes.new('ShaderNodeMapRange');ramp.inputs['To Min'].default_value=.72;ramp.inputs['To Max'].default_value=1
        links.new(dot.outputs['Value'],ramp.inputs[0])
        shade=nodes.new('ShaderNodeMixRGB');shade.blend_type='MULTIPLY';shade.inputs[0].default_value=1;shade.inputs[1].default_value=mat.diffuse_color
        links.new(ramp.outputs[0],shade.inputs[2])
        emission=nodes.new('ShaderNodeEmission');links.new(shade.outputs[0],emission.inputs[0]);links.new(emission.outputs[0],nodes.get('Material Output').inputs['Surface'])
        return mat
    timber=material('weathered timber','9B896C');metal=material('garden iron','5C6D61');plaster=material('planter render','B7B9A6');leaf=material('foliage','899C7A')

    def mesh(name,vertices,faces,mat):
        data=bpy.data.meshes.new(name);data.from_pydata(vertices,[],faces);data.update();data.materials.append(mat)
        obj=bpy.data.objects.new('Play area · '+name,data);street.objects.link(obj);return obj
    def box(name,position,size,mat):
        x,y,z=[v/2 for v in size]
        obj=mesh(name,[(-x,-y,-z),(-x,-y,z),(-x,y,-z),(-x,y,z),(x,-y,-z),(x,-y,z),(x,y,-z),(x,y,z)],[(2,6,4,0),(5,7,3,1),(4,5,1,0),(3,7,6,2),(1,3,2,0),(6,7,5,4)],mat)
        obj.location=position
        mod=obj.modifiers.new('Small edge','BEVEL');mod.width=.003;mod.segments=1
        return obj
    def rod(name,a,b,radius,mat):
        a,b=Vector(a),Vector(b);bm=bmesh.new();bmesh.ops.create_cone(bm,cap_ends=True,segments=10,radius1=radius,radius2=radius,depth=(b-a).length)
        data=bpy.data.meshes.new(name);bm.to_mesh(data);bm.free();data.materials.append(mat)
        obj=bpy.data.objects.new('Play area · '+name,data);street.objects.link(obj);obj.location=(a+b)/2;obj.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return obj
    def greenery(position):
        bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=1,radius=1)
        data=bpy.data.meshes.new('Garden foliage');bm.to_mesh(data);bm.free();data.materials.append(leaf)
        obj=bpy.data.objects.new('Play area · foliage',data);street.objects.link(obj);obj.location=position;obj.scale=(.32,.52,.35)
    barriers=[]
    for x in [-5.25,6.35]:
        for y in [8.6,10.7,12.8]:
            box('courtyard planter',(x,y,.39),(.5,1.7,.72),plaster)
            for dy in [-.45,.1,.55]:greenery((x,y+dy,.91))
        box('courtyard timber rail',(x,10.5,.79),(.08,6.1,.08),timber)
    for x in [-2.5,2.5]:
        box('arrival planter',(x,-8.55,.4),(.5,2.1,.74),plaster)
        for y in [-9.1,-8.5,-8.0]:greenery((x,y,.93))
    box('arrival end rail',(0,-9.65,.24),(4.6,.1,.12),timber)
    for x in [-2.15,0,2.15]:box('arrival rail post',(x,-9.65,.14),(.08,.08,.26),metal)
    box('courtyard side closure',(5.4,13.65,.4),(1.5,.35,.74),plaster)
    for x in [4.95,5.4,5.85]:greenery((x,13.65,.91))
    box('café low room divider',(2.72,16.2,.55),(3.35,.10,.9),plaster)
    box('café divider top',(2.72,16.2,1.01),(3.4,.14,.045),timber)
    barriers.extend([(-5.5,-5,7.4,13.6),(6.1,6.6,7.4,13.6),(-2.75,-2.25,-9.6,-7.5),(2.25,2.75,-9.6,-7.5),(-2.3,2.3,-9.7,-9.6),(1.045,4.4,16.15,16.25),(3.9,5.7,9.08,9.53)])
    seats=[
        {'id':'laneChair','label':'Café chair','x':-1.3,'z':3.63,'surfaceY':.586,'yaw':0,'approach':{'x':-.36,'z':3.63}},
        {'id':'courtyardBench','label':'Courtyard bench','x':4.65,'z':-9.3,'surfaceY':.5475,'yaw':0,'approach':{'x':4.65,'z':-8.4}},
        {'id':'cafeStool','label':'Window seat','x':2.12,'z':-14.6,'surfaceY':.58,'yaw':math.pi/2,'approach':{'x':1.43,'z':-14.6}},
    ]
    residents=[
        {'id':'laneRegular','x':-1.3,'z':4.9,'surfaceY':.586,'yaw':math.pi,'palette':'clay','offset':1.1},
        {'id':'courtyardRegular','x':3.465,'z':-10.62,'surfaceY':.53,'yaw':math.pi/3,'palette':'ink','offset':4.2},
    ]
    for seat in seats+residents:
        x,y=seat['x'],-seat['z'];yaw=seat['yaw'];z=seat['surfaceY']-.256
        forward=Vector((math.sin(yaw),-math.cos(yaw),0));across=Vector((math.cos(yaw),math.sin(yaw),0))
        centre=Vector((x,y,z))+forward*.26
        rod('seat footrest',centre-across*.245,centre+across*.245,.012,metal)
        for side in [-1,1]:
            top=centre+across*side*.20
            rod('footrest support',(top.x,top.y,.06),top,.012,metal)

    # Editable seated residents for native Blender previews. Runtime uses animated
    # clones of the same player asset, so these copies are excluded from the GLB.
    asset=folder.parents[1]/'characters'/'cafe-walker'/'cafe-walker.blend'
    with bpy.data.libraries.load(str(asset),link=False) as (available,loaded):
        loaded.collections=[next(name for name in available.collections if name.startswith('01 · Editable walker'))]
    source=list(loaded.collections[0].all_objects)
    for resident in residents:
        copies={original:original.copy() for original in source}
        for original,obj in copies.items():
            obj.name='Preview resident · '+resident['id']+' / '+original.name
            street.objects.link(obj);obj.parent=copies.get(original.parent);obj.matrix_basis=original.matrix_basis.copy();obj.hide_render=False
        def part(name):return copies[next(obj for obj in source if obj.name.split('.')[0]==name)]
        root=part('cafeWalker');root.location=(resident['x'],-resident['z'],resident['surfaceY']-.45);root.rotation_euler.z=resident['yaw']
        for side in ['left','right']:
            part(side+'Leg').rotation_euler.x=-1.25;part(side+'LowerLeg').rotation_euler.x=1.25
            part(side+'Arm').rotation_euler.x=-.35;part(side+'ForeArm').rotation_euler.x=-1.1
        bpy.context.view_layer.update()
        hand=part('rightHand');cup=part('heldCup')
        cup.matrix_world=Matrix.Translation(hand.matrix_world.translation+root.matrix_world.to_3x3()@Vector((-.045,-.14,.03)))@Matrix.Rotation(resident['yaw'],4,'Z')
        colors={'clay':{'cap':'BB8B75','top':'778F83','bottom':'515F63'},'ink':{'cap':'617787','top':'CBB998','bottom':'536965'}}[resident['palette']]
        material_copies={}
        for original,obj in copies.items():
            if obj.type not in {'MESH','CURVE'}:continue
            obj.data=original.data.copy()
            for index,old in enumerate(list(obj.data.materials)):
                if old not in material_copies:
                    mat=old.copy();role=old.name.removeprefix('Walker · ').split('.')[0];mat.name='Walker · '+role+' '+resident['id']
                    if role in colors:
                        rgb=[int(colors[role][i:i+2],16)/255 for i in (0,2,4)];mat.diffuse_color=tuple(v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in rgb)+(1,)
                        mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=mat.diffuse_color
                    material_copies[old]=mat
                obj.data.materials[index]=material_copies[old]
    bpy.data.collections.remove(loaded.collections[0])
    bpy.context.view_layer.update()
    return {'walkableAreas':[{'minX':-2.25,'maxX':2.25,'minZ':5.5,'maxZ':9.6},{'minX':-1.9,'maxX':1.9,'minZ':-8.8,'maxZ':6.6},{'minX':-5,'maxX':6.1,'minZ':-13.6,'maxZ':-7.4},{'minX':-4.35,'maxX':4.35,'minZ':-16.15,'maxZ':-12.4}], 'seats':seats,'residents':residents,'barriers':barriers}


def apply_layout(layout,details):
    layout['walkableAreas']=details['walkableAreas'];layout['seats']=details['seats'];layout['residents']=details['residents']
    layout['bounds']={'minX':-5,'maxX':6.1,'minZ':-16.15,'maxZ':9.6}
    for x0,x1,y0,y1 in details['barriers']:
        obstacle={'minX':x0,'maxX':x1,'minZ':-y1,'maxZ':-y0}
        if obstacle not in layout['obstacles']:layout['obstacles'].append(obstacle)
    return layout

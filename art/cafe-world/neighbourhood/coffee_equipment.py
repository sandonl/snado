"""Detailed café equipment. Local +Y is always the barista's operating side.

Independent of the neighbourhood primitive helpers so this small asset can be
rebuilt in the saved world without regenerating the entire block.
"""
import bpy
import bmesh
import math
from mathutils import Vector


def build_coffee_equipment(scene, collection, camera_collection):
    for obj in list(scene.objects):
        if obj.name.startswith(('Interior espresso ', 'Interior grinder ', 'Coffee equipment · ')):
            bpy.data.objects.remove(obj, do_unlink=True)

    def material(name, value):
        name='Equipment · '+name
        existing=bpy.data.materials.get(name)
        if existing:return existing
        mat=bpy.data.materials.new(name)
        rgb=[int(value[i:i+2],16)/255 for i in (0,2,4)]
        mat.diffuse_color=tuple(v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in rgb)+(1,)
        mat.use_nodes=True
        nodes=mat.node_tree.nodes;links=mat.node_tree.links
        output=nodes.get('Material Output')
        if 'hopper glazing' in name:
            clear=nodes.new('ShaderNodeBsdfTransparent')
            clear.inputs['Color'].default_value=(.94,.97,.95,1)
            tint=nodes.new('ShaderNodeBsdfDiffuse');tint.inputs['Color'].default_value=mat.diffuse_color
            mix=nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.2
            links.new(clear.outputs[0],mix.inputs[1]);links.new(tint.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],output.inputs['Surface'])
        else:
            normal=nodes.new('ShaderNodeNewGeometry')
            dot=nodes.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.48,-.55,.72)
            links.new(normal.outputs['Normal'],dot.inputs[0])
            ramp=nodes.new('ShaderNodeMapRange');ramp.inputs['From Min'].default_value=-1;ramp.inputs['From Max'].default_value=1
            ramp.inputs['To Min'].default_value=.62;ramp.inputs['To Max'].default_value=1
            links.new(dot.outputs['Value'],ramp.inputs['Value'])
            shade=nodes.new('ShaderNodeMixRGB');shade.blend_type='MULTIPLY';shade.inputs[0].default_value=1;shade.inputs[1].default_value=mat.diffuse_color
            links.new(ramp.outputs['Result'],shade.inputs[2])
            emission=nodes.new('ShaderNodeEmission');links.new(shade.outputs[0],emission.inputs['Color']);links.new(emission.outputs[0],output.inputs['Surface'])
        return mat

    steel=material('brushed stainless steel','AEB8B4')
    chrome=material('polished edge trim','D2D8CC')
    green=material('painted customer panels','596D61')
    rubber=material('rubber and black bakelite','3D4443')
    wood=material('walnut side cheeks','8A6950')
    brass=material('group head brass','B9A16E')
    white=material('porcelain and gauge enamel','E2DFCD')
    dark=material('recessed grille shadows','59615B')
    led=material('quiet green indicator','9DAE8E')
    glass=material('hopper glazing','BACCC3')
    bean=material('roasted coffee beans','625344')
    root=None

    def mesh(name, vertices, faces, mat, edge=0):
        data=bpy.data.meshes.new(name);data.from_pydata(vertices,[],faces);data.update()
        obj=bpy.data.objects.new('Coffee equipment · '+name,data);collection.objects.link(obj)
        obj.parent=root;data.materials.append(mat)
        if edge:
            mod=obj.modifiers.new('Small manufactured edge','BEVEL');mod.width=edge;mod.segments=2
        return obj

    def box(name, position, size, mat, edge=.002):
        x,y,z=[v/2 for v in size]
        vertices=[(-x,-y,-z),(-x,-y,z),(-x,y,-z),(-x,y,z),(x,-y,-z),(x,-y,z),(x,y,-z),(x,y,z)]
        obj=mesh(name,vertices,[(2,6,4,0),(5,7,3,1),(4,5,1,0),(3,7,6,2),(1,3,2,0),(6,7,5,4)],mat,edge)
        obj.location=position
        return obj

    def cylinder(name, position, radius, depth, mat, count=24, top_radius=None):
        top=radius if top_radius is None else top_radius
        vertices=[(r*math.cos(i*math.tau/count),r*math.sin(i*math.tau/count),z) for r,z in [(radius,-depth/2),(top,depth/2)] for i in range(count)]
        faces=[tuple(reversed(range(count))),tuple(range(count,count*2))]
        faces.extend((i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count))
        obj=mesh(name,vertices,faces,mat,.0008);obj.location=position
        return obj

    def rod(name,start,end,radius,mat,count=12):
        start,end=Vector(start),Vector(end)
        obj=cylinder(name,(start+end)/2,radius,(end-start).length,mat,count)
        obj.rotation_euler=(end-start).to_track_quat('Z','Y').to_euler()
        return obj

    def curve(name,points,radius,mat):
        data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.resolution_u=8;data.bevel_depth=radius;data.bevel_resolution=1
        spline=data.splines.new('BEZIER');spline.bezier_points.add(len(points)-1)
        for point,position in zip(spline.bezier_points,points):point.co=position;point.handle_left_type=point.handle_right_type='AUTO'
        obj=bpy.data.objects.new('Coffee equipment · '+name,data);collection.objects.link(obj);obj.parent=root;data.materials.append(mat)
        return obj

    def cup(name,x,y,z):
        count=24
        rings=[(.027,z),(.038,z+.066),(.033,z+.066),(.023,z+.008)]
        vertices=[(x+r*math.cos(i*math.tau/count),y+r*math.sin(i*math.tau/count),level) for r,level in rings for i in range(count)]
        faces=[]
        for ring in range(3):
            faces.extend((ring*count+i,ring*count+(i+1)%count,(ring+1)*count+(i+1)%count,(ring+1)*count+i) for i in range(count))
        faces.extend([tuple(reversed(range(count))),tuple(range(count*3,count*4))])
        mesh(name+' hollow porcelain',vertices,faces,white)
        curve(name+' loop handle',[(x+.033,y,z+.052),(x+.061,y,z+.05),(x+.061,y,z+.023),(x+.031,y,z+.02)],.005,white)

    root=bpy.data.objects.new('Coffee equipment · two-group espresso machine',None);collection.objects.link(root)
    root.location=(-2.82,16.62,1.085)
    root['operatingSide']='+Y, behind the counter';root['customerSide']='-Y, towards the café entrance'
    # A profiled boiler case leaves a genuine recess below the operator fascia.
    profile=[(-.235,.065),(.14,.065),(.14,.285),(.25,.285),(.25,.445),(.18,.49),(-.17,.49),(-.235,.405)]
    vertices=[(x,y,z) for x in [-.43,.43] for y,z in profile]
    count=len(profile);faces=[tuple(reversed(range(count))),tuple(range(count,count*2))]
    faces.extend((i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count))
    shell=mesh('espresso profiled boiler case',vertices,faces,steel,.007)
    normals=bmesh.new();normals.from_mesh(shell.data);bmesh.ops.recalc_face_normals(normals,faces=list(normals.faces));normals.to_mesh(shell.data);normals.free()
    for x in [-.34,.34]:
        for y in [-.16,.17]:cylinder('espresso rubber foot',(x,y,.017),.024,.034,rubber,16)
    box('espresso lower stainless plinth',(0,-.015,.049),(.88,.49,.035),chrome,.004)
    # Customer sees a finished back with ventilation, fasteners and an oval badge.
    box('espresso customer rear panel',(0,-.243,.267),(.81,.012,.285),green,.004)
    box('espresso customer upper trim',(0,-.248,.425),(.84,.016,.022),chrome)
    box('espresso customer lower vent recess',(0,-.253,.163),(.62,.008,.062),dark)
    for i in range(13):box('espresso rear ventilation slot',(-.282+i*.047,-.259,.163),(.023,.005,.04),rubber,.0005)
    badge=cylinder('espresso customer oval badge',(0,-.257,.309),.046,.008,chrome,32);badge.rotation_euler.x=math.pi/2;badge.scale.x=1.65;badge.scale.y=.55
    for x in [-.37,.37]:
        for z in [.145,.38]:
            screw=cylinder('espresso rear panel screw',(x,-.254,z),.006,.004,chrome,12);screw.rotation_euler.x=math.pi/2
            box('espresso screw head slot',(x,-.257,z),(.007,.002,.0015),dark,0)
    for x in [-.438,.438]:
        box('espresso walnut end cheek',(x,-.006,.255),(.013,.405,.352),wood,.007)
        for y in [-.16,.15]:
            screw=cylinder('espresso side cheek fastener',(x+(-.009 if x<0 else .009),y,.275),.007,.004,chrome,12);screw.rotation_euler.y=math.pi/2
    # All controls, group heads and dispensing hardware face the staff aisle (+Y).
    box('espresso operator control fascia',(0,.256,.397),(.81,.012,.115),rubber,.002)
    for x in [-.195,.195]:
        box('espresso operator brew switch surround',(x,.265,.41),(.15,.006,.061),steel,.002)
        for dx in [-.048,-.016,.016,.048]:
            button=cylinder('espresso operator brew pushbutton',(x+dx,.271,.412),.008,.006,white,16);button.rotation_euler.x=math.pi/2
        box('espresso operator status light',(x,.271,.39),(.018,.006,.005),led,.0005)
        cylinder('espresso group brass collar',(x,.23,.292),.061,.042,brass,24)
        cylinder('espresso group chrome head',(x,.25,.259),.055,.031,chrome,24)
        cylinder('espresso portafilter basket',(x,.26,.231),.043,.026,steel,24,top_radius=.052)
        rod('espresso portafilter neck',(x,.278,.242),(x+.025,.345,.242),.012,chrome)
        rod('espresso operator portafilter handle',(x+.025,.345,.242),(x+.04,.458,.235),.016,rubber)
        for dx in [-.019,.019]:curve('espresso twin brew spout',[(x+dx,.26,.219),(x+dx,.27,.208),(x+dx,.282,.205)],.005,chrome)
    gauge=cylinder('espresso operator pressure gauge bezel',(0,.269,.406),.043,.012,chrome,32);gauge.rotation_euler.x=math.pi/2
    face=cylinder('espresso operator pressure gauge enamel',(0,.277,.406),.036,.004,white,32);face.rotation_euler.x=math.pi/2
    for i in range(9):
        angle=math.radians(-125+i*31.25)
        rod('espresso gauge graduation',(math.sin(angle)*.027,.281,.406+math.cos(angle)*.027),(math.sin(angle)*.032,.281,.406+math.cos(angle)*.032),.0012,dark,6)
    rod('espresso pressure gauge needle',(0,.282,.406),(.019,.282,.42),.0015,rubber,6)
    for x in [-.363,.363]:
        knob=cylinder('espresso operator steam valve',(x,.273,.399),.025,.027,rubber,20);knob.rotation_euler.x=math.pi/2
        ring=cylinder('espresso operator steam valve chrome collar',(x,.257,.399),.029,.009,chrome,24);ring.rotation_euler.x=math.pi/2
        box('espresso steam valve marker',(x,.29,.411),(.003,.003,.012),white,.0005)
        curve('espresso articulated steam wand',[(x,.248,.34),(x,.303,.32),(x,.361,.2),(x+.018,.365,.133)],.006,chrome)
        rod('espresso steam wand insulated grip',(x,.317,.287),(x,.337,.247),.01,rubber)
        cylinder('espresso steam tip',(x+.018,.365,.128),.009,.019,steel,12)
    # An inset grate sits above a real dark catch basin, not intersecting faces.
    box('espresso operator drip tray basin',(0,.297,.05),(.81,.305,.036),rubber,.004)
    box('espresso drip tray rim front',(0,.451,.075),(.82,.015,.03),chrome)
    for x in [-.404,.404]:box('espresso drip tray rim end',(x,.302,.075),(.012,.296,.03),chrome)
    for i in range(25):box('espresso drip tray grate bar',(-.372+i*.031,.303,.074),(.012,.275,.012),steel,.0006)
    for x in [-.195,.195]:cup('espresso serving cup',x,.305,.082)
    # Warming deck and restrained steel cup rail, with genuinely hollow empty cups.
    box('espresso cup warming deck',(0,-.014,.495),(.77,.35,.015),chrome,.002)
    for x in [-.37,.37]:
        for y in [-.17,.12]:rod('espresso warming rail stanchion',(x,y,.507),(x,y,.557),.004,chrome,8)
        rod('espresso warming side rail',(x,-.17,.557),(x,.12,.557),.004,chrome,8)
    rod('espresso warming rear rail',(-.37,-.17,.557),(.37,-.17,.557),.004,chrome,8)
    for x in [-.22,0,.22]:cup('espresso warming cup',x,-.035,.508)

    for x in [-3.51,-2.04]:
        root=bpy.data.objects.new('Coffee equipment · burr grinder',None);collection.objects.link(root);root.location=(x,16.62,1.085)
        root['operatingSide']='+Y, behind the counter'
        box('grinder weighted base',(0,.015,.025),(.215,.29,.05),rubber,.006)
        box('grinder base stainless edge',(0,.025,.051),(.205,.265,.012),chrome,.002)
        box('grinder motor housing',(0,-.025,.192),(.18,.205,.275),green,.009)
        box('grinder customer rear inset',(0,-.131,.19),(.14,.008,.17),rubber,.002)
        for z in [.15,.18,.21,.24]:box('grinder rear cooling louvre',(0,-.137,z),(.11,.004,.008),steel,.0007)
        box('grinder operator display bezel',(0,.083,.265),(.12,.012,.062),rubber,.002)
        box('grinder operator display',(0,.091,.269),(.083,.004,.027),dark,.0008)
        for dx in [-.026,-.009,.009,.026]:box('grinder display indicator',(dx,.094,.269),(.009,.002,.013),led,.0005)
        button=cylinder('grinder operator dose button',(.057,.094,.224),.011,.008,chrome,16);button.rotation_euler.x=math.pi/2
        curve('grinder operator dosing chute',[(0,.071,.225),(0,.131,.215),(0,.167,.18)],.019,steel)
        box('grinder dosing chute dark outlet',(0,.167,.171),(.03,.032,.012),rubber,.001)
        for dx in [-.038,.038]:rod('grinder operator portafilter fork',(dx,.08,.121),(dx,.224,.121),.006,chrome)
        box('grinder grounds catch tray',(0,.154,.064),(.14,.146,.014),steel,.002)
        cylinder('grinder burr adjustment collar',(0,-.025,.343),.101,.034,rubber,32)
        for i in range(16):
            angle=i*math.tau/16
            rod('grinder collar setting tick',(.09*math.cos(angle),-.025+.09*math.sin(angle),.361),(.099*math.cos(angle),-.025+.099*math.sin(angle),.361),.0015,chrome,6)
        cylinder('grinder hopper throat',(0,-.025,.389),.048,.06,rubber,24)
        cylinder('grinder transparent bean hopper',(0,-.025,.514),.065,.235,glass,32,top_radius=.111)
        cylinder('grinder coffee bean fill',(0,-.025,.479),.062,.15,bean,24,top_radius=.088)
        for i in range(23):
            angle=i*2.4;radius=.074*math.sqrt(i/23)
            bean_obj=cylinder('grinder visible coffee bean',(math.cos(angle)*radius,-.025+math.sin(angle)*radius,.557),.008,.01,bean,8)
            bean_obj.scale.x=1.5;bean_obj.rotation_euler.y=.4
        cylinder('grinder hopper lid',(0,-.025,.642),.116,.019,rubber,32)
        cylinder('grinder lid grip',(0,-.025,.659),.019,.018,chrome,16)

    for name,position,target in [
        ('Coffee equipment customer view',(-1.5,14.95,1.78),(-2.75,16.62,1.4)),
        ('Coffee equipment operator view',(-1.5,17.85,1.93),(-2.75,16.62,1.4)),
    ]:
        camera=scene.objects.get(name)
        if camera is None:
            camera=bpy.data.objects.new(name,bpy.data.cameras.new(name));camera_collection.objects.link(camera)
        camera.location=position;camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=40
    bpy.context.view_layer.update()

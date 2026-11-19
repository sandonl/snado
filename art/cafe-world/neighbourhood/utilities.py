"""Terminate retained workshop power wires on actual poles, visible from all sides."""
import bpy
import math

def install_utilities(scene,street):
    concrete=next(mat for mat in bpy.data.materials if mat.name=='Café · old concrete')
    iron=next(mat for mat in bpy.data.materials if 'Neighbourhood iron' in mat.name)
    porcelain=next(mat for mat in bpy.data.materials if mat.name=='Café · porcelain')
    def pole_part(name,x,y,bottom,height,radius,mat):
        count=12
        vertices=[(x+radius*math.cos(i*math.tau/count),y+radius*math.sin(i*math.tau/count),z) for z in [bottom,bottom+height] for i in range(count)]
        faces=[tuple(reversed(range(count))),tuple(range(count,count*2))]
        faces.extend((i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count))
        mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.materials.append(mat)
        obj=bpy.data.objects.new(name,mesh);street.objects.link(obj)
        return obj
    for x,height in [(-12.3,9.5),(12.6,8.1)]:
        pole_part('Street wire terminal pole',x,13.85,0,height+.08,.085,concrete)
        for i in range(5):
            y=13.85+(i-2)*.11
            pole_part('Street wire terminal insulator',x,y,height-.12,.12,.027,porcelain)
        # Crossarm is a rotated cylindrical steel member, with complete end caps.
        arm=pole_part('Street wire terminal crossarm',0,0,-.4,.8,.027,iron)
        arm.rotation_euler.x=math.pi/2;arm.location=(x,13.85,height-.14)
    upper=sorted((obj for obj in scene.objects if 'Sagging overhead power cable' in obj.name),key=lambda obj:obj.name)
    lower=sorted((obj for obj in scene.objects if 'Layered lower service wires' in obj.name),key=lambda obj:obj.name)
    for index,obj in enumerate(upper):
        obj.data=obj.data.copy()
        for spline in obj.data.splines:
            spline.bezier_points[0].co.x=-12.3
            spline.bezier_points[-1].co.x=12.6
    for index,obj in enumerate(lower):
        obj.data=obj.data.copy()
        # Existing objects carry the source study's +14m placement transform.
        inverse=obj.matrix_world.inverted()
        from mathutils import Vector
        for spline in obj.data.splines:
            spline.bezier_points[0].co=inverse@Vector((-12.3,13.75+index*.1,6.6))
            spline.bezier_points[-1].co=inverse@Vector((12.6,13.75+index*.1,7.4))

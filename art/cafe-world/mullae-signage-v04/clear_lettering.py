"""Give street lettering clear, physically appropriate backing surfaces.

Run against the saved v04 scene. Positions are absolute so this pass can be
reapplied. Keeps signs on their original boards and window decals inside panes.
"""
import bpy
import math
import json
from pathlib import Path
from mathutils import Vector

folder=Path(__file__).resolve().parent
scene=bpy.context.scene
source=(folder/'style_signage.py').read_text()
exec(source[source.index('def fit_sign('):source.index('sign_frames=[')],globals())

frames=[
    ('Weathered long warehouse fascia retained workshop lettering',(-.27,-1.289,3.59),1.5,.5),
    ('Teumsae English wordmark',(1.51,-1.29,3.72),2.05,.13),
    ('Teumsae handwritten signature',(1.55,-1.29,3.49),2.1,.1),
    ('Rest stamp character',(-1.65,-1.304,3.59),.24,.24),
    ('Ghost of original workshop name',(-3.92,-1.29,3.75),.64,.09),
    ('Ghost of original workshop trade',(-3.92,-1.29,3.59),.64,.065),
    ('Window handwritten welcome',(3.92,-1.108,2.46),.45,.4),
    ('Window slow coffee note',(.02,-1.108,2.55),.54,.28),
    ('Window small lower inscription',(2.83,-1.125,.64),1.4,.055),
    ('Rear building old Hangul',(.96,4.19,7.31),.43,2.72),
]
scene.objects['Window slow coffee note'].data.body='good coffee,\nno hurry.'
scene.objects['Rear building old Hangul'].data.space_line=1.35
for name,centre,width,height in frames:
    fit_sign(scene.objects[name],centre,width,height)

ring=scene.objects['Red rest stamp ring']
for index,point in enumerate(ring.data.splines[0].bezier_points):
    angle=index*math.tau/12
    point.co=(-1.65+math.cos(angle)*.17,-1.293,3.59+math.sin(angle)*.17)
    point.handle_left_type=point.handle_right_type='AUTO'
underline=scene.objects['Teumsae loose painted underline']
for point,position in zip(underline.data.splines[0].bezier_points,[(.58,-1.297,3.37),(1.28,-1.297,3.34),(2.3,-1.297,3.37)]):
    point.co=position
    point.handle_left_type=point.handle_right_type='AUTO'

# Keep chipped paint around the lettering, with a quiet area directly under ink.
depsgraph=bpy.context.evaluated_depsgraph_get()
def bounds(obj):
    mesh=bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph),depsgraph=depsgraph)
    points=[obj.matrix_world@vertex.co for vertex in mesh.vertices]
    bpy.data.meshes.remove(mesh)
    return (min(p.x for p in points),max(p.x for p in points),min(p.z for p in points),max(p.z for p in points))

reserved=[]
for name in ['Weathered long warehouse fascia retained workshop lettering','Teumsae English wordmark','Teumsae handwritten signature','Ghost of original workshop name','Ghost of original workshop trade','Rest stamp character']:
    left,right,bottom,top=bounds(scene.objects[name])
    reserved.append((left-.05,right+.05,bottom-.035,top+.035))
hidden=[]
for obj in list(scene.objects):
    if not obj.name.startswith('Irregular age on fascia boards'):
        continue
    # Temporarily enable a previously hidden patch so reruns use the same geometry.
    obj.hide_viewport=False
    bpy.context.view_layer.update()
    left,right,bottom,top=bounds(obj)
    overlaps=any(left<r and right>l and bottom<t and top>b for l,r,b,t in reserved)
    obj.hide_render=overlaps
    obj.hide_viewport=overlaps
    if overlaps:hidden.append(obj.name)

# The entrance plant sat directly in front of two lines on the small menu board.
plant_objects=[obj for obj in scene.objects if obj.name.startswith('Modest entrance plant') and obj.matrix_world.translation.x<0]
pot=scene.objects['Modest entrance plant clay pot']
shift=-1.97-pot.location.x
for obj in plant_objects:obj.location.x+=shift

bpy.context.view_layer.update()
audit_namespace={'__name__':'audit'}
audit_path=folder/'audit_lettering.py'
exec(compile(audit_path.read_text(),str(audit_path),'exec'),audit_namespace)
report=audit_namespace['audit_lettering'](scene)
report['passed']=not any(report[key] for key in ['cameraBlockedSamples','surfaceBlockedSamples','wrongBackingSamples'])
(folder/'lettering-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
if not report['passed']:
    raise RuntimeError('Street lettering still overlaps geometry; inspect lettering-audit.json before saving.')
manifest_path=folder/'signage-manifest.json'
if manifest_path.is_file():
    manifest=json.loads(manifest_path.read_text())
    manifest['copy']=[{'name':obj.name,'text':obj.data.body} for obj in scene.objects if obj.type=='FONT']
    manifest['geometryValidation']='lettering-audit.json'
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
scene['letteringClearance']='Lettering fitted below roof trim, inside individual glass panes; paint chips kept clear of ink; menu plant moved aside.'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath,compress=True)
result={'hiddenOverlappingPaintPatches':len(hidden),'audit':{key:value for key,value in report.items() if key!='rows'},'remaining':[row for row in report['rows'] if row['cameraBlocked'] or row['surfaceBlocked'] or row['wrongBackingSamples']]}

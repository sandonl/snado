"""Export an approved art scene as a compact GLB for the playable prototype.

Blender --background source.blend --python export_runtime.py -- neighbourhood
Runs in an isolated background process; never saves over the editable source.
"""
import bpy
import sys
import json
from pathlib import Path

asset_name=sys.argv[sys.argv.index('--')+1]
if asset_name not in {'melbourne','seoul','neighbourhood'}:raise ValueError('Unknown scene')
folder=Path(__file__).resolve().parents[2]/'public'/'models'
folder.mkdir(parents=True,exist_ok=True)
source=bpy.context.scene
if source.name=='Scene':
    source=next(s for s in bpy.data.scenes if s.name.startswith('Sandon ·'))
bpy.context.window.scene=source
sources=[]
seen=set()
for collection in list(source.collection.children)[:3]:
    for obj in collection.objects:
        if obj.name in seen or obj.hide_render or obj.hide_viewport or obj.name.startswith('Preview resident · '):continue
        seen.add(obj.name)
        if obj.type not in {'MESH','CURVE','FONT'} or obj.name=='Continuous old street':continue
        if obj.type=='CURVE':
            obj.data.resolution_u=min(obj.data.resolution_u,4)
            obj.data.bevel_resolution=0
        sources.append((collection.name,obj))
bpy.context.view_layer.update()
depsgraph=bpy.context.evaluated_depsgraph_get()
runtime=bpy.data.scenes.new(asset_name+' · browser export')
runtime.unit_settings.system='METRIC'
material_cache={}
runtime_groups={}
for group_name,original in sources:
    mesh=bpy.data.meshes.new_from_object(original.evaluated_get(depsgraph),depsgraph=depsgraph)
    if not mesh or not len(mesh.vertices):continue
    for index,original_mat in enumerate(list(mesh.materials)):
        if original_mat is None:continue
        is_text=original.type=='FONT'
        key=(original_mat.name,is_text)
        if key not in material_cache:
            prefix='text/' if is_text else ('glass/' if any(label in original_mat.name for label in ['small old glass panes','hopper glazing']) else 'surface/')
            mat=bpy.data.materials.new(prefix+original_mat.name)
            mat.diffuse_color=original_mat.diffuse_color
            mat.use_nodes=True
            shader=mat.node_tree.nodes.get('Principled BSDF')
            shader.inputs['Base Color'].default_value=original_mat.diffuse_color
            shader.inputs['Roughness'].default_value=1
            material_cache[key]=mat
        mesh.materials[index]=material_cache[key]
    obj=bpy.data.objects.new(original.name,mesh)
    runtime.collection.objects.link(obj)
    obj.matrix_world=original.matrix_world.copy()
    runtime_groups.setdefault(group_name+('/lettering' if original.type=='FONT' else '/surfaces'),[]).append(obj)
bpy.context.window.scene=runtime
for group_name,objects in runtime_groups.items():
    for obj in bpy.context.selected_objects:obj.select_set(False)
    for obj in objects:obj.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.object.join()
    objects[0].name=asset_name+'/'+group_name
    objects[0]['cameraCollision']=group_name.startswith(('01','02'))
bpy.ops.export_scene.gltf(filepath=str(folder/(asset_name+'.glb')),export_format='GLB',use_active_scene=True,export_apply=True,export_extras=True,export_animations=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
for obj in runtime.objects:
    if obj.type=='MESH':obj.data.calc_loop_triangles()
report={'asset':asset_name,'bytes':(folder/(asset_name+'.glb')).stat().st_size,'meshes':len([obj for obj in runtime.objects if obj.type=='MESH']),'materials':len(material_cache),'triangles':sum(len(obj.data.loop_triangles) for obj in runtime.objects if obj.type=='MESH')}
(folder/(asset_name+'-export.json')).write_text(json.dumps(report,indent=2))
print('WORLD_ASSET_EXPORTED '+json.dumps(report),flush=True)

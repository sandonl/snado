"""Make a compact GLB from the editable source, then render the three art-review views.

Run: Blender --background melbourne-seoul-cafes.blend --python export_and_render.py
The render rig stays in the Blender source and is deliberately omitted from the GLB.
"""
import bpy
import json
import sys
from pathlib import Path
from mathutils import Matrix

output = Path(__file__).resolve().parent
source = next(scene for scene in bpy.data.scenes if scene.name.startswith('Sandon ·'))
bpy.context.window.scene = source
for font in bpy.data.fonts:
    if Path(font.filepath).is_file() and hasattr(font, 'pack'):
        font.pack()

depsgraph = bpy.context.evaluated_depsgraph_get()
runtime = bpy.data.scenes.new('Cafés · runtime export')
runtime.unit_settings.system = 'METRIC'
runtime.unit_settings.scale_length = 1
report = {'units': 'metres', 'upAxis': 'Y', 'status': 'Art prototype; not integrated into the portfolio yet.', 'regions': []}
regions = []
for source_collection in list(source.collection.children)[:3]:
    region = bpy.data.collections.new(source_collection.name + ' · runtime')
    runtime.collection.children.link(region)
    root = bpy.data.objects.new(source_collection.name, None)
    region.objects.link(root)
    root.location = (-4.6, 1.2, .3) if source_collection.name.startswith('01') else ((4.4, .9, .3) if source_collection.name.startswith('02') else (0,0,0))
    regions.append((region,root))
    region_objects = []
    for original in source_collection.objects:
        if original.type == 'EMPTY':
            obj = original.copy()
            region.objects.link(obj)
            obj.parent = root
            obj.matrix_basis = Matrix.Translation(-root.location) @ original.matrix_world
        elif original.type in {'MESH','CURVE','FONT'}:
            evaluated = original.evaluated_get(depsgraph)
            mesh = bpy.data.meshes.new_from_object(evaluated, depsgraph=depsgraph)
            if mesh is None or len(mesh.vertices) == 0:
                continue
            obj = bpy.data.objects.new(original.name, mesh)
            region.objects.link(obj)
            obj.parent = root
            obj.matrix_basis = Matrix.Translation(-root.location) @ original.matrix_world
            region_objects.append(obj)
    # One static mesh per region, with a primitive per shared material.
    bpy.context.window.scene = runtime
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    for obj in region_objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = region_objects[0]
    bpy.ops.object.join()
    merged = region_objects[0]
    merged.name = source_collection.name + ' · static mesh'
    merged.data.calc_loop_triangles()
    report['regions'].append({'name':source_collection.name, 'triangles':len(merged.data.loop_triangles), 'vertices':len(merged.data.vertices), 'materials':len(set(merged.data.materials))})
    bpy.context.window.scene = source

bpy.context.window.scene = runtime
bpy.ops.export_scene.gltf(filepath=str(output/'melbourne-seoul-cafes.glb'),export_format='GLB',use_active_scene=True,export_apply=True,export_extras=True,export_animations=False,export_cameras=False,export_lights=False)
for index, filename in [(0, 'melbourne-cafe.glb'), (1, 'seoul-cafe.glb')]:
    region, root = regions[index]
    position = root.location.copy()
    root.location = (0,0,0)
    bpy.ops.export_scene.gltf(filepath=str(output/filename),export_format='GLB',collection=region.name,export_apply=True,export_extras=True,export_animations=False)
    root.location = position
bpy.context.window.scene = source
report['glbBytes'] = (output/'melbourne-seoul-cafes.glb').stat().st_size
(output/'asset-report.json').write_text(json.dumps(report,indent=2))
for other_scene in list(bpy.data.scenes):
    if other_scene != source:
        bpy.data.scenes.remove(other_scene)
# Save a normal standalone file, so opening it shows the café scene immediately.
bpy.ops.wm.save_as_mainfile(filepath=str(output/'melbourne-seoul-cafes.blend'),compress=True)

if '--export-only' in sys.argv:
    print('CAFE_EXPORT_COMPLETE ' + json.dumps(report), flush=True)
    raise SystemExit(0)

for camera_name, filename, width, height, samples in [
    ('Camera · both worlds', 'both-worlds.png', 1720, 1220, 40),
    ('Camera · Melbourne', 'melbourne-cafe.png', 1200, 1200, 40),
    ('Camera · Seoul', 'seoul-cafe.png', 1200, 1200, 40),
]:
    source.camera = source.objects[camera_name]
    source.render.resolution_x = width
    source.render.resolution_y = height
    source.cycles.samples = samples
    source.render.filepath = str(output/'previews'/filename)
    bpy.ops.render.render(write_still=True)
    print('CAFE_PREVIEW_SAVED ' + filename, flush=True)

print('CAFE_STUDY_COMPLETE ' + json.dumps(report), flush=True)

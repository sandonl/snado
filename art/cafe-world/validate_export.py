"""Re-import the GLB and check geometry placement against the editable source.

Use actual evaluated vertices: transformed object bounding boxes overestimate
the extent of rotated signs, cylinders and text and give misleading results.
"""
import bpy
import json
import math
from pathlib import Path

output = Path(__file__).resolve().parent
source = bpy.context.scene

def geometry_bounds(objects, depsgraph):
    minimum = [float('inf')]*3
    maximum = [-float('inf')]*3
    triangles = 0
    for obj in objects:
        if obj.type not in {'MESH','CURVE','FONT'}:
            continue
        mesh = bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph), depsgraph=depsgraph)
        mesh.calc_loop_triangles()
        triangles += len(mesh.loop_triangles)
        for vertex in mesh.vertices:
            point = obj.matrix_world @ vertex.co
            if not all(math.isfinite(value) for value in point):
                raise ValueError('Non-finite geometry in ' + obj.name)
            for axis in range(3):
                minimum[axis] = min(minimum[axis], point[axis])
                maximum[axis] = max(maximum[axis], point[axis])
        bpy.data.meshes.remove(mesh)
    return (minimum, maximum), triangles

bpy.context.view_layer.update()
depsgraph = bpy.context.evaluated_depsgraph_get()
expected = {c.name:geometry_bounds(c.objects, depsgraph) for c in list(source.collection.children)[:3]}
imported = bpy.data.scenes.new('QA import · not saved')
bpy.context.window.scene = imported
bpy.ops.import_scene.gltf(filepath=str(output/'melbourne-seoul-cafes.glb'))
bpy.context.view_layer.update()
depsgraph = bpy.context.evaluated_depsgraph_get()
regions = []
for name, (source_bounds, source_triangles) in expected.items():
    objects = [obj for obj in imported.objects if obj.type == 'MESH' and obj.name.startswith(name)]
    imported_bounds, imported_triangles = geometry_bounds(objects, depsgraph)
    error = max(abs(a-b) for side_a,side_b in zip(source_bounds,imported_bounds) for a,b in zip(side_a,side_b))
    regions.append({'name':name,'sourceTriangles':source_triangles,'importedTriangles':imported_triangles,'maximumPositionErrorMetres':error,'passed':error<.0001 and source_triangles==imported_triangles})
anchors = [obj for obj in imported.objects if obj.get('role') == 'discovery-anchor']
result = {'passed':all(region['passed'] for region in regions) and len(anchors)==2,'regions':regions,'discoveryAnchors':len(anchors),'importedMeshes':sum(obj.type=='MESH' for obj in imported.objects),'scope':'GLB re-import and geometry validation in Blender. Not a browser performance or gameplay test.'}
(output/'asset-validation.json').write_text(json.dumps(result,indent=2))
print('CAFE_VALIDATION ' + json.dumps(result), flush=True)
if not result['passed']:
    raise RuntimeError('Export differs from source; inspect asset-validation.json')

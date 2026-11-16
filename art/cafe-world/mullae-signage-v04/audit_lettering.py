"""Check actual glyph geometry for occlusion in the saved Blender scene.

Camera rays catch roof/trim overlaps. Short rays along a label's front normal
catch local decorations or backing surfaces crossing the ink. This audits real
evaluated geometry rather than checking the coordinates assigned by the builder.
Run in Blender; writes lettering-audit.json beside the source.
"""
import bpy
import json
from pathlib import Path
from mathutils import Vector

def audit_lettering(scene):
    bpy.context.view_layer.update()
    depsgraph=bpy.context.evaluated_depsgraph_get()
    rows=[]
    fascia_labels={'Weathered long warehouse fascia retained workshop lettering','Teumsae English wordmark','Teumsae handwritten signature','Ghost of original workshop name','Ghost of original workshop trade'}
    for obj in scene.objects:
        if obj.type!='FONT' or obj.hide_render:
            continue
        mesh=bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph),depsgraph=depsgraph)
        mesh.calc_loop_triangles()
        # Only sample fronts of glyphs, not side/back faces of extruded letters.
        front=[triangle for triangle in mesh.loop_triangles if triangle.normal.z>.8]
        step=max(1,len(front)//100)
        points=[]
        for triangle in front[::step]:
            vertices=[mesh.vertices[index].co for index in triangle.vertices]
            centre=sum(vertices,Vector())/3
            points.append(obj.matrix_world @ centre)
            points.extend(obj.matrix_world @ (vertex*.95+centre*.05) for vertex in vertices)
        normal=(obj.matrix_world.to_3x3() @ Vector((0,0,1))).normalized()
        counts={'camera':{},'surface':{},'wrongBacking':{}}
        for point in points:
            for mode,origin in [('camera',scene.camera.matrix_world.translation),('surface',point+normal*.3)]:
                offset=point-origin
                hit,location,hit_normal,index,blocker,matrix=scene.ray_cast(depsgraph,origin,offset.normalized(),distance=offset.length-.002)
                if hit and blocker!=obj:
                    counts[mode][blocker.name]=counts[mode].get(blocker.name,0)+1
            if obj.name in fascia_labels:
                # Painted lettering must sit over the wooden fascia, not float over
                # roof trim just because it happens to be visible to one camera.
                hit,location,hit_normal,index,backing,matrix=scene.ray_cast(depsgraph,point-normal*.003,-normal,distance=.15)
                if hit and not backing.name.startswith(('Weathered long warehouse fascia','Irregular age on fascia boards')):
                    counts['wrongBacking'][backing.name]=counts['wrongBacking'].get(backing.name,0)+1
        rows.append({'name':obj.name,'samples':len(points),'cameraBlocked':sum(counts['camera'].values()),'surfaceBlocked':sum(counts['surface'].values()),'wrongBackingSamples':sum(counts['wrongBacking'].values()),'blockers':counts})
        bpy.data.meshes.remove(mesh)
    return {'camera':scene.camera.name,'textObjects':len(rows),'cameraBlockedSamples':sum(row['cameraBlocked'] for row in rows),'surfaceBlockedSamples':sum(row['surfaceBlocked'] for row in rows),'wrongBackingSamples':sum(row['wrongBackingSamples'] for row in rows),'rows':rows}

if __name__=='__main__':
    result=audit_lettering(bpy.context.scene)
    folder=Path(__file__).resolve().parent
    (folder/'lettering-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print('LETTERING_AUDIT '+json.dumps({key:value for key,value in result.items() if key!='rows'}))
    for row in result['rows']:
        if row['cameraBlocked'] or row['surfaceBlocked'] or row['wrongBackingSamples']:
            print(json.dumps(row,ensure_ascii=False))

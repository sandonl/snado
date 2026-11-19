"""Probe the saved world for open routes and closed exterior surfaces."""
import bpy
import json
from pathlib import Path
from mathutils import Vector

scene=bpy.context.scene
bpy.context.view_layer.update()
depsgraph=bpy.context.evaluated_depsgraph_get()
probes=[]
assert not any('mullae' in obj.data.body.lower() or '문래' in obj.data.body
               for obj in scene.objects if obj.type=='FONT'), 'A visible sign uses the reference place name.'
def probe(name,origin,direction,distance,expected_hit,expected_name=None,expected_normal_y=None):
    hit,location,normal,index,obj,matrix=scene.ray_cast(depsgraph,Vector(origin),Vector(direction),distance=distance)
    correct_name=expected_name is None or (hit and expected_name in obj.name)
    correct_normal=expected_normal_y is None or (hit and normal.y*expected_normal_y>.9)
    row={'name':name,'passed':hit==expected_hit and correct_name and correct_normal,'hit':obj.name if hit else None}
    if expected_normal_y is not None:row['normalY']=round(normal.y,3) if hit else None
    probes.append(row)

probe('Arrival lane stays clear at walking height',(0,-8.8,1.4),(0,1,0),16.4,False)
probe('Lane opens into the shared courtyard',(0,7.6,1.4),(0,1,0),4.6,False)
probe('Café bay remains open',(-2.8,12,1.5),(0,1,0),1.35,False)
probe('Café rear eave is enclosed',(3.0,19.2,4.05),(0,-1,0),1.1,True)
probe('Café east window header is enclosed',(5.3,15.4,3.6),(-1,0,0),1.0,True)
probe('Café west eave is enclosed',(-5.0,17.9,3.92),(1,0,0),.8,True)
probe('Workshop rear eave is enclosed',(-7.2,18.2,3.82),(0,-1,0),1,True)
probe('Café roof is closed',(2.8,16.1,6),(0,0,-1),2.3,True)
probe('Fabrication lane opens into the print yard',(0,-.35,1.45),(1,0,0),5.4,False)
probe('Print room display has a window',(4.9,-.81,1.42),(1,0,0),1.15,True,'Print room display')
probe('Restaurant timber shopfront faces the arrival street',(-4.79,-7.4,1.44),(0,1,0),1.7,True,'Corner restaurant street front')
probe('Restaurant windows look into the room',(-4.42,-5.66,1.89),(0,1,0),1.0,False)
probe('Restaurant has an open lane entrance',(-1.1,-2.39,1.5),(-1,0,0),2.6,False)
probe('Market has an open lane entrance',(1.1,-4.58,1.5),(1,0,0),2.6,False)
probe('Studio has an open lane entrance',(-1.1,.31,1.5),(-1,0,0),2.6,False)
probe('Restaurant has a set dining table',(-5.28,-3.87,2.2),(0,0,-1),1.55,True,'Restaurant set plate')
probe('Market has a checkout inside',(5.92,-4.54,2.3),(0,0,-1),1.2,True,'Market till')
probe('Studio has a potter’s wheel',(-5.67,-.62,1.70),(0,0,-1),.80,True,'Studio clay bowl')
probe('Market canvas projects above the footway',(4.45,-6.02,3.2),(0,0,-1),1,True,'Corner market street front striped awning')
probe('Metal cutting shop keeps its roller shutter',(0,5.1,1.3),(-1,0,0),2.25,True,'Metal cutting shop roller shutter')
probe('Arrival street tree is rooted in the footway',(-3.9,-9.05,.7),(0,1,0),1.3,True,'Lane canopy tree trunk')
for name,x,y,z,dx,dy in [
    ('Rear brick block rear',-.4,23.1,4.2,0,-1),
    ('Rear brick block west',-5.3,20.1,4.2,1,0),
    ('Rear brick block east',2.8,20.1,4.2,-1,0),
    ('Side-lane block rear',9.3,22.7,4.7,0,-1),
    ('Side-lane block outer side',12.0,18.7,4.7,-1,0),
    ('Side-lane block inner side',6.6,18.7,4.7,1,0),
    ('Far workshop rear',6,27.0,3.0,0,-1),
]:probe(name,(x,y,z),(dx,dy,0),1.35,True)
probe('Interior entry aisle stays clear',(-2.8,13.25,1.4),(0,1,0),2.35,False)
probe('Full timber bar exists',(-2.5,15.6,.8),(0,1,0),1.3,True,'Interior timber bar')
probe('Quiet seating partition exists',(.75,17.4,.7),(1,0,0),.4,True,'Interior low seating partition')
# Probe the actual working surfaces from the fixed staff and customer aisles.
# Reversing an assembly or putting its controls on the customer side fails here.
probe('Espresso controls face the barista aisle',(-3.015,17.3,1.50),(0,-1,0),1,True,'espresso operator',1)
probe('Espresso finished rear faces customers',(-2.70,15.9,1.38),(0,1,0),1,True,'espresso customer',-1)
for x in [-3.51,-2.04]:
    probe('Grinder controls face the barista aisle',(x+.034,17.3,1.354),(0,-1,0),1,True,'grinder operator display',1)
report={'passed':all(row['passed'] for row in probes),'probeCount':len(probes),'probes':probes,'scope':'Actual saved Blender geometry: lane, print yard and café entrance clear; sampled side/rear surfaces, eave closures and roofs present; coffee equipment operating faces checked from the staff aisle. This does not claim furnished interiors behind closed doors.'}
(Path(__file__).resolve().parent/'geometry-audit.json').write_text(json.dumps(report,indent=2))
print('NEIGHBOURHOOD_GEOMETRY_AUDIT '+json.dumps(report),flush=True)
if not report['passed']:raise RuntimeError('A world route or enclosure probe failed.')

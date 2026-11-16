"""Remove decorative English slogans and align functional lettering to its signs.

Run against the cleared v04 scene. Saves a separate v05; hidden old lettering is
retained as editable history. Uses actual type geometry and the existing art style.
"""
import bpy
import math
import json
from pathlib import Path
from mathutils import Vector

folder=Path(__file__).resolve().parent
scene=bpy.context.scene
if not scene.name.startswith('Sandon · Mullae'):
    raise RuntimeError('Open the Mullae café scene before applying this refinement.')
scene.name='Sandon · Mullae · restrained street lettering · v05'
prior_folder=folder.parent/'mullae-signage-v04'
source=(prior_folder/'style_signage.py').read_text()
exec(source[source.index('def fit_sign('):source.index('sign_frames=[')],globals())

removed=[
    'Teumsae handwritten signature',
    'Teumsae loose painted underline',
    'Window slow coffee note',
    'Window small lower inscription',
    'Teumsae English wordmark',
]
for name in removed:
    obj=scene.objects[name]
    obj.hide_render=True
    obj.hide_viewport=True

plain_font=bpy.data.fonts.load('/System/Library/Fonts/Helvetica.ttc')
english_labels=[
    ('Small café board menu','FILTER · LATTE',(-1.28,-1.638,.29),.055,.43,.045),
    ('Mullae corner plaque English','MULLAE-DONG',(4.47,-1.262,2.74),.05,.55,.045),
]
for name,body,centre,size,width,height in english_labels:
    obj=scene.objects[name]
    obj.data.body=body
    obj.data.font=plain_font
    obj.data.size=size
    obj.data.space_character=1.12 if name=='Teumsae English wordmark' else 1
    obj.scale=(1,1,1)
    # The text's local XY plane follows the sign's XZ face, with no invented tilt.
    obj.rotation_euler=(math.pi/2,0,0)
    fit_sign(obj,centre,width,height)
if not plain_font.packed_file:plain_font.pack()

bpy.context.view_layer.update()
audit_namespace={'__name__':'audit'}
audit_path=prior_folder/'audit_lettering.py'
exec(compile(audit_path.read_text(),str(audit_path),'exec'),audit_namespace)
report=audit_namespace['audit_lettering'](scene)
report['passed']=not any(report[key] for key in ['cameraBlockedSamples','surfaceBlockedSamples','wrongBackingSamples'])
report['englishSurfaceAlignment']=[{'name':name,'normalMatchesFront':(scene.objects[name].matrix_world.to_3x3()@Vector((0,0,1))).normalized().dot(Vector((0,-1,0)))>.99999} for name,*rest in english_labels]
if not report['passed'] or not all(row['normalMatchesFront'] for row in report['englishSurfaceAlignment']):
    raise RuntimeError('Lettering alignment or visibility check failed.')
(folder/'lettering-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
scene['cafeWorkingName']='틈새'
scene['signageDirection']='Korean café name; plain menu and address lettering. No English café wordmark, decorative English slogans or artificial tilt.'
scene.render.filepath=str(folder/'mullae-lettering-v05.png')
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'mullae-lettering-v05.blend'),compress=True)
manifest={'workingName':scene['cafeWorkingName'],'removedFromView':removed,'copy':[{'name':obj.name,'text':obj.data.body} for obj in scene.objects if obj.type=='FONT' and not obj.hide_render],'validation':'lettering-audit.json'}
(folder/'signage-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
result={'file':bpy.data.filepath,'visibleTextObjects':report['textObjects'],'visibilityPassed':report['passed'],'englishAlignment':report['englishSurfaceAlignment']}

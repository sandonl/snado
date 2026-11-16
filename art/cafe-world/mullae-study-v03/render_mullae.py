"""Render the Mullae-dong industrial café style study."""
import bpy
from pathlib import Path
folder=Path(__file__).resolve().parent
scene=next(s for s in bpy.data.scenes if s.name.startswith('Sandon · Mullae'))
bpy.context.window.scene=scene
for other_scene in list(bpy.data.scenes):
    if other_scene!=scene:bpy.data.scenes.remove(other_scene)
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA'
            area.spaces.active.overlay.show_overlays=False
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'mullae-workshop-v03.blend'),compress=True)
scene.render.filepath=str(folder/'mullae-workshop-v03.png')
bpy.ops.render.render(write_still=True)
print('MULLAE_STUDY_RENDER_COMPLETE',flush=True)

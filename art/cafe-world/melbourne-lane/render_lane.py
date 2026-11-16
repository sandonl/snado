import bpy
from pathlib import Path
folder=Path(__file__).resolve().parent
scene=next(value for value in bpy.data.scenes if value.name=='Sandon · Melbourne café lane')
bpy.context.window.scene=scene
for other in list(bpy.data.scenes):
    if other!=scene:bpy.data.scenes.remove(other)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'melbourne-lane.blend'),compress=True)
scene.render.filepath=str(folder/'melbourne-lane.png')
bpy.ops.render.render(write_still=True)
print('MELBOURNE_LANE_RENDER_COMPLETE',flush=True)

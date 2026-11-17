import bpy,json
from pathlib import Path
folder=Path(__file__).resolve().parent
scene=bpy.context.scene
street=next(group for group in scene.collection.children if group.name.startswith('03'))
module=folder/'play_area.py'
exec(compile(module.read_text(),str(module),'exec'),globals())
details=install_play_area(scene,street,folder)
layout_path=folder.parents[2]/'src/world/layout.json'
layout=json.loads(layout_path.read_text());apply_layout(layout,details);layout_path.write_text(json.dumps(layout,indent=2)+'\n')
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'neighbourhood.blend'),compress=True)
print('PUBLIC_PLAY_AREA_UPDATED',flush=True)

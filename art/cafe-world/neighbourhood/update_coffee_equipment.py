"""Refresh equipment in neighbourhood.blend without rebuilding the street.

blender --background art/cafe-world/neighbourhood/neighbourhood.blend \
  --python-exit-code 1 --python art/cafe-world/neighbourhood/update_coffee_equipment.py
"""
import bpy
from pathlib import Path
folder=Path(__file__).resolve().parent
source=folder/'neighbourhood.blend'
if Path(bpy.data.filepath).resolve()!=source.resolve():
    raise ValueError('Open the canonical neighbourhood.blend before updating equipment.')
scene=bpy.context.scene
collection=next(group for group in scene.collection.children if group.name.startswith('02'))
rig=next(group for group in scene.collection.children if group.name.startswith('04'))
module=folder/'coffee_equipment.py'
exec(compile(module.read_text(),str(module),'exec'),globals())
build_coffee_equipment(scene,collection,rig)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(source),compress=True)
audit=folder/'audit_geometry.py'
exec(compile(audit.read_text(),str(audit),'exec'),{'__file__':str(audit),'__name__':'__main__'})
print('COFFEE_EQUIPMENT_UPDATED',flush=True)

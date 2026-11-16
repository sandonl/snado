import bpy
import sys
from pathlib import Path
folder=Path(__file__).resolve().parent
scene=bpy.context.scene
requested=set(sys.argv[sys.argv.index('--')+1:]) if '--' in sys.argv else set()
for name,filename in [('Café interior at eye level','cafe-interior.png'),('Quiet tiled seating','quiet-seating.png'),('Lane into workshop courtyard','lane-courtyard.png'),('Rear building inspection','rear-buildings.png'),('Street and distant scenery','scenery.png'),('Neighbourhood overview','overview.png')]:
    if requested and filename not in requested:continue
    scene.camera=scene.objects[name]
    scene.render.filepath=str(folder/filename)
    bpy.ops.render.render(write_still=True)
    print('NEIGHBOURHOOD_PREVIEW '+filename,flush=True)

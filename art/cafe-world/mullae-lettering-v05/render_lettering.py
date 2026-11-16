"""Render the pared-back lettering pass from the established street camera."""
import bpy
from pathlib import Path
folder=Path(__file__).resolve().parent
bpy.context.scene.render.filepath=str(folder/'mullae-lettering-v05.png')
bpy.ops.render.render(write_still=True)
print('REFINED_LETTERING_RENDER_COMPLETE',flush=True)

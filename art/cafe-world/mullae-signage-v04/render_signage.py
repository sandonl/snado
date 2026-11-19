"""Render the approved architectural view with the new street typography."""
import bpy
from pathlib import Path
folder=Path(__file__).resolve().parent
scene=bpy.context.scene
scene.render.filepath=str(folder/'mullae-signage-v04.png')
bpy.ops.render.render(write_still=True)
print('SIGNAGE_RENDER_COMPLETE',flush=True)

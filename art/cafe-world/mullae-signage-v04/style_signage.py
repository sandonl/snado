"""Add a varied, locally rooted typographic layer to the Mullae workshop study.

Run against the saved v03 Blender scene. Architecture stays shared with the approved
study; v04 is saved separately. All copy is fictional environmental art, not a claim
about a real business. Nanum font sources and SIL OFL notices live in ../fonts.
"""
import bpy
import math
import json
from pathlib import Path

folder=Path(__file__).resolve().parent
scene=bpy.context.scene
if not scene.name.startswith('Sandon · Mullae'):
    raise RuntimeError('Open the Mullae workshop study before applying this pass.')
scene.name='Sandon · Mullae · Teumsae street lettering · v04'
cafe_collection=next(c for c in scene.collection.children if c.name.startswith('01'))
street_collection=next(c for c in scene.collection.children if c.name.startswith('03'))
active_collection=cafe_collection

def existing_material(label):
    return next(mat for mat in bpy.data.materials if mat.name=='Café · '+label or mat.name.startswith('Café · '+label+'.'))

def colour(hex_value):
    rgb=[int(hex_value[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in rgb)

def sign_material(name,hex_value):
    value=existing_material('porcelain').copy()
    value.name='Lettering · '+name
    base=colour(hex_value)
    value.diffuse_color=(*base,1)
    for node in value.node_tree.nodes:
        if node.type=='MIX_RGB':
            node.inputs[1].default_value=(base[0]*.74,base[1]*.77,base[2]*.85,1)
            node.inputs[2].default_value=(*base,1)
        elif node.type=='BSDF_PRINCIPLED':
            node.inputs['Base Color'].default_value=(*base,1)
    return value

ivory=sign_material('warm signwriter cream','E8DDB9')
ink=sign_material('deep petrol lettering','354B49')
faded=sign_material('ghost workshop paint','AAA38A')
stamp_red=sign_material('faded vermilion stamp','AD5D43')
poster_paper=sign_material('old paper','D4C9A6')
tape=sign_material('masking tape','B8B68C')
enamel_blue=sign_material('old blue enamel','4C6671')

# Reuse geometry helpers without rebuilding any architecture.
helper_code=(folder.parent/'build_cafes.py').read_text()
exec(helper_code[helper_code.index('def link_object'):helper_code.index('font = bpy.data.fonts.load')],globals())
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/SignPainter.ttc')
brush_font=bpy.data.fonts.load(str(folder.parent/'fonts'/'NanumBrushScript-Regular.ttf'))
heritage_font=bpy.data.fonts.load(str(folder.parent/'fonts'/'NanumMyeongjo-ExtraBold.ttf'))
serif_font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Baskerville.ttc')
korean_font=brush_font
exec(helper_code[helper_code.index('def text('):helper_code.index('def panel_window(')],globals())

def lettering(name,body,position,size,style='brush',mat=ivory,max_width=None,tilt=0):
    obj=text(name,body,position,size,mat,korean=True)
    obj.data.font={'brush':brush_font,'heritage':heritage_font,'script':font,'serif':serif_font}[style]
    obj.data.space_line=.9
    obj.data.extrude=.0007
    obj.rotation_euler.rotate_axis('Z',math.radians(tilt))
    bpy.context.view_layer.update()
    if max_width and obj.dimensions.x>max_width:
        obj.scale.x*=max_width/obj.dimensions.x
    return obj

def revise(name,body,size,style='brush',mat=ivory,position=None,max_width=None,tracking=1):
    obj=scene.objects[name]
    obj.data.body=body
    obj.data.size=size
    obj.data.font={'brush':brush_font,'heritage':heritage_font,'script':font,'serif':serif_font}[style]
    obj.data.space_character=tracking
    obj.data.space_line=.9
    obj.data.extrude=.0007
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    if position:obj.location=position
    bpy.context.view_layer.update()
    if max_width and obj.dimensions.x>max_width:
        obj.scale.x*=max_width/obj.dimensions.x
    return obj

# Café identity: loose Korean brush lettering, a red rest-stamp, and quiet English type.
revise('Weathered long warehouse fascia retained workshop lettering','틈새',1.13,position=(-.27,-1.289,3.77),max_width=1.5)
lettering('Teumsae English wordmark','T E U M S A E',(1.51,-1.29,3.82),.205,'serif',max_width=2.05)
lettering('Teumsae handwritten signature','between sips & cities',(1.55,-1.29,3.57),.16,'script',max_width=2.1,tilt=-1.4)
curve('Teumsae loose painted underline',[(.58,-1.297,3.47),(1.28,-1.297,3.44),(2.3,-1.297,3.47)],.006,ivory)
stamp=curve('Red rest stamp ring',[(-1.65+math.cos(i*math.tau/12)*.205,-1.293,3.76+math.sin(i*math.tau/12)*.205) for i in range(12)],.011,stamp_red)
stamp.data.splines[0].use_cyclic_u=True
lettering('Rest stamp character','쉼',(-1.65,-1.304,3.76),.39,'brush',stamp_red,max_width=.32,tilt=-8)
revise('Small coffee lettering','한 잔, 천천히',.16,'brush',ink,max_width=1.04)
revise('Coffee corner lightbox','틈\n새',.46,'brush',ink,max_width=.27)

# The old factory names retain their own, heavier typographic voice.
revise('Retained factory sign','형제 철공소',.57,'heritage',ink,max_width=4.13,tracking=.92)
revise('Small old sign subline','작은 수리도 합니다',.145,'brush',ink,position=(-7.1,-1.094,3.19),max_width=2.9)
revise('Rear building old Hangul','대\n성\n정\n밀',.39,'heritage',ink,max_width=.43)
revise('Old side-lane shop Hangul','홍상회',.5,'heritage',ink,max_width=2.65,tracking=1.2)
lettering('Ghost of original workshop name','대성정밀',(-3.77,-1.29,3.94),.16,'heritage',faded,max_width=1.1)
lettering('Ghost of original workshop trade','절삭 · 용접',(-3.77,-1.29,3.74),.095,'heritage',faded,max_width=1)

# Notes at pedestrian scale are friendly, slightly crooked, and placed on actual panes.
lettering('Window handwritten welcome','쉬어\n가요',(3.96,-1.134,2.52),.27,'brush',ivory,max_width=.55,tilt=2)
lettering('Window slow coffee note','good coffee, no hurry.',(.0,-1.134,2.48),.16,'script',ivory,max_width=1.55,tilt=-2)
lettering('Window small lower inscription','HAVE A LITTLE PAUSE',(2.83,-1.125,.43),.075,'serif',ivory,max_width=1.4)

# A handwritten menu replaces generic placeholders on the existing small board.
board=scene.objects['Small café sandwich board']
board.scale.x*=1.35
revise('Small café board coffee','오늘의\n커피',.21,'brush',ink,position=(-1.28,-1.638,.81),max_width=.45)
revise('Small café board hours','한 잔 더?',.14,'brush',stamp_red,position=(-1.28,-1.638,.49),max_width=.43)
revise('Small café board menu','stay a little.',.085,'script',ink,position=(-1.28,-1.638,.29),max_width=.43)

# A taped message on the old steel door feels added by the café owner.
box('Door note paper',(-1.45,-1.164,2.02),(.42,.012,.52),poster_paper,.001)
lettering('Door handwritten invitation','오늘은\n천천히.',(-1.45,-1.177,2.02),.18,'brush',ink,max_width=.35,tilt=-3)
strip=box('Door note masking tape',(-1.45,-1.183,2.29),(.17,.012,.045),tape,.001)
strip.rotation_euler.y=math.radians(-8)

# An enamel corner plate and a coffee-arrow guide someone walking into the side lane.
box('Mullae enamel street plaque',(4.47,-1.238,2.83),(.65,.035,.3),enamel_blue,.003)
lettering('Mullae corner plaque title','문래동',(4.47,-1.262,2.87),.135,'heritage',ivory,max_width=.54)
lettering('Mullae corner plaque English','MULLAE-DONG',(4.47,-1.262,2.74),.05,'serif',ivory,max_width=.55)
lettering('Small hand-painted alley note','골목 안쪽',(4.47,-1.22,2.47),.105,'brush',ivory,max_width=.47)
for points in [[(4.29,-1.226,2.34),(4.63,-1.226,2.34)],[(4.56,-1.226,2.4),(4.63,-1.226,2.34),(4.56,-1.226,2.28)]]:
    curve('Hand-painted coffee arrow',points,.007,ivory)

# Fonts use different baseline metrics. Fit the actual ink, rather than assuming
# the same font size places every typeface inside a physical signboard.
# Mount the workshop sign ahead of the corrugated roof lip, which passes across
# its face at this camera height if the board stays flush against the old wall.
scene.objects['Old neighbouring workshop fascia'].location.y=-1.25
def fit_sign(obj,center,width,height):
    def ink_bounds():
        depsgraph=bpy.context.evaluated_depsgraph_get()
        mesh=bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph),depsgraph=depsgraph)
        points=[obj.matrix_world @ vertex.co for vertex in mesh.vertices]
        bpy.data.meshes.remove(mesh)
        return (min(p.x for p in points),max(p.x for p in points),min(p.z for p in points),max(p.z for p in points))
    bpy.context.view_layer.update()
    left,right,bottom,top=ink_bounds()
    ratio=min(1,width/(right-left),height/(top-bottom))
    obj.scale*=ratio
    bpy.context.view_layer.update()
    left,right,bottom,top=ink_bounds()
    obj.location.x+=center[0]-(left+right)/2
    obj.location.z+=center[2]-(bottom+top)/2
    obj.location.y=center[1]

sign_frames=[
    ('Weathered long warehouse fascia retained workshop lettering',(-.27,-1.289,3.72),1.5,.63),
    ('Teumsae English wordmark',(1.51,-1.29,3.82),2.05,.19),
    ('Teumsae handwritten signature',(1.55,-1.29,3.58),2.1,.12),
    ('Rest stamp character',(-1.65,-1.304,3.76),.29,.29),
    ('Small coffee lettering',(-2.88,-1.34,3.56),1.04,.16),
    ('Coffee corner lightbox',(4.8,-1.15,3.61),.27,.77),
    ('Retained factory sign',(-7.1,-1.36,3.46),4.13,.39),
    ('Small old sign subline',(-7.1,-1.36,3.2),2.9,.1),
    ('Rear building old Hangul',(.96,4.19,7.08),.43,2.72),
    ('Old side-lane shop Hangul',(9.3,.726,3.14),2.65,.35),
    ('Ghost of original workshop name',(-3.77,-1.29,3.94),1.1,.1),
    ('Ghost of original workshop trade',(-3.77,-1.29,3.74),1,.07),
    ('Window handwritten welcome',(3.96,-1.134,2.52),.55,.48),
    ('Window slow coffee note',(0,-1.134,2.48),1.55,.13),
    ('Window small lower inscription',(2.83,-1.125,.43),1.4,.065),
    ('Small café board coffee',(-1.28,-1.638,.81),.45,.28),
    ('Small café board hours',(-1.28,-1.638,.49),.43,.1),
    ('Small café board menu',(-1.28,-1.638,.29),.43,.065),
    ('Door handwritten invitation',(-1.45,-1.177,2.02),.35,.38),
    ('Mullae corner plaque title',(4.47,-1.262,2.87),.54,.11),
    ('Mullae corner plaque English',(4.47,-1.262,2.74),.55,.045),
    ('Small hand-painted alley note',(4.47,-1.22,2.47),.47,.09),
]
for name,center,width,height in sign_frames:
    fit_sign(scene.objects[name],center,width,height)

# Let the lettering's own strokes carry the fine text. Extra black contour lines
# otherwise swallow small cream brush strokes at the street camera's resolution.
letter_collection=bpy.data.collections.new('05 · Street lettering · native strokes')
scene.collection.children.link(letter_collection)
for obj in scene.objects:
    if obj.type=='FONT':letter_collection.objects.link(obj)
line_set=scene.view_layers[0].freestyle_settings.linesets[0]
line_set.select_by_collection=True
line_set.collection=letter_collection
line_set.collection_negation='EXCLUSIVE'

for loaded_font in [font,brush_font,heritage_font,serif_font]:
    if not loaded_font.packed_file:loaded_font.pack()
scene['signageDirection']='Individual signwriter voices: brush café identity, heritage factory serif, loose English script, window decals, enamel street plaque, taped notes.'
scene['cafeWorkingName']='틈새 / TEUMSAE · between sips & cities'
scene['signageCopy']='Fictional art-direction copy for this portfolio environment.'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'mullae-signage-v04.blend'),compress=True)
clear_path=folder/'clear_lettering.py'
clear_namespace={'__file__':str(clear_path),'__name__':'cleanup'}
exec(compile(clear_path.read_text(),str(clear_path),'exec'),clear_namespace)
manifest={'cafeWorkingName':scene['cafeWorkingName'],'fonts':[{'name':'Nanum Brush Script','source':'https://github.com/google/fonts/tree/main/ofl/nanumbrushscript','license':'SIL Open Font License; notice in ../fonts/NanumBrushScript-OFL.txt'},{'name':'Nanum Myeongjo ExtraBold','source':'https://github.com/google/fonts/tree/main/ofl/nanummyeongjo','license':'SIL Open Font License; notice in ../fonts/NanumMyeongjo-OFL.txt'},{'name':'SignPainter and Baskerville','source':'macOS system fonts'}],'copy':[{'name':obj.name,'text':obj.data.body} for obj in scene.objects if obj.type=='FONT']}
(folder/'signage-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
result={'source':bpy.data.filepath,'textObjects':sum(obj.type=='FONT' for obj in scene.objects),'cafeName':scene['cafeWorkingName']}

"""Neighbourhood shopfronts, a working metal shop and a side yard for the print room.

Executed by build_neighbourhood.py. The room openings and fixtures also
generate the collision boxes and walkable areas used by Explore.
"""
panel_green=material('Workshop faded machine green','657E72',1)
panel_clay=material('Workshop weathered oxide','926C60',1)
stained_render=material('Workshop stained concrete','A09B8E',1)
sign_ochre=material('Workshop faded sign enamel','BDA877',1)
sign_font=next(font for font in bpy.data.fonts if Path(font.filepath).name=='NanumMyeongjo-ExtraBold.ttf')
workshop_footprints=[]
shop_rooms={}
shop_portals=[]

def workshop(name, label, side, y0, y1, height, wall, shutter):
    inner=side*2.1
    outer=side*6.35
    center_x=(inner+outer)/2
    center_y=(y0+y1)/2
    length=y1-y0
    yaw=-side*math.pi/2
    box(name+' shell',(center_x,center_y,height/2),(4.25,length,height),wall,.008)
    for i in range(23):
        x=min(inner,outer)+.08+i*.186
        rod(name+' metal roof rib',(x,y0-.14,height-.04),(x,y1+.14,height+.15),.017,roof_metal,6)
    roof=box(name+' sloped sheet roof',(center_x,center_y,height+.035),(4.57,length+.28,.10),roof_metal,.003)
    roof.rotation_euler.x=math.atan2(.19,length+.28)
    for edge_y in [y0+.12,y1-.12]:
        box(name+' exposed steel frame',(inner-side*.04,edge_y,height/2),(.14,.17,height),iron,.003)
    # Pressed roller panels and guide rails read from the lane at walking height.
    width=min(2.7,length-.56)
    box(name+' roller shutter',(inner-side*.04,center_y,1.22),(.085,width,2.37),shutter,.004)
    for i in range(19):
        box(name+' shutter seam',(inner-side*.088,center_y,.15+i*.116),(.019,width-.05,.014),iron,.001)
    for dy in [-width/2,width/2]:
        box(name+' shutter guide',(inner-side*.115,center_y+dy,1.21),(.13,.065,2.39),iron,.003)
    box(name+' painted signboard',(inner-side*.065,center_y,2.66),(.13,width+.16,.39),sign_ochre,.004)
    sign=text(name+' Hangul sign',label,(inner-side*.138,center_y,2.66),.24,ink,(math.pi/2,0,yaw))
    sign.data.font=sign_font
    wall_window(name+' high workshop window',inner,center_y,height-.42,width*.66,.34,yaw)
    service_door(name+' rear service door',outer,center_y,-yaw)
    wall_window(name+' end window',center_x,y0,2.48,1.26,.52)
    wall_window(name+' back window',center_x,y1,2.48,1.26,.52,math.pi)
    for edge_y in [y0+.28,y1-.22]:
        curve(name+' exposed conduit',[(inner-side*.12,edge_y,.22),(inner-side*.12,edge_y,2.88),
              (inner-side*.12,edge_y-side*.11,2.99),(inner-side*.12,center_y,2.99)],.016,iron)
    workshop_footprints.append((min(inner,outer)-.14,max(inner,outer)+.14,y0,y1))

restaurant_wall=material('Restaurant worn sand plaster','B9A589',1)
rust_awning=material('Restaurant rust-red canopy','915A44',1)
window_wood=material('Restaurant dark timber','6D503B',1)
market_green=material('Market green canvas','627E63',1)
market_cream=material('Market cream canvas','E4D8B7',1)
studio_blue=material('Studio painted teal','4D7774',1)
indigo_canvas=material('Flower shop indigo canvas','58717C',1)
rose_flower=material('Flower shop dusty rose','BC7987',1)
white_flower=material('Flower shop ivory petals','E9DEBB',1)
display_glazing=material('shop display glazing','ACCBBF',1)
display_back=material('Warm display plaster','C5AB82',1)
brush_font=next(font for font in bpy.data.fonts if Path(font.filepath).name=='NanumBrushScript-Regular.ttf')
fruit_colours=[material('Market produce '+name,colour,1) for name,colour in [('pear','A3A366'),('tangerine','C88743'),('apple','A45B4C')]]

def cut_shell(shell, cutter):
    cutter.hide_render=True
    cutter.hide_set(True)
    opening=shell.modifiers.new(cutter.name,'BOOLEAN')
    opening.operation='DIFFERENCE'
    opening.object=cutter

def shopfront(name,shell,x,y,yaw,width,frame,sign_label,sign_colour,awning,display,stripe=None,
              has_room=False,entry=None,display_depth=1):
    """Build a shopfront with a display recess or a view into a furnished room."""
    turn=Matrix.Rotation(yaw,3,'Z')
    def point(u,depth,z):
        return Vector((x,y,z))+turn@Vector((u,-depth*display_depth if depth<0 else -depth,0))

    def panel(label,u,depth,z,w,d,h,mat,slope=0):
        scale=display_depth if depth<0 and label!='display opening' else 1
        obj=box(name+' '+label,point(u,depth,z),(w,d*scale,h),mat,.004)
        obj.rotation_euler=(slope,0,yaw)
        return obj

    window_center=-.36
    window_width=width-.85
    if entry:
        door_y,half_width=entry
        door_u=(door_y-y)*math.sin(yaw)
        left=-width/2+.10
        right=door_u-half_width-.075
        window_center=(left+right)/2
        window_width=right-left
    opening=window_width-.11
    cut_shell(shell,panel('display opening',window_center,-.37,1.44,opening,1.15,1.41,frame))
    if not has_room:
        panel('display back wall',window_center,-.91,1.44,opening,.04,1.41,display_back)
    panel('display floor',window_center,-.43,.74,opening,.88,.052,frame)
    panel('display glazing',window_center,.053,1.44,opening,.008,1.40,display_glazing)
    panel('display kickboard',window_center,.066,.42,window_width,.06,.61,frame)
    panel('display header',window_center,.065,2.175,window_width,.07,.07,frame)
    for u in [window_center-window_width*.49,window_center-window_width*.23,window_center,window_center+window_width*.23,window_center+window_width*.49]:
        panel('display upright',u,.082,1.44,.052,.075,1.44,frame)
    panel('display transom',window_center,.083,1.70,window_width,.07,.045,frame)
    panel('stock shelf',window_center,-.59,1.07,opening-.11,.43,.061,wood)
    if display in ('market','print','ceramics'):
        panel('upper stock shelf',window_center,-.65,1.59,opening-.11,.36,.05,frame)

    for index,u in enumerate([window_center-opening*.29,window_center,window_center+opening*.29]):
        if display=='restaurant':
            panel('table',u,-.54,1.08,opening*.25,.48,.05,window_wood)
            panel('bench back',u,-.83,1.30,opening*.25,.10,.34,rust_awning)
            sphere(name+' ceramic bowl',point(u-.06,-.47,1.13),(.085,.076,.038),ivory,2)
            cylinder(name+' tea flask',point(u+.10,-.65,1.20),.037,.18,studio_blue,10)
        elif display=='market':
            panel('produce crate',u,-.51,1.16,opening*.26,.34,.145,wood,-.14)
            for row in range(2):
                for column in range(4):
                    sphere(name+' produce',point(u+(column-1.5)*opening*.047,-.62+row*.11,1.24+row*.014),
                           (.052,.054,.05),fruit_colours[index],1)
            for column in range(4):
                panel('dry goods tin',u+(column-1.5)*opening*.048,-.69,1.7,.08,.11,.16,
                      market_green if (index+column)%2 else sign_ochre)
        elif display=='ceramics':
            for column in range(3):
                offset=(column-1)*opening*.07
                colour=[ivory,studio_blue,terracotta][(index+column)%3]
                cylinder(name+' thrown vessel',point(u+offset,-.55,1.20),.047,.19,colour,14,top_radius=.063)
                cylinder(name+' vase neck',point(u+offset,-.55,1.31),.034,.055,colour,14)
                sphere(name+' shelf bowl',point(u+offset,-.66,1.65),(.055,.050,.025),colour,2)
        elif display=='flowers':
            cylinder(name+' florist bucket',point(u,-.49,1.20),.10,.19,frame,12,top_radius=.13)
            for stem in range(5):
                dx=(stem-2)*.052
                tip=point(u+dx,-.51+(stem%2)*.053,1.49+(stem%3)*.082)
                rod(name+' flower stem',point(u,-.49,1.25),tip,.008,green,5)
                sphere(name+' flower head',tip,(.052,.045,.057),[white_flower,rose_flower,sign_ochre][index],1)
        else:
            for row in range(5):
                panel('paper ream',u,-.53,1.115+row*.036,opening*.24,.30,.03,paper if row%2 else market_cream)
            panel('mounted print',u,-.835,1.85,opening*.23,.022,.31,[panel_clay,studio_blue,sign_ochre][index])
    if entry:
        cut_shell(shell,panel('doorway opening',door_u,-.14,1.13,half_width*2,.76,2.27,frame))
        for side in [-1,1]:
            panel('door jamb',door_u+side*(half_width+.034),.058,1.12,.068,.13,2.24,frame)
        panel('door lintel',door_u,.058,2.26,half_width*2+.14,.13,.09,frame)
        panel('open threshold',door_u,.02,.019,half_width*2,.31,.037,frame)
        # The leaf sits against the interior wall with a clear way through.
        leaf=panel('open timber door',door_u+half_width-.045,-.44,1.10,.76,.043,2.15,frame)
        leaf.rotation_euler.z+=math.pi/2
        panel('low entry mat',door_u,.32,.029,.86,.42,.012,sign_colour)
    else:
        panel('recessed door',width/2-.37,.04,1.18,.69,.10,2.24,frame)
        panel('door window',width/2-.37,.104,1.62,.53,.025,.86,glass)
        panel('door pull',width/2-.57,.14,1.06,.031,.045,.24,ivory)
    if display=='restaurant':
        for plank in range(5):
            panel('wooden sign plank',0,.101,2.73+plank*.087,width+.16,.11,.083,
                  window_wood if plank%2 else wood)
    else:
        panel('signboard',0,.101,2.90,width+.13,.11,.39,sign_colour)
        for edge in [-.17,.17]:
            panel('painted sign border',0,.16,2.90+edge,width+.04,.01,.02,market_cream)
    sign=text(name+' Hangul sign',sign_label,point(0,.168,2.9),
              .40 if display=='restaurant' else .28,ivory,(math.pi/2,0,yaw))
    sign.data.font=brush_font if display=='restaurant' else sign_font
    if display in ('ceramics','flowers','print'):
        blade_yaw=yaw+math.pi/2
        blade=box(name+' projecting sign',point(width/2-.18,.39,2.71),(.37,.08,.62),sign_colour,.018)
        blade.rotation_euler.z=blade_yaw
        rod(name+' sign bracket',point(width/2-.18,.02,3.06),point(width/2-.18,.52,3.06),.018,iron,8)
        word={'ceramics':'공\n방','flowers':'꽃','print':'인\n쇄'}[display]
        for face in [-1,1]:
            lettering=text(name+' vertical sign',word,point(width/2-.18+face*.05,.39,2.71),.19,
                           ivory,(math.pi/2,0,blade_yaw+(math.pi if face<0 else 0)))
            lettering.data.font=brush_font

    if stripe:
        for i in range(12):
            panel('striped awning',width*((i+.5)/12-.5),.45,2.42,width/12,.86,.048,
                  awning if i%2==0 else stripe,.16)
        panel('canvas valance',0,.875,2.31,width,.06,.17,awning)
    else:
        panel('sloped canopy',0,.47,2.43,width+.17,.9,.055,awning,.16)
        for i in range(int(width/.14)):
            u=i*.14-width/2+.06
            rod(name+' canopy seam',point(u,.08,2.52),point(u,.92,2.39),.016,awning,6)
        for u in [-width*.38,0,width*.38]:
            rod(name+' globe bracket',point(u,.17,2.69),point(u,.81,2.54),.019,iron,7)
            sphere(name+' warm globe',point(u,.81,2.43),(.105,.105,.11),lamp_glow,2)

def shop_room(key,name,shell,bounds,lane_side,entry,floor):
    x0,x1,y0,y1=bounds
    door_y,half_width=entry
    wall=.17
    room=(x0+wall,x1-wall,y0+wall,y1-wall)
    center_x=(x0+x1)/2
    center_y=(y0+y1)/2
    cut_shell(shell,box(name+' room cavity',(center_x,center_y,1.53),(x1-x0-2*wall,y1-y0-2*wall,2.98),floor,.002))
    box(name+' finished floor',(center_x,center_y,.045),(x1-x0-2*wall+.02,y1-y0-2*wall+.02,.05),floor,.002)

    lower_wall=(x0,x0+wall)
    upper_wall=(x1-wall,x1)
    lane_wall=upper_wall if lane_side>0 else lower_wall
    outer_wall=lower_wall if lane_side>0 else upper_wall
    workshop_footprints.extend([
        (*outer_wall,y0,y1),(x0,x1,y0,y0+wall),(x0,x1,y1-wall,y1),
        (*lane_wall,y0,door_y-half_width),(*lane_wall,door_y+half_width,y1),
    ])
    lane_x=x1 if lane_side>0 else x0
    shop_rooms[key]=room
    shop_portals.append((min(lane_x-lane_side*1.23,lane_side*-.9),
                         max(lane_x-lane_side*1.23,lane_side*-.9),door_y-half_width,door_y+half_width))

def fixture(name,x,y,w,d,height,mat):
    box(name,(x,y,height/2),(w,d,height),mat,.009)
    workshop_footprints.append((x-w/2,x+w/2,y-d/2,y+d/2))

def shop_pendant(name,x,y,z):
    rod(name+' hanging cable',(x,y,z),(x,y,3.04),.012,iron,6)
    cylinder(name+' spun shade',(x,y,z),.22,.15,iron,16,top_radius=.10)
    sphere(name+' warm bulb',(x,y,z-.07),(.15,.15,.055),lamp_glow,2)

restaurant_entry=(-2.39,.69)
market_entry=(-4.58,.70)
studio_entry=(.31,.65)
restaurant_tile=material('Restaurant warm tiled floor','B9997C',1)
market_tile=material('Market terrazzo floor','B9B49A',1)
studio_floor=material('Studio clay-dusted concrete','B7AEA0',1)

# A low restaurant wraps around the sunny corner, with a brick upper storey set back.
restaurant_shell=box('Corner restaurant plaster shell',(-4.43,-3.71,1.63),(4.14,4.08,3.26),restaurant_wall,.008)
box('Corner restaurant weathered coping',(-4.43,-3.71,3.28),(4.35,4.26,.19),stained_render,.008)
box('Restaurant setback brick upper storey',(-5.04,-3.19,4.21),(2.75,2.86,1.86),rear_brick,.008)
box('Restaurant upper parapet',(-5.04,-3.19,5.17),(2.89,3,.21),rear_brick,.003)
for x in [-5.84,-4.57]:
    wall_window('Restaurant upper sash',x,-4.64,4.29,.72,.97,frame=window_wood)
wall_window('Restaurant side upper sash',-3.65,-3.14,4.29,1.15,.97,math.pi/2,window_wood)
shopfront('Corner restaurant street front',restaurant_shell,-4.43,-5.77,0,3.63,window_wood,'골목 식당',window_wood,rust_awning,'restaurant',has_room=True,display_depth=.60)
shopfront('Corner restaurant lane front',restaurant_shell,-2.35,-3.72,math.pi/2,3.62,window_wood,'따뜻한 한 끼',window_wood,rust_awning,'restaurant',has_room=True,entry=restaurant_entry)
shop_room('restaurant','Restaurant',restaurant_shell,(-6.5,-2.36,-5.75,-1.67),1,restaurant_entry,restaurant_tile)
workshop_footprints.extend([(-6.12,-3.47,-5.60,-5.19),(-3.27,-2.52,-5.38,-3.15)])
for y in [-2.48,-3.87]:
    fixture('Restaurant window banquette',-6.05,y,.46,1.15,.54,rust_awning)
    box('Restaurant upholstered back',(-6.21,y,.81),(.14,1.15,.54),rust_awning,.009)
    fixture('Restaurant dining table',-5.28,y,.72,.83,.79,window_wood)
    sphere('Restaurant set plate',(-5.29,y,.811),(.115,.115,.017),ivory,2)
    cylinder('Restaurant table flask',(-5.49,y+.19,.91),.046,.24,studio_blue,12)
shop_pendant('Restaurant pendant',-4.52,-3.51,2.42)

# The market has a lighter painted base and a taller, offset brick upper floor.
market_shell=box('Corner market painted shell',(4.67,-4.01,1.58),(4.06,2.98,3.16),cream,.006)
box('Corner market flat concrete cap',(4.67,-4.01,3.18),(4.22,3.14,.14),trim,.005)
box('Corner market upper brick shell',(5.2,-3.83,4.24),(2.85,2.37,2.12),rear_brick,.007)
box('Corner market upper roof',(5.2,-3.83,5.34),(2.98,2.50,.19),trim,.004)
wall_window('Market upper paired sash',5.08,-5.025,4.27,1.57,1.1)
wall_window('Market upper lane sash',3.76,-3.83,4.28,1.18,1.0,-math.pi/2)
shopfront('Corner market street front',market_shell,4.66,-5.51,0,3.52,panel_green,'골목 상회',market_green,market_green,'market',market_cream,has_room=True,display_depth=.42)
shopfront('Corner market lane front',market_shell,2.63,-4.02,-math.pi/2,2.48,panel_green,'과일 · 채소',market_green,market_green,'market',market_cream,has_room=True,entry=market_entry)
for x,z,mat in [(5.75,.22,studio_blue),(5.75,.51,market_green),(6.37,.20,sign_ochre)]:
    box('Market stacked produce crate',(x,-6.1,z),(.53,.42,.27),mat,.008)
shop_room('market','Market',market_shell,(2.64,6.70,-5.50,-2.52),-1,market_entry,market_tile)
workshop_footprints.extend([(5.45,6.65,-6.32,-5.84),(3.16,6.04,-5.48,-5.15),(2.79,3.50,-4.08,-2.89)])
fixture('Market checkout counter',5.69,-4.55,1.05,.61,1.02,window_wood)
box('Market till',(5.92,-4.54,1.14),(.28,.24,.23),iron,.008)
for y in [-2.91,-3.76]:
    fixture('Market wall stock rack',6.20,y,.44,.66,1.86,market_green)
    for row in range(3):
        level=.64+row*.46
        box('Market shelf pale edge',(5.96,y,level),(.08,.66,.05),market_cream,.004)
        for dy in [-.22,0,.22]:
            box('Market shelf packet',(5.93,y+dy,level+.108),(.10,.15,.19),fruit_colours[row],.005)
shop_pendant('Market pendant',4.64,-3.71,2.45)

# A narrower studio and flower shop alternate with a single standing metal shop.
studio_shell=box('Ceramics studio limewash shell',(-4.25,-.25,1.54),(4.24,2.60,3.08),plaster,.006)
studio_roof=box('Ceramics studio sloping roof',(-4.28,-.32,3.16),(4.37,2.62,.18),roof_metal,.006)
studio_roof.rotation_euler.y=-.06
shopfront('Ceramics studio',studio_shell,-2.12,-.32,math.pi/2,2.12,studio_blue,'도자기 공방',studio_blue,indigo_canvas,'ceramics',market_cream,has_room=True,entry=studio_entry)
shop_room('studio','Ceramics studio',studio_shell,(-6.37,-2.13,-1.55,1.05),1,studio_entry,studio_floor)
workshop_footprints.append((-3.04,-2.29,-1.31,-.16))
fixture('Studio clay workbench',-5.78,-.64,.77,1.27,.89,wood)
cylinder('Studio throwing wheel',(-5.67,-.62,.94),.23,.095,iron,24)
cylinder('Studio clay bowl on wheel',(-5.67,-.62,1.06),.09,.16,terracotta,24,top_radius=.15)
for x in [-5.54,-5.06,-4.59]:
    fixture('Studio drying shelf base',x,-1.18,.45,.28,.76,window_wood)
    box('Studio drying shelf upper',(x,-1.18,1.42),(.45,.29,.053),wood,.004)
    for level in [.76,1.45]:
        cylinder('Studio kiln-fired vessel',(x,-1.18,level+.11),.093,.22,ivory,16,top_radius=.063)
shop_pendant('Studio pendant',-4.62,-.17,2.42)

workshop('Metal cutting shop','정밀 금속',-1,2.8,7.46,4.05,stained_render,panel_clay)

flower_shell=box('Flower shop plaster shell',(4.25,4.27,1.57),(4.29,4.9,3.14),plaster,.006)
box('Flower shop roof',(4.25,4.27,3.18),(4.41,5.02,.16),render_wall,.005)
box('Flower shop narrow tile base',(2.10,4.27,.32),(.10,4.83,.57),studio_blue,.006)
shopfront('Flower shop',flower_shell,2.07,4.34,-math.pi/2,3.24,studio_blue,'계절 꽃집',studio_blue,indigo_canvas,'flowers',market_cream)
wall_window('Flower shop end sash',4.09,1.80,1.64,1.6,1.38,frame=studio_blue)
flower_pink=material('Flower shop faded pink blooms','BE7C83',1)
for y,mat in [(3.08,flower_pink),(3.63,sign_ochre),(5.58,ivory)]:
    pot('Flower shop pavement pot',1.77,y,.032,.30)
    for dy in [-.09,.06,.14]:
        sphere('Flower shop blooms',(1.78,y+dy,.58+abs(dy)),(.075,.061,.07),mat,1)
workshop_footprints.extend([(1.94,6.52,1.82,6.74),(1.56,1.99,2.88,3.8),(1.56,1.99,5.38,5.78)])

# The print room faces a small yard between the welding and steel shops.
print_shell=box('Print room shell',(7.4,-.35,1.65),(3.0,4.34,3.3),render_wall,.006)
box('Print room metal cap',(7.4,-.35,3.32),(3.23,4.54,.15),roof_metal,.005)
shopfront('Print room',print_shell,5.89,-.35,-math.pi/2,2.87,panel_clay,
          '골목 인쇄실',window_wood,rust_awning,'print')
workshop_footprints.append((5.73,8.9,-2.52,1.82))

# The forecourt reads as part of the street, with paving and a low kerb.
active_collection=street
box('Arrival paved footway',(0,-7.09,.011),(13.25,5.03,.032),concrete,.002)
for x in [-6.6,-5.4,-4.2,-3.0,-1.8,-.6,.6,1.8,3.0,4.2,5.4]:
    stroke('Arrival paving joint',[(x,-9.55,.035),(x,-5.9,.035)],.002)
for x in [-5.65,-1.2,1.2,5.8]:
    cylinder('Arrival kerb bollard',(x,-9.62,.34),.06,.65,iron,8)

# Shallow concrete patches soften the utility lane and mark the paved print yard.
active_collection=street
box('Fabrication lane concrete',(0,1.05,.012),(4.15,12.91,.038),concrete,.002)
box('Print yard concrete',(3.9,-.35,.012),(4.04,4.30,.038),concrete,.002)
for y in [-5.4,-2.55,1.85,4.7]:
    stroke('Fabrication lane concrete joint',[(-2.03,y,.033),(1.98,y+.04,.033)],.003)
for x in [2.8,4.34]:
    stroke('Print yard joint',[(x,-2.48,.033),(x+.04,1.76,.033)],.0025)
for y in [-5.3,-1.48,2.24,7.28]:
    box('Lane drain frame',(-1.87,y,.034),(.26,.39,.025),iron,.001)
    for i in range(6):
        box('Lane drain bar',(-1.87,y-.16+i*.064,.05),(.22,.032,.009),roof_metal,.001)
# Utility cables follow the shopfronts, with concrete poles at each end.
for x in [-2.03,2.04]:
    for y in [-5.85,7.58]:
        rod('Fabrication lane concrete service pole',(x,y,.03),(x,y,5.65),.083,trim,9)
    for z in [5.25,5.58]:
        curve('Fabrication lane sagging service wire',[(x,-5.85,z),(x+.05,.8,z-.65),(x,7.58,z)],.014,iron)

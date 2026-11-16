"""Human-scale laneway details; the central route stays clear."""
active_collection=street
street_footprints=[]
trunk_mat=material('Street tree bark','7F7560',1)
leaf_soft=[material('Street foliage wash '+str(i),value,1) for i,value in enumerate(['7B8A71','8E9E7D','A4AB88','697E70'])]
patron_skin=material('Street patron skin','B99B84',1)
patron_hair=material('Street patron hair','504B43',1)
patron_coat=[material('Street patron coat '+str(i),value,1) for i,value in enumerate(['7D8E8A','B19D83','737F91'])]

def neighbourhood_tree(name,x,y,height):
    cylinder(name+' tree pit',(x,y,.04),.49,.055,soil,14)
    rod(name+' trunk',(x,y,.04),(x+.12,y,height*.72),.065,trunk_mat,9)
    for i,(dx,dy) in enumerate([(-.55,.1),(.48,.25),(.1,-.4)]):
        rod(name+' branch',(x+.05,y,height*.48),(x+dx,y+dy,height*.82),.027,trunk_mat,7)
    random.seed(int((x+30)*100+y*3))
    # Overlapping flattened clusters keep the irregular silhouette of a foliage wash.
    for i in range(12):
        angle=i*2.4;radius=.58*(i%4)/3
        sphere(name+' foliage',(x+math.cos(angle)*radius,y+math.sin(angle)*radius,height-.45+random.uniform(-.3,.35)),(.65,.57,.44),leaf_soft[i%4],2)

for x,y,height in [(-7.3,-4.6,4.2),(7.4,-4.8,3.8),(-7.5,5.3,4.35),(7.65,3.6,4.1),(-10.6,10.4,4.7),(9.9,8.0,4.5)]:
    neighbourhood_tree('Neighbourhood street tree',x,y,height)
    street_footprints.append((x-.45,x+.45,y-.45,y+.45))
# A vine canopy and window boxes soften the one- and two-storey buildings.
for side,y in [(-1,-3.5),(1,.9),(-1,5.35)]:
    x=side*1.98
    box('Lane planted window box',(x,y,3.29),(.31,1.22,.19),terracotta,.003)
    for i in range(6):
        sphere('Lane window-box trailing foliage',(x-side*.06,y-.5+i*.19,3.31-(i%3)*.07),(.2,.2,.15),leaf_soft[i%4],1)
for x,y in [(-1.78,-4.5),(1.79,1.9),(-1.79,6.4)]:
    curve('Lane climbing vine',[(x,y,.15),(x,y+.06,1.3),(x,y-.05,2.5),(x,y+.25,3.6)],.008,trunk_mat)
    for i in range(15):
        z=.6+i*.2
        sphere('Lane climbing vine leaf',(x+(i%2)*.07,y+math.sin(i)*.12,z),(.09,.14,.1),leaf_soft[i%4],1)
# A low shop display and upright bicycle add things to discover at walking height.
box('Bookshop outdoor book crate',(-1.4,.1,.27),(.48,.67,.43),wood,.003)
for i in range(8):
    book=box('Bookshop secondhand book',(-1.4,.1-.26+i*.07,.5),(.29,.055,.32),paper if i%3 else patron_coat[i%3],.001)
    book.rotation_euler.x=(i%3-1)*.07
street_footprints.append((-1.72,-1.08,-.3,.5))
# Bicycle wheels lie parallel to the service wall.
x,y=-6.5,1.1
for wheel_y in [y-.52,y+.52]:
    points=[(x,wheel_y+math.sin(i*math.tau/24)*.31,.39+math.cos(i*math.tau/24)*.31) for i in range(25)]
    curve('Lane bicycle tyre',points,.023,iron)
    for i in range(8):
        rod('Lane bicycle spoke',(x,wheel_y,.39),(x,wheel_y+math.sin(i*math.tau/8)*.29,.39+math.cos(i*math.tau/8)*.29),.003,trim,5)
for a,b in [((x,y-.52,.39),(x,y-.18,.91)),((x,y-.18,.91),(x,y+.13,.39)),((x,y+.13,.39),(x,y-.52,.39)),((x,y-.18,.91),(x,y+.36,.91)),((x,y+.36,.91),(x,y+.13,.39)),((x,y+.36,.91),(x,y+.52,.39))]:rod('Lane bicycle steel frame',a,b,.017,red,8)
box('Lane bicycle saddle',(x,y-.18,.99),(.16,.21,.045),iron,.003)
rod('Lane bicycle handlebar',(x-.17,y+.39,1.07),(x+.17,y+.39,1.07),.014,iron,8)
# Two quiet figures, proportioned like the player; no floating faces or billboard people.
def seated_reader(name,x,y,angle,coat):
    def p(a,b,z):return(x+a*math.cos(angle)-b*math.sin(angle),y+a*math.sin(angle)+b*math.cos(angle),z)
    for side in [-1,1]:
        rod(name+' trouser calf',p(side*.1,-.24,.1),p(side*.1,-.23,.48),.065,ink,8)
        rod(name+' trouser thigh',p(side*.1,-.23,.48),p(side*.1,.01,.53),.074,ink,8)
        box(name+' shoe',p(side*.1,-.29,.1),(.13,.25,.1),iron,.002).rotation_euler.z=angle
    torso=box(name+' torso',p(0,.02,.82),(.37,.24,.54),coat,.008);torso.rotation_euler.z=angle
    sphere(name+' head',p(0,-.02,1.25),(.15,.14,.19),patron_skin,2)
    sphere(name+' hair',p(0,.01,1.35),(.155,.145,.11),patron_hair,2)
    for side in [-1,1]:
        rod(name+' upper sleeve',p(side*.22,.0,1.0),p(side*.24,-.17,.77),.055,coat,8)
        rod(name+' forearm',p(side*.24,-.17,.77),p(side*.11,-.35,.77),.045,patron_skin,8)
    book=box(name+' open book',p(0,-.36,.79),(.27,.2,.022),paper,.001);book.rotation_euler.z=angle
    box(name+' seat',p(0,.04,.51),(.44,.4,.04),wood,.002).rotation_euler.z=angle
    for a in [-.17,.17]:
        for b in [-.13,.18]:rod(name+' chair leg',p(a,b,.05),p(a,b,.5),.015,iron,7)
seated_reader('Lane reader',-1.31,-4.28,math.pi/2,patron_coat[0])
seated_reader('Courtyard coffee visitor',3.5,10.6,math.pi/3,patron_coat[1])
street_footprints.extend([(-1.7,-.9,-4.7,-3.8),(3.1,3.9,10.2,11.0)])
# Small communal bench where lane paving spills into the shared courtyard.
box('Courtyard timber bench seat',(6.4,10.7,.51),(1.65,.4,.075),wood,.003)
for x in [5.75,7.05]:box('Courtyard bench steel leg',(x,10.7,.28),(.055,.32,.46),iron,.002)
street_footprints.append((5.5,7.3,10.45,10.95))

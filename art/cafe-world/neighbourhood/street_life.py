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

# Taller deciduous trees at the entrance and in gaps between the buildings.
# Each crown combines irregular clusters and loose leaf silhouettes in two meshes.
canopy_colours=[material('Deciduous foliage '+str(i),value,1) for i,value in enumerate(
    ['596B44','75844E','8D984F','A7A85D','AE9852'])]
bark_light=material('Street tree bark pale patches','AF9D7C',1)
tree_shade=material('Deciduous foliage ground shade','969D91',1)
tree_shade_light=material('Deciduous foliage ground shade edge','A6AA98',1)

def mature_street_tree(name,x,y,height,spread,seed):
    rng=random.Random(seed)
    cylinder(name+' stone tree grate',(x,y,.027),.54,.056,trim,12)
    cylinder(name+' soil bed',(x,y,.057),.46,.012,soil,12)
    trunk_top=(x-.12,y+.13,height*.69)
    rod(name+' trunk',(x,y,.02),trunk_top,.17,trunk_mat,11)
    # Pale bark patches break up the silhouette at pedestrian height.
    for i in range(12):
        theta=rng.uniform(0,math.tau)
        z=rng.uniform(.25,height*.54)
        radius=.171
        anchor=(x-.12*z/(height*.69)+radius*math.cos(theta),
                y+.13*z/(height*.69)+radius*math.sin(theta),z)
        obj=box(name+' pale bark',anchor,(rng.uniform(.045,.097),.009,rng.uniform(.09,.29)),bark_light,0)
        obj.rotation_euler.z=theta+math.pi/2

    crown=bmesh.new()
    flecks=[]
    faces=[]
    colours=[]
    for index in range(9):
        angle=index*2.4+rng.uniform(-.25,.25)
        radial=spread*(.22+.39*(index%3)/2)
        center=Vector((x+math.cos(angle)*radial,y+math.sin(angle)*radial,
                      height*(.70+.25*(index%4)/3)))
        fork=Vector((x-.07,y+.08,height*(.39+.18*(index%3)/2)))
        branch_tip=fork.lerp(center,.88)
        rod(name+' spreading branch',fork,branch_tip,.061-index*.003,trunk_mat,7)
        reach=Vector((spread*rng.uniform(.39,.56),spread*rng.uniform(.36,.51),height*rng.uniform(.13,.18)))
        for bunch in range(4):
            jitter=Vector((rng.uniform(-.27,.27),rng.uniform(-.29,.29),rng.uniform(-.24,.24)))
            size=reach*rng.uniform(.52,.85)
            vertices=bmesh.ops.create_icosphere(crown,subdivisions=2,radius=1)['verts']
            for vertex in vertices:
                unit=vertex.co.copy()
                grain=rng.uniform(.77,1.22)
                vertex.co=center+jitter+Vector((unit.x*size.x,unit.y*size.y,unit.z*size.z))*grain
            for face in {face for vertex in vertices for face in vertex.link_faces}:
                face.material_index=rng.choices(range(5),[3,7,10,6,2])[0]
        for i in range(37):
            theta=rng.uniform(0,math.tau)
            upward=rng.uniform(-.9,.9)
            radius=math.sqrt(1-upward*upward)*rng.uniform(.72,1.15)
            leaf_center=center+Vector((math.cos(theta)*reach.x*radius,math.sin(theta)*reach.y*radius,upward*reach.z))
            across=Vector((math.cos(theta),math.sin(theta),rng.uniform(-.65,.65)))*rng.uniform(.075,.165)
            tip=Vector((-math.sin(theta),math.cos(theta),rng.uniform(-.9,.9)))*rng.uniform(.085,.17)
            first=len(flecks)
            flecks.extend([leaf_center-across,leaf_center+tip,leaf_center+across,leaf_center-tip])
            faces.append((first,first+1,first+2,first+3))
            colours.append(rng.randrange(5))
    crown_mesh=bpy.data.meshes.new(name+' crown')
    leaf_mesh=bpy.data.meshes.new(name+' outer leaves')
    leaf_mesh.from_pydata(flecks,[],faces)
    for mesh in [crown_mesh,leaf_mesh]:
        for mat in canopy_colours:
            mesh.materials.append(mat)
    crown.to_mesh(crown_mesh)
    crown.free()
    link_object(name+' crown',crown_mesh)
    link_object(name+' outer leaves',leaf_mesh)
    for polygon,index in zip(leaf_mesh.polygons,colours):
        polygon.material_index=index

    # Leave a faint broken shadow on the pavement even in the browser's painted lighting.
    shadow_vertices=[]
    shadow_faces=[]
    for i in range(47):
        theta=rng.uniform(0,math.tau)
        radius=math.sqrt(rng.random())*spread*.89
        sx=x+.8+math.cos(theta)*radius
        sy=y+.63+math.sin(theta)*radius*.79
        width=rng.uniform(.055,.24)
        depth=rng.uniform(.048,.14)
        first=len(shadow_vertices)
        z=.0345+i*.000008
        shadow_vertices.extend([(sx-width,sy,z),(sx-width*.13,sy-depth,z),
                                (sx+width,sy-depth*.16,z),(sx+width*.55,sy+depth,z),(sx-width*.45,sy+depth*.72,z)])
        shadow_faces.append(tuple(range(first,first+5)))
    shadow_mesh=bpy.data.meshes.new(name+' broken pavement shade')
    shadow_mesh.from_pydata(shadow_vertices,[],shadow_faces)
    shadow_mesh.materials.append(tree_shade)
    shadow_mesh.materials.append(tree_shade_light)
    for polygon in shadow_mesh.polygons:
        polygon.material_index=polygon.index%2
    link_object(name+' painted shade',shadow_mesh)
    street_footprints.append((x-.48,x+.48,y-.48,y+.48))

for x,y,height,spread,seed in [
    (-3.9,-8.15,7.6,3.05,49),(4.05,-7.71,8.35,3.25,72),
    (-2.59,1.82,7.15,2.75,93),(4.85,11.56,6.1,2.55,47),
]:
    mature_street_tree('Lane canopy tree',x,y,height,spread,seed)

for x,y,height in [(-7.3,-4.6,4.2),(7.4,-4.8,3.8),(-7.5,5.3,4.35),(7.65,3.6,4.1),(-10.6,10.4,4.7),(9.9,8.0,4.5)]:
    neighbourhood_tree('Neighbourhood street tree',x,y,height)
    street_footprints.append((x-.45,x+.45,y-.45,y+.45))
# A print rack and stacked paper sit beside the print-room display window.
box('Print yard paper crate',(5.16,1.38,.29),(.64,.56,.48),wood,.003)
for i in range(8):
    box('Print yard stacked paper',(5.15,1.37,.54+i*.018),(.49,.35,.016),paper if i%3 else patron_coat[0],.001)
street_footprints.append((4.82,5.49,1.09,1.67))
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
# A seated reader marks the courtyard bench area.
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
seated_reader('Courtyard coffee visitor',3.5,10.6,math.pi/3,patron_coat[1])
street_footprints.append((3.1,3.9,10.2,11.0))
# Small communal bench where lane paving spills into the shared courtyard.
box('Courtyard timber bench seat',(6.4,10.7,.51),(1.65,.4,.075),wood,.003)
for x in [5.75,7.05]:box('Courtyard bench steel leg',(x,10.7,.28),(.055,.32,.46),iron,.002)

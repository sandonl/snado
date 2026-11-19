"""Distant, complete scenery surrounds the playable block on every side.

Low neighbourhood roofs sit in front of a soft, layered tree canopy and low hills.
These are scenery, outside the walking bounds; not a second playable scene.
"""
active_collection=street
random.seed(83)
scenery_green=[material('Scenery foliage mist '+str(i),value,1) for i,value in enumerate(['A5B3A1','B6BFB0','C4CBC0','94A797'])]
scenery_stone=[material('Scenery roof wash '+str(i),value,1) for i,value in enumerate(['ACB7AF','B9B8A7','C1B4A2','A7B1AB'])]
scenery_ground=material('Scenery garden ground','B3B8A3',1)
box('Scenery continuous surrounding ground',(0,8,-.22),(280,280,.22),scenery_ground,0)
# Low relief, closed hill meshes; irregular ridges fade into the distant tree line.
for distance,height in [(66,8),(88,13)]:
    for side in [-1,1]:
        for axis in ['x','y']:
            for i in range(6):
                along=-65+i*26+random.uniform(-7,7)
                x,y=(side*distance,along) if axis=='x' else (along,side*distance)
                sphere('Scenery distant ridge',(x,y,-5),(28,24,height),scenery_green[2 if distance>70 else 1],2)
# A loose belt of trees and roofs hides the empty horizon in every camera direction.
for side in [-1,1]:
    for i in range(12):
        along=-35+i*8.3
        for axis in ['x','y']:
            across=side*(36+random.uniform(-3,5))
            x,y=(across,along) if axis=='x' else (along,across)
            height=random.uniform(3.2,6.2);width=random.uniform(3.2,5.5)
            box('Scenery low neighbourhood building',(x,y,height/2),(width,random.uniform(3,5),height),scenery_stone[i%4],.002)
            box('Scenery roof rim',(x,y,height+.07),(width+.13,4.4,.13),scenery_stone[(i+1)%4],.002)
            for wx in [x-width*.25,x+width*.25]:
                box('Scenery distant recessed window',(wx,y-2.23,height*.62),(.56,.015,.9),scenery_green[0],.001)
            tree_x=x+random.uniform(-3,3);tree_y=y+side*7
            for cluster in range(4):
                sphere('Scenery layered tree wash',(tree_x+random.uniform(-1.5,1.5),tree_y+random.uniform(-1.5,1.5),random.uniform(3.4,5.6)),(2.5,2.4,1.7),scenery_green[(i+cluster)%4],2)
# Nearer pocket gardens connect the block to the scenery rather than a plinth edge.
for side in [-1,1]:
    box('Scenery garden verge',(side*17,9,-.04),(5.5,40,.09),scenery_ground,.001)
    for y in [-8,-1,6,13,21,28]:
        neighbourhood_tree('Garden street tree',side*(16+random.uniform(-1,1)),y,random.uniform(4.5,6.5))
    for y in [-4,6,16,26]:
        box('Scenery low garden wall',(side*20,y,.36),(.27,8.6,.7),render_wall,.002)
        for i in range(5):sphere('Scenery garden hedge',(side*20,y-3.5+i*1.5,.9),(.65,.9,.55),scenery_green[0],1)
# Street at each end continues into the haze, with curb edges instead of a hard void.
for y in [-12.2,30.8]:
    box('Scenery cross street',(0,y,-.08),(87,4.8,.11),asphalt,.001)
    for offset in [-2.55,2.55]:box('Scenery cross-street curb',(0,y+offset,.04),(87,.18,.15),trim,.002)

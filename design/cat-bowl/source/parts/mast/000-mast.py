from math import sin, radians
w=param('mast_width',28.0)
h=param('mast_body_length',62.11808800909513)
peg_w=param('mast_peg_width',16.0)
peg_h=param('mast_peg_height',7.0)
edge=param('mast_edge_chamfer',0.6)
angle=param('mast_seat_angle_deg',10.0)
seat_rise=param('mast_seat_center_rise',9.0)
seat_d=param('mast_seat_diameter',60.0)
count=param('mast_detent_count',5)
pitch=param('mast_detent_pitch',10.0)
first_z=param('mast_detent_first_z',10.0)
dimple_d=param('mast_detent_diameter',5.8)
depth=param('mast_detent_depth',1.2)
lead=param('mast_detent_leadin',0.35)
seat_z=h+seat_rise
body=Cylinder(w/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
body=chamfer(body.edges().sort_by(Axis.Z)[0],edge)
bottom=Pos(0,0,h)*Circle(w/2)
top=Pos(0,0,seat_z)*Rot(0,angle,0)*Circle(seat_d/2)
body+=loft([bottom,top])
peg=Pos(0,0,h)*Box(peg_w,peg_w,seat_rise+peg_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
peg=chamfer(peg.edges().group_by(Axis.Z)[-1],edge)
body+=peg
# Local -X faces the rear screw. Flat-bottom shallow pockets accept a flat M5 end.
for i in range(int(count)):
 z=first_z+i*pitch
 cut=Pos(-w/2+depth,0,z)*Rot(0,-90,0)*Cylinder(dimple_d/2,depth+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
 mouth=Pos(-w/2+lead,0,z)*Rot(0,-90,0)*Cone(dimple_d/2,dimple_d/2+lead,lead,align=(Align.CENTER,Align.CENTER,Align.MIN))
 body=body-cut-mouth
assert body.is_valid and len(body.solids())==1
assert seat_rise>seat_d/2*sin(radians(angle))
assert first_z-dimple_d/2>edge and first_z+(count-1)*pitch+dimple_d/2<h
assert int(count)==5 and abs((count-1)*pitch-40)<1e-6
print('Rear pocket local Z:',[first_z+i*pitch for i in range(int(count))], 'depth:',depth)
publish('mast',body,'五档浅凹圆升降柱')
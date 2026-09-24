from math import sin,radians
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
hole=param('mast_detent_square_width',6.4)
depth=param('mast_square_pocket_depth',8.5)
seat_z=h+seat_rise
body=Cylinder(w/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
body=chamfer(body.edges().sort_by(Axis.Z)[0],edge)
bottom=Pos(0,0,h)*Circle(w/2)
top=Pos(0,0,seat_z)*Rot(0,angle,0)*Circle(seat_d/2)
body+=loft([bottom,top])
peg=Pos(0,0,h)*Box(peg_w,peg_w,seat_rise+peg_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
peg=chamfer(peg.edges().group_by(Axis.Z)[-1],edge)
body+=peg
for i in range(int(count)):
 z=first_z+i*pitch
 body-=Pos(-w/2-1,0,z)*Box(depth+1,hole,hole,align=(Align.MIN,Align.CENTER,Align.CENTER))
assert body.is_valid and len(body.solids())==1
assert seat_rise>seat_d/2*sin(radians(angle))
assert first_z-hole/2>edge and first_z+(count-1)*pitch+hole/2<h
assert pitch-hole>=3 and int(count)==5 and abs((count-1)*pitch-40)<1e-6
assert w-depth>3
publish('mast',body,'五档方孔升降柱')
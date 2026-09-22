from math import sin, radians
w=param('mast_width',28.0)
h=param('mast_body_length',62.11808800909513)
peg_w=param('mast_peg_width',16.0)
peg_h=param('mast_peg_height',7.0)
edge=param('mast_edge_chamfer',0.6)
angle=param('mast_seat_angle_deg',10.0)
seat_rise=param('mast_seat_center_rise',9.0)
seat_d=param('mast_seat_diameter',60.0)
seat_z=h+seat_rise
body=Cylinder(w/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
body=chamfer(body.edges().sort_by(Axis.Z)[0],edge)
bottom=Pos(0,0,h)*Circle(w/2)
top=Pos(0,0,seat_z)*Rot(0,angle,0)*Circle(seat_d/2)
body+=loft([bottom,top])
peg=Pos(0,0,h)*Box(peg_w,peg_w,seat_rise+peg_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
peg=chamfer(peg.edges().group_by(Axis.Z)[-1],edge)
body+=peg
assert body.is_valid and len(body.solids())==1
assert seat_rise>seat_d/2*sin(radians(angle))
publish('mast',body,'斜承托台与圆升降柱')
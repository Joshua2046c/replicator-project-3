from math import sqrt, cos, radians, tan
D=param('bowl_diameter',140.0)
Db=param('bowl_bottom_diameter',90.0)
depth=param('bowl_depth',18.0)
wall=param('bowl_wall',3.0)
angle=param('bowl_tilt_deg',10.0)
floor_t=param('bowl_floor_thickness',6.5)
socket_w=param('bowl_socket_outer',30.0)
socket_upper=param('bowl_socket_upper_diameter',60.0)
socket_in=param('bowl_socket_inner',16.5)
socket_drop=param('bowl_socket_drop',14.0)
socket_depth=param('bowl_socket_depth',8.0)
blend=param('bowl_inner_fillet',2.0)
seat_rise=param('bowl_seat_center_rise',9.0)
recess_depth=param('bowl_recess_center_depth',2.0)
recess_clearance=param('bowl_recess_radial_clearance',0.3)
recess_wall=param('bowl_recess_min_wall',3.0)
seat_d=param('bowl_seat_diameter',60.0)
seat_z=-socket_drop+seat_rise
lip_z=seat_z-recess_depth
recess_r=seat_d/2+recess_clearance
outer=Cone(Db/2,D/2,depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
outer=fillet(outer.edges().sort_by(Axis.Z)[0],blend)
slope=(D-Db)/(2*depth)
radial_wall=wall*sqrt(1+slope*slope)
inner_r0=Db/2+slope*floor_t-radial_wall
inner_h=depth-floor_t+2
inner=Pos(0,0,floor_t)*Cone(inner_r0,inner_r0+slope*inner_h,inner_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
inner=fillet(inner.edges().sort_by(Axis.Z)[0],blend)
outer=Rot(0,angle,0)*outer
inner=Rot(0,angle,0)*inner
# Inclined reinforced rim; outer dimensions are lower bounds on the safe wall.
lip_r=max(socket_w/2,recess_r+recess_wall)
socket=Pos(0,0,lip_z)*Rot(0,angle,0)*Cone(lip_r,max(socket_upper/2,lip_r+wall),floor_t-lip_z,align=(Align.CENTER,Align.CENTER,Align.MIN))
body=(outer+socket)-inner
# This inclined groove is vertically swept, not an angled withdrawal undercut.
seat_face=Pos(0,0,seat_z)*Rot(0,angle,0)*Circle(recess_r)
body-=extrude(seat_face,amount=socket_drop+depth,dir=(0,0,-1))
pocket_roof=seat_z+socket_depth
hole=Pos(0,0,lip_z-seat_d)*Box(socket_in,socket_in,pocket_roof-lip_z+seat_d,align=(Align.CENTER,Align.CENTER,Align.MIN))
body-=hole
closing=floor_t/cos(radians(angle))-socket_in/2*tan(radians(angle))-pocket_roof
assert closing>=2.0
assert body.is_valid and len(body.solids())==1
publish('bowl',body,'匹配斜台凹槽可拆碗')
print('seat center',seat_z,'lip',lip_z,'recess diameter',2*recess_r,'pocket closing min',closing)
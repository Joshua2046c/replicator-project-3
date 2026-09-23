from math import sqrt, cos, sin, pi, radians, tan
D=param('bowl_diameter',140.0)
depth=param('bowl_depth',32.0)
wall=param('bowl_wall',3.0)
angle=param('bowl_tilt_deg',10.0)
floor_t=param('bowl_floor_thickness',6.5)
body_scale=param('bowl_body_scale',1.05)
socket_w=param('bowl_socket_outer',30.0)
socket_upper=param('bowl_socket_upper_diameter',60.0)
socket_in=param('bowl_socket_inner',16.5)
socket_drop=param('bowl_socket_drop',14.0)
socket_depth=param('bowl_socket_depth',8.0)
seat_rise=param('bowl_seat_center_rise',9.0)
recess_depth=param('bowl_recess_center_depth',2.0)
recess_clearance=param('bowl_recess_radial_clearance',0.3)
recess_wall=param('bowl_recess_min_wall',3.0)
seat_d=param('bowl_seat_diameter',60.0)
petals=param('bowl_rim_petals',6)
phase=param('bowl_rim_phase_deg',30.0)
# New photo-derived shallow circular-arc petals, not the retired cosine waves.
sag=param('bowl_photo_petal_sag',4.0)*body_scale
arc_span=param('bowl_photo_arc_span',0.96)
D*=body_scale
depth*=body_scale
wall*=body_scale
floor_t*=body_scale
R=((D/2)**2+depth**2)/(2*depth)
inner_depth=depth-floor_t
inner_radius=D/2-wall
Ri=(inner_radius**2+inner_depth**2)/(2*inner_depth)
# Continuous spherical bowl, no large flat floor or straight conical wall.
outer=Pos(0,0,R)*Sphere(R)
clip=Pos(0,0,-1)*Box(3*D,3*D,depth+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
outer=outer & clip
inner=Pos(0,0,floor_t+Ri)*Sphere(Ri)
assert 0<sag<inner_depth and 0<arc_span<1
for j in range(int(petals)):
 sections=[]
 for i in range(33):
  t=-1+2*i/32
  a=radians(phase)-pi/petals+2*pi*j/petals+t*pi/petals
  h=depth-sag*(1-sqrt(1-(arc_span*t)**2))/(1-sqrt(1-arc_span**2))
  r0=D/4
  r1=D
  top=depth+sag+wall
  pts=[(r0*cos(a),r0*sin(a),h),(r1*cos(a),r1*sin(a),h),(r1*cos(a),r1*sin(a),top),(r0*cos(a),r0*sin(a),top)]
  sections.append(Face(Wire(Polyline(*pts,close=True).edges())))
 cutter=loft(sections)
 assert cutter.is_valid
 outer-=cutter
outer=Rot(0,angle,0)*outer
inner=Rot(0,angle,0)*inner
seat_z=-socket_drop+seat_rise
lip_z=seat_z-recess_depth
recess_r=seat_d/2+recess_clearance
lip_r=max(socket_w/2,recess_r+recess_wall)
# Original seat and peg interface dimensions and datum retained.
# Extend the reinforcement into the new curved floor for a true union.
socket_h=floor_t-lip_z+wall
socket=Pos(0,0,lip_z)*Rot(0,angle,0)*Cone(lip_r,max(socket_upper/2,lip_r+wall),socket_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
body=(outer+socket)-inner
seat_face=Pos(0,0,seat_z)*Rot(0,angle,0)*Circle(recess_r)
body-=extrude(seat_face,amount=socket_drop+depth,dir=(0,0,-1))
pocket_roof=seat_z+socket_depth
hole=Pos(0,0,lip_z-seat_d)*Box(socket_in,socket_in,pocket_roof-lip_z+seat_d,align=(Align.CENTER,Align.CENTER,Align.MIN))
body-=hole
closing=floor_t/cos(radians(angle))-socket_in/2*tan(radians(angle))-pocket_roof
assert closing>=2.0
assert body.is_valid and len(body.solids())==1
print('Photo bowl: diameter',D,'depth',depth,'outer sphere R',R,'inner sphere R',Ri,'petal sag',sag,'pocket roof lower bound',closing)
publish('bowl',body,'圆弧浅瓣参考碗')
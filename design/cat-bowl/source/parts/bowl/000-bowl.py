from math import sqrt, cos, sin, pi, radians, tan
D=param('bowl_diameter',140.0)
Db=param('bowl_bottom_diameter',90.0)
depth=param('bowl_depth',32.0)
wall=param('bowl_wall',3.0)
angle=param('bowl_tilt_deg',10.0)
floor_t=param('bowl_floor_thickness',6.5)
socket_w=param('bowl_socket_outer',30.0)
socket_upper=param('bowl_socket_upper_diameter',60.0)
socket_in=param('bowl_socket_inner',16.5)
socket_drop=param('bowl_socket_drop',14.0)
socket_depth=param('bowl_socket_depth',8.0)
blend=param('bowl_inner_fillet',12.0)
seat_rise=param('bowl_seat_center_rise',9.0)
recess_depth=param('bowl_recess_center_depth',2.0)
recess_clearance=param('bowl_recess_radial_clearance',0.3)
recess_wall=param('bowl_recess_min_wall',3.0)
seat_d=param('bowl_seat_diameter',60.0)
petals=param('bowl_rim_petals',6)
wave=param('bowl_rim_radial_relief',6.0)
transition=param('bowl_rim_transition_height',12.0)
phase=param('bowl_rim_phase_deg',30.0)
vertical_relief=param('bowl_rim_vertical_relief',10.0)
seat_z=-socket_drop+seat_rise
lip_z=seat_z-recess_depth
recess_r=seat_d/2+recess_clearance
slope=(D-Db)/(2*depth)
radial_wall=wall*sqrt(1+slope*slope)
outer=Cone(Db/2,D/2,depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
outer=fillet(outer.edges().sort_by(Axis.Z)[0],blend)
inner_r0=Db/2+slope*floor_t-radial_wall
inner_h=depth-floor_t+2
inner=Pos(0,0,floor_t)*Cone(inner_r0,inner_r0+slope*inner_h,inner_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
inner=fillet(inner.edges().sort_by(Axis.Z)[0],blend)
z0=depth-transition
assert z0>floor_t+blend/2 and wave>=0 and int(petals)==petals
# Matching periodic patches preserve the original lower round bowl.
def rim_section(z,inset):
 u=max(0.0,min(1.0,(z-z0)/transition))
 f=u*u*(3-2*u)
 radius=Db/2+slope*z-inset
 edges=[]
 for j in range(int(petals)):
  if u==0:
   edges.append(Pos(0,0,z)*CenterArc((0,0),radius,360*j/petals,360/petals))
  else:
   points=[]
   for i in range(25):
    a=2*pi*(j+i/24)/petals
    r=radius-wave*f*(1+cos(petals*(a-radians(phase))))/2
    points.append((r*cos(a),r*sin(a),z))
   edges.append(Spline(*points))
 return Face(Wire(edges))
lower_clip=Pos(0,0,-depth)*Box(3*D,3*D,depth+z0,align=(Align.CENTER,Align.CENTER,Align.MIN))
z_sections=[z0,z0+transition/6,z0+transition/3,z0+transition/2,z0+2*transition/3,z0+5*transition/6,depth]
outer=(outer & lower_clip)+loft([rim_section(z,0) for z in z_sections])
inner=(inner & lower_clip)+loft([rim_section(z,radial_wall) for z in z_sections+[depth+2]])
assert outer.is_valid and inner.is_valid
# Six smooth radial-sector cutters give the rim real vertical scallops.
# Crest height stays at depth, preserving the accepted highest-rim range.
assert 0<vertical_relief<transition
for j in range(int(petals)):
 sections=[]
 for i in range(17):
  a=radians(phase)+2*pi*(j-0.5+i/16)/petals
  h=depth-vertical_relief*(1+cos(petals*(a-radians(phase))))/2
  r0=Db/2
  r1=D
  top=depth+transition
  pts=[(r0*cos(a),r0*sin(a),h),(r1*cos(a),r1*sin(a),h),(r1*cos(a),r1*sin(a),top),(r0*cos(a),r0*sin(a),top)]
  sections.append(Face(Wire(Polyline(*pts,close=True).edges())))
 cutter=loft(sections)
 assert cutter.is_valid
 outer=outer-cutter
assert outer.is_valid
outer=Rot(0,angle,0)*outer
inner=Rot(0,angle,0)*inner
lip_r=max(socket_w/2,recess_r+recess_wall)
socket=Pos(0,0,lip_z)*Rot(0,angle,0)*Cone(lip_r,max(socket_upper/2,lip_r+wall),floor_t-lip_z,align=(Align.CENTER,Align.CENTER,Align.MIN))
body=(outer+socket)-inner
seat_face=Pos(0,0,seat_z)*Rot(0,angle,0)*Circle(recess_r)
body-=extrude(seat_face,amount=socket_drop+depth,dir=(0,0,-1))
pocket_roof=seat_z+socket_depth
hole=Pos(0,0,lip_z-seat_d)*Box(socket_in,socket_in,pocket_roof-lip_z+seat_d,align=(Align.CENTER,Align.CENTER,Align.MIN))
body-=hole
closing=floor_t/cos(radians(angle))-socket_in/2*tan(radians(angle))-pocket_roof
assert closing>=2.0
assert body.is_valid and len(body.solids())==1
print('Petals',petals,'vertical relief',vertical_relief,'crest local Z',depth,'valley local Z',depth-vertical_relief,'pocket roof',closing)
publish('bowl',body,'立体六瓣花口碗')
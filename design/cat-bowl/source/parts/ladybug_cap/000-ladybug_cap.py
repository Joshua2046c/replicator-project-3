diam=param('ladybug_cap_diameter',28.0)
edge_t=param('ladybug_cap_edge_thickness',4.0)
rise=param('ladybug_cap_dome_rise',6.0)
socket=param('ladybug_cap_socket_width',6.2)
socket_depth=param('ladybug_cap_socket_depth',5.5)
shoulder=param('ladybug_cap_shoulder_recess_width',9.2)
shoulder_depth=param('ladybug_cap_shoulder_recess_depth',1.2)
engrave=param('ladybug_cap_engraving_depth',0.8)
seam=param('ladybug_cap_seam_width',0.7)
head_y=param('ladybug_cap_head_center_y',10.0)
head_r=param('ladybug_cap_head_radius',6.0)
spot_r=param('ladybug_cap_spot_radius',1.7)
spot_x=param('ladybug_cap_spot_offset_x',5.5)
spot_pitch=param('ladybug_cap_spot_row_pitch',5.5)
eye_r=param('ladybug_cap_eye_radius',0.8)
eye_spacing=param('ladybug_cap_eye_spacing',4.4)
eye_y=param('ladybug_cap_eye_y',11.3)
r=diam/2
R=(r*r+rise*rise)/(2*rise)
sphere=Pos(0,0,edge_t+rise-R)*Sphere(R)
clip=Pos(0,0,edge_t)*Box(diam+2,diam+2,rise+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
outer=Cylinder(r,edge_t,align=(Align.CENTER,Align.CENTER,Align.MIN))+(sphere & clip)
# A surface-following engraved skin keeps every mark shallow on the dome.
skin=outer-(Pos(0,0,-engrave)*outer)
ring=Pos(0,head_y,0)*(Cylinder(head_r+seam/2,edge_t+rise+2,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(head_r-seam/2,edge_t+rise+2,align=(Align.CENTER,Align.CENTER,Align.MIN)))
marks=ring+Pos(0,(-r+head_y-head_r)/2,0)*Box(seam,r+head_y-head_r,edge_t+rise+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
for x in [-spot_x,spot_x]:
 for y in [-spot_pitch,0,spot_pitch]:
  marks+=Pos(x,y,0)*Cylinder(spot_r,edge_t+rise+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
for x in [-eye_spacing/2,eye_spacing/2]:
 marks+=Pos(x,eye_y,0)*Cylinder(eye_r,edge_t+rise+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
body=outer-(skin & marks)
body-=Box(shoulder,shoulder,shoulder_depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
body-=Box(socket,socket,socket_depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert edge_t+rise-engrave-socket_depth>=3
assert body.is_valid and len(body.solids())==1
publish('ladybug_cap',body,'圆形瓢虫插接帽')
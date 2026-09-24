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
spot_x=param('ladybug_cap_spot_offset_x',7.0)
spot_pitch=param('ladybug_cap_spot_row_pitch',5.5)
spot_down=param('ladybug_cap_spot_downshift',1.2)
mid_out=param('ladybug_cap_middle_spot_outshift',1.3)
center_y=param('ladybug_cap_center_spot_y',-1.0)
seam_gap=param('ladybug_cap_center_spot_seam_gap',0.45)
eye_r=param('ladybug_cap_eye_radius',0.8)
eye_spacing=param('ladybug_cap_eye_spacing',4.4)
eye_y=param('ladybug_cap_eye_y',11.3)
r=diam/2
R=(r*r+rise*rise)/(2*rise)
sphere=Pos(0,0,edge_t+rise-R)*Sphere(R)
clip=Pos(0,0,edge_t)*Box(diam+2,diam+2,rise+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
outer=Cylinder(r,edge_t,align=(Align.CENTER,Align.CENTER,Align.MIN))+(sphere & clip)
# Same surface-following shallow engravings; rear interface is unchanged.
skin=outer-(Pos(0,0,-engrave)*outer)
cut_h=edge_t+rise+2
ring=Pos(0,head_y,0)*(Cylinder(head_r+seam/2,cut_h,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(head_r-seam/2,cut_h,align=(Align.CENTER,Align.CENTER,Align.MIN)))
wing_seam=Pos(0,(-r+head_y-head_r)/2,0)*Box(seam,r+head_y-head_r,cut_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Interrupt seam locally so the seventh spot reads as a complete circle.
wing_seam-=Pos(0,center_y-spot_down,0)*Cylinder(spot_r+seam_gap,cut_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
marks=ring+wing_seam
for sign in [-1,1]:
 for row in [-1,0,1]:
  x=sign*(spot_x+(mid_out if row==0 else 0))
  y=row*spot_pitch-spot_down
  assert (x*x+y*y)**0.5+spot_r<r
  marks+=Pos(x,y,0)*Cylinder(spot_r,cut_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
marks+=Pos(0,center_y-spot_down,0)*Cylinder(spot_r,cut_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
for x in [-eye_spacing/2,eye_spacing/2]:
 marks+=Pos(x,eye_y,0)*Cylinder(eye_r,cut_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
body=outer-(skin & marks)
body-=Box(shoulder,shoulder,shoulder_depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
body-=Box(socket,socket,socket_depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert edge_t+rise-engrave-socket_depth>=3
assert body.is_valid and len(body.solids())==1
publish('ladybug_cap',body,'圆形瓢虫插接帽')
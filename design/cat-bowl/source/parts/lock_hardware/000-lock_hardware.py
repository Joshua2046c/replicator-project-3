from math import sin,cos,pi
# Stable object ID retained for assembly compatibility; now a threadless square pin.
knob_d=param('lock_screw_knob_diameter',28.0)
knob_h=param('lock_screw_knob_thickness',8.0)
lobes=param('lock_screw_knob_lobes',5)
scallop=param('lock_screw_knob_scallop_radius',6.0)
edge=param('lock_screw_knob_edge_radius',3.0)
width=param('lock_screw_square_width',6.0)
length=param('lock_screw_square_length',14.0)
lead=param('lock_screw_square_tip_chamfer',0.5)
knob=Cylinder(knob_d/2,knob_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
for i in range(int(lobes)):
 a=2*pi*i/lobes
 knob-=Pos((knob_d/2+scallop/2)*cos(a),(knob_d/2+scallop/2)*sin(a),knob_h/2)*Cylinder(scallop,knob_h+2)
knob=fillet(knob.edges().filter_by(Axis.Z),edge)
horizontal=[e for e in knob.edges() if e.bounding_box().size.Z<0.0001]
knob=chamfer(horizontal,edge/2)
shaft=Box(width,width,length,align=(Align.CENTER,Align.CENTER,Align.MAX))
shaft=chamfer(shaft.edges().group_by(Axis.Z)[0],lead)
body=knob+shaft
assert body.is_valid and len(body.solids())==1
publish('lock_screw',body,'五瓣手柄方插销')
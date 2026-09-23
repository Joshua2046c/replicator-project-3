from math import sin,cos,pi
from bd_warehouse.fastener import SocketHeadCapScrew
from bd_warehouse.thread import IsoThread
phase=param('lock_screw_thread_phase_deg',0.0)
visible=param('lock_screw_visible_thread_length',12.0)
knob_d=param('lock_screw_knob_diameter',28.0)
knob_h=param('lock_screw_knob_thickness',8.0)
lobes=param('lock_screw_knob_lobes',6)
scallop=param('lock_screw_knob_scallop_radius',4.0)
edge=param('lock_screw_knob_edge_radius',0.8)
# ISO M5x0.8x12 shaft: bd-warehouse exact catalog envelope. Custom knob, not ISO head.
SIZE='M5-0.8'; MAJOR=5.0; PITCH=0.8; LENGTH=12.0
s=SocketHeadCapScrew(size=SIZE,length=LENGTH,fastener_type='iso4762',simple=True)
t=IsoThread(major_diameter=MAJOR,pitch=PITCH,length=LENGTH,external=True,simple=True)
# Simplified minor-diameter threaded shaft, NOT literal smooth manufactured shank.
core_limit=Cylinder(t.min_radius,LENGTH,align=(Align.CENTER,Align.CENTER,Align.MAX))
core=s & core_limit
TIP_LENGTH=1.5
end=s & Pos(0,0,-LENGTH+TIP_LENGTH/2)*Box(MAJOR+2,MAJOR+2,TIP_LENGTH)
knob=Cylinder(knob_d/2,knob_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
for i in range(int(lobes)):
 a=2*pi*i/lobes
 knob-=Pos((knob_d/2+scallop/2)*cos(a),(knob_d/2+scallop/2)*sin(a),knob_h/2)*Cylinder(scallop,knob_h+2)
knob=fillet(knob.edges().filter_by(Axis.Z),edge)
horizontal=[e for e in knob.edges() if e.bounding_box().size.Z<0.0001]
knob=chamfer(horizontal,edge/2)
body=core.fuse(end,knob)
body=Rot(0,0,phase)*body
assert body.is_valid and len(body.solids())==1
assert abs(body.bounding_box().min.Z+LENGTH)<0.001
print('Nominal M5x0.8x12; simplified core diameter:',2*t.min_radius,'knob:',knob_d,knob_h)
publish('lock_screw',body,'六瓣手拧螺丝（简化螺纹）')
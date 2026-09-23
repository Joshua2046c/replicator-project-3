from math import sin,cos,pi
from bd_warehouse.thread import IsoThread
phase=param('lock_screw_thread_phase_deg',0.0)
visible=param('lock_screw_visible_thread_length',12.0)
knob_d=param('lock_screw_knob_diameter',28.0)
knob_h=param('lock_screw_knob_thickness',8.0)
lobes=param('lock_screw_knob_lobes',6)
scallop=param('lock_screw_knob_scallop_radius',4.0)
edge=param('lock_screw_knob_edge_radius',0.8)
tip_d=param('lock_screw_tip_diameter',5.0)
tip_l=param('lock_screw_tip_length',2.0)
# ISO M6-1 confirmed in bd-warehouse catalog. Custom integral head, not ISO4762 head.
MAJOR=6.0; PITCH=1.0; LENGTH=12.0
assert abs(visible-LENGTH)<1e-6
thread=IsoThread(major_diameter=MAJOR,pitch=PITCH,length=LENGTH,external=True,end_finishes=('raw','raw'),align=(Align.CENTER,Align.CENTER,Align.MAX))
# Same axial phase as the base's expanded screw negative. Clip raw end overruns.
clip=Pos(0,0,-(LENGTH-tip_l)/2)*Box(MAJOR+2,MAJOR+2,LENGTH-tip_l)
teeth=thread & clip
core=Cylinder(thread.min_radius+0.01,LENGTH-tip_l,align=(Align.CENTER,Align.CENTER,Align.MAX))
# Short reduced flat end fits existing5.8 mm pockets without changing the mast.
end=Pos(0,0,-LENGTH)*Cylinder(tip_d/2,tip_l+0.05,align=(Align.CENTER,Align.CENTER,Align.MIN))
knob=Cylinder(knob_d/2,knob_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
for i in range(int(lobes)):
 a=2*pi*i/lobes
 knob-=Pos((knob_d/2+scallop/2)*cos(a),(knob_d/2+scallop/2)*sin(a),knob_h/2)*Cylinder(scallop,knob_h+2)
knob=fillet(knob.edges().filter_by(Axis.Z),edge)
horizontal=[e for e in knob.edges() if e.bounding_box().size.Z<0.0001]
knob=chamfer(horizontal,edge/2)
body=core.fuse(end,knob,*teeth.solids())
body=Rot(0,0,phase)*body
assert body.is_valid and len(body.solids())==1
assert abs(body.bounding_box().min.Z+LENGTH)<0.001
print('Modeled external M6x1, root diameter:',2*(thread.min_radius+0.01),'tip:',tip_d,tip_l)
publish('lock_screw',body,'M6螺纹六瓣手拧螺丝')
from screwjoint import make_screw_joint_v1, ScrewJointNotApplicableV1
from bd_warehouse.thread import IsoThread
base_d=param('base_diameter',160.0)
plate_t=param('base_thickness',8.0)
h=param('base_sleeve_height',66.0)
od=param('base_sleeve_diameter',40.0)
bore=param('base_round_bore',28.6)
floor=param('base_bore_floor',4.0)
flare_r=param('base_flare_radius',39.0)
flare_h=param('base_flare_height',18.0)
lock_z=param('base_lock_height',54.0)
edge_r=param('base_edge_radius',1.5)
engage=param('base_thread_engagement',4.5)
compensation=param('base_thread_diametral_compensation',0.45)
thread_origin=param('base_thread_reference_x',-24.8)
# ISO M6 coarse pitch, catalog bd-warehouse M6-1. Compensation for PETG from kit.
MAJOR=6.0; PITCH=1.0; LENGTH=12.0
body=Cylinder(base_d/2,plate_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
body=fillet(body.edges().filter_by(GeomType.CIRCLE),edge_r)
body+=Pos(0,0,plate_t)*Cylinder(od/2,h-plate_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
root=[e for e in body.edges() if e.geom_type==GeomType.CIRCLE and abs(e.center().Z-plate_t)<1e-5 and abs(e.radius-od/2)<1e-5]
assert len(root)==1
radius=flare_r-od/2
body=fillet(root,radius)
assert abs(radius-flare_h)<1.01
body-=Pos(0,0,floor)*Cylinder(bore/2,h+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
rear=body & Pos(-od/2,0,h/2)*Box(od,od+2,h+2)
frame=Location((-od/2-1,0,lock_z),(0,-90,0))
try:
 joint=make_screw_joint_v1(size='M6',at=frame,through=[],engage_depth=engage,into=rear,head='socket_cap',strategy='molded_thread',termination='through',material='PETG',boss='none',print_axis='horizontal',label='height_lock')
except ScrewJointNotApplicableV1 as exc:
 print('height_lock FREE after kit rejection:',str(exc))
 # A compensated library screw negative, sharing male thread axial origin and hand.
 thread=IsoThread(major_diameter=MAJOR+compensation,pitch=PITCH,length=LENGTH,external=True,end_finishes=('raw','raw'),align=(Align.CENTER,Align.CENTER,Align.MAX))
 cutter=Cylinder(thread.min_radius+0.01,LENGTH,align=(Align.CENTER,Align.CENTER,Align.MAX)).fuse(*thread.solids())
 body=body-(Location((thread_origin,0,lock_z),(0,-90,0))*cutter)
else:
 body=body-joint.engage_cuts
assert body.is_valid and len(body.solids())==1
connections={'round_slide':'free','bowl_detach':'free','height_lock':'free_after_kit_rejection'}
assert len(connections)==3
print('M6x1 internal thread; cutter major',MAJOR+compensation)
publish('base',body,'M6内螺纹圆底座')
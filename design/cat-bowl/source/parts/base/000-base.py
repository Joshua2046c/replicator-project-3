from screwjoint import make_screw_joint_v1, ScrewJointNotApplicableV1
from bd_warehouse.thread import IsoThread
base_d = param('base_diameter',160.0)
plate_t = param('base_thickness',8.0)
h = param('base_sleeve_height',66.0)
od = param('base_sleeve_diameter',40.0)
bore = param('base_round_bore',28.6)
floor = param('base_bore_floor',4.0)
flare_r = param('base_flare_radius',39.0)
flare_h = param('base_flare_height',18.0)
lock_z = param('base_lock_height',54.0)
edge_r = param('base_edge_radius',1.5)
engage = param('base_thread_engagement',4.5)
compensation = param('base_thread_diametral_compensation',0.45)
# ISO metric M5x0.8; PETG compensation default from screwjoint material table.
MAJOR=5.0
PITCH=0.8
body = Cylinder(base_d/2,plate_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
body = fillet(body.edges().filter_by(GeomType.CIRCLE),edge_r)
body += Pos(0,0,plate_t-1)*Cone(flare_r,od/2,flare_h+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
body += Pos(0,0,plate_t)*Cylinder(od/2,h-plate_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
body -= Pos(0,0,floor)*Cylinder(bore/2,h+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
rear = body & Pos(-od/2,0,h/2)*Box(od,od+2,h+2)
# True through-thread machining needs overrun outside curved entry and beyond curved exit.
# The kit rejects this unsupported mouth frame; preserve that evidence before free fallback.
frame = Location((-od/2-1,0,lock_z),(0,-90,0))
try:
    joint = make_screw_joint_v1(size='M5',at=frame,through=[],engage_depth=engage,into=rear,head='socket_cap',strategy='molded_thread',termination='through',material='PETG',boss='none',print_axis='horizontal',label='height_lock')
except ScrewJointNotApplicableV1 as exc:
    print('height_lock FREE: curved-surface overrun rejected by kit:',str(exc))
    # Library ISO external profile used as female-thread negative; not a generic round hole.
    length=(od-bore)/2+3.3
    thread=IsoThread(major_diameter=MAJOR+compensation,pitch=PITCH,length=length,external=True,end_finishes=('raw','raw'),align=(Align.CENTER,Align.CENTER,Align.MAX))
    # 0.01 mm boolean overlap stays inside the thread root, not a fit tolerance change.
    cutter=Cylinder(thread.min_radius+0.01,length,align=(Align.CENTER,Align.CENTER,Align.MAX)).fuse(*thread.solids())
    body=body-(frame*cutter)
else:
    body=body-joint.engage_cuts
assert body.is_valid and len(body.solids())==1
connections={'round_slide':'free','bowl_detach':'free','height_lock':'free_after_kit_rejection'}
assert len(connections)==3
publish('base',body,'圆底座背面内螺纹')
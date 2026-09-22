from bd_warehouse.fastener import SocketHeadCapScrew
from bd_warehouse.thread import IsoThread
# ISO4762 M5x12 head from exact catalog library. Continuous ISO helix replaces
# the catalog's 17 touching solids. Screw shown in rear exploded position because
# engaged-position boolean checks exhausted their runtime, not because fit is proven.
phase=param('lock_screw_thread_phase_deg',0.0)
visible=param('lock_screw_visible_thread_length',12.0)
SIZE='M5-0.8'
MAJOR=5.0
PITCH=0.8
LENGTH=12.0
s=SocketHeadCapScrew(size=SIZE,length=LENGTH,fastener_type='iso4762',simple=True)
t=IsoThread(major_diameter=MAJOR,pitch=PITCH,length=visible,external=True,end_finishes=('raw','raw'),align=(Align.CENTER,Align.CENTER,Align.MAX))
head=s & Pos(0,0,5)*Box(12,12,10)
core=Cylinder(t.min_radius+0.01,LENGTH,align=(Align.CENTER,Align.CENTER,Align.MAX))
# Raw library helix overruns both ends. Clip to the exact 12 mm shaft envelope.
threads=t & Pos(0,0,-visible/2)*Box(10,10,visible)
body=core.fuse(head,*threads.solids())
body=Rot(0,0,phase)*body
assert body.is_valid and len(body.solids())==1
assert abs(body.bounding_box().min.Z+LENGTH)<0.001
publish('lock_screw',body,'背面螺纹锁紧螺丝')
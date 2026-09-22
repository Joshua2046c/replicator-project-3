from math import sqrt, sin, cos, radians
D = param('bowl_diameter',140.0)
Db = param('bowl_bottom_diameter',90.0)
depth = param('bowl_depth',18.0)
wall = param('bowl_wall',3.0)
angle = param('bowl_tilt_deg',10.0)
# Existing socket outer parameter now describes the circular lower diameter.
socket_w = param('bowl_socket_outer',30.0)
socket_upper = param('bowl_socket_upper_diameter',60.0)
socket_in = param('bowl_socket_inner',16.5)
socket_drop = param('bowl_socket_drop',14.0)
socket_depth = param('bowl_socket_depth',12.0)
blend = param('bowl_inner_fillet',2.0)
shoulder_w = param('bowl_socket_shoulder_width',22.0)
relief_h = param('bowl_socket_bottom_relief',0.8)
outer = Cone(Db/2,D/2,depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
outer = fillet(outer.edges().sort_by(Axis.Z)[0],blend)
slope = (D-Db)/(2*depth)
radial_wall = wall*sqrt(1+slope*slope)
inner_r0 = Db/2+slope*wall-radial_wall
inner_h = depth-wall+2
inner = Pos(0,0,wall)*Cone(inner_r0,inner_r0+slope*inner_h,inner_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
inner = fillet(inner.edges().sort_by(Axis.Z)[0],blend)
outer = Rot(0,angle,0)*outer
inner = Rot(0,angle,0)*inner
# Rounded tapered reinforcement merges into bowl floor; only the receiving pocket is square.
socket = Pos(0,0,-socket_drop+relief_h)*Cone(socket_w/2,socket_upper/2,socket_drop+wall-relief_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
shoulder=Pos(0,0,-socket_drop)*Cylinder(shoulder_w/2,relief_h+wall,align=(Align.CENTER,Align.CENTER,Align.MIN))
body = (outer+socket+shoulder)-inner
hole = Pos(0,0,-socket_drop-1)*Box(socket_in,socket_in,socket_depth+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
body -= hole
assert len(body.solids())==1
assert socket_drop-socket_depth > socket_in/2*sin(radians(angle))
publish('bowl',body,'加厚底部可拆斜碗')
print('rim high above origin',depth*cos(radians(angle))+D/2*sin(radians(angle)))
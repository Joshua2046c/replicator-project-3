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
hole=param('base_pin_hole_width',6.4)
body=Cylinder(base_d/2,plate_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
body=fillet(body.edges().filter_by(GeomType.CIRCLE),edge_r)
body+=Pos(0,0,plate_t)*Cylinder(od/2,h-plate_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
root=[e for e in body.edges() if e.geom_type==GeomType.CIRCLE and abs(e.center().Z-plate_t)<1e-5 and abs(e.radius-od/2)<1e-5]
assert len(root)==1
body=fillet(root,flare_r-od/2)
assert abs(flare_r-od/2-flare_h)<1.01
body-=Pos(0,0,floor)*Cylinder(bore/2,h+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Rear side square passage ends in the round guide bore; no front opening or thread.
body-=Pos(-od/2-1,0,lock_z)*Box(od/2+1,hole,hole,align=(Align.MIN,Align.CENTER,Align.CENTER))
assert body.is_valid and len(body.solids())==1
connections={'round_slide':'free','bowl_detach':'free','height_lock':'free_square_pin'}
assert len(connections)==3
publish('base',body,'方孔圆底座')
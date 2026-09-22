# mast_width retained as editable transverse size, now round diameter.
w = param('mast_width',22.0)
h = param('mast_body_length',62.11808800909513)
peg_w = param('mast_peg_width',16.0)
peg_h = param('mast_peg_height',11.0)
edge = param('mast_edge_chamfer',0.6)
body = Cylinder(w/2,h,align=(Align.CENTER,Align.CENTER,Align.MIN))
body = chamfer(body.edges().sort_by(Axis.Z)[0],edge)
peg = Pos(0,0,h)*Box(peg_w,peg_w,peg_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
peg = chamfer(peg.edges().group_by(Axis.Z)[-1],edge)
body += peg
assert len(body.solids())==1
publish('mast',body,'圆形升降柱与方榫')
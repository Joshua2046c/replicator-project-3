width=param('lock_screw_square_width',6.0)
length=param('lock_screw_square_length',14.0)
lead=param('lock_screw_square_tip_chamfer',0.5)
shoulder=param('lock_screw_shoulder_width',9.0)
st=param('lock_screw_shoulder_thickness',1.2)
tongue=param('lock_screw_cap_tongue_length',4.0)
shaft=Box(width,width,length,align=(Align.CENTER,Align.CENTER,Align.MAX))
shaft=chamfer(shaft.edges().group_by(Axis.Z)[0],lead)
body=shaft+Box(shoulder,shoulder,st,align=(Align.CENTER,Align.CENTER,Align.MIN))
tip=Pos(0,0,st)*Box(width,width,tongue,align=(Align.CENTER,Align.CENTER,Align.MIN))
tip=chamfer(tip.edges().group_by(Axis.Z)[-1],lead)
body+=tip
assert body.is_valid and len(body.solids())==1
publish('lock_screw',body,'独立双端方销')
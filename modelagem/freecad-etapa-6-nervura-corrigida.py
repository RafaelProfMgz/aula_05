import FreeCAD as App
import FreeCADGui as Gui
import Part, Sketcher, math
from FreeCAD import Vector

doc = App.getDocument("suporte")
body = doc.getObject("corpo")
body.Tip = doc.getObject("furo_passante")
for nome in ("nervura", "esboco_nervura"):
    if doc.getObject(nome):
        doc.removeObject(nome)
doc.recompute()

E, Y1, Y2, Z1, Z2 = 8.0, 10.0, 30.0, 10.0, 35.0
sk = doc.addObject("Sketcher::SketchObject", "esboco_nervura")
body.addObject(sk)
sk.Placement = App.Placement(Vector(50, 0, 0), App.Rotation(Vector(1, 1, 1), 120))

tri = [(Y1, Z1), (Y2, Z1), (Y1, Z2)]
for i in range(3):
    a, b = tri[i], tri[(i + 1) % 3]
    sk.addGeometry(Part.LineSegment(Vector(a[0], a[1], 0), Vector(b[0], b[1], 0)), False)
for i in range(3):
    sk.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i + 1) % 3, 1))
sk.addConstraint(Sketcher.Constraint("Horizontal", 0))
sk.addConstraint(Sketcher.Constraint("Vertical", 2))
sk.addConstraint(Sketcher.Constraint("Distance", 0, Y2 - Y1))
sk.renameConstraint(sk.ConstraintCount - 1, "comprimento_nervura")
sk.addConstraint(Sketcher.Constraint("Distance", 2, Z2 - Z1))
sk.renameConstraint(sk.ConstraintCount - 1, "altura_nervura")
sk.addConstraint(Sketcher.Constraint("DistanceX", -1, 1, 0, 1, Y1))
sk.renameConstraint(sk.ConstraintCount - 1, "nervura_em_y")
sk.addConstraint(Sketcher.Constraint("DistanceY", -1, 1, 0, 1, Z1))
sk.renameConstraint(sk.ConstraintCount - 1, "nervura_em_z")
sk.solve(); doc.recompute()
print("esboco_nervura: restringido=%s redundantes=%s | bbox global: %s"
      % (sk.FullyConstrained, list(sk.RedundantConstraints), sk.Shape.BoundBox))

pad = doc.addObject("PartDesign::Pad", "nervura")
body.addObject(pad); pad.Profile = sk; pad.Length = E; pad.Midplane = True
sk.Visibility = False
doc.recompute()

bb = body.Shape.BoundBox
vol = body.Shape.Volume
esp = 61857.3 + 0.5 * (Y2 - Y1) * (Z2 - Z1) * E
print("ETAPA 6 - nervura de reforco")
print("   caixa envolvente mm : %.2f x %.2f x %.2f" % (bb.XLength, bb.YLength, bb.ZLength))
print("   volume mm3          : %.1f  (esperado %.1f, erro %.4f)" % (vol, esp, vol - esp))
print("   espessura           : %.2f mm, centrada em X=50 (X de %.1f a %.1f)" % (E, 50 - E / 2, 50 + E / 2))
print("   altura              : %.2f mm acima do topo da base" % (Z2 - Z1))
print("   comprimento na base : %.2f mm (Y de %.1f a %.1f)" % (Y2 - Y1, Y1, Y2))
print("   folga ate o rasgo   : %.2f mm (rasgo comeca em Y=32.5)" % (32.5 - Y2))
print("   nervura bbox        :", pad.Shape.BoundBox)
v = Gui.ActiveDocument.ActiveView
v.viewIsometric(); v.fitAll()
v.saveImage("/home/angel/tep/aula05/capturas/etapa-6-nervura.png", 1280, 720, "White")
print("   captura             : etapa-6-nervura.png")
print()
print("HISTORICO:", [o.Name for o in body.Group])
print("solidos:", len(body.Shape.Solids), "| shape valido:", body.Shape.isValid())
doc.save()

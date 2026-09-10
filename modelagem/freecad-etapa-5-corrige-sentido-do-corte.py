import FreeCAD as App
import FreeCADGui as Gui
import math
doc = App.getDocument("suporte")
body = doc.getObject("corpo")
pk = doc.getObject("furo_passante")
pk.Reversed = True
doc.recompute()
print("estado do furo:", pk.State)

vol = body.Shape.Volume
e5 = 73195.2 - math.pi * 12.5 ** 2 * 15
e6 = e5 + 0.5 * 35 * 40 * 10
bb = body.Shape.BoundBox
print("ETAPA 5 + 6 recalculadas pelo historico")
print("   volume final mm3 : %.1f  (esperado %.1f, erro %+.4f)" % (vol, e6, vol - e6))
print("   caixa envolvente : %.2f x %.2f x %.2f" % (bb.XLength, bb.YLength, bb.ZLength))
print("   solidos: %d | valido: %s" % (len(body.Shape.Solids), body.Shape.isValid()))

# confere o furo na geometria
cil = [f for f in body.Shape.Faces if f.Surface.__class__.__name__ == "Cylinder"]
for f in cil:
    s = f.Surface
    if abs(s.Radius - 12.5) < 0.01:
        print("   furo MEDIDO: Ø%.2f mm | eixo em Y=%.2f Z=%.2f | direcao %s"
              % (2 * s.Radius, s.Center.y, s.Center.z, tuple(round(c, 3) for c in s.Axis)))
    if abs(s.Radius - 20.0) < 0.01:
        print("   arco do canto MEDIDO: R%.2f | centro Y=%.2f Z=%.2f" % (s.Radius, s.Center.y, s.Center.z))

v = Gui.ActiveDocument.ActiveView
for nome in ("etapa-5-furo-passante.png", "etapa-6-nervura.png"):
    v.viewIsometric(); v.fitAll()
    v.saveImage("/home/angel/tep/aula05/capturas/" + nome, 1280, 720, "White")
print("   capturas 5 e 6 refeitas")
doc.save()

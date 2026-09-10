import FreeCAD as App
import FreeCADGui as Gui
import Part, Sketcher, math
from FreeCAD import Vector

CAP = "/home/angel/tep/aula05/capturas/"

def sk_novo(doc, body, nome, placement):
    sk = doc.addObject("Sketcher::SketchObject", nome)
    body.addObject(sk)
    sk.Placement = placement
    return sk

def retangulo(sk, u1, v1, u2, v2):
    pts = [(u1, v1), (u2, v1), (u2, v2), (u1, v2)]
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        sk.addGeometry(Part.LineSegment(Vector(a[0], a[1], 0), Vector(b[0], b[1], 0)), False)
    for i in range(4):
        sk.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i + 1) % 4, 1))
    for i, t in ((0, "Horizontal"), (2, "Horizontal"), (1, "Vertical"), (3, "Vertical")):
        sk.addConstraint(Sketcher.Constraint(t, i))

def cota(sk, tipo, *args, nome=None):
    sk.addConstraint(Sketcher.Constraint(tipo, *args))
    if nome:
        sk.renameConstraint(sk.ConstraintCount - 1, nome)

def est(sk):
    sk.solve()
    return "restringido=%s redundantes=%s" % (sk.FullyConstrained, list(sk.RedundantConstraints))

def captura(nome):
    v = Gui.ActiveDocument.ActiveView
    v.viewIsometric(); v.fitAll()
    v.saveImage(CAP + nome, 1280, 720, "White")
    return nome

def medir(body, titulo, esperado):
    bb = body.Shape.BoundBox
    vol = body.Shape.Volume
    print(titulo)
    print("   caixa envolvente mm : %.2f x %.2f x %.2f" % (bb.XLength, bb.YLength, bb.ZLength))
    print("   volume mm3          : %.1f  (esperado %.1f, erro %+.4f)" % (vol, esperado, vol - esperado))

for d in list(App.listDocuments()):
    App.closeDocument(d)
doc = App.newDocument("suporte")
Gui.ActiveDocument = Gui.getDocument("suporte")
body = doc.addObject("PartDesign::Body", "corpo")

XY  = App.Placement(Vector(0, 0, 0),  App.Rotation(0, 0, 0, 1))
YZ  = App.Placement(Vector(0, 0, 0),  App.Rotation(Vector(1, 1, 1), 120))   # u=Y, v=Z, normal=+X
XZ90 = App.Placement(Vector(0, 90, 0), App.Rotation(Vector(1, 0, 0), 90))   # u=X, v=Z

# ================================================= ETAPA 1 - base 100 x 50 x 10
sk = sk_novo(doc, body, "esboco_base", XY)
retangulo(sk, 0, 0, 50, 100)
cota(sk, "DistanceX", 0, 1, 0, 2, 50.0,  nome="largura_base")
cota(sk, "DistanceY", 1, 1, 1, 2, 100.0, nome="comprimento_base")
cota(sk, "DistanceX", -1, 1, 0, 1, 0.0)
cota(sk, "DistanceY", -1, 1, 0, 1, 0.0)
print("esboco_base:", est(sk))
pad = doc.addObject("PartDesign::Pad", "extrusao_base")
body.addObject(pad); pad.Profile = sk
cota_esp = 10.0
pad.Length = cota_esp
sk.Visibility = False
doc.recompute()
medir(body, "ETAPA 1 - base 100 x 50 x 10", 50000.0)
print("   captura:", captura("etapa-1-base.png"))

# ================================================= ETAPA 2 - rasgo oblongo
R, CX, Y1, Y2 = 7.5, 25.0, 15.0, 40.0
sk = sk_novo(doc, body, "esboco_rasgo", App.Placement(Vector(0, 0, 10), App.Rotation(0, 0, 0, 1)))
n = Vector(0, 0, 1)
# arco inferior (180->360) e arco superior (0->180), unidos por dois lados verticais
sk.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(CX, Y1, 0), n, R), math.pi, 2 * math.pi), False)  # 0
sk.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(CX, Y2, 0), n, R), 0.0, math.pi), False)          # 1
sk.addGeometry(Part.LineSegment(Vector(CX + R, Y1, 0), Vector(CX + R, Y2, 0)), False)                # 2
sk.addGeometry(Part.LineSegment(Vector(CX - R, Y2, 0), Vector(CX - R, Y1, 0)), False)                # 3
for a, b in ((0, 2), (2, 1), (1, 3), (3, 0)):
    sk.addConstraint(Sketcher.Constraint("Coincident", a, 2, b, 1))
sk.addConstraint(Sketcher.Constraint("Vertical", 2))
sk.addConstraint(Sketcher.Constraint("Equal", 0, 1))
cota(sk, "Radius", 0, R, nome="raio_rasgo")
cota(sk, "DistanceY", 0, 3, 1, 3, Y2 - Y1, nome="distancia_centros")
cota(sk, "DistanceX", -1, 1, 0, 3, CX, nome="rasgo_centrado_na_largura")
cota(sk, "DistanceY", -1, 1, 0, 3, Y1, nome="rasgo_ate_aresta_frontal")
print("esboco_rasgo:", est(sk))
pk = doc.addObject("PartDesign::Pocket", "rasgo_oblongo")
body.addObject(pk); pk.Profile = sk; pk.Type = 1
sk.Visibility = False
doc.recompute()
e2 = 50000.0 - ((Y2 - Y1) * 2 * R + math.pi * R * R) * 10
medir(body, "ETAPA 2 - rasgo oblongo passante", e2)
print("   centros dos arcos   : Y=%.1f e Y=%.1f (afastados %.1f mm)" % (Y1, Y2, Y2 - Y1))
print("   centrado na largura : X=%.1f de 50.0" % CX)
print("   captura:", captura("etapa-2-rasgo-oblongo.png"))

# ================================================= ETAPA 3 - parede vertical
ESP_PAREDE, YP1, YP2, ZP1, ZP2 = 15.0, 50.0, 100.0, 10.0, 50.0
sk = sk_novo(doc, body, "esboco_parede", YZ)
retangulo(sk, YP1, ZP1, YP2, ZP2)
cota(sk, "DistanceX", 0, 1, 0, 2, YP2 - YP1, nome="comprimento_parede")
cota(sk, "DistanceY", 1, 1, 1, 2, ZP2 - ZP1, nome="altura_parede")
cota(sk, "DistanceX", -1, 1, 0, 1, YP1, nome="parede_em_y")
cota(sk, "DistanceY", -1, 1, 0, 1, ZP1)
print("esboco_parede:", est(sk))
pad = doc.addObject("PartDesign::Pad", "extrusao_parede")
body.addObject(pad); pad.Profile = sk; pad.Length = ESP_PAREDE
sk.Visibility = False
doc.recompute()
e3 = e2 + (YP2 - YP1) * (ZP2 - ZP1) * ESP_PAREDE
medir(body, "ETAPA 3 - parede vertical", e3)
print("   espessura: %.1f mm (X de 0 a %.1f) | altura ate Z=%.1f" % (ESP_PAREDE, ESP_PAREDE, ZP2))
print("   captura:", captura("etapa-3-parede-vertical.png"))

# ================================================= ETAPA 4 - canto arredondado R20
RT = 20.0
alvo = None
for i, e in enumerate(pad.Shape.Edges):
    vs = e.Vertexes
    if len(vs) == 2:
        ys = [round(p.Y, 3) for p in vs]; zs = [round(p.Z, 3) for p in vs]; xs = [round(p.X, 3) for p in vs]
        if ys == [YP1, YP1] and zs == [ZP2, ZP2] and xs[0] != xs[1]:
            alvo = "Edge%d" % (i + 1)
print("   aresta do canto:", alvo)
fil = doc.addObject("PartDesign::Fillet", "canto_arredondado")
body.addObject(fil)
fil.Base = (pad, [alvo])
fil.Radius = RT
doc.recompute()
print("   estado do filete:", fil.State)
e4 = e3 - (RT * RT - math.pi * RT * RT / 4) * ESP_PAREDE
medir(body, "ETAPA 4 - canto arredondado R20", e4)
CY, CZ = YP1 + RT, ZP2 - RT
print("   centro do arco      : Y=%.1f  Z=%.1f" % (CY, CZ))
print("   tangencia: arco R20 encosta na face Y=%.1f e no topo Z=%.1f" % (YP1, ZP2))
print("   captura:", captura("etapa-4-canto-arredondado.png"))

# ================================================= ETAPA 5 - furo Ø25
D = 25.0
sk = sk_novo(doc, body, "esboco_furo", YZ)
sk.addGeometry(Part.Circle(Vector(CY, CZ, 0), n, D / 2), False)
cota(sk, "Diameter", 0, D, nome="diametro_furo")
cota(sk, "DistanceX", -1, 1, 0, 3, CY, nome="furo_em_y")
cota(sk, "DistanceY", -1, 1, 0, 3, CZ, nome="furo_em_z")
print("esboco_furo:", est(sk))
pk = doc.addObject("PartDesign::Pocket", "furo_passante")
body.addObject(pk); pk.Profile = sk; pk.Type = 1
sk.Visibility = False
doc.recompute()
e5 = e4 - math.pi * (D / 2) ** 2 * ESP_PAREDE
medir(body, "ETAPA 5 - furo passante Ø25", e5)
print("   centro do furo      : Y=%.1f  Z=%.1f" % (CY, CZ))
print("   centro do arco R20  : Y=%.1f  Z=%.1f  -> CONCENTRICO" % (CY, CZ))
print("   altura do centro sobre o topo da base: %.1f mm" % (CZ - 10.0))
print("   captura:", captura("etapa-5-furo-passante.png"))

# ================================================= ETAPA 6 - nervura triangular
EN, XN1, XN2, ZN1, ZN2 = 10.0, 15.0, 50.0, 10.0, 50.0
sk = sk_novo(doc, body, "esboco_nervura", XZ90)
tri = [(XN1, ZN1), (XN2, ZN1), (XN1, ZN2)]
for i in range(3):
    a, b = tri[i], tri[(i + 1) % 3]
    sk.addGeometry(Part.LineSegment(Vector(a[0], a[1], 0), Vector(b[0], b[1], 0)), False)
for i in range(3):
    sk.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i + 1) % 3, 1))
sk.addConstraint(Sketcher.Constraint("Horizontal", 0))
sk.addConstraint(Sketcher.Constraint("Vertical", 2))
cota(sk, "Distance", 0, XN2 - XN1, nome="base_nervura")
cota(sk, "Distance", 2, ZN2 - ZN1, nome="altura_nervura")
cota(sk, "DistanceX", -1, 1, 0, 1, XN1, nome="nervura_em_x")
cota(sk, "DistanceY", -1, 1, 0, 1, ZN1)
print("esboco_nervura:", est(sk))
pad = doc.addObject("PartDesign::Pad", "nervura")
body.addObject(pad); pad.Profile = sk; pad.Length = EN; pad.Reversed = True
sk.Visibility = False
doc.recompute()
e6 = e5 + 0.5 * (XN2 - XN1) * (ZN2 - ZN1) * EN
medir(body, "ETAPA 6 - nervura triangular", e6)
print("   espessura: %.1f mm (Y de 90 a 100) | cateto na base %.1f | cateto vertical %.1f"
      % (EN, XN2 - XN1, ZN2 - ZN1))
print("   encosta na parede em X=%.1f (face externa da parede)" % XN1)
print("   captura:", captura("etapa-6-nervura.png"))

print()
print("HISTORICO:", [o.Name for o in body.Group])
print("solidos: %d | shape valido: %s" % (len(body.Shape.Solids), body.Shape.isValid()))
bb = body.Shape.BoundBox
print("caixa envolvente final: %.2f x %.2f x %.2f mm" % (bb.XLength, bb.YLength, bb.ZLength))
doc.saveAs("/home/angel/tep/aula05/suporte.FCStd")
print("salvo: suporte.FCStd")

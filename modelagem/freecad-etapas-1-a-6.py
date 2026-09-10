import FreeCAD as App
import FreeCADGui as Gui
import Part, Sketcher, math
from FreeCAD import Vector

CAP = "/home/angel/tep/aula05/capturas/"

def novo_sk(doc, body, nome, placement):
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
    sk.addConstraint(Sketcher.Constraint("Horizontal", 0))
    sk.addConstraint(Sketcher.Constraint("Horizontal", 2))
    sk.addConstraint(Sketcher.Constraint("Vertical", 1))
    sk.addConstraint(Sketcher.Constraint("Vertical", 3))

def cota(sk, tipo, *args, nome=None):
    sk.addConstraint(Sketcher.Constraint(tipo, *args))
    if nome:
        sk.renameConstraint(sk.ConstraintCount - 1, nome)

def estado(sk):
    sk.solve()
    return ("restringido=%s redundantes=%s conflitantes=%s"
            % (sk.FullyConstrained, list(sk.RedundantConstraints), list(sk.ConflictingConstraints)))

def captura(nome):
    v = Gui.ActiveDocument.ActiveView
    v.viewIsometric(); v.fitAll()
    v.saveImage(CAP + nome, 1280, 720, "White")
    return nome

def medir(body, titulo, esperado=None):
    bb = body.Shape.BoundBox
    vol = body.Shape.Volume
    print("%s" % titulo)
    print("   caixa envolvente mm : %.2f x %.2f x %.2f" % (bb.XLength, bb.YLength, bb.ZLength))
    if esperado is not None:
        print("   volume mm3          : %.1f  (esperado %.1f, erro %.4f)" % (vol, esperado, vol - esperado))
    else:
        print("   volume mm3          : %.1f" % vol)
    return bb, vol

# ---------------------------------------------------------------- documento
for d in list(App.listDocuments()):
    App.closeDocument(d)
doc = App.newDocument("suporte")
Gui.ActiveDocument = Gui.getDocument("suporte")
body = doc.addObject("PartDesign::Body", "corpo")

XY = App.Placement(Vector(0, 0, 0), App.Rotation(0, 0, 0, 1))
XZ = App.Placement(Vector(0, 0, 0), App.Rotation(Vector(1, 0, 0), 90))
YZ = App.Placement(Vector(50, 0, 0), App.Rotation(Vector(1, 1, 1), 120))

# ---------------------------------------------------------------- ETAPA 1
sk = novo_sk(doc, body, "esboco_base", XY)
retangulo(sk, 0, 0, 100, 50)
cota(sk, "DistanceX", 0, 1, 0, 2, 100.0, nome="comprimento_base")
cota(sk, "DistanceY", 1, 1, 1, 2, 50.0, nome="largura_base")
cota(sk, "DistanceX", -1, 1, 0, 1, 0.0)
cota(sk, "DistanceY", -1, 1, 0, 1, 0.0)
print("esboco_base:", estado(sk))
pad = doc.addObject("PartDesign::Pad", "extrusao_base")
body.addObject(pad); pad.Profile = sk; pad.Length = 10.0
sk.Visibility = False
doc.recompute()
medir(body, "ETAPA 1 - base 100 x 50 x 10", 50000.0)
print("   captura             :", captura("etapa-1-base.png"))

# ---------------------------------------------------------------- ETAPA 2
R, CY, X1, X2 = 7.5, 40.0, 37.5, 62.5
sk = novo_sk(doc, body, "esboco_rasgo", App.Placement(Vector(0, 0, 10), App.Rotation(0, 0, 0, 1)))
n = Vector(0, 0, 1)
sk.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(X1, CY, 0), n, R), math.pi / 2, 3 * math.pi / 2), False)
sk.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(X2, CY, 0), n, R), -math.pi / 2, math.pi / 2), False)
sk.addGeometry(Part.LineSegment(Vector(X1, CY - R, 0), Vector(X2, CY - R, 0)), False)
sk.addGeometry(Part.LineSegment(Vector(X2, CY + R, 0), Vector(X1, CY + R, 0)), False)
for a, b in ((0, 2), (2, 1), (1, 3), (3, 0)):
    sk.addConstraint(Sketcher.Constraint("Coincident", a, 2, b, 1))
sk.addConstraint(Sketcher.Constraint("Horizontal", 2))
sk.addConstraint(Sketcher.Constraint("Equal", 0, 1))
cota(sk, "Radius", 0, R, nome="raio_rasgo")
cota(sk, "DistanceX", 0, 3, 1, 3, 25.0, nome="distancia_centros")
cota(sk, "DistanceY", -1, 1, 0, 3, CY, nome="rasgo_ate_aresta_frontal")
cota(sk, "DistanceX", -1, 1, 0, 3, X1, nome="rasgo_em_x")
print("esboco_rasgo:", estado(sk))
pk = doc.addObject("PartDesign::Pocket", "rasgo_oblongo")
body.addObject(pk); pk.Profile = sk; pk.Type = 1
sk.Visibility = False
doc.recompute()
esp2 = 50000.0 - (25 * 15 + math.pi * R * R) * 10
medir(body, "ETAPA 2 - rasgo oblongo passante", esp2)
print("   centro -> aresta frontal (Y=0)  : %.2f mm" % CY)
print("   centro -> aresta traseira (Y=50): %.2f mm" % (50 - CY))
print("   centro em X                     : %.2f mm" % ((X1 + X2) / 2))
print("   captura             :", captura("etapa-2-rasgo-oblongo.png"))

# ---------------------------------------------------------------- ETAPA 3
sk = novo_sk(doc, body, "esboco_parede", XZ)
retangulo(sk, 30, 0, 70, 50)
cota(sk, "DistanceX", 0, 1, 0, 2, 40.0, nome="largura_parede")
cota(sk, "DistanceY", 1, 1, 1, 2, 50.0, nome="altura_parede_reta")
cota(sk, "DistanceX", -1, 1, 0, 1, 30.0, nome="parede_em_x")
cota(sk, "DistanceY", -1, 1, 0, 1, 0.0)
print("esboco_parede:", estado(sk))
pad = doc.addObject("PartDesign::Pad", "extrusao_parede")
body.addObject(pad); pad.Profile = sk; pad.Length = 10.0; pad.Reversed = True
sk.Visibility = False
doc.recompute()
esp3 = esp2 + (40 * 50 - 40 * 10) * 10
medir(body, "ETAPA 3 - parede vertical", esp3)
print("   espessura da parede : 10.00 mm")
print("   altura reta         : 50.00 mm (ate o centro do arco do topo)")
print("   captura             :", captura("etapa-3-parede-vertical.png"))

# ---------------------------------------------------------------- ETAPA 4
CX, CZ, RT = 50.0, 50.0, 20.0
sk = novo_sk(doc, body, "esboco_topo", XZ)
sk.addGeometry(Part.ArcOfCircle(Part.Circle(Vector(CX, CZ, 0), n, RT), 0.0, math.pi), False)
sk.addGeometry(Part.LineSegment(Vector(CX - RT, CZ, 0), Vector(CX + RT, CZ, 0)), False)
sk.addConstraint(Sketcher.Constraint("Coincident", 0, 2, 1, 1))
sk.addConstraint(Sketcher.Constraint("Coincident", 1, 2, 0, 1))
cota(sk, "Radius", 0, RT, nome="raio_topo")
cota(sk, "DistanceX", -1, 1, 0, 3, CX, nome="topo_em_x")
cota(sk, "DistanceY", -1, 1, 0, 3, CZ, nome="topo_em_z")
print("esboco_topo:", estado(sk))
pad = doc.addObject("PartDesign::Pad", "topo_arredondado")
body.addObject(pad); pad.Profile = sk; pad.Length = 10.0; pad.Reversed = True
sk.Visibility = False
doc.recompute()
esp4 = esp3 + math.pi * RT * RT / 2 * 10
medir(body, "ETAPA 4 - topo arredondado R20", esp4)
for z in (50.0, 55.0, 60.0, 65.0, 69.0):
    sec = body.Shape.slice(App.Vector(0, 0, 1), z)
    if sec:
        xmin = min(w.BoundBox.XMin for w in sec); xmax = max(w.BoundBox.XMax for w in sec)
        teo = 40.0 if z <= 50 else 2 * math.sqrt(max(RT * RT - (z - CZ) ** 2, 0))
        print("   Z=%5.1f largura %6.2f mm (teorica %6.2f, erro %+.4f)" % (z, xmax - xmin, teo, xmax - xmin - teo))
print("   tangencia: largura em Z=50 igual a da parede (40.00) -> arco tangente as laterais")
print("   captura             :", captura("etapa-4-topo-arredondado.png"))

# ---------------------------------------------------------------- ETAPA 5
D = 25.0
sk = novo_sk(doc, body, "esboco_furo", XZ)
sk.addGeometry(Part.Circle(Vector(CX, CZ, 0), n, D / 2), False)
cota(sk, "Diameter", 0, D, nome="diametro_furo")
cota(sk, "DistanceX", -1, 1, 0, 3, CX, nome="furo_em_x")
cota(sk, "DistanceY", -1, 1, 0, 3, CZ, nome="furo_em_z")
print("esboco_furo:", estado(sk))
pk = doc.addObject("PartDesign::Pocket", "furo_passante")
body.addObject(pk); pk.Profile = sk; pk.Type = 1
sk.Visibility = False
doc.recompute()
esp5 = esp4 - math.pi * (D / 2) ** 2 * 10
medir(body, "ETAPA 5 - furo passante Ø25", esp5)
print("   centro do furo      : X=%.2f  Z=%.2f" % (CX, CZ))
print("   centro do arco topo : X=%.2f  Z=%.2f  -> concentrico" % (CX, CZ))
print("   captura             :", captura("etapa-5-furo-passante.png"))

# ---------------------------------------------------------------- ETAPA 6
E, Y1, Y2, Z1, Z2 = 8.0, 10.0, 30.0, 10.0, 35.0
sk = novo_sk(doc, body, "esboco_nervura", YZ)
tri = [(Y1, Z1), (Y2, Z1), (Y1, Z2)]
for i in range(3):
    a, b = tri[i], tri[(i + 1) % 3]
    sk.addGeometry(Part.LineSegment(Vector(a[0], a[1], 0), Vector(b[0], b[1], 0)), False)
for i in range(3):
    sk.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i + 1) % 3, 1))
sk.addConstraint(Sketcher.Constraint("Horizontal", 0))
sk.addConstraint(Sketcher.Constraint("Vertical", 2))
cota(sk, "DistanceX", 0, 1, 0, 2, Y2 - Y1, nome="comprimento_nervura")
cota(sk, "DistanceY", 2, 1, 2, 2, Z2 - Z1, nome="altura_nervura")
cota(sk, "DistanceX", -1, 1, 0, 1, Y1, nome="nervura_em_y")
cota(sk, "DistanceY", -1, 1, 0, 1, Z1, nome="nervura_em_z")
print("esboco_nervura:", estado(sk))
pad = doc.addObject("PartDesign::Pad", "nervura")
body.addObject(pad); pad.Profile = sk; pad.Length = E; pad.Midplane = True
sk.Visibility = False
doc.recompute()
esp6 = esp5 + 0.5 * (Y2 - Y1) * (Z2 - Z1) * E
medir(body, "ETAPA 6 - nervura de reforco", esp6)
print("   espessura da nervura: %.2f mm (centrada em X=50)" % E)
print("   altura              : %.2f mm acima da base" % (Z2 - Z1))
print("   comprimento na base : %.2f mm (Y de %.1f a %.1f)" % (Y2 - Y1, Y1, Y2))
print("   captura             :", captura("etapa-6-nervura.png"))

# ---------------------------------------------------------------- fechamento
print()
print("HISTORICO:", [o.Name for o in body.Group])
print("solidos no corpo:", len(body.Shape.Solids), "-> corpo unico:", len(body.Shape.Solids) == 1)
print("shape valido:", body.Shape.isValid())
doc.saveAs("/home/angel/tep/aula05/suporte.FCStd")
print("documento salvo: suporte.FCStd")

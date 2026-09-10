import FreeCAD as App
import FreeCADGui as Gui
import Import, Mesh, math, time, os

doc = App.getDocument("suporte")
body = doc.getObject("corpo")
sk = doc.getObject("esboco_furo")
S = "/home/angel/tep/aula05/saidas/"
v = Gui.ActiveDocument.ActiveView

# ---------------------------------------------------------------- PASSO 8 (Ø25)
def exporta(base):
    Import.export([body], S + base + ".step")
    Mesh.export([body], S + base + ".stl")
    m = Mesh.Mesh(S + base + ".stl")
    return os.path.getsize(S + base + ".step"), os.path.getsize(S + base + ".stl"), m.CountFacets

st, sl, nf = exporta("suporte")
print("PASSO 8 - exportacao da peca do desenho (furo Ø25)")
print("   suporte.step %6d bytes | suporte.stl %6d bytes, %d facetas" % (st, sl, nf))
print("   volume: %.1f mm3" % body.Shape.Volume)
v.viewIsometric(); v.fitAll()
v.saveImage("/home/angel/tep/aula05/capturas/passo-8-exportacao.png", 1280, 720, "White")

# ---------------------------------------------------------------- PASSO 7 (Ø25 -> Ø30)
antes = body.Shape.Volume
nops = len(body.Group)
print()
print("PASSO 7 - alteracao da cota pelo historico")
print("   antes : diametro_furo = %s | volume %.1f mm3" % (sk.getDatum("diametro_furo"), antes))
t0 = time.perf_counter()
sk.setDatum("diametro_furo", App.Units.Quantity("30 mm"))
doc.recompute()
t1 = time.perf_counter()
depois = body.Shape.Volume
esperado = antes + math.pi * (12.5 ** 2 - 15.0 ** 2) * 15
print("   depois: diametro_furo = %s | volume %.1f mm3" % (sk.getDatum("diametro_furo"), depois))
print("   tempo de recalculo  : %.3f s" % (t1 - t0))
print("   volume esperado     : %.1f | obtido %.1f | erro %+.4f" % (esperado, depois, depois - esperado))
print("   operacoes: %d antes, %d depois -> nenhuma acrescentada" % (nops, len(body.Group)))
print("   solidos: %d | valido: %s" % (len(body.Shape.Solids), body.Shape.isValid()))

print()
print("   conferencia de que nada mais mudou:")
for nome, cotas in (("esboco_base", ["largura_base", "comprimento_base"]),
                    ("esboco_rasgo", ["raio_rasgo", "distancia_centros", "rasgo_ate_aresta_frontal"]),
                    ("esboco_parede", ["comprimento_parede", "altura_parede"]),
                    ("esboco_nervura", ["base_nervura", "altura_nervura"])):
    s = doc.getObject(nome)
    print("      %-16s %s" % (nome + ":", ", ".join("%s=%s" % (c, s.getDatum(c)) for c in cotas)))
print("      canto_arredondado: R%s" % doc.getObject("canto_arredondado").Radius)

for f in body.Shape.Faces:
    s = f.Surface
    if s.__class__.__name__ == "Cylinder" and abs(s.Radius - 15.0) < 0.01:
        print("   furo MEDIDO na geometria: Ø%.2f mm" % (2 * s.Radius))
print("   parede remanescente entre o furo Ø30 e o arco R20: %.1f mm" % (20.0 - 15.0))

v.viewIsometric(); v.fitAll()
v.saveImage("/home/angel/tep/aula05/capturas/passo-7-furo-30mm.png", 1280, 720, "White")
st2, sl2, nf2 = exporta("suporte-furo30")
print("   exportado tambem: suporte-furo30.step (%d bytes) e .stl (%d facetas)" % (st2, nf2))
doc.save()

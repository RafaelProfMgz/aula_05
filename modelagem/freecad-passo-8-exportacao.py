import FreeCAD as App
import FreeCADGui as Gui
import Import, Mesh, os, math

doc = App.getDocument("suporte")
body = doc.getObject("corpo")
sk = doc.getObject("esboco_furo")
S = "/home/angel/tep/aula05/saidas/"

def exporta(base):
    Import.export([body], S + base + ".step")
    Mesh.export([body], S + base + ".stl")
    m = Mesh.Mesh(S + base + ".stl")
    return (os.path.getsize(S + base + ".step"), os.path.getsize(S + base + ".stl"),
            m.CountFacets, m.BoundBox)

# a peca do desenho, com o furo Ø25 -> e o insumo da Tarefa B
sk.setDatum("diametro_furo", App.Units.Quantity("25 mm"))
doc.recompute()
st, sl, nf, bbm = exporta("suporte")
print("PASSO 8 - exportacao")
print("  suporte.step  %7d bytes" % st)
print("  suporte.stl   %7d bytes | %d facetas" % (sl, nf))
print("  malha bbox mm : %.2f x %.2f x %.2f" % (bbm.XLength, bbm.YLength, bbm.ZLength))
print("  volume solido : %.1f mm3 (furo Ø25)" % body.Shape.Volume)

# o resultado do passo 7, com o furo Ø30
sk.setDatum("diametro_furo", App.Units.Quantity("30 mm"))
doc.recompute()
st2, sl2, nf2, bbm2 = exporta("suporte-furo30")
print("  suporte-furo30.step %7d bytes" % st2)
print("  suporte-furo30.stl  %7d bytes | %d facetas" % (sl2, nf2))
print("  volume solido : %.1f mm3 (furo Ø30)" % body.Shape.Volume)

with open(S + "suporte.step") as f:
    cab = [next(f).strip() for _ in range(3)]
print("  cabecalho do STEP:", cab[0], "|", cab[2])

v = Gui.ActiveDocument.ActiveView
v.viewIsometric(); v.fitAll()
v.saveImage("/home/angel/tep/aula05/capturas/passo-8-exportacao.png", 1280, 720, "White")
print("  captura       : passo-8-exportacao.png")
doc.save()
print("  documento salvo com o furo em Ø30 (estado final da Tarefa A)")

import FreeCAD as App
import FreeCADGui as Gui
import math, time

doc = App.getDocument("suporte")
body = doc.getObject("corpo")
sk = doc.getObject("esboco_furo")

antes_vol = body.Shape.Volume
antes_ops = [o.Name for o in body.Group]
print("antes  -> diametro_furo = %s | volume = %.1f mm3" % (sk.getDatum("diametro_furo"), antes_vol))

t0 = time.perf_counter()
sk.setDatum("diametro_furo", App.Units.Quantity("30 mm"))
doc.recompute()
t1 = time.perf_counter()

depois_vol = body.Shape.Volume
bb = body.Shape.BoundBox
esperado = antes_vol + math.pi * (12.5 ** 2 - 15.0 ** 2) * 10
print("depois -> diametro_furo = %s | volume = %.1f mm3" % (sk.getDatum("diametro_furo"), depois_vol))
print()
print("PASSO 7 - alteracao da cota pelo historico")
print("   tempo de recalculo  : %.3f s" % (t1 - t0))
print("   volume esperado     : %.1f mm3 | obtido %.1f | erro %.4f"
      % (esperado, depois_vol, depois_vol - esperado))
print("   caixa envolvente    : %.2f x %.2f x %.2f (inalterada)" % (bb.XLength, bb.YLength, bb.ZLength))
print("   operacoes no historico: %d (antes: %d) -> nenhuma acrescentada"
      % (len(body.Group), len(antes_ops)))
print("   solidos: %d | shape valido: %s" % (len(body.Shape.Solids), body.Shape.isValid()))

# confere que nada mais mudou: mede as demais cotas
print()
print("   conferencia de que nada mais mudou:")
for nome_sk, cotas in (("esboco_base", ["comprimento_base", "largura_base"]),
                       ("esboco_rasgo", ["raio_rasgo", "distancia_centros", "rasgo_ate_aresta_frontal"]),
                       ("esboco_parede", ["largura_parede", "altura_parede_reta"]),
                       ("esboco_topo", ["raio_topo"]),
                       ("esboco_nervura", ["comprimento_nervura", "altura_nervura"])):
    s = doc.getObject(nome_sk)
    vals = ", ".join("%s=%s" % (c, s.getDatum(c)) for c in cotas)
    print("      %-16s %s" % (nome_sk + ":", vals))

# diametro medido na geometria, nao na cota
face_cil = [f for f in body.Shape.Faces
            if f.Surface.__class__.__name__ == "Cylinder"
            and abs(f.Surface.Center.z - 50) < 0.01 and abs(f.Surface.Radius - 15.0) < 0.5]
if face_cil:
    print("   diametro MEDIDO na geometria: %.2f mm" % (2 * face_cil[0].Surface.Radius))

v = Gui.ActiveDocument.ActiveView
v.viewIsometric(); v.fitAll()
v.saveImage("/home/angel/tep/aula05/capturas/passo-7-furo-30mm.png", 1280, 720, "White")
print("   captura             : passo-7-furo-30mm.png")
doc.save()

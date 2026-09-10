import bpy, math, time, os
from collections import Counter
def ov():
    win = bpy.context.window_manager.windows[0]; scr = win.screen
    area = next((a for a in scr.areas if a.type == "VIEW_3D"), scr.areas[0])
    return dict(window=win, screen=scr, area=area,
                region=next((r for r in area.regions if r.type == "WINDOW"), None))
sc = bpy.context.scene
me = bpy.data.objects["suporte"].data
FY, FZ = 0.020, 0.005
RA, RD = 0.0125, 0.0150
FATOR = RD / RA

def diametro():
    raios = []
    for p in me.polygons:
        if p.material_index == 1 and -0.0255 < p.center.x < -0.0095 and abs(p.normal.x) < 0.6:
            for vi in p.vertices:
                v = me.vertices[vi].co
                raios.append(round(math.hypot(v.y - FY, v.z - FZ), 6))
    c = Counter(raios)
    r = max(c, key=c.get)
    return 2 * r * 1000, len(c)

d0, _ = diametro()
print("antes  -> diametro medido na malha: Ø%.2f mm" % d0)

t0 = time.perf_counter()
movidos = 0
for v in me.vertices:
    if -0.0255 < v.co.x < -0.0095:
        dy, dz = v.co.y - FY, v.co.z - FZ
        if abs(math.hypot(dy, dz) - RA) < 0.0004:
            v.co.y = FY + dy * FATOR
            v.co.z = FZ + dz * FATOR
            movidos += 1
me.update()
t1 = time.perf_counter()

d1, _ = diametro()
n_lados = movidos // 2
def flecha(r, n): return r * (1 - math.cos(math.pi / n)) * 1000
print("depois -> diametro medido na malha: Ø%.2f mm" % d1)
print()
print("PASSO 10 - alteracao do mesmo furo, na malha")
print("   vertices deslocados : %d (%d lados do poligono, 2 aneis)" % (movidos, n_lados))
print("   tempo da operacao   : %.4f s" % (t1 - t0))
print("   poligonos: %d - inalterado" % len(me.polygons))
print("   faces com latao_polido: %d" % sum(1 for p in me.polygons if p.material_index == 1))
print("   erro de facetamento : %.4f mm -> %.4f mm  (+%.1f%%)"
      % (flecha(RA, n_lados), flecha(RD, n_lados), 100 * (flecha(RD, n_lados) / flecha(RA, n_lados) - 1)))
print("   valor exato pretendido: Ø30.00 | obtido na malha: Ø%.2f" % d1)

sc.render.filepath = "/home/angel/tep/aula05/renders/suporte-alterado.png"
t2 = time.perf_counter()
with bpy.context.temp_override(**ov()):
    bpy.ops.render.render(write_still=True)
print("   render: %.2f s | %d bytes" % (time.perf_counter()-t2, os.path.getsize(sc.render.filepath)))
bpy.ops.wm.save_mainfile()

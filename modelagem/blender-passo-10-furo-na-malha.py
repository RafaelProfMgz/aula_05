import bpy, math, time, os
from mathutils import Vector

def ov():
    win = bpy.context.window_manager.windows[0]; scr = win.screen
    area = next((a for a in scr.areas if a.type == "VIEW_3D"), scr.areas[0])
    return dict(window=win, screen=scr, area=area,
                region=next((r for r in area.regions if r.type == "WINDOW"), None))

sc = bpy.context.scene
obj = bpy.data.objects["suporte"]
me = obj.data
CZ = 0.015                 # eixo do furo em Z (coordenada local)
R_ANTES, R_DEPOIS = 0.0125, 0.0150
FATOR = R_DEPOIS / R_ANTES

def mede_furo():
    raios = []
    for v in me.vertices:
        if -0.0251 < v.co.y < -0.0149:
            r = math.hypot(v.co.x, v.co.z - CZ)
            if 0.0100 < r < 0.0175:
                raios.append(r)
    return raios

antes = mede_furo()
print("antes  -> vertices no furo: %d | raio %.4f a %.4f m -> diametro %.2f mm"
      % (len(antes), min(antes), max(antes), 2 * max(antes) * 1000))

# ---- a alteracao propriamente dita, cronometrada
t0 = time.perf_counter()
alterados = 0
for v in me.vertices:
    if -0.0251 < v.co.y < -0.0149:
        dx, dz = v.co.x, v.co.z - CZ
        r = math.hypot(dx, dz)
        if abs(r - R_ANTES) < 0.0004:
            v.co.x = dx * FATOR
            v.co.z = CZ + dz * FATOR
            alterados += 1
me.update()
t1 = time.perf_counter()

depois = mede_furo()
print("depois -> vertices movidos: %d | raio %.4f a %.4f m -> diametro %.2f mm"
      % (alterados, min(depois), max(depois), 2 * max(depois) * 1000))
print()
print("PASSO 10 - alteracao do mesmo furo, na malha")
print("   tempo da operacao   : %.3f s" % (t1 - t0))
print("   poligonos: %d (inalterado) | facetas do furo: as mesmas, agora sobre um circulo maior"
      % len(me.polygons))

# o que a malha NAO sabe: nao ha historico, nada recalcula.
# confere se o material do furo sobreviveu
n_mat1 = sum(1 for p in me.polygons if p.material_index == 1)
print("   faces com latao_polido apos a alteracao: %d" % n_mat1)

# erro de facetamento antes e depois (corda x arco)
n_lados = len([v for v in me.vertices if -0.0251 < v.co.y < -0.0149
               and abs(math.hypot(v.co.x, v.co.z - CZ) - R_DEPOIS) < 0.0004]) // 2
if n_lados:
    def flecha(r, n):
        return r * (1 - math.cos(math.pi / n)) * 1000
    print("   lados do poligono do furo: %d" % n_lados)
    print("   erro de facetamento: %.4f mm antes -> %.4f mm depois (+%.1f%%)"
          % (flecha(R_ANTES, n_lados), flecha(R_DEPOIS, n_lados),
             100 * (flecha(R_DEPOIS, n_lados) / flecha(R_ANTES, n_lados) - 1)))

sc.render.filepath = "/home/angel/tep/aula05/renders/suporte-alterado.png"
t2 = time.perf_counter()
with bpy.context.temp_override(**ov()):
    bpy.ops.render.render(write_still=True)
t3 = time.perf_counter()
print("   render: %.2f s | %s (%d bytes)"
      % (t3 - t2, sc.render.filepath, os.path.getsize(sc.render.filepath)))
bpy.ops.wm.save_mainfile()

import bpy, math, time, os
from mathutils import Vector, Matrix

def ov():
    win = bpy.context.window_manager.windows[0]
    scr = win.screen
    area = next((a for a in scr.areas if a.type == "VIEW_3D"), scr.areas[0])
    region = next((r for r in area.regions if r.type == "WINDOW"), None)
    return dict(window=win, screen=scr, area=area, region=region)

t0 = time.perf_counter()
bpy.ops.wm.read_homefile(use_empty=True)
sc = bpy.context.scene

# ---------------------------------------------------------- importa o STL
antes = set(bpy.data.objects.keys())
with bpy.context.temp_override(**ov()):
    bpy.ops.wm.stl_import(filepath="/home/angel/tep/aula05/saidas/suporte.stl")
novos = [bpy.data.objects[n] for n in bpy.data.objects.keys() if n not in antes]
obj = novos[0]
obj.name = "suporte"
me = obj.data
me.name = "malha_suporte"

def caixa(mesh):
    xs = [v.co.x for v in mesh.vertices]
    ys = [v.co.y for v in mesh.vertices]
    zs = [v.co.z for v in mesh.vertices]
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))

mn, mx = caixa(me)
print("STL importado (unidades do arquivo): %.2f x %.2f x %.2f"
      % (mx[0] - mn[0], mx[1] - mn[1], mx[2] - mn[2]))

# mm -> metro, direto nos vertices (sem operador)
me.transform(Matrix.Scale(0.001, 4))
# centraliza a origem na peca, medindo os vertices e nao o bound_box do objeto
mn, mx = caixa(me)
centro = Vector(((mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, (mn[2] + mx[2]) / 2))
me.transform(Matrix.Translation(-centro))
obj.location = (0, 0, 0)
me.update()

mn, mx = caixa(me)
print("importado : %s | dimensoes mm: %.2f x %.2f x %.2f | poligonos: %d"
      % (obj.name, (mx[0] - mn[0]) * 1000, (mx[1] - mn[1]) * 1000,
         (mx[2] - mn[2]) * 1000, len(me.polygons)))
print("            faixa Z local: %.4f a %.4f m" % (mn[2], mx[2]))

# suavizacao apenas nas faces curvas (normal fora dos eixos)
n_suave = 0
for pol in me.polygons:
    n = pol.normal
    eixo = max(abs(n.x), abs(n.y), abs(n.z))
    if eixo < 0.999:
        pol.use_smooth = True
        n_suave += 1
print("faces curvas suavizadas: %d de %d" % (n_suave, len(me.polygons)))

# ---------------------------------------------------------- dois materiais
def material(nome, cor, metal, rug):
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = cor
    p.inputs["Metallic"].default_value = metal
    p.inputs["Roughness"].default_value = rug
    return m

corpo = material("aco_pintado",  (0.16, 0.22, 0.30, 1.0), 0.0, 0.42)
furos = material("latao_polido", (0.72, 0.52, 0.18, 1.0), 1.0, 0.18)
me.materials.append(corpo)
me.materials.append(furos)

# peca centrada: furo no eixo Y, x=0, z=+0.015 ; base em z de -0.035 a -0.025
CFZ, RF = 0.015, 0.0125
n_furo = n_rasgo = 0
for pol in me.polygons:
    c = pol.center
    if abs(c.y) < 0.0055 and math.hypot(c.x, c.z - CFZ) < RF * 1.15 and abs(pol.normal.y) < 0.6:
        pol.material_index = 1; n_furo += 1; continue
    if -0.0349 < c.z < -0.0251 and abs(pol.normal.z) < 0.5:
        dy = c.y - 0.015
        dx = max(abs(c.x) - 0.0125, 0.0)
        if math.hypot(dx, dy) < 0.0090:
            pol.material_index = 1; n_rasgo += 1
print("materiais : %s / %s | faces no 2o material: %d (furo) + %d (rasgo)"
      % (corpo.name, furos.name, n_furo, n_rasgo))

# ---------------------------------------------------------- chao (sem operador)
mc = bpy.data.meshes.new("malha_chao")
mc.from_pydata([(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)], [], [(0, 1, 2, 3)])
mc.update()
chao = bpy.data.objects.new("chao", mc)
sc.collection.objects.link(chao)
chao.location = (0, 0, -0.0351)
mc.materials.append(material("chao_neutro", (0.35, 0.35, 0.38, 1.0), 0.0, 0.7))

# ---------------------------------------------------------- iluminacao de tres pontos
def luz(nome, energia, pos, tamanho):
    dados = bpy.data.lights.new(nome, type="AREA")
    dados.energy = energia
    dados.size = tamanho
    o = bpy.data.objects.new(nome, dados)
    sc.collection.objects.link(o)
    o.location = pos
    o.rotation_euler = (Vector((0, 0, 0.005)) - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
    return o

luz("luz_principal",     120.0, (0.22, -0.20, 0.22), 0.30)
luz("luz_preenchimento",  35.0, (-0.26, -0.16, 0.10), 0.45)
luz("luz_contorno",       90.0, (-0.10, 0.26, 0.20), 0.25)

# ---------------------------------------------------------- camera
cd = bpy.data.cameras.new("camera")
cd.lens = 55
cam = bpy.data.objects.new("camera", cd)
sc.collection.objects.link(cam)
cam.location = (0.16, -0.14, 0.105)
cam.rotation_euler = (Vector((0, 0, 0.002)) - cam.location).to_track_quat("-Z", "Y").to_euler()
sc.camera = cam

# ---------------------------------------------------------- render
sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x = 1920
sc.render.resolution_y = 1080
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = "/home/angel/tep/aula05/renders/suporte.png"
mundo = bpy.data.worlds.new("mundo")
mundo.use_nodes = True
mundo.node_tree.nodes["Background"].inputs[0].default_value = (0.045, 0.05, 0.06, 1)
sc.world = mundo

t1 = time.perf_counter()
with bpy.context.temp_override(**ov()):
    bpy.ops.render.render(write_still=True)
t2 = time.perf_counter()

p = sc.render.filepath
print()
print("TAREFA B - cena montada e renderizada")
print("   objetos           : %s" % sorted(o.name for o in sc.objects))
print("   materiais na malha: %s" % [m.name for m in me.materials])
print("   resolucao         : %dx%d | motor: %s" % (sc.render.resolution_x, sc.render.resolution_y, sc.render.engine))
print("   montagem: %.2f s | render: %.2f s" % (t1 - t0, t2 - t1))
print("   arquivo : %s (%d bytes)" % (p, os.path.getsize(p) if os.path.exists(p) else -1))
bpy.ops.wm.save_as_mainfile(filepath="/home/angel/tep/aula05/suporte.blend")
print("   cena salva: suporte.blend")

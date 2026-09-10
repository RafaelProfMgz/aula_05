import bpy, math, time, os
from mathutils import Vector, Matrix

def ov():
    win = bpy.context.window_manager.windows[0]; scr = win.screen
    area = next((a for a in scr.areas if a.type == "VIEW_3D"), scr.areas[0])
    return dict(window=win, screen=scr, area=area,
                region=next((r for r in area.regions if r.type == "WINDOW"), None))

def caixa(m):
    xs = [v.co.x for v in m.vertices]; ys = [v.co.y for v in m.vertices]; zs = [v.co.z for v in m.vertices]
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))

t0 = time.perf_counter()
bpy.ops.wm.read_homefile(use_empty=True)
sc = bpy.context.scene

antes = set(bpy.data.objects.keys())
with bpy.context.temp_override(**ov()):
    bpy.ops.wm.stl_import(filepath="/home/angel/tep/aula05/saidas/suporte.stl")
obj = [bpy.data.objects[n] for n in bpy.data.objects.keys() if n not in antes][0]
obj.name = "suporte"
me = obj.data; me.name = "malha_suporte"

mn, mx = caixa(me)
print("STL importado (unidades do arquivo): %.2f x %.2f x %.2f" % (mx[0]-mn[0], mx[1]-mn[1], mx[2]-mn[2]))
me.transform(Matrix.Scale(0.001, 4))                       # mm -> metro
mn, mx = caixa(me)
centro = Vector([(mn[i] + mx[i]) / 2 for i in range(3)])
me.transform(Matrix.Translation(-centro))
obj.location = (0, 0, 0); me.update()
mn, mx = caixa(me)
print("importado : dimensoes mm: %.2f x %.2f x %.2f | poligonos: %d"
      % ((mx[0]-mn[0])*1000, (mx[1]-mn[1])*1000, (mx[2]-mn[2])*1000, len(me.polygons)))

n_suave = 0
for pol in me.polygons:
    n = pol.normal
    if max(abs(n.x), abs(n.y), abs(n.z)) < 0.999:
        pol.use_smooth = True; n_suave += 1
print("faces curvas suavizadas: %d de %d" % (n_suave, len(me.polygons)))

def material(nome, cor, metal, rug):
    m = bpy.data.materials.new(nome); m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = cor
    p.inputs["Metallic"].default_value = metal
    p.inputs["Roughness"].default_value = rug
    return m

me.materials.append(material("aco_pintado",  (0.10, 0.14, 0.20, 1.0), 0.0, 0.42))
me.materials.append(material("latao_polido", (0.72, 0.52, 0.18, 1.0), 1.0, 0.18))

# peca centrada: furo eixo X em (Y=+0.020, Z=+0.005), parede em X de -0.025 a -0.010
# rasgo: base em Z de -0.025 a -0.015, eixo em X=0, Y de -0.035 a -0.010
FY, FZ, RF = 0.020, 0.005, 0.0125
n_furo = n_rasgo = 0
for pol in me.polygons:
    c = pol.center
    if -0.0255 < c.x < -0.0095 and math.hypot(c.y - FY, c.z - FZ) < RF * 1.15 and abs(pol.normal.x) < 0.6:
        pol.material_index = 1; n_furo += 1; continue
    if -0.0249 < c.z < -0.0151 and abs(pol.normal.z) < 0.5:
        dy = max(-0.035 - c.y, c.y + 0.010, 0.0)
        if math.hypot(c.x, dy) < 0.0090:
            pol.material_index = 1; n_rasgo += 1
print("faces no 2o material: %d (furo) + %d (rasgo)" % (n_furo, n_rasgo))

mc = bpy.data.meshes.new("malha_chao")
mc.from_pydata([(-1,-1,0),(1,-1,0),(1,1,0),(-1,1,0)], [], [(0,1,2,3)]); mc.update()
chao = bpy.data.objects.new("chao", mc); sc.collection.objects.link(chao)
chao.location = (0, 0, -0.0251)
mc.materials.append(material("chao_neutro", (0.20, 0.20, 0.22, 1.0), 0.0, 0.7))

alvo = Vector((0, 0, 0.002))
def luz(nome, energia, pos, tam):
    d = bpy.data.lights.new(nome, type="AREA"); d.energy = energia; d.size = tam
    o = bpy.data.objects.new(nome, d); sc.collection.objects.link(o)
    o.location = pos
    o.rotation_euler = (alvo - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
luz("luz_principal",     16.0, (-0.26, -0.24, 0.26), 0.30)
luz("luz_preenchimento",  5.0, ( 0.30, -0.20, 0.10), 0.50)
luz("luz_contorno",      10.0, ( 0.06,  0.30, 0.24), 0.24)

cd = bpy.data.cameras.new("camera"); cd.lens = 50
cam = bpy.data.objects.new("camera", cd); sc.collection.objects.link(cam)
cam.location = (-0.22, -0.235, 0.165)
cam.rotation_euler = (alvo - cam.location).to_track_quat("-Z", "Y").to_euler()
sc.camera = cam

sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x = 1920; sc.render.resolution_y = 1080
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = "/home/angel/tep/aula05/renders/suporte.png"
w = bpy.data.worlds.new("mundo"); w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.035, 0.04, 0.05, 1)
sc.world = w
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Base Contrast"

t1 = time.perf_counter()
with bpy.context.temp_override(**ov()):
    bpy.ops.render.render(write_still=True)
t2 = time.perf_counter()
print()
print("TAREFA B - cena montada e renderizada")
print("   objetos : %s" % sorted(o.name for o in sc.objects))
print("   materiais: %s" % [m.name for m in me.materials])
print("   %dx%d | %s | montagem %.2f s | render %.2f s | %d bytes"
      % (sc.render.resolution_x, sc.render.resolution_y, sc.render.engine,
         t1-t0, t2-t1, os.path.getsize(sc.render.filepath)))
bpy.ops.wm.save_as_mainfile(filepath="/home/angel/tep/aula05/suporte.blend")

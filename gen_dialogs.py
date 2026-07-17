# Генератор диалогов dcs (схема спеццветов — в шапке text.vsh).
# Локализация: тексты в lang-файлах (ru_ru/en_us), окна = translate-компоненты.
# Окно может быть двухстрочным: вторая строка кодируется в lang-значении negative-space
# глифами (шрифт dcs:offsets, биты E100..E108 = -1..-256, E110..E118 = +1..+256):
#   значение row2 = [минус ширина row1][текст][добивка до ширины объединения строк]
# — ширины считаются на каждый язык отдельно, поэтому вёрстка верна и в ru, и в en.
import json, os
from PIL import Image

# --- ПУТИ. По умолчанию пишет в resourcepack/ и datapack/ рядом с этим файлом.
# Для работы прямо в карту укажи абсолютные пути к её ресурспаку и датапаку.
BASE = os.path.dirname(os.path.abspath(__file__))
RP = os.path.join(BASE, "resourcepack")                # ресурспак: сюда пишутся lang, отсюда читаются PNG шрифтов
JARFONT = os.path.join(BASE, "mcfont")                 # распакованные из client.jar ванильные шрифты (замеры ширин)
OUT = os.path.join(BASE, "datapack", "data", "dcs", "function", "npc")   # функции окон
NL = chr(10)
os.makedirs(os.path.join(OUT, "dialog"), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(OUT), "dialog"), exist_ok=True)

# --- таблица advance по провайдерам vanilla + текстурам ресурспака ---
providers = json.load(open(os.path.join(JARFONT, "assets/minecraft/font/include/default.json"), encoding="utf-8"))["providers"]
ADV = {" ": 4}

for p in providers:
    tex_rel = p["file"].replace("minecraft:", "minecraft/textures/")
    path = os.path.join(RP, "assets", tex_rel)
    if not os.path.exists(path):
        path = os.path.join(JARFONT, "assets", tex_rel)
    img = Image.open(path).convert("RGBA")
    rows = p["chars"]
    cw, chh = img.size[0] // len(rows[0]), img.size[1] // len(rows)
    scale = p.get("height", 8) / chh
    alpha = img.getchannel("A").load()
    for ri, row in enumerate(rows):
        for ci, ch in enumerate(row):
            if ch == "\x00" or ch in ADV:
                continue
            x0, y0 = ci * cw, ri * chh
            w = 0
            for x in range(cw - 1, -1, -1):
                if any(alpha[x0 + x, y0 + y] > 0 for y in range(chh)):
                    w = x + 1
                    break
            if w:
                ADV[ch] = int(0.5 + w * scale) + 1

ADV["🍄"] = 9  # глиф-мухомор: bitmap-провайдер в оверрайде minecraft:font/default.json, height 8

def width(s, bold=False):
    total = 0
    for ch in s:
        if ch not in ADV:
            raise KeyError(f"нет глифа для {ch!r} — добавь вручную")
        total += ADV[ch] + (1 if bold and ch != " " else 0)
    return total

def off_str(px):
    """строка спейсер-глифов суммарной ширины px (|px| <= 511)"""
    if px == 0:
        return ""
    base = 0xE100 if px < 0 else 0xE110
    n = abs(px)
    assert n <= 511, f"спейсер вне диапазона: {px}"
    return "".join(chr(base + i) for i in range(9) if n >> i & 1)

ICON_ADV = 17
ICON_CHARS = {1: "\\uE001", 2: "\\uE002", 3: "\\uE003", 4: "\\uE004", 5: "\\uE005"}
PALETTE = {1: (60, 190, 100), 2: (255, 130, 40), 3: (85, 255, 255),
           4: (255, 255, 85), 5: (255, 70, 60)}

def dim(rgb, step):
    k = (step + 1) / 8
    return "#%02X%02X%02X" % tuple(round(v * k) for v in rgb)

# --- контент: окно = (ru, en); строка либо "текст", либо ("ряд 1", "ряд 2") ---
npcs = {
    "jagermeistars": (1, "JagerMeistars", "block.note_block.guitar", 0.7, {
        "bracket": [
            (("Ёкарный бабай, почему опять не работает?", "А, скобка..."),
             ("For crying out loud, why is it broken AGAIN?", "Oh. A bracket..."))],
        "shaders": [
            (("Шейдер на освещение, шейдер на анимации,", "пост-эффекты..."),
             ("A shader for lighting, a shader for animations,", "post-effects...")),
            ("Я что вам, эксперт по шейдерам?",
             "What am I, some kind of shader expert?"),
            ("А, ну да.",
             "Oh. Right. I am.")],
        "call": [
            (("А? Алексей зовёт? Опять забыл, как код писать?", "Сейчас подойду..."),
             ("Hm? Alexey's calling? Forgot how to write code", "again? Coming, coming..."))]}),
    "chayosi": (2, "Chayosi", "block.note_block.pling", 0.9, {
        "model": [
            ("Так-с... Нужно создать модель скибиди туалета.",
             "So... Time to model a skibidi toilet."),
            (("Этот кубик вот такой ширины,", "этот — вот такой высоты..."),
             ("This cube goes this wide,", "and this one — this tall...")),
            (("Пиксель там, пиксель здесь...", "Иии... Моделька готова!"),
             ("A pixel here, a pixel there...", "Aaand... the model's done!")),
            ("Аа, точно, ещё анимировать надо...",
             "Ah, right. Still gotta animate it...")],
        "tired": [
            (("Я, конечно, стараюсь делать всё побыстрее,", "но мне таааак тягостно..."),
             ("I do try to work fast, of course,", "but it's all sooooo draining...")),
            (("Порой я задумываюсь бросить всё,", "но я не хочу никого подставлять."),
             ("Sometimes I think about quitting it all,", "but I don't want to let anyone down.")),
            (("Впрочем, главное — не сдаваться", "и идти до конца."),
             ("Still, the main thing is to not give up", "and see it through.")),
            ("Ты когда-нибудь пробовал куриные ножки в мёду?",
             "Have you ever tried chicken legs in honey?")],
        "edge": [
            (("Надеюсь, у тебя всё хорошо.", "Я порой как будто на грани."),
             ("Hope you're doing okay.", "Me — I feel on the edge sometimes.")),
            (("Вот щас доделаю эту штучку", "и отдохну немножечко."),
             ("Lemme just finish this little thing", "and then I'll rest a bit.")),
            ("Вааай как хорошо получилось-то!",
             "Woooow, that came out so nice!")],
        "warn": [
            ("Не смотри ей в глаза...",
             "Don't look her in the eyes...")],
        "help": [
            ("А? Чем-то помочь? Конечно!",
             "Hm? Need a hand? Of course!"),
            (("Сразу говорю — в твой дедлайн", "вряд ли успею."),
             ("Fair warning though — no way", "I make your deadline.")),
            ("Подожди немного...",
             "Just wait a bit...")]}),
    "dreamliner": (3, "DreamLiner", "block.note_block.cow_bell", 0.8, {
        "a": [
            (("Емае, как пишется эта команда...", ["Джага! ", ("Помогать!", "pulse")]),
             ("Ugh, how do you spell this command...", ["Jaga! ", ("Heeelp!", "pulse")])),
            (("Текстурка какая-то фигня.", "Теней нет, градиент фигня..."),
             ("This texture is garbage.", "No shadows, gradient's trash...")),
            (["Чай! ", ("Помогать!", "pulse")],
             ["Chay! ", ("Heeelp!", "pulse")]),
            ("«И вот ГГ заходит в комнату с аномалией!»",
             "'And so the hero enters the anomaly room!'"),
            (("Не, фигня какая-то. Как игрок узнал,", "куда идти? Как он дверь открыл? Не дело."),
             ("Nah, that's lame. How did the player know", "where to go? How'd he even open the door?")),
            (["Дафигвам! ", ("Помогать!", "pulse")],
             ["DaFigVam! ", ("Heeelp!", "pulse")])],
        "b": [
            ([("Пум-пурум-пурум", "bouncy"), ", где там моё светленькое, нефильтрованное?"],
             [("Pum-purum-purum", "bouncy"), ", where's my light unfiltered one?"]),
            ("О, нашёл.",
             "Oh, found it."),
            ("Опять баги на карте. Достали уже.",
             "Bugs on the map again. So sick of them."),
            (("Как будто я не карту с багами делал,", "а баг с картой."),
             ("Like I wasn't making a map with bugs,", "but a bug with a map.")),
            (("Пойду отдохну от этих карт.", "Зайду-ка на сервачок, побегаю."),
             ("I need a break from these maps.", "Gonna go run around on some server."))]}),
    "smilekek": (4, "SmileKek", "block.note_block.flute", 0.6, [
        ("Vanilla Maps, Vanilla Maps, Vanilla Maps...",
         "Vanilla Maps, Vanilla Maps, Vanilla Maps..."),
        ([("VAAAAANILLA MAAAPS! ХАХАХАХАХ!", "shake")],
         [("VAAAAANILLA MAAAPS! HAHAHAHAH!", "shake")])]),
    "dafigvam": (5, "DaFigVam", "block.candle.extinguish", 1.0, {
        "1": [("Мы почти закончили. Осталось только начать.",
               "We're almost done. All that's left is to start.")],
        "2": [("Нам нужен трейлер к Future Maps Fest!",
               "We need a trailer for Future Maps Fest!")],
        "3": [(("Красота-то какая, лепота!", "Только бы оно еще и заработало..."),
               ("What a beauty, magnificent!", "Now if only it actually worked..."))],
        "4": [("Не забудьте Смайл Кеку подсыпать грибов.",
               "Don't forget to slip SmileKek his mushrooms.")],
        "5": [(("Вы все молодцы.", "Это феноменально редкостная дрянь."),
               ("Great job, everyone.", "This is phenomenally rare garbage."))],
        "6": [("Мухомор сам себя не вырастит.",
               "The fly agaric won't grow itself.")]}),
}

LANG_RU, LANG_EN = {}, {}

def head_width(nid, name):
    return ICON_ADV + width(f" [{name}]: ", bold=True)

def lang_two_row(row1, row2):
    """lang-значение второй строки: спейсеры под конкретный язык"""
    w1, w2 = width(row1), width(row2)
    u = max(w1, w2)
    return off_str(-w1) + row2 + off_str(2 + u - w2)

FX_IDS = {"shake": 1, "glitch": 2, "pulse": 3, "bouncy": 4}

def segs(row):
    """нормализация строки в список сегментов (text, fx|None)"""
    if isinstance(row, str):
        return [(row, None)]
    return [(s, None) if isinstance(s, str) else (s[0], s[1]) for s in row]

def row_text(row):
    return "".join(t for t, _ in segs(row))

def seg_component(key, fx, step, row2):
    if fx:
        g = FX_IDS[fx] | (8 if row2 else 0) | (step << 4)
        return f'{{"translate":"{key}","color":"#FA{g:02X}00","shadow_color":0}}'
    if row2:
        return f'{{"translate":"{key}","color":"#F9{step << 4:02X}00","shadow_color":0}}'
    return f'{{"translate":"{key}","color":"{dim((255,255,255), step)}","shadow_color":0}}'

def window_json(nid, name, seglists, step, two_row):
    """seglists: [(key, fx, row2), ...] в порядке компонентов"""
    icon = ICON_CHARS[nid]
    marker_b = nid | (8 if two_row else 0) | (step << 4)
    parts = [f'{{"text":".","color":"#DC50{marker_b:02X}","shadow_color":0}}',
             f'{{"text":"{icon}","font":"dcs:icons","color":"{dim((255,255,255), step)}","shadow_color":0}}',
             f'{{"text":" [{name}]: ","color":"{dim(PALETTE[nid], step)}","bold":true,"shadow_color":0}}']
    for key, fx, row2 in seglists:
        parts.append(seg_component(key, fx, step, row2))
    return "[" + ",".join(parts) + "]"

def duration(ru, en):
    lr = sum(len(x) for x in ru) if isinstance(ru, tuple) else len(ru)
    le = sum(len(x) for x in en) if isinstance(en, tuple) else len(en)
    return max(45, min(140, 25 + round(1.3 * max(lr, le))))

def emit_seq(key, nid, name, windows, sound_lines):
    folder = "dialog"
    wjs = []   # список seglists на окно
    durs = []
    for i, win in enumerate(windows, 1):
        ru, en = win[0], win[1]
        fx_all = win[2] if len(win) > 2 else None
        base = f"dcs.d.{key}.{i}"
        two = isinstance(ru, tuple)
        assert two == isinstance(en, tuple), f"структуры языков расходятся: {base}"
        seglist = []
        if two:
            rows_ru, rows_en = ru, en
        else:
            rows_ru, rows_en = (ru,), (en,)
        for ri, (rru, ren) in enumerate(zip(rows_ru, rows_en)):
            s_ru, s_en = segs(rru), segs(ren)
            assert len(s_ru) == len(s_en), f"число сегментов расходится: {base} ряд {ri}"
            row2 = ri == 1
            for j, ((tru, fru), (ten, fen)) in enumerate(zip(s_ru, s_en), 1):
                assert fru == fen, f"эффекты сегментов расходятся: {base}"
                k = f"{base}{'ab'[ri] if two else ''}{j if len(s_ru) > 1 else ''}"
                vru, ven = tru, ten
                if row2 and j == 1:  # спейсеры второй строки: в первый сегмент — сдвиг к началу
                    vru = off_str(-width(row_text(rows_ru[0]))) + vru
                    ven = off_str(-width(row_text(rows_en[0]))) + ven
                if row2 and j == len(s_ru):  # в последний — добивка до объединения
                    w1r, w2r = width(row_text(rows_ru[0])), width(row_text(rows_ru[1]))
                    w1e, w2e = width(row_text(rows_en[0])), width(row_text(rows_en[1]))
                    vru = vru + off_str(2 + max(w1r, w2r) - w2r)
                    ven = ven + off_str(2 + max(w1e, w2e) - w2e)
                LANG_RU[k], LANG_EN[k] = vru, ven
                seglist.append((k, fru or (fx_all if not two else None), row2))
        wjs.append(seglist)
        lr = sum(len(row_text(r)) for r in rows_ru)
        le = sum(len(row_text(r)) for r in rows_en)
        durs.append(max(45, min(140, 25 + round(1.3 * max(lr, le)))))
    dur = sum(durs) + 10
    w = lambda i, step=7: window_json(nid, name, wjs[i], step, any(r2 for _, _, r2 in wjs[i]))
    tagname = key
    entry = [f'function dcs:dialog/begin {{npc:"{tagname}",dur:{dur}}}',
             f"title @s actionbar {w(0, 0)}"] + sound_lines
    steps = ["# окна с длительностью по длине текста; фейды по 8 кадров"]
    for st in range(1, 8):
        steps.append(f"execute if score @s dcs.dlg matches {dur - st} run title @s actionbar {w(0, st)}")
    hi = dur
    for i in range(len(windows)):
        lo = hi - durs[i] + 1 if i < len(windows) - 1 else 10
        top = hi - 8 if i == 0 else hi
        steps.append(f"execute if score @s dcs.dlg matches {lo}..{top} run title @s actionbar {w(i, 7)}")
        if i > 0:
            steps.append(f"execute if score @s dcs.dlg matches {hi} run playsound minecraft:{VOICE} player @s ~ ~ ~ {VOL} {round(PITCH * (1.12 if i % 2 else 0.94), 2)}")
        hi = lo - 1
    for st in range(6, -1, -1):
        steps.append(f"execute if score @s dcs.dlg matches {st + 3} run title @s actionbar {w(len(windows) - 1, st)}")
    steps.append('execute if score @s dcs.dlg matches 2 run title @s actionbar {"text":""}')
    open(os.path.join(OUT, folder, f"{key}.mcfunction"), "w", encoding="utf-8").write(NL.join(entry) + NL)
    open(os.path.join(OUT, folder, f"{key}_lines.mcfunction"), "w", encoding="utf-8").write(NL.join(steps) + NL)
    return tagname, f"dcs:npc/{folder}/{key}_lines"

def write_dispatcher(path_key, folder, variants):
    lines = [f"execute store result score #r dcs.data run random value 1..{len(variants)}"]
    for i, vkey in enumerate(variants, 1):
        lines.append(f"execute if score #r dcs.data matches {i} run function dcs:npc/{folder}/{vkey}")
    open(os.path.join(OUT, folder, f"{path_key}.mcfunction"), "w", encoding="utf-8").write(NL.join(lines) + NL)

ROUTING = []

for key, (nid, name, voice, pitch, reps) in npcs.items():
    VOICE, PITCH, VOL = voice, pitch, (1.0 if "candle" in voice else 0.9)
    snd = [f"playsound minecraft:{voice} player @s ~ ~ ~ {VOL} {pitch}"]
    if isinstance(reps, dict):
        vkeys = []
        for v, rl in reps.items():
            ROUTING.append(emit_seq(f"{key}_{v}", nid, name, rl, snd))
            vkeys.append(f"{key}_{v}")
        write_dispatcher(key, "dialog", vkeys)
        print("dialog ok", key, f"({len(reps)} набора)")
    else:
        ROUTING.append(emit_seq(key, nid, name, reps, snd))
        print("dialog ok", key)

# --- реакции на попадание банкой (вызываются из dcs:can/npc_hit, в /random-диспетчеры не входят) ---
hits = {
    "jagermeistars": [
        ("Ай! Ёкарный бабай, кто кидается?!",
         "Ow! For crying out loud, who's throwing stuff?!"),
        ("Мне тут вообще-то код писать.",
         "Some of us are trying to write code here.")],
    "chayosi": [
        ("Ойй!.. Банкой-то за что?..",
         "Oww!.. A can? What did I do?.."),
        ("Ладно... Бывает, наверное...",
         "Okay... I guess that happens...")],
    "dreamliner": [
        ("Эй! Ты чего кидаешься?!",
         "Hey! What are you throwing stuff for?!"),
        ("...О. Пиво. Ладно, прощён.",
         "...Oh. Beer. Fine, you're forgiven.")],
    "smilekek": [
        ("ХАХАХАХ! Промазал!",
         "HAHAHAH! You missed!"),
        ("...А, нет. Не промазал.",
         "...Oh wait. You didn't.")],
    "dafigvam": [
        ("...",
         "..."),
        ("Я это запомнил.",
         "I will remember that.")],
}
for key, wins in hits.items():
    nid, name, voice, pitch, _ = npcs[key]
    VOICE, PITCH, VOL = voice, pitch, (1.0 if "candle" in voice else 0.9)
    snd = [f"playsound minecraft:{voice} player @s ~ ~ ~ {VOL} {pitch}"]
    ROUTING.append(emit_seq(f"{key}_hit", nid, name, wins, snd))
    print("hit ok", key)

# --- маршрутизация: begin/tick/end из реестра окон ---
ROUTING = [(f"dcs.dlg.{t}", fn) for t, fn in ROUTING]
DLG = os.path.join(os.path.dirname(OUT), "dialog")
tick = ["# executor = игрок с активным окном (dcs.dlg >= 1). Файл генерируется gen_dialogs.py",
        "scoreboard players remove @s dcs.dlg 1"]
tick += [f"execute if entity @s[tag={t}] run function {fn}" for t, fn in ROUTING]
tick.append("execute if score @s dcs.dlg matches ..0 run function dcs:dialog/end")
open(os.path.join(DLG, "tick.mcfunction"), "w", encoding="utf-8").write(NL.join(tick) + NL)

begin = ["# macro: {npc:..., dur:...} — начать окно. executor = игрок. Файл генерируется gen_dialogs.py"]
begin += [f"tag @s remove {t}" for t, _ in ROUTING]
begin += ["$tag @s add dcs.dlg.$(npc)", "$scoreboard players set @s dcs.dlg $(dur)"]
open(os.path.join(DLG, "begin.mcfunction"), "w", encoding="utf-8").write(NL.join(begin) + NL)

end = ["# executor = игрок. Фейд-аут делают _lines, тут только чистка. Файл генерируется gen_dialogs.py",
       "scoreboard players set @s dcs.dlg 0"]
end += [f"tag @s remove {t}" for t, _ in ROUTING]
open(os.path.join(DLG, "end.mcfunction"), "w", encoding="utf-8").write(NL.join(end) + NL)

# --- прочие ключи локализации ---
LANG_RU["dcs.item.beer"] = "Пиво"
LANG_EN["dcs.item.beer"] = "Beer"
LANG_RU["dcs.item.beer.lore"] = "Светлое, нефильтрованное."
LANG_EN["dcs.item.beer.lore"] = "Light, unfiltered."
LANG_RU["dcs.item.beer.lore2"] = "Правда кажется оно заварено..."
LANG_EN["dcs.item.beer.lore2"] = "Though it does seem... brewed?"
LANG_RU["dcs.item.beer.lore3"] = "Любимое DreamLiner."
LANG_EN["dcs.item.beer.lore3"] = "DreamLiner's favorite."

# ПОКА en_us зеркалит ru_ru: часть русских игроков играет на английской локали.
# Английские тексты сохранены в контенте — при готовности вернуть, поставить False
EN_MIRROR_RU = True

# --- lang-файлы ---
lang_dir = os.path.join(RP, "assets", "dcs", "lang")
os.makedirs(lang_dir, exist_ok=True)
json.dump(LANG_RU, open(os.path.join(lang_dir, "ru_ru.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(LANG_RU if EN_MIRROR_RU else LANG_EN, open(os.path.join(lang_dir, "en_us.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"routing ok: {len(ROUTING)} окон; lang: {len(LANG_RU)} ключей (ru+en)")

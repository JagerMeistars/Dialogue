#version 330

// dcs: диалоговые окна — маркер-глиф "." растягивается в панель под actionbar-репликой,
// спеццвета кодируют сдвиги/фейд/волну. Весь остальной текст рендерится ванильно.
// (идея по мотивам TheSalt's Text Effects)
//
// В 26.3 шейдер называется text.* и компилируется в вариантах:
//   #if !defined(IS_GUI) && !defined(IS_SEE_THROUGH) — мировой вариант с Sampler2/UV2/fog;
//   IS_GUI — вариант actionbar/GUI: НЕТ Sampler2/UV2, НЕТ fog UBO.
// Диалоги Dialogue — actionbar, т.е. IS_GUI-вариант. Поэтому все панели/имена/ряды
// (#DC/#FB/#F9) обходятся без Sampler2/UV2/fog; лайтмап трогается только в мировом
// варианте (эффект-текст #FA на text_display).
//
// Магические цвета (только GUI, кроме #FA — он работает и в мире):
//  #DC GG BB — маркер панели. BB: биты 0-2 = id NPC (1..5), бит 3 = две строки,
//              биты 4-6 = ступень фейда (0..7 -> альфа 12..100%).
//              GG всегда 80. Ширины двухстрочных решают negative-space глифы в lang.
//  #FB GG BB — имя/ряд 1. BB = сдвиг вправо (px). GG: биты 0-2 = палитра
//              (0 белый, 1..5 NPC, 6 фиолетовый), бит 3 = волна, биты 4-6 = ступень фейда.
//  #F9 GG BB — ряд 2 (вниз на 12px). BB = сдвиг влево (px), GG: биты 0-1 = старшие биты
//              сдвига, бит 3 = волна, биты 4-6 = ступень фейда. Перекрашивается в белый.
//  #FA GG BB — эффект-текст: GG биты 0-2 = эффект (1 дрожь, 2 глитч, 3 пульс, 4 прыжки),
//              бит 3 = сегмент второй строки (вниз 12px), биты 4-6 = фейд;
//              BB = палитра (0 белый, 1..5 NPC, 6 фиолетовый).

#if !defined(IS_GUI) && !defined(IS_SEE_THROUGH)
#moj_import <minecraft:fog.glsl>
#moj_import <minecraft:sample_lightmap.glsl>
#endif

#moj_import <minecraft:dynamictransforms.glsl>
#moj_import <minecraft:projection.glsl>
#moj_import <minecraft:globals.glsl>

in vec3 Position;
in vec4 Color;
in vec2 UV0;
#if !defined(IS_GUI) && !defined(IS_SEE_THROUGH)
in ivec2 UV2;
#endif

#if !defined(IS_GUI) && !defined(IS_SEE_THROUGH)
uniform sampler2D Sampler2;
out float sphericalVertexDistance;
out float cylindricalVertexDistance;
#endif

out vec4 vertexColor;
out vec2 texCoord0;

flat out int dcsPanel;
flat out float dcsPanelA;

vec3 dcsPalette(int pal) {
    return pal == 1 ? vec3(0.24, 0.75, 0.39)   // JagerMeistars — егерь-зелёный
         : pal == 2 ? vec3(1.00, 0.51, 0.16)   // Chayosi — оранжевый
         : pal == 3 ? vec3(0.33, 1.00, 1.00)   // DreamLiner — aqua (бывший Chayosi)
         : pal == 4 ? vec3(1.00, 1.00, 0.33)   // SmileKek — yellow
         : pal == 5 ? vec3(1.00, 0.27, 0.24)   // DaFigVam — мухоморно-красный
         :            vec3(1.0);               // 0 — белый

}

float dcsWave(int flag) {
    if (flag == 0) return 0.0;
    return sin(GameTime * 24000.0 * 0.35 + float(gl_VertexID / 4) * 0.7) * 0.6;
}

void main() {
    texCoord0 = UV0;

    dcsPanel = 0;
    dcsPanelA = 1.0;

    // Базовый цвет: в мировом варианте домножаем на лайтмап и считаем дистанции для тумана,
    // в GUI-варианте лайтмапа/тумана нет.
#if !defined(IS_GUI) && !defined(IS_SEE_THROUGH)
    sphericalVertexDistance = fog_spherical_distance(Position);
    cylindricalVertexDistance = fog_cylindrical_distance(Position);
    vertexColor = Color * sample_lightmap(Sampler2, UV2);
#else
    vertexColor = Color;
#endif

    ivec3 c = ivec3(round(Color.rgb * 255.0));
    bool gui = ProjMat[3][3] != 0.0;
    float kx = ProjMat[0][0];  // NDC на 1 GUI-пиксель по x
    float ky = ProjMat[1][1];  // NDC на 1 GUI-пиксель по y (отрицательный)

    // --- эффект-текст (#FA): GG биты 0-2 = эффект (1 дрожь, 2 глитч), биты 4-6 = фейд; BB = палитра ---
    // Единственный спеццвет, работающий и в мире (text_display), и в GUI.
    if (c.r == 250 && (c.g & 0x80) == 0 && (c.g & 7) >= 1 && (c.g & 7) <= 4 && c.b <= 6) {
        float fade = float(((c.g >> 4) & 7) + 1) / 8.0;
        int fx = c.g & 7;
        float cid = float(gl_VertexID / 4);
        vec4 clip4 = ProjMat * ModelViewMat * vec4(Position, 1.0);
        float seed = floor(GameTime * 24000.0 * 0.5);  // обновление раз в 2 тика
        float r1 = fract(sin(dot(vec2(cid, seed), vec2(12.9898, 78.233))) * 43758.5453);
        float r2 = fract(sin(dot(vec2(seed, cid), vec2(39.3468, 11.135))) * 24634.6345);
        vec2 jit = vec2(0.0);
        float t = GameTime * 24000.0;
        if (fx == 1) {                                 // дрожь
            jit = (vec2(r1, r2) - 0.5) * 1.6;
        } else if (fx == 2) {                          // глитч: редкие резкие рывки
            if (r1 > 0.82) jit.x = (r2 - 0.5) * 6.0;
            if (r2 > 0.93) jit.y = (r1 - 0.5) * 3.0;
        } else if (fx == 3) {                          // пульс: буквы дышат размером
            float s = sin(t * 0.25 + cid * 0.9) * 0.8;
            int pv = gl_VertexID % 4;
            vec2 cd = pv == 0 ? vec2(-1.0, -1.0) : pv == 1 ? vec2(-1.0, 1.0)
                    : pv == 2 ? vec2(1.0, 1.0)   :           vec2(1.0, -1.0);
            jit = cd * s;
        } else {                                       // прыжки волной по буквам
            jit.y = -abs(sin(t * 0.3 + cid * 0.55)) * 2.2;
        }
        if ((c.g & 8) != 0) jit.y += 12.0;             // бит 3: сегмент второй строки
        if (gui) {
            gl_Position = vec4(clip4.x + jit.x * kx, clip4.y + jit.y * ky, clip4.z, clip4.w);
            vertexColor = vec4(dcsPalette(c.b) * fade, Color.a);
        } else {
            // мировой текст (text_display): дрожь в локальных координатах глифа (1 px = 0.025 бл.)
            gl_Position = ProjMat * ModelViewMat * vec4(Position + vec3(jit.x, -jit.y, 0.0) * 0.025, 1.0);
#if !defined(IS_GUI) && !defined(IS_SEE_THROUGH)
            vertexColor = vec4(dcsPalette(c.b) * fade, Color.a) * sample_lightmap(Sampler2, UV2);
#else
            vertexColor = vec4(dcsPalette(c.b) * fade, Color.a);
#endif
        }
        return;
    }

    // Остальные спеццвета — только actionbar/GUI. В GUI-варианте нет Sampler2/UV2/fog,
    // поэтому ниже нигде не трогаем лайтмап: vertexColor = чистый цвет (как ванильный GUI-текст).

    // --- ряд 2 (#F9) ---
    if (c.r == 249 && (c.g & 0x84) == 0 && gui) {
        float shift = float((c.g & 3) * 256 + c.b);
        float fade = float(((c.g >> 4) & 7) + 1) / 8.0;
        vec4 clip2 = ProjMat * ModelViewMat * vec4(Position, 1.0);
        gl_Position = vec4(clip2.x - shift * kx,
                           clip2.y + (12.0 + dcsWave(c.g & 8)) * ky, clip2.z, clip2.w);
        vertexColor = vec4(vec3(fade), Color.a);
        return;
    }

    // --- имя / ряд 1 (#FB) ---
    if (c.r == 251 && (c.g & 0x80) == 0 && (c.g & 7) <= 6 && gui) {
        float fade = float(((c.g >> 4) & 7) + 1) / 8.0;
        vec4 clip3 = ProjMat * ModelViewMat * vec4(Position, 1.0);
        gl_Position = vec4(clip3.x + float(c.b) * kx,
                           clip3.y + dcsWave(c.g & 8) * ky, clip3.z, clip3.w);
        vertexColor = vec4(dcsPalette(c.g & 7) * fade, Color.a);
        return;
    }

    // --- маркер панели (#DC) ---
    // двухстрочность (бит 8) влияет только на высоту: горизонтальную вёрстку второй строки
    // делают negative-space глифы в lang-файлах, ширина склейки уже язык-корректна
    int npcId = c.b & 7;
    bool twoRow = (c.b & 8) != 0;
    if (c.r == 220 && npcId >= 1 && npcId <= 5 && c.b <= 125 && c.g == 80 && gui) {
        int vid = gl_VertexID % 4;
        vec2 cornerDir = vid == 0 ? vec2(0.0, 0.0)
                       : vid == 1 ? vec2(0.0, 1.0)
                       : vid == 2 ? vec2(1.0, 1.0)
                       :            vec2(1.0, 0.0);
        // Работаем в NDC: actionbar центрируется матрицей, NDC конца строки = -NDC начала.
        vec4 clip = ProjMat * ModelViewMat * vec4(Position, 1.0);
        // маркер — точка ".": квад 1px шириной, 8px высотой, advance 2 (замерено по ascii.png)
        float lineLeftN = clip.x - cornerDir.x * 1.0 * kx;
        float rowTopN   = clip.y - cornerDir.y * 8.0 * ky;
        float leftN  = lineLeftN + (2.0 - 10.0) * kx;
        float rightN = -lineLeftN + 14.0 * kx;
        float panelH = twoRow ? 44.0 : 32.0;
        gl_Position = vec4(mix(leftN, rightN, cornerDir.x),
                           rowTopN + (-12.0 + panelH * cornerDir.y) * ky,
                           clip.z, clip.w);
        dcsPanel = 1;
        dcsPanelA = float(((c.b >> 4) & 7) + 1) / 8.0;
        return;
    }

    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);
}

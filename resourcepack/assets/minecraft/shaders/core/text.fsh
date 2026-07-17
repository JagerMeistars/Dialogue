#version 330

// dcs: диалоговая плашка — плоский полупрозрачный прямоугольник (см. text.vsh).
// В 26.3 текст обязан проходить через OIT-конвейер (executeAlphaOnlyPhase /
// calculateFinalColor), поэтому плашка не пишет fragColor напрямую, а просто
// подставляет свой цвет в тот же путь, что и обычный текст.

#if !defined(IS_GUI) && !defined(IS_SEE_THROUGH)
#moj_import <minecraft:fog.glsl>
#endif

#moj_import <minecraft:dynamictransforms.glsl>
#moj_import <minecraft:oit.glsl>

uniform sampler2D Sampler0;

#if !defined(IS_GUI) && !defined(IS_SEE_THROUGH)
in float sphericalVertexDistance;
in float cylindricalVertexDistance;
#endif

in vec4 vertexColor;
in vec2 texCoord0;

flat in int dcsPanel;
flat in float dcsPanelA;

#ifndef OIT_ALPHA_ONLY
out vec4 fragColor;
#endif

vec4 calculateFinalColor(vec4 color) {
    #ifdef OIT_ACCUMULATE
    color = sampleColorForAccumulation(color);
    #endif

    #if !defined(IS_SEE_THROUGH) && !defined(IS_GUI)

    #ifdef OIT_ACCUMULATE
    vec4 fogColor = vec4(FogColor.rgb * color.a, FogColor.a);
    #else
    vec4 fogColor = FogColor;
    #endif

    color = apply_fog(color, sphericalVertexDistance, cylindricalVertexDistance, FogEnvironmentalStart, FogEnvironmentalEnd, FogRenderDistanceStart, FogRenderDistanceEnd, fogColor);
    #endif

    return color;
}

void main() {
    vec4 color;

    if (dcsPanel == 1) {
        // Плашка: тёмный плоский цвет, без текстуры. Альфа очень мала на слабых фейдах,
        // поэтому ванильный порог discard к ней НЕ применяем (иначе бледные панели исчезнут).
        color = vec4(vec3(0.024, 0.02, 0.038), 0.55 * dcsPanelA * vertexColor.a * ColorModulator.a);
    } else {
        #ifdef IS_GRAYSCALE
        vec4 texColor = texture(Sampler0, texCoord0).rrrr;
        #else
        vec4 texColor = texture(Sampler0, texCoord0);
        #endif

        color = texColor * vertexColor * ColorModulator;

        if (color.a < 0.1) {
            discard;
        }
    }

    #ifdef OIT_ALPHA_ONLY
    executeAlphaOnlyPhase(gl_FragCoord.z, color.a);
    #else
    fragColor = calculateFinalColor(color);
    #endif
}

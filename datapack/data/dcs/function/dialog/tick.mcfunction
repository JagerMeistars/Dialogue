# executor = игрок с активным окном (dcs.dlg >= 1). Файл генерируется gen_dialogs.py
scoreboard players remove @s dcs.dlg 1
execute if entity @s[tag=dcs.dlg.jagermeistars_bracket] run function dcs:npc/dialog/jagermeistars_bracket_lines
execute if entity @s[tag=dcs.dlg.jagermeistars_shaders] run function dcs:npc/dialog/jagermeistars_shaders_lines
execute if entity @s[tag=dcs.dlg.jagermeistars_call] run function dcs:npc/dialog/jagermeistars_call_lines
execute if entity @s[tag=dcs.dlg.chayosi_model] run function dcs:npc/dialog/chayosi_model_lines
execute if entity @s[tag=dcs.dlg.chayosi_tired] run function dcs:npc/dialog/chayosi_tired_lines
execute if entity @s[tag=dcs.dlg.chayosi_edge] run function dcs:npc/dialog/chayosi_edge_lines
execute if entity @s[tag=dcs.dlg.chayosi_warn] run function dcs:npc/dialog/chayosi_warn_lines
execute if entity @s[tag=dcs.dlg.chayosi_help] run function dcs:npc/dialog/chayosi_help_lines
execute if entity @s[tag=dcs.dlg.dreamliner_a] run function dcs:npc/dialog/dreamliner_a_lines
execute if entity @s[tag=dcs.dlg.dreamliner_b] run function dcs:npc/dialog/dreamliner_b_lines
execute if entity @s[tag=dcs.dlg.smilekek] run function dcs:npc/dialog/smilekek_lines
execute if entity @s[tag=dcs.dlg.dafigvam_1] run function dcs:npc/dialog/dafigvam_1_lines
execute if entity @s[tag=dcs.dlg.dafigvam_2] run function dcs:npc/dialog/dafigvam_2_lines
execute if entity @s[tag=dcs.dlg.dafigvam_3] run function dcs:npc/dialog/dafigvam_3_lines
execute if entity @s[tag=dcs.dlg.dafigvam_4] run function dcs:npc/dialog/dafigvam_4_lines
execute if entity @s[tag=dcs.dlg.dafigvam_5] run function dcs:npc/dialog/dafigvam_5_lines
execute if entity @s[tag=dcs.dlg.dafigvam_6] run function dcs:npc/dialog/dafigvam_6_lines
execute if entity @s[tag=dcs.dlg.jagermeistars_hit] run function dcs:npc/dialog/jagermeistars_hit_lines
execute if entity @s[tag=dcs.dlg.chayosi_hit] run function dcs:npc/dialog/chayosi_hit_lines
execute if entity @s[tag=dcs.dlg.dreamliner_hit] run function dcs:npc/dialog/dreamliner_hit_lines
execute if entity @s[tag=dcs.dlg.smilekek_hit] run function dcs:npc/dialog/smilekek_hit_lines
execute if entity @s[tag=dcs.dlg.dafigvam_hit] run function dcs:npc/dialog/dafigvam_hit_lines
execute if score @s dcs.dlg matches ..0 run function dcs:dialog/end

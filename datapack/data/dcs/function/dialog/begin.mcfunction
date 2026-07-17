# macro: {npc:..., dur:...} — начать окно. executor = игрок. Файл генерируется gen_dialogs.py
tag @s remove dcs.dlg.jagermeistars_bracket
tag @s remove dcs.dlg.jagermeistars_shaders
tag @s remove dcs.dlg.jagermeistars_call
tag @s remove dcs.dlg.chayosi_model
tag @s remove dcs.dlg.chayosi_tired
tag @s remove dcs.dlg.chayosi_edge
tag @s remove dcs.dlg.chayosi_warn
tag @s remove dcs.dlg.chayosi_help
tag @s remove dcs.dlg.dreamliner_a
tag @s remove dcs.dlg.dreamliner_b
tag @s remove dcs.dlg.smilekek
tag @s remove dcs.dlg.dafigvam_1
tag @s remove dcs.dlg.dafigvam_2
tag @s remove dcs.dlg.dafigvam_3
tag @s remove dcs.dlg.dafigvam_4
tag @s remove dcs.dlg.dafigvam_5
tag @s remove dcs.dlg.dafigvam_6
tag @s remove dcs.dlg.jagermeistars_hit
tag @s remove dcs.dlg.chayosi_hit
tag @s remove dcs.dlg.dreamliner_hit
tag @s remove dcs.dlg.smilekek_hit
tag @s remove dcs.dlg.dafigvam_hit
$tag @s add dcs.dlg.$(npc)
$scoreboard players set @s dcs.dlg $(dur)

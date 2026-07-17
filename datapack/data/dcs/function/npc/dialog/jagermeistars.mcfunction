execute store result score #r dcs.data run random value 1..3
execute if score #r dcs.data matches 1 run function dcs:npc/dialog/jagermeistars_bracket
execute if score #r dcs.data matches 2 run function dcs:npc/dialog/jagermeistars_shaders
execute if score #r dcs.data matches 3 run function dcs:npc/dialog/jagermeistars_call

execute store result score #r dcs.data run random value 1..2
execute if score #r dcs.data matches 1 run function dcs:npc/dialog/dreamliner_a
execute if score #r dcs.data matches 2 run function dcs:npc/dialog/dreamliner_b

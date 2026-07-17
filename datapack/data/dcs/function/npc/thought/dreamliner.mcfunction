execute store result score #r dcs.data run random value 1..4
execute if score #r dcs.data matches 1 run function dcs:npc/thought/dreamliner_1
execute if score #r dcs.data matches 2 run function dcs:npc/thought/dreamliner_2
execute if score #r dcs.data matches 3 run function dcs:npc/thought/dreamliner_3
execute if score #r dcs.data matches 4 run function dcs:npc/thought/dreamliner_4

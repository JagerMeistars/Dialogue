execute store result score #r dcs.data run random value 1..3
execute if score #r dcs.data matches 1 run function dcs:npc/thought/jagermeistars_1
execute if score #r dcs.data matches 2 run function dcs:npc/thought/jagermeistars_2
execute if score #r dcs.data matches 3 run function dcs:npc/thought/jagermeistars_3

execute store result score #r dcs.data run random value 1..6
execute if score #r dcs.data matches 1 run function dcs:npc/dialog/dafigvam_1
execute if score #r dcs.data matches 2 run function dcs:npc/dialog/dafigvam_2
execute if score #r dcs.data matches 3 run function dcs:npc/dialog/dafigvam_3
execute if score #r dcs.data matches 4 run function dcs:npc/dialog/dafigvam_4
execute if score #r dcs.data matches 5 run function dcs:npc/dialog/dafigvam_5
execute if score #r dcs.data matches 6 run function dcs:npc/dialog/dafigvam_6

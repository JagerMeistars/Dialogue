execute store result score #r dcs.data run random value 1..5
execute if score #r dcs.data matches 1 run function dcs:npc/dialog/chayosi_model
execute if score #r dcs.data matches 2 run function dcs:npc/dialog/chayosi_tired
execute if score #r dcs.data matches 3 run function dcs:npc/dialog/chayosi_edge
execute if score #r dcs.data matches 4 run function dcs:npc/dialog/chayosi_warn
execute if score #r dcs.data matches 5 run function dcs:npc/dialog/chayosi_help

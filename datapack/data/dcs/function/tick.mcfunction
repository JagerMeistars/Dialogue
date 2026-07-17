# таймер оверлей-диалогов (единственный тиковый хук системы)
execute as @a[scores={dcs.dlg=1..}] at @s run function dcs:dialog/tick

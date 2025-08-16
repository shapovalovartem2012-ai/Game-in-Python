Ny_names_Kak_Bu = {
    "я": "Артем",
    "учитель ": "Не знаю как вас зовкт Ибрагим",
    "Ну кто-то": "Вася"
}

terminius = input("Введите имя кого хочишь задоксить ")

if terminius in Ny_names_Kak_Bu:
    print(Ny_names_Kak_Bu[terminius])
else:
    print("Термин не найден в словаре.")
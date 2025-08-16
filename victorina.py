vopr = {
 "Как я": "хорошо",
 "как ты": "прекрасно",
 "как он": "помер"
}

ochco = 0

for vorp, atvet in vopr.items():
    user_atvet = input(atvet)
    if user_atvet.lower() == atvet.lower():
        print("Ну да")
        ochco += 1
    else:
        print("ну нет")

print("Итоговый счет:", ochco)


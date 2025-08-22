# Генерация всех комбинаций
codes = []
for i in range(9**4):
    code = (
        str((i // 729) % 9 + 1) +
        str((i // 81) % 9 + 1) +
        str((i // 9) % 9 + 1) +
        str(i % 9 + 1)
    )
    codes.append(code)

# Пример первых 10 комбинаций
print("Первые 10 комбинаций:")
print('\n'.join(codes[:10]))

# Пример последних 10 комбинаций
print("\nПоследние 10 комбинаций:")
print('\n'.join(codes[-10:]))

# Сохранение в файл (по желанию)
with open("all_codes.txt", "w") as f:
    f.write('\n'.join(codes))
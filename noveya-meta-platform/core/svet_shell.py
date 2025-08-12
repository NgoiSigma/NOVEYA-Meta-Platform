class SVET:
    def __init__(self):
        self.energy_level = 100
        self.harmony = True

    def balance(self, input_energy):
        if input_energy > 120:
            self.harmony = False
            return "Перегрузка! Система стабилизируется..."
        elif input_energy < 80:
            self.harmony = False
            return "Энергии недостаточно. Активация резонанса..."
        else:
            self.harmony = True
            return "Баланс энергии сохранён."

import math

class NoveyaMatrix:
    def __init__(self, axis_tilt=23.4, current_sun_spots=0):
        self.theta = axis_tilt  # Текущий угол наклона оси Земли
        self.ss = current_sun_spots  # Индекс Чижевского (пятна на Солнце)
        
    def get_sen_cyr_shift(self, epoch_year):
        # Расчет фазового сдвига семантической линейки
        precession_step = (epoch_year % 2160) / 2160
        return math.log10(self.theta * (1 + precession_step))

    def decrypt_metaphor(self, metaphor_vector, epoch_year):
        shift = self.get_sen_cyr_shift(epoch_year)
        
        # Модуляция биологического ядра (по Чижевскому)
        blood_iron_excitation = self.ss * 1.15
        lymphocyte_activity = 100 / (1 + (self.ss * 0.08))
        
        # Модуляция экономического ядра (Кондратьев / Чибрикин)
        k_wave_phase = math.sin(2 * math.pi * (epoch_year / 54))
        chibrikin_emission_rate = math.cos(2 * math.pi * (epoch_year / 1.5))
        
        output_norm = {
            "biomedical_status": "CRITICAL_AGRESS" if blood_iron_excitation > 80 else "STABLE",
            "lymphocyte_efficiency_pct": lymphocyte_activity,
            "resource_allocation_ratio": 1.0 - (abs(k_wave_phase) * 0.3),
            "credit_emission_control": "LOCK_EXPLOITATION" if chibrikin_emission_rate > 0.7 else "FREE"
        }
        
        return output_norm

# Инициализация для текущих параметров среды (2026 год, фаза цикла)
node = NoveyaMatrix(axis_tilt=23.4, current_sun_spots=120)
system_orders = node.decrypt_metaphor(metaphor_vector=["мор", "возбуждение"], epoch_year=2026)
print(system_orders)

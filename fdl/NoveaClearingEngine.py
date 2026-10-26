"""
Core Engine: NoveaClearingEngine
Component: Bi-lateral Commodity & Raw Material Clearing Module (Woodchips / Heat)
Methodology: Formal Dialectics (-FDL) & Multi-Agent AI-Orchestration
"""

import logging
from typing import Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [CLEARING-CORE] %(message)s')

class NoveaClearingEngine:
    def __init__(self):
        self.shrine_pct = 0.10          # 10% отчислений в Фонд Нового Витка (FNV)
        self.fe_transport_cost = 8.5    # Эквивалентная стоимость 1 транспортной ФЕ (в условных единицах)
        self.base_q_mw = 3.5            # Базовая теплотворная способность нормативной щепы (МВт*ч / тонна)
        
    def calculate_woodchip_energy_value(self, volume_m3: float, density: float, moisture_pct: float, boiler_efficiency: float) -> Tuple[float, float]:
        """
        Расчет реальной энергетической ценности поставки с учетом влажности.
        Возвращает: (Чистая масса в тоннах, Энергетическая ценность в МВт*ч).
        """
        if volume_m3 <= 0 or density <= 0:
            raise ValueError("Объем и плотность сырья должны быть строго положительными.")
            
        # Расчет физической массы
        mass_tons = volume_m3 * density
        
        # Диалектическое падение теплотворности при росте влажности (f(K) среды сырья)
        # Нормативная влажность — 20%. Каждый процент превышения снижает отдачу.
        if moisture_pct > 20.0:
            moisture_penalty = (moisture_pct - 20.0) * 0.05
            actual_q = self.base_q_mw * (1.0 - moisture_penalty)
        else:
            actual_q = self.base_q_mw
            
        # Учет КПД котельных КП "Николаевоблтеплоэнерго"
        effective_energy_mwh = mass_tons * actual_q * boiler_efficiency
        return mass_tons, effective_energy_mwh

    def execute_clearing_transaction(self, community_id: str, current_debt_fe: float, volume_m3: float, 
                                   density: float, moisture_pct: float, boiler_efficiency: float = 0.85) -> Dict[str, Any]:
        """
        Исполнение двустороннего клиринга. Погашение фиатного кассового разрыва 
        транспортного КП за счет энергетического вклада пригородной общины.
        """
        # 1. Вычисление физико-энергетического баланса поставки
        mass_tons, energy_mwh = self.calculate_woodchip_energy_value(
            volume_m3, density, moisture_pct, boiler_efficiency
        )
        
        # Коэффициент качества сырья (C_raw)
        c_raw = 1.0 if moisture_pct <= 20.0 else max(0.1, 1.0 - ((moisture_pct - 20.0) / 100.0))
        
        # 2. Конвертация МВт*ч щепы в эквивалент транспортных ФЕ (пассажиро-километров)
        # 1 МВт*ч тепловой энергии условно эквивалентен 150 транспортным ФЕ по паритету КУБ v1
        fe_generated = energy_mwh * 150.0 * c_raw
        
        # 3. Применение правила десятины (10% уходит в Фонд Нового Витка FNV на амортизацию котлов)
        fnv_allocation_fe = fe_generated * self.shrine_pct
        net_fe_for_clearing = fe_generated - fnv_allocation_fe
        
        # 4. Процедура списания долга в реестре КУБ v1
        old_debt = current_debt_fe
        new_debt = max(0.0, old_debt - net_fe_for_clearing)
        extinguished_debt = old_debt - new_debt
        
        # Расчет остаточного профицита, если община привезла больше щепы, чем была должна
        surplus_fe = max(0.0, net_fe_for_clearing - old_debt)
        
        logging.info(
            f"[КЛИРИНГ УСПЕШЕН] Община '{community_id}' поставила {mass_tons:.2f} тонн щепы ({volume_m3} м3). "
            f"Сгенерировано: {fe_generated:.2f} ФЕ. Направлено в FNV: {fnv_allocation_fe:.2f} ФЕ. "
            f"Погашен долг перед КП 'Николаевэлектротранс': {extinguished_debt:.2f} ФЕ. Новый баланс долга: {new_debt:.2f} ФЕ."
        )
        
        return {
            "status": "CLEARING_COMPLETED",
            "delivered_mass_tons": round(mass_tons, 2),
            "effective_energy_mwh": round(energy_mwh, 2),
            "extinguished_debt_fe": round(extinguished_debt, 2),
            "new_debt_balance_fe": round(new_debt, 2),
            "community_surplus_credit_fe": round(surplus_fe, 2),
            "fnv_tax_retained_fe": round(fnv_allocation_fe, 2)
        }

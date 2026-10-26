import logging
from typing import Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [CLEARING-CORE] %(message)s')

class NoveaClearingEngine:
    def __init__(self):
        self.shrine_pct = 0.10
        self.fe_transport_cost = 8.5
        self.base_q_mw = 3.5

    def calculate_woodchip_energy_value(self, volume_m3: float, density: float, moisture_pct: float, boiler_efficiency: float) -> Tuple[float, float]:
        if volume_m3 <= 0 or density <= 0:
            raise ValueError("Объем и плотность сырья должны быть строго положительными.")
        mass_tons = volume_m3 * density
        if moisture_pct > 20.0:
            moisture_penalty = (moisture_pct - 20.0) * 0.05
            actual_q = self.base_q_mw * (1.0 - moisture_penalty)
        else:
            actual_q = self.base_q_mw
        effective_energy_mwh = mass_tons * actual_q * boiler_efficiency
        return mass_tons, effective_energy_mwh

    def execute_clearing_transaction(self, community_id: str, current_debt_fe: float, volume_m3: float, 
                                   density: float, moisture_pct: float, boiler_efficiency: float = 0.85) -> Dict[str, Any]:
        mass_tons, energy_mwh = self.calculate_woodchip_energy_value(volume_m3, density, moisture_pct, boiler_efficiency)
        c_raw = 1.0 if moisture_pct <= 20.0 else max(0.1, 1.0 - ((moisture_pct - 20.0) / 100.0))
        fe_generated = energy_mwh * 150.0 * c_raw
        fnv_allocation_fe = fe_generated * self.shrine_pct
        net_fe_for_clearing = fe_generated - fnv_allocation_fe
        old_debt = current_debt_fe
        new_debt = max(0.0, old_debt - net_fe_for_clearing)
        extinguished_debt = old_debt - new_debt
        surplus_fe = max(0.0, net_fe_for_clearing - old_debt)
        return {
            "status": "CLEARING_COMPLETED",
            "delivered_mass_tons": round(mass_tons, 2),
            "effective_energy_mwh": round(energy_mwh, 2),
            "extinguished_debt_fe": round(extinguished_debt, 2),
            "new_debt_balance_fe": round(new_debt, 2),
            "community_surplus_credit_fe": round(surplus_fe, 2),
            "fnv_tax_retained_fe": round(fnv_allocation_fe, 2)
        }

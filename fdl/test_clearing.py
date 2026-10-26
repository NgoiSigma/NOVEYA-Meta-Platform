import pytest
from NoveaClearingEngine import NoveaClearingEngine

def test_galitsynovo_community_clearing_success():
    engine = NoveaClearingEngine()
    
    # Исходные условия до решения:
    # Долг общины перед КП составляет 5000 ФЕ (пассажиро-километров подвоза жителей)
    initial_debt = 5000.0
    
    # Параметры машины с щепой (40 м3, влажность завышена — 30% вместо 20% нормативных)
    result = engine.execute_clearing_transaction(
        community_id="Galitsynovo_Gromada",
        current_debt_fe=initial_debt,
        volume_m3=40.0,
        density=0.32,         # 320 кг на метр кубический
        moisture_pct=30.0,    # Сырое сырье (вызывает штрафной коэффициент)
        boiler_efficiency=0.85 # Стандартный промышленный котел
    )
    
    # Верификация результатов ИИ-аудита
    assert result["status"] == "CLEARING_COMPLETED"
    assert result["delivered_mass_tons"] == 12.8  # 40 * 0.32 = 12.8 тонн
    
    # Долг должен быть частично или полностью погашен БЕЗ ИСПОЛЬЗОВАНИЯ ГРИВНЫ
    assert result["extinguished_debt_fe"] > 0
    assert result["new_debt_balance_fe"] < initial_debt
    
    # Проверка, что десятина 10% строго ушла в реестр FNV на ремонт сетей
    assert result["fnv_tax_retained_fe"] == pytest.approx(result["extinguished_debt_fe"] * 0.11111, rel=1e-2)

import pytest
from NoveaClearingEngine import NoveaClearingEngine

def test_galitsynovo_community_clearing_success():
    engine = NoveaClearingEngine()
    result = engine.execute_clearing_transaction(
        community_id="Galitsynovo_Gromada",
        current_debt_fe=5000.0,
        volume_m3=40.0,
        density=0.32,
        moisture_pct=30.0
    )
    assert result["status"] == "CLEARING_COMPLETED"
    assert result["delivered_mass_tons"] == 12.8
    assert result["extinguished_debt_fe"] > 0

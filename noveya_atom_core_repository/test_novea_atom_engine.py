import pytest
from unittest.mock import MagicMock, patch
from NoveaAtomEngine import NoveaAtomEngine

MOCK_CLIENT_ID = "AYz4b_NoveaAtomFakeClientID_KUB_v1_TestKey2026_XYZ"
MOCK_CLIENT_SECRET = "EKn_NoveaAtomFakeSecret_FNV_DevelopmentFund_999"

@pytest.fixture
def engine():
    return NoveaAtomEngine(client_id=MOCK_CLIENT_ID, client_secret=MOCK_CLIENT_SECRET, mode="sandbox")

@pytest.mark.parametrize("delta_m_kg, passengers_in, route_length_km, expected_n_fe", [
    (3500.0, 50, 10.0, 500.0),
    (7000.0, 100, 15.0, 1500.0)
])
def test_telemetry_to_fe_conversion(delta_m_kg, passengers_in, route_length_km, expected_n_fe):
    calculated_passengers_by_mass = delta_m_kg / 70.0
    assert abs(calculated_passengers_by_mass - passengers_in) < 1e-5
    n_fe = passengers_in * route_length_km
    assert n_fe == expected_n_fe

def test_calculate_nrm_metrics_success(engine):
    nr_base, nr_fact, k_sn = engine.calculate_nrm_metrics(100.0, 80.0, 500.0)
    assert nr_base == 0.2
    assert nr_fact == 0.16
    assert k_sn == 1.25

@patch("NoveaAtomEngine.requests.post")
def test_execute_payout_success(mock_post, engine):
    mock_response_oauth = MagicMock()
    mock_response_oauth.status_code = 200
    mock_response_oauth.json.return_value = {"access_token": "ACCESS_TOKEN_MOCK_2026_VALID"}
    mock_response_payout = MagicMock()
    mock_response_payout.status_code = 201
    mock_response_payout.json.return_value = {"batch_header": {"payout_batch_id": "MOCK_BATCH_ID_999", "batch_status": "PENDING"}}
    mock_post.side_effect = [mock_response_oauth, mock_response_payout]
    result = engine.execute_payout(10.0, 1.2, 800, "driver.nikolaev@communa.org", "REYS_2026_10_26_001")
    assert result["status"] == "SUCCESS"
    assert result["net_payout"] == 133.92

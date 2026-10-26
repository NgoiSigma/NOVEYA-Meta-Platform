import logging
import requests
from typing import Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [FDL-CORE] %(message)s')

class NoveaAtomEngine:
    def __init__(self, client_id: str, client_secret: str, mode: str = "sandbox"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = "https://api-m.sandbox.paypal.com" if mode == "sandbox" else "https://api-m.paypal.com"
        self.shrine_pct = 0.10
        self.r_rate = 15.5

    def _get_paypal_token(self) -> str:
        url = f"{self.api_url}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en_US"}
        try:
            response = requests.post(
                url, 
                auth=(self.client_id, self.client_secret), 
                data={"grant_type": "client_credentials"}, 
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()["access_token"]
        except Exception as e:
            logging.error(f"Ошибка авторизации PayPal API: {e}")
            raise

    def calculate_nrm_metrics(self, t_base: float, t_fact: float, n_fe: float) -> Tuple[float, float, float]:
        if n_fe <= 0:
            raise ValueError("Количество Функциональных Единиц (N_FE) должно быть больше нуля.")
        nr_base = t_base / n_fe
        nr_fact = t_fact / n_fe
        k_sn = nr_base / nr_fact if nr_fact > 0 else 0.0
        return nr_base, nr_fact, k_sn

    def calculate_true_labor(self, t_base: float, c_ch: float, f_k: float) -> float:
        denominator = c_ch - f_k
        if denominator <= 0.01:
            denominator = 0.01
        return t_base / denominator

    def evaluate_fdl_score(self, k_sn: float, c_ch: float, f_k: float) -> int:
        base_score = (k_sn * 400) + (c_ch * 300) + (f_k * 100)
        return int(max(0, min(1000, base_score)))

    def execute_payout(self, tr: float, k_sn: float, fdl_score: int, recipient_email: str, job_id: str) -> Dict[str, Any]:
        if fdl_score < 700:
            logging.error(f"Отказ в выплате. FDL-Score ({fdl_score}) ниже нормативного порога 700.")
            return {"status": "REJECTED", "reason": "Low FDL-Score"}
        t_fdl = (tr * k_sn * fdl_score) / 1000.0
        gross_payout = t_fdl * self.r_rate
        fnv_deduction = gross_payout * self.shrine_pct
        net_payout = round(gross_payout - fnv_deduction, 2)
        token = self._get_paypal_token()
        url = f"{self.api_url}/v1/payouts"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        payload = {
            "sender_batch_header": {
                "sender_batch_id": f"BATCH_{job_id}",
                "email_subject": "Выплата по хозрасчету громады (NoveaAtomEngine)",
                "recipient_type": "EMAIL"
            },
            "items": [{
                "recipient_type": "EMAIL",
                "amount": {"value": f"{net_payout}", "currency": "USD"},
                "note": "Оплата за транспортный вклад громады по системе КУБ v1. Удержано 10% в FNV.",
                "receiver": recipient_email,
                "sender_item_id": f"ITEM_{job_id}"
            }]
        }
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        return {"status": "SUCCESS", "net_payout": net_payout, "fnv_allocation": fnv_deduction, "paypal_response": response.json()}

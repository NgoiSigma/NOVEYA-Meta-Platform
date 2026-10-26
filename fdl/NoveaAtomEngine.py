"""
Core Engine: NoveaAtomEngine
Component: FDL-Audit, Resource Norming (NRM) & PayPal Payouts Gateway
Language: Python 3.10+
License: Open-Source Community Property (KUB v1)
"""

import sys
import logging
import requests
from typing import Dict, Any, Tuple

# Настройка логирования хозрасчета
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [FDL-CORE] %(message)s')

class NoveaAtomEngine:
    def __init__(self, client_id: str, client_secret: str, mode: str = "sandbox"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = "https://paypal.com" if mode == "sandbox" else "https://paypal.com"
        self.shrine_pct = 0.10  # 10% отчислений в Фонд Нового Витка (FNV)
        self.r_rate = 15.5      # Базовый курс компенсации труда общины (UAH/USD эквивалент за единицу Tr)

    def _get_paypal_token(self) -> str:
        """Получение токена авторизации OAuth 2.0 в контуре PayPal API."""
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
        """
        Блок требований (БТ) и Идей (БИ) по методике НРМ.
        Вычисление базовой ресурсоемкости, фактической ресурсоемкости и Ksn.
        """
        if n_fe <= 0:
            raise ValueError("Количество Функциональных Единиц (N_FE) должно быть больше нуля.")
        
        nr_base = t_base / n_fe
        nr_fact = t_fact / n_fe
        
        # Коэффициент совершенствования нормирования (Ksn)
        k_sn = nr_base / nr_fact if nr_fact > 0 else 0.0
        return nr_base, nr_fact, k_sn

    def calculate_true_labor(self, t_base: float, c_ch: float, f_k: float) -> float:
        """
        Расчет трудоемкости при истинном качестве исполнения (Tr) по формуле ФДЛ:
        Tr = To / (Cч - f(K))
        """
        # Ограничения показателей (ОГПО): Cч в границах [0.3, 1.8], f(K) штрафная/поощрительная функция
        # Знаменатель защищен от деления на ноль и сингулярности среды
        denominator = c_ch - f_k
        if denominator <= 0.01:
            logging.warning("Критическое падение качества среды! Применение защитного лимита знаменателя.")
            denominator = 0.01
            
        tr = t_base / denominator
        return tr

    def evaluate_fdl_score(self, k_sn: float, c_ch: float, f_k: float) -> int:
        """
        Диалектический аудит ИИ-Агента (Синтез FDL-Score).
        Интегральная оценка от 0 до 1000 баллов.
        """
        base_score = (k_sn * 400) + (c_ch * 300) + (f_k * 100)
        fdl_score = int(max(0, min(1000, base_score)))
        return fdl_score

    def execute_payout(self, tr: float, k_sn: float, fdl_score: int, recipient_email: str, job_id: str) -> Dict[str, Any]:
        """
        Блок Исполнения (PayPal Bridge). Конвертация Tfdl и выплата с удержанием 10% в FNV.
        """
        if fdl_score < 700:
            logging.error(f"Отказ в выплате. FDL-Score ({fdl_score}) ниже нормативного порога 700.")
            return {"status": "REJECTED", "reason": "Low FDL-Score"}

        # 1. Эмиссия FDL-Токенов
        t_fdl = (tr * k_sn * fdl_score) / 1000.0
        
        # 2. Расчет финансового эквивалента (USD/UAH) с удержанием 10% в Фонд Нового Витка
        gross_payout = t_fdl * self.r_rate
        fnv_deduction = gross_payout * self.shrine_pct
        net_payout = round(gross_payout - fnv_deduction, 2)
        
        logging.info(f"Труд верифицирован. T_fdl: {t_fdl:.2f}. Начислено: {gross_payout:.2f}. В FNV удержано: {fnv_deduction:.2f}. К выплате: {net_payout}")

        # 3. Формирование транзакции к PayPal API Gateway
        token = self._get_paypal_token()
        url = f"{self.api_url}/v1/payouts"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        payload = {
            "sender_batch_header": {
                "sender_batch_id": f"BATCH_{job_id}",
                "email_subject": "Выплата по хозрасчету громады (NoveaAtomEngine)",
                "recipient_type": "EMAIL"
            },
            "items": [
                {
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": f"{net_payout}",
                        "currency": "USD"
                    },
                    "note": f"Оплата за транспортный вклад громады по системе КУБ v1. Удержано 10% в FNV.",
                    "receiver": recipient_email,
                    "sender_item_id": f"ITEM_{job_id}"
                }
            ]
        }

        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        
        logging.info(f"Выплата PayPal успешно инициирована для {recipient_email}. Batch ID: {f'BATCH_{job_id}'}")
        return {
            "status": "SUCCESS",
            "net_payout": net_payout,
            "fnv_allocation": fnv_deduction,
            "paypal_response": response.json()
        }

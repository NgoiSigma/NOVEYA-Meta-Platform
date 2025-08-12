fdl_lexicon_guard.py

Σ-FDL::TAURUS-ΣIGIL

Лексико-смысловой модуль различения и защиты инфополя

class LexiconGuard: """ Модуль выявления опасных лексем, подмен и враждебных формулировок в текстах. Строит простую эвристику смыслового различения и сигнализирует о потенциальных подменах. """

def __init__(self):
    self.triggers = {
        "sustainable development": "проверить контекст: часто используется как прикрытие контроля",
        "inclusive economy": "возможна подмена: уточнить, кого включают и как",
        "zero ownership": "проверить, не внедряется ли сценарий обнуления частной субъектности",
        "AI regulation": "проверить, кто регулирует и в чьих интересах",
        "smart society": "проверить, не подменяется ли живое на управляемое"
    }

def scan(self, text: str) -> dict:
    """
    Анализирует текст и возвращает найденные подозрительные лексемы с комментариями.
    """
    findings = {}
    for key in self.triggers:
        if key.lower() in text.lower():
            findings[key] = self.triggers[key]
    return findings

Пример использования

if name == "main": lg = LexiconGuard() sample = "The inclusive economy is part of our sustainable development plan." results = lg.scan(sample) print("Анализ лексики:") for term, comment in results.items(): print(f"- '{term}': {comment}")

# fdl_lexicon_guard.py
# Σ-FDL::TAURUS-ΣIGIL
# Лексико-смысловой модуль различения и защиты инфополя

class LexiconGuard:
    """
    Модуль выявления опасных лексем, подмен и враждебных формулировок в текстах.
    Строит простую эвристику смыслового различения и сигнализирует о потенциальных подменах.
    """

    def __init__(self):
        self.triggers = {
            "sustainable development": "проверить контекст: часто используется как прикрытие контроля",
            "inclusive economy": "возможна подмена: уточнить, кого включают и как",
            "zero ownership": "проверить, не внедряется ли сценарий обнуления частной субъектности",
            "AI regulation": "проверить, кто регулирует и в чьих интересах",
            "smart society": "проверить, не подменяется ли живое на управляемое"
        }

    def scan(self, text: str) -> dict:
        """
        Анализирует текст и возвращает найденные подозрительные лексемы с комментариями.
        """
        findings = {}
        for key in self.triggers:
            if key.lower() in text.lower():
                findings[key] = self.triggers[key]
        return findings

# Пример использования
if __name__ == "__main__":
    lg = LexiconGuard()
    sample = "The inclusive economy is part of our sustainable development plan."
    results = lg.scan(sample)
    print("Анализ лексики:")
    for term, comment in results.items():
        print(f"- '{term}': {comment}")

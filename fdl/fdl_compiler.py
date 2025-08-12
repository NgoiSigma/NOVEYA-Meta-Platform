fdl_compiler.py

""" FDL Compiler — преобразователь FDL-языка в исполняемую логическую структуру (AST + runtime) Фаза: интерпретация резонансных блоков, проверка обратимости, инициация откликов """

import json from typing import List, Dict

class FDLBlock: def init(self, block_id: str, structure: Dict): self.block_id = block_id self.structure = structure

def __repr__(self):
    return f"FDLBlock<{self.block_id}>"

class FDLCompiler: def init(self): self.blocks: List[FDLBlock] = [] self.errors: List[str] = []

def parse(self, source: str):
    current = {}
    block_id = "block_0"
    for line in source.strip().splitlines():
        if ':' in line:
            key, val = line.strip().split(':', 1)
            current[key.strip()] = val.strip()
    self.blocks.append(FDLBlock(block_id, current))

def validate(self):
    for block in self.blocks:
        required_fields = ["замысел", "форма", "поток"]
        for field in required_fields:
            if field not in block.structure:
                self.errors.append(f"{block.block_id}: отсутствует поле '{field}'")

def compile(self):
    if self.errors:
        return None
    return json.dumps([b.structure for b in self.blocks], ensure_ascii=False, indent=2)

def report(self):
    if self.errors:
        return {"status": "ошибки", "errors": self.errors}
    return {"status": "готово", "blocks": len(self.blocks)}

Пример использования

if name == 'main': source = """ замысел: протестировать систему форма: логический анализ поток: от агента к ядру сигнал: обратная связь отклик: лог печати контур: проверка синтаксиса """ compiler = FDLCompiler() compiler.parse(source) compiler.validate() result = compiler.compile() print(result if result else compiler.report())

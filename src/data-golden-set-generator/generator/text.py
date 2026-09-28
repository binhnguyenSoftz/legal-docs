"""Văn bản tự do (lý do đề nghị, mô tả).

Hiện chỉ chọn từ `fallback` trong schema. Khi nối LLM:
- Sinh theo lô trước, lưu cache theo (procedure, doc_type, field, seed) vào generated/_llm_cache/,
  để cùng seed luôn ra cùng câu, không gọi lại model.
- Không đưa dữ liệu persona vào prompt nếu không cần; văn bản không được chứa trường có cấu trúc.
"""

import random


def llm_text(rng: random.Random, params: dict, ctx: dict) -> str:
    return rng.choice(params.get("fallback") or [""])

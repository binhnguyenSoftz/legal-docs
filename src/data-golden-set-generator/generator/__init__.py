"""Sinh hồ sơ hành chính giả có ground truth cho golden set (AIP-026).

Tăng GENERATOR_VERSION mỗi khi đổi logic sinh làm thay đổi kết quả với cùng seed.
"""

from pathlib import Path

GENERATOR_VERSION = "0.4.0"

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
RESOURCES_DIR = ROOT / "resources"
GENERATED_DIR = ROOT / "generated"

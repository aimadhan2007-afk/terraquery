"""Optional before/after change detection utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ChangeDetectionResult:
	"""A compact summary of how much two images differ."""

	before_path: str
	after_path: str
	score: float
	changed: bool


def compute_change_score(before_path: str | Path, after_path: str | Path) -> float:
	"""Compute a simple normalized pixel-difference score.

	This optional utility intentionally stays lightweight; it can be replaced
	later with a learned change-detection model without changing the public API.
	"""

	try:
		from PIL import Image
		import numpy as np
	except ImportError as exc:  # pragma: no cover - depends on optional package
		raise ImportError("Pillow and numpy are required for change detection") from exc

	before = Image.open(before_path).convert("RGB")
	after = Image.open(after_path).convert("RGB")
	if before.size != after.size:
		after = after.resize(before.size)

	before_array = np.asarray(before, dtype=np.float32)
	after_array = np.asarray(after, dtype=np.float32)
	return float(np.mean(np.abs(before_array - after_array)) / 255.0)


def detect_change(before_path: str | Path, after_path: str | Path, threshold: float = 0.12) -> ChangeDetectionResult:
	score = compute_change_score(before_path, after_path)
	return ChangeDetectionResult(
		before_path=str(before_path),
		after_path=str(after_path),
		score=score,
		changed=score >= threshold,
	)

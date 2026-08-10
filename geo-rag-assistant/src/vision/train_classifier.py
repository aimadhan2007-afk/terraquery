"""Train or fine-tune the EuroSAT land-cover classifier."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class TrainingConfig:
	"""Configuration for a land-cover training run."""

	data_root: str
	output_path: str = "models/eurosat_resnet18.pt"
	num_classes: int = 10
	batch_size: int = 32
	epochs: int = 5
	learning_rate: float = 1e-4
	image_size: int = 64


def load_eurosat_dataset(data_root: str, split: str = "train"):
	"""Load EuroSAT from torchgeo.

	Importing torchgeo lazily keeps this module importable in lightweight test
	environments while still exposing the requested training workflow.
	"""

	try:
		from torchgeo.datasets import EuroSAT
	except ImportError as exc:  # pragma: no cover - depends on optional package
		raise ImportError("torchgeo is required to load EuroSAT") from exc

	return EuroSAT(root=data_root, split=split, download=False)


def build_resnet18(num_classes: int):
	"""Create a ResNet-18 classifier with a custom head."""

	try:
		import torch
		from torchvision.models import ResNet18_Weights, resnet18
	except ImportError as exc:  # pragma: no cover - depends on optional package
		raise ImportError("torch and torchvision are required for classifier training") from exc

	model = resnet18(weights=ResNet18_Weights.DEFAULT)
	model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
	return model


def create_transforms(image_size: int = 64):
	"""Return a standard augmentation pipeline for satellite patches."""

	try:
		from torchvision import transforms
	except ImportError as exc:  # pragma: no cover - depends on optional package
		raise ImportError("torchvision is required for classifier training") from exc

	return transforms.Compose(
		[
			transforms.Resize((image_size, image_size)),
			transforms.RandomHorizontalFlip(),
			transforms.RandomVerticalFlip(),
			transforms.ToTensor(),
		]
	)


def save_model(model, output_path: str | Path) -> str:
	"""Persist model weights to disk."""

	try:
		import torch
	except ImportError as exc:  # pragma: no cover - depends on optional package
		raise ImportError("torch is required to save model weights") from exc

	output_path = Path(output_path)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	torch.save(model.state_dict(), output_path)
	return str(output_path)


def train_classifier(config: TrainingConfig) -> str:
	"""Train a ResNet-18 classifier and save the resulting checkpoint."""

	try:
		import torch
		from torch import nn
		from torch.utils.data import DataLoader
	except ImportError as exc:  # pragma: no cover - depends on optional package
		raise ImportError("torch is required for training") from exc

	dataset = load_eurosat_dataset(config.data_root, split="train")
	model = build_resnet18(config.num_classes)
	criterion = nn.CrossEntropyLoss()
	optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
	loader = DataLoader(dataset, batch_size=config.batch_size, shuffle=True)

	model.train()
	for _ in range(config.epochs):
		for images, labels in loader:
			optimizer.zero_grad()
			logits = model(images)
			loss = criterion(logits, labels)
			loss.backward()
			optimizer.step()

	return save_model(model, config.output_path)


if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description="Train a EuroSAT land-cover classifier.")
	parser.add_argument("data_root")
	parser.add_argument("--output-path", default="models/eurosat_resnet18.pt")
	parser.add_argument("--num-classes", type=int, default=10)
	parser.add_argument("--batch-size", type=int, default=32)
	parser.add_argument("--epochs", type=int, default=5)
	parser.add_argument("--learning-rate", type=float, default=1e-4)
	args = parser.parse_args()

	checkpoint = train_classifier(
		TrainingConfig(
			data_root=args.data_root,
			output_path=args.output_path,
			num_classes=args.num_classes,
			batch_size=args.batch_size,
			epochs=args.epochs,
			learning_rate=args.learning_rate,
		)
	)
	print(f"Saved trained model to {checkpoint}")

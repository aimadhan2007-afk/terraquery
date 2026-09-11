from torchvision.datasets import ImageFolder

def load_eurosat(root: str = "data/imagery/eurosat") -> None:
    dataset = ImageFolder(root=root)
    print(f"Loaded {len(dataset)} images")
    print(f"Classes: {dataset.classes}")

if __name__ == "__main__":
    load_eurosat()
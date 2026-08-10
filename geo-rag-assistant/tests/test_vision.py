"""Vision tests for the geospatial RAG prototype."""

from src.vision.image_to_metadata import ImageMetadata, metadata_to_description, metadata_to_json


def test_metadata_serialization_uses_expected_schema():
	metadata = ImageMetadata(region="Bengaluru", date="2026-08-10", class_name="Urban", confidence=0.91)

	assert metadata.to_dict() == {
		"region": "Bengaluru",
		"date": "2026-08-10",
		"class": "Urban",
		"confidence": 0.91,
	}
	assert "Region: Bengaluru" in metadata_to_description(metadata)
	assert metadata_to_json(metadata) == '{"region": "Bengaluru", "date": "2026-08-10", "class": "Urban", "confidence": 0.91}'

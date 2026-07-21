from services import document
from services import constants

doc = document.nouveau_document()

assert doc["info"]["version"] != ""
assert doc["info"]["errors"] == []

assert len(doc["competitors"]) == constants.COMPETITOR_COUNT

assert "race" in doc
assert "calculation" in doc

assert doc["race"]["run"] == 1

doc["competitors"][0]["bib"] = "12"
assert doc["competitors"][1]["bib"] == ""

doc["calculation"]["reference_indexes"].append(3)

doc2 = document.nouveau_document()
assert doc2["calculation"]["reference_indexes"] == []

print("Tous les tests Document sont OK")
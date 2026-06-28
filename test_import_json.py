from pprint import pprint

import json

from services.document import nouveau_document
from services.importer import importer_json

with open(
    "examples/fis.json",
    encoding="utf-8"
) as f:

    data = json.load(f)

document = nouveau_document()

importer_json(
    document,
    data
)

pprint(
    document,
    sort_dicts=False
)
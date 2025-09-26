from pathlib import Path
import json

INPUT_JSON = "ALLOBATES-A0A0G2T1Z6.json"
OUTPUT_TSV = "entry.tsv"

data = json.loads(Path(INPUT_JSON).read_text(encoding="utf-8"))

try:
    protein_name = data["proteinDescription"]["recommendedName"]["fullName"]["value"]
except KeyError:
    protein_name = ""

row = {
    "primaryAccession": data.get("primaryAccession"),
    "uniProtkbId":      data.get("uniProtkbId"),
    "entryType":        data.get("entryType"),
    "proteinName":      protein_name,
    "organism_scientificName": (data.get("organism") or {}).get("scientificName"),
    "organism_taxonId":        (data.get("organism") or {}).get("taxonId"),
    "sequence_length":  (data.get("sequence") or {}).get("length"),
    "sequence":         (data.get("sequence") or {}).get("value"),
}

headers = list(row.keys())
with open(OUTPUT_TSV, "w", encoding="utf-8") as f:
    f.write("\t".join(headers) + "\n")
    f.write("\t".join("" if row[h] is None else str(row[h]) for h in headers) + "\n")

print(f"Listo: 1 fila → {OUTPUT_TSV}")

from pathlib import Path
import json
# Archivo de entrada (JSON de UniProt) y de salida (TSV)
INPUT_JSON = "ALLOBATES-A0A0G2T1Z6.json"
OUTPUT_TSV = "entry.tsv"
# Leo el JSON completo como texto y lo convierto a diccionario
data = json.loads(Path(INPUT_JSON).read_text(encoding="utf-8"))
# Leo el JSON completo como texto y lo convierto a diccionario
try:
    protein_name = data["proteinDescription"]["recommendedName"]["fullName"]["value"]
except KeyError:
    protein_name = ""
# Armo una sola fila con los campos que me interesan; uso .get para evitar errores si faltan claves
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
# Extraigo el orden de columnas desde las llaves del diccionario
headers = list(row.keys())
# Escribo un TSV simple: primera línea encabezados, segunda línea los valores
with open(OUTPUT_TSV, "w", encoding="utf-8") as f:
    f.write("\t".join(headers) + "\n")
    # Convierto None a "" y todo a str para que no falle el join
    f.write("\t".join("" if row[h] is None else str(row[h]) for h in headers) + "\n")
#Aviso de que ya esta listo
print(f"Listo: 1 fila → {OUTPUT_TSV}")

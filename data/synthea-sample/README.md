# Synthea Sample Data

Generated from [Synthea](https://github.com/synthetichealth/synthea) v3.5.0 (master-branch-latest), an open-source synthetic patient generator.

## Source

```bash
java -jar synthea-with-dependencies.jar -p 10000 \
  --exporter.baseDirectory=sim/synthea/output
```

## Full dataset (local only, ~30GB)

- **Location:** `data/synthea/fhir/` (gitignored)
- **11,462 patients** (10,000 alive + 1,462 deceased)
- **15.2M FHIR R4 resources** across 25 NDJSON files
- All resource types: Patient, Encounter, Observation, Condition, MedicationRequest, Procedure, etc.
- US-weighted demographics (Massachusetts default region)

## Sample (this directory, committed, ~20MB)

- **FHIR NDJSON:** `fhir/*.ndjson` — ~0.07% random subsample of each resource type (20MB total)
- **CSV:** `patients.csv` — all 11,462 patients flattened to a single table with fields: id, given_name, family_name, gender, birth_date, deceased, city, state, marital_status, race
- Race field is drawn from Synthea's ethnicity extension; values may be empty for some patients

## Regenerating

To regenerate the full dataset:

```bash
brew install openjdk
curl -L -o /tmp/synthea.jar \
  https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar
java -jar /tmp/synthea.jar -p 10000
```

Or via Docker (slower on ARM64, requires Rosetta emulation).

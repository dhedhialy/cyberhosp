# Architecture Overview

*Coming soon — see README.md for the high-level architecture diagram and component map.*

## Data Flow

```
EHR → FHIR/HL7 Adapter → Audit Pipeline → Detection Engine → Response Layer → SIEM/Dashboard
```

## Key Design Decisions

1. **Immutable audit logs** — cryptographic chain-of-custody for compliance and forensic integrity.
2. **Out-of-band monitoring** — read-only access to EHR audit streams; zero write-back to clinical systems.
3. **Pluggable EHR adapters** — vendor-specific adapters implement a common interface; adding a new EHR is a single module.
4. **Policy-as-code** — DLP rules, anomaly thresholds, and incident playbooks are declarative YAML.

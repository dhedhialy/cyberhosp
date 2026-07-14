# Threat Coverage Map

Mapping the Splunk Top 50 Cybersecurity Threats against CyberHosp's
scope.  Only threats that manifest at the EHR data-access layer (post-
authentication) are in scope.

## Already Covered

| # | Threat | Detector | Alert Type |
|---|--------|----------|------------|
| 2 | Data exfiltration (bulk) | MassAccessDetector | MASS_RECORD_ACCESS |
| 22 | Insider threat (compromised creds) | All detectors combined | Various |

## In Scope — Need Detection Rules

| # | Threat | What to detect | Priority |
|---|--------|---------------|----------|
| 1 | APT | Long-term slow data access patterns, staging behavior | High |
| 3 | Session hijacking | Token reuse across IPs/devices, concurrent sessions | High |
| 13 | Data exfiltration (cloud) | Outbound API calls to unusual destinations, bulk FHIR exports | High |
| 14 | Insecure APIs | FHIR API abuse, parameter tampering, forced browsing | High |
| 17 | SaaS authentication exploits | Auth anomalies, unusual token grants | Medium |
| 20 | Suspicious cloud auth | Impossible travel (partially done), device fingerprint changes | Medium |
| 21 | Brute force attack | Failed login rate per user, per IP | High |
| 23 | Insider misuse / privilege escalation | Role changes, department switches, permission grants | High |
| 24 | MFA fatigue attacks | Repeated MFA push rejections followed by accept | Medium |
| 25 | Password spraying | Distributed failed logins across many accounts | High |
| 41 | BEC (post-compromise) | Abnormal financial record access, payment data views | Medium |
| 48 | API exploitation | FHIR API abuse, pagination scraping, IDOR attempts | High |

## Out of Scope (Infrastructure / Network / Endpoint / Web App)

All AI threats (#6-11), network/infrastructure (#27-32), malware/exploits
(#33-40), web application vulnerabilities (#49-53), and phishing delivery
vectors (#42-47 pre-compromise).  These require endpoint, network, or
email security tools outside CyberHosp's data-layer focus.

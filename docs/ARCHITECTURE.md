# System Architecture

```text
User
  ↓
Privacy Questionnaire
  ↓
Input Validation
  ↓
Privacy Feature Extraction
  ↓
┌─────────────────────────────┐
│ Profile Exposure Analyzer   │
│ Personal Info Analyzer      │
│ Location Analyzer           │
│ Content Analyzer            │
│ Connections Analyzer        │
│ Tagging Analyzer            │
│ Account Security Analyzer   │
│ Third-Party Apps Analyzer   │
│ Social Engineering Analyzer │
│ Digital Footprint Analyzer  │
└─────────────────────────────┘
  ↓
Category Scores (0–100)
  ↓
Weighted Risk Scoring
  ↓
Overall Risk + Classification
  ↓
Findings Engine
  ↓
Recommendation Engine
  ↓
Dashboard / Improvement Simulator / Report
  ↓
Privacy-safe SQLite metadata
```

The design follows the project specification's defensive scope: no live scraping, no private-profile access, no real-user tracking, and no unnecessary PII collection.

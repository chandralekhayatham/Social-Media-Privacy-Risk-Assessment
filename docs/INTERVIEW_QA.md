# Interview Preparation

1. **Explain your project.** — It is a defensive privacy-risk assessment framework. A questionnaire converts self-reported practices into category scores, a weighted engine produces an overall 0–100 risk score, and the application generates findings, recommendations, a simulator, dashboard, and report.
2. **Privacy vs security?** — Privacy controls how personal information is exposed and used; security protects accounts and systems from unauthorized access. A strong password does not automatically mean strong privacy.
3. **What is a digital footprint?** — Information associated with online activity. The project assesses only self-reported practices such as old-post review and public profile exposure.
4. **How is risk scored?** — Ten categories produce 0–100 scores and are combined using configurable weights from the project specification.
5. **How can oversharing increase social-engineering risk?** — Public context can make fraudulent messages more believable, so the project focuses on reducing unnecessary exposure.
6. **Why MFA?** — Account security and privacy overlap; MFA can reduce account-takeover risk and therefore protect non-public information.
7. **Third-party app risk?** — Old or unnecessary integrations can retain permissions. The project recommends periodic review and least privilege.
8. **Privacy by Design?** — The project asks whether sensitive information is public rather than collecting the information itself, and stores minimal assessment metadata.
9. **What is the simulator?** — It compares a current assessment with a hypothetical improved configuration and shows the framework's estimated risk reduction.
10. **How did you test it?** — Automated tests cover questionnaire size, scoring, thresholds, findings, and simulation; manual privacy checks verify that sensitive information is not stored.

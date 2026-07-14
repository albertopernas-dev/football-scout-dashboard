# Provider Decisions

This folder contains decision records for market-context data providers evaluated for Football Scout Dashboard.

Provider decision records are planning and due-diligence documents. They should be written before integrating provider-specific code or loading provider data into the app workflow.

Do not include:

- credentials;
- API keys;
- proprietary datasets;
- raw provider dumps;
- restricted screenshots;
- copied data that cannot be redistributed.

Decision records can evaluate:

- official league or club sources;
- licensed sports data providers;
- public APIs with explicit terms;
- manually reviewed public references;
- existing provider limitations.

Each evaluated provider or source type should have its own file. Use [`provider_decision_template.md`](provider_decision_template.md) as the starting point.

When a decision record evaluates a provider payload, it should link to or complete the [Provider Payload Evaluation Checklist](../provider_payload_evaluation_checklist.md) before any integration work begins.

Related documents:

- [v0.4.0 Provider Evaluation / Licensed Data Integration Plan](../v0_4_0_provider_evaluation_plan.md)
- [Data Provider Decision](../data_provider_decision.md)
- [Provider Payload Evaluation Checklist](../provider_payload_evaluation_checklist.md)

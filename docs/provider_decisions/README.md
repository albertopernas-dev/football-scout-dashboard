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

Each evaluated provider or source type should have its own file. Use [`provider_decision_template.md`](provider_decision_template.md) for a general provider evaluation. Use [`provider_payload_evaluation_template.md`](provider_payload_evaluation_template.md) when evaluating a specific payload.

Every real payload evaluation must complete or link to the [Provider Payload Evaluation Checklist](../provider_payload_evaluation_checklist.md) before any integration work begins.

For v0.7.0, a concrete candidate payload must use the payload evaluation template and complete the checklist before any local experiment begins. The candidate review pack organizes the review but does not replace the payload decision record.

Related documents:

- [Sportmonks Payload Decision Record](sportmonks_payload_decision_record.md) - draft/pre-trial governance record; it does not approve Sportmonks.
- [v0.4.0 Provider Evaluation / Licensed Data Integration Plan](../v0_4_0_provider_evaluation_plan.md)
- [Data Provider Decision](../data_provider_decision.md)
- [Provider Payload Evaluation Checklist](../provider_payload_evaluation_checklist.md)
- [v0.7.0 Permitted Provider Candidate Review Plan](../v0_7_0_permitted_provider_candidate_review_plan.md)
- [v0.7.0 Candidate Review Workflow](../v0_7_0_candidate_review_workflow.md)
- [v0.7.0 Candidate Review Pack Template](../v0_7_0_candidate_review_pack_template.md)
- [Provider Payload Evaluation Template](provider_payload_evaluation_template.md)
- [Synthetic Payload Evaluation Example](example_synthetic_payload_evaluation.md) - synthetic documentation example only; not approval of a real provider.

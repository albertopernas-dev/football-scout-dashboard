# Release Notes v0.8.0

## Summary

v0.8.0 closes provider permission response handling for Sportmonks as a candidate.

It adds governance records, local-only scaffold validation and one aggregate preview.

Sportmonks remains unapproved.

## Added

- Permission response summary.
- Payload checklist.
- Ignored local trial scope governance.
- Secure credential setup verification.
- Minimal ID discovery summary.
- Minimal payload field review summary.
- Transform design plan.
- Implementation plan.
- First local-only Sportmonks transform scaffold.
- Synthetic tests.
- Preview approval decision.
- Local preview summary.
- Preview result decision.
- Closeout decision.

## Technical Validation

- Local-only transform scaffold implemented.
- Synthetic tests passed previously.
- One approved preview completed.
- Preview result:
  - `row_count 6`
  - `has_position_ids 0`
  - `has_jersey_numbers 0`
- No raw JSON included.
- No player IDs or names included.

## Limitations

- Sportmonks not approved.
- No app integration.
- No SQLite loading.
- No `.local.csv`.
- No local trial.
- Labels unresolved.
- Position coverage unresolved.
- Jersey coverage unresolved.
- Market Context unresolved.

## Safety

- No API calls during closeout.
- No manual raw JSON review.
- No additional cache reading.
- Credentials remain ignored.
- Provider cache remains ignored.
- No provider payloads committed.

## Next

Future v0.9.0 may choose whether to continue Sportmonks exploration, compare providers, design label lookup, plan a local trial or stop.

# Setup Guide

## Requirements

- n8n with Code, Webhook, Execute Workflow, Data Table, Telegram, and LangChain nodes
- OpenAI credential configured in n8n
- Google Gemini credential configured in n8n
- Telegram credential configured in n8n if HITL notifications are enabled
- A private job knowledge-base document mounted outside the repository

## Import order

Import and configure the workflows in this order:

1. `job-context-rag-worker.json`
2. `eligibility-screening-worker.json`
3. `match-scorecard-worker.json`
4. `ai-evaluation-supervisor.json`
5. `error-handler.json`
6. `candidate-screening-orchestrator.json`
7. `application-intake.json`

After import, select the corresponding workflow in every Execute Workflow node. The public JSON files contain `REPLACE_WITH_WORKFLOW_ID` placeholders instead of deployment-specific identifiers.

## Credentials

Open each model and Telegram node and select a locally configured n8n credential. Credentials and credential references are intentionally absent from the repository.

## Private RAG source

The RAG worker expects a private file at:

```text
/data/private-recruiting-knowledge-base.pdf
```

Change the path in the **Read Private Knowledge Base PDF** node if needed. Do not add the document to this repository.

The indexed document metadata should include:

| Field | Purpose |
| --- | --- |
| `document_id` | Stable private document identifier |
| `document_title` | Human-readable source title |
| `version` | Source version |
| `job_id` | Job identifier used by the application payload |
| `source_file` | Internal source filename |

## Data Tables

Create two Data Tables and select them manually in the relevant nodes.

### Idempotency table

| Column | Type |
| --- | --- |
| `idempotency_key` | String |
| `trace_id` | String |
| `status` | String |
| `execution_id` | String |

### Audit table

Use the field schema exposed by the **Write Audit Log** node. Core fields include `trace_id`, `timestamp`, `candidate_id`, `job_id`, `decision_band`, `autonomy_level`, `evidence`, supervisor metrics, RAG metadata, token estimates, and `cost_usd`.

## Error workflow

In the orchestrator workflow settings, select **Recruiting - Error Handler** as the error workflow. This reference is intentionally removed from the public export.

## Human review

Set `REVIEW_TEAM_CHAT_ID` in the n8n runtime environment or provide `review_team_chat_id` through a secure upstream configuration. Never commit a real chat ID.

## Safe test sequence

1. Keep every workflow inactive.
2. Configure credentials, sub-workflow references, Data Tables, and the private RAG file.
3. Run `examples/application.json` in `staging` with `deployment_phase: 0`.
4. Confirm PII masking, RAG coverage, audit writes, and supervisor output.
5. Repeat the exact payload to confirm duplicate prevention.
6. Test a controlled failure and retry before activating production intake.


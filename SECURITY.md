# Security and Privacy

## Do not commit

- Candidate resumes, answers, messages, names, email addresses, or phone numbers
- Employer job descriptions or internal hiring notes
- API keys, OAuth tokens, passwords, or exported `.env` files
- n8n credential objects or credential identifiers
- Telegram chat IDs
- Data Table, spreadsheet, document, project, or production workflow IDs
- Local file-system paths that disclose user or organization information
- n8n execution exports containing production data

## Before publishing an n8n export

1. Remove every `credentials` object.
2. Replace workflow, Data Table, chat, document, and spreadsheet identifiers.
3. Remove pinned data and execution samples.
4. Remove instance metadata, workflow IDs, and production webhook paths.
5. Search for names, email addresses, phone numbers, local paths, and organization names.
6. Run `python scripts/validate_exports.py`.

## Candidate-data handling

Use fictional data for development and repository examples. Production candidate data should be stored only in systems authorized by the employer and processed according to applicable privacy, retention, and employment requirements.

## Responsible use

This project provides recruiter decision support. Human reviewers remain responsible for hiring decisions, candidate communications, legal compliance, and verification of model-generated conclusions.


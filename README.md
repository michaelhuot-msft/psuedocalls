# Pseudocalls – Fake Customer Call Generator for Foundry IQ

Generate realistic fake customer call transcripts for testing AI agents, analytics pipelines, and conversation tools. Each call simulates a ~10-minute meeting between 3–5 participants (Solution Engineers, Solution Architects, Technical Leads, etc.) discussing **Foundry IQ** implementation across multiple vertical markets.

## Features

- **5 Vertical Markets**: Healthcare, Financial Services, Retail, Manufacturing, Technology
- **4 Call Archetypes**:
  - **Problem Discovery** – Participants articulate current pain points with business impact
  - **Requirements Gathering** – Explicit functional and non-functional requirements discussion
  - **Architecture Review** – Deep technical dives on ontology, pipelines, CI/CD, and security
  - **Mixed** – Combination of all three segments
- **Realistic Dialogue**: Natural speaker rotation, follow-up questions, clarifications, and action items
- **Timestamped Transcripts**: Every line includes `[MM:SS]` timestamps
- **Structured Metadata**: JSON output with call details, participants, vertical, duration, and call type

## Quick Start

```bash
python generate_fake_calls.py
```

This generates two files:

| File | Description |
|------|-------------|
| `fake_customer_calls_2.txt` | All call transcripts with timestamps |
| `calls_metadata_2.json` | Structured metadata for each call |

## Configuration

Edit the constants at the top of `generate_fake_calls.py` to customize:

- **Number of calls** – Change the range in the `main()` loop (default: 50)
- **Output filenames** – Change `output_file` and `metadata_file` in `main()`
- **Verticals** – Add/remove entries in the `VERTICALS` dict
- **Participant roles** – Modify the `PARTICIPANT_ROLES` list
- **Companies** – Add to the `COMPANIES` list

## Sample Output

```
================================================================================
CALL #001 - Pioneer Tech (Healthcare)
Date: 2026-02-11
Duration: ~10 minutes
Participants: 5
Call Type: Problem Discovery
================================================================================

[00:00] Priya White (Data Engineer):
Good morning everyone, thanks for joining today's call. I'm Priya White and I'll
be facilitating our discussion on the Foundry IQ implementation for Pioneer Tech.

[00:10] Priya White (Data Engineer):
Before we jump in, let me do a quick round of introductions so everyone knows
who's on the line.

[00:16] Michael Jones (Customer Success Manager):
Hey team, I'm Michael Jones, serving as Customer Success Manager. Looking forward
to a productive session.

[00:24] Wei Jones (Solution Engineer):
Hi everyone, Wei Jones here. I'm the Solution Engineer on this engagement.
Excited to be part of this.

[01:10] Priya White (Data Engineer):
Let's start by getting a clear picture of the current pain points. Can someone
walk us through the biggest challenges you're facing today?

[01:25] Amanda Nakamura (Product Manager):
Our population health models are running on stale data - sometimes 48 hours old.
By the time we identify at-risk patients, interventions are already too late.

[01:46] Daniel Thompson (Solution Architect):
Walk me through a specific example. What does that look like day-to-day for
your team?
```

## Sample Metadata

```json
{
  "call_id": 1,
  "company": "Pioneer Tech",
  "vertical": "Healthcare",
  "call_type": "problem_discovery",
  "participants": [
    "Priya White (Data Engineer)",
    "Michael Jones (Customer Success Manager)",
    "Wei Jones (Solution Engineer)",
    "Amanda Nakamura (Product Manager)",
    "Daniel Thompson (Solution Architect)"
  ],
  "duration_seconds": 623,
  "duration_minutes": 10.4
}
```

## Requirements

- Python 3.6+
- No external dependencies (stdlib only)

## License

MIT

# AI Helpdesk Assistant — NASSCOM Hackathon UI

A Streamlit prototype for an IT helpdesk workflow. Users enter an issue, the app assigns a category and priority, shows a suggested response, and lets the user mark the response as helpful or request escalation. A second interface lets a service team review escalated tickets.

## Current scope

The current `ticket.py` uses **keyword-based demonstration rules**, not a trained machine-learning model or a connected ticketing backend.

| Example input pattern | Category | Priority | Demonstration response |
| --- | --- | --- | --- |
| Text contains `internet` | Network | High | Restart router, check cables, update drivers |
| Text contains `login` | Application | Medium | Reset password and clear cache |
| Anything else | General | Low | Ask the user for more details |

The confidence values and status decisions are hard-coded for this prototype. They should not be interpreted as calibrated model confidence or an automated diagnosis of a real IT incident.

## Features

- User interface to submit and analyze an issue.
- Rule-based category, priority, confidence, and suggested solution.
- Feedback controls for “Helpful” and “Not Helpful”.
- Escalation view for the service team.
- Session-based ticket counter and conversation history.

## Run locally

Requirements: Python 3.9+ and Streamlit.

```bash
git clone https://github.com/astro538/Narcomm.git
cd Narcomm
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
pip install streamlit
streamlit run ticket.py
```

**macOS / Linux**
```bash
source .venv/bin/activate
pip install streamlit
streamlit run ticket.py
```

Streamlit prints a local URL in the terminal; open it in a browser. The app runs locally by default.

## Project structure

```text
Narcomm/
├── ticket.py    # Streamlit UI and demo ticket-processing rules
└── README.md
```

## Limitations

- Tickets and feedback are stored in Streamlit session state. The current app does not provide durable database storage or guaranteed ticket persistence across sessions.
- There is no authentication, role-based access control, audit log, external notification, or integration with a real helpdesk platform.
- The issue matching is simplistic and may misclassify text.
- Do not place confidential user, organization, or infrastructure information into a publicly deployed demo.

## Next steps

A research or production-oriented version could replace the keyword rules with an evaluated classifier or language model, connect to a persistent ticket database, add authentication and authorization, and report metrics such as category precision/recall, escalation rate, and resolution time.

## License

No explicit license file was identified in the repository when this README was prepared.

# m365-automation-toolkit

Original Microsoft Graph read-only reporting and Power Automate/Logic Apps workflow recipes.

## Architecture

Interactive delegated authentication → Graph v1.0 → selected organization-free profile fields → local CSV. Workflow recipes connect Outlook, SharePoint, Teams, Excel, and Planner in a development environment.

## Prerequisites

Python 3.12; Entra public-client app configured for device-code authentication; delegated User.Read consent. Power Automate/Logic Apps recipes require development connections, licenses, and test resources.

## Setup

1. Create a public-client Entra application for a development tenant, enabling public client flows. No client secret is needed.
2. Run `pip install -r requirements.txt` and set `GRAPH_CLIENT_ID` and `GRAPH_TENANT_ID` in your shell using local values.
3. Run `python examples/profile_report.py --dry-run` to inspect the endpoint without signing in.
4. Run without `--dry-run`, complete device-code sign-in, and inspect untracked `output/profile.csv`.
5. Follow `examples/workflows.md` to build and manually test development flows; imported production connections are not included.

## Sample workflow

Graph profile → local CSV, plus documented Teams notification, Outlook intake, SharePoint approval, Excel reporting, Planner task creation, and Logic Apps orchestration recipes.

## Security

Read [SECURITY.md](SECURITY.md). Environment examples contain placeholders only.
Never commit local environment values or production exports. No deployment is automated.

## Troubleshooting

Sign-in error: verify public client configuration, development tenant, and consent. HTTP 403: verify delegated User.Read. Throttling: retry later using Retry-After. CSV is private local output and excluded from Git.

## License and attribution

Original implementations and documentation by Mudit Dholakia, licensed under MIT.
No upstream code was imported. These references informed the learning scope:
- https://github.com/pnp/powerautomate-samples
- https://github.com/pnp/script-samples
- https://github.com/Azure/logicapps
- https://github.com/microsoftgraph/msgraph-sdk-powershell
Platform services, SDK distributions, and third-party content retain their own terms.

## Updating

This is an original repository and has no upstream remote. Run `git pull --ff-only origin main`.
Review Dependabot changes and current platform documentation before upgrading.

## Validation limits

Python syntax and local smoke tests are checked before publication. Cloud execution,
tenant integrations, Tableau workbook authoring, and live agent evaluation require
your development environments and have not been verified by local checks.

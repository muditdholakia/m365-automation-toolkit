# Development workflow recipes

These are build instructions, not deployable flow exports. Use synthetic messages and
test sites; connection references and IDs belong in your environment, outside Git.

| Scenario | Trigger | Actions | Validation |
| --- | --- | --- | --- |
| Teams notification | Manual trigger with synthetic status | Teams: post message in test channel | One message; no sensitive fields |
| Outlook processing | New email in dedicated test folder | Filter subject prefix DEMO; create test SharePoint list item | Ignore unrelated messages; deduplicate by message ID |
| SharePoint approval | New item in test list | Start and wait for approval; update status; notify test Teams channel | Reject and approve paths; no self-approval for sensitive actions |
| Excel reporting | Scheduled/manual | List rows from test SharePoint list; add rows to Excel table | Serialize writes; retry lock errors; prevent formula injection |
| Planner creation | Approved test request | Create task in dedicated test plan; persist resulting task ID | Check ID before retry to avoid duplicate tasks |
| Logic Apps orchestration | Recurrence | Managed-identity HTTP call to an authorized Graph endpoint; transform; persist to test storage | Review permission model, 429 Retry-After, failed runs |

## Operational controls

Set trigger concurrency and idempotency storage deliberately. Configure timeout and
failure branches for approvals. Disable triggers before editing connections. Review
DLP policies and connector licensing. Do not assume Graph supports application
permissions for every Teams, Excel, or Planner operation; check the specific endpoint.
Use Graph v1.0 unless a documented lab explicitly labels a beta dependency.

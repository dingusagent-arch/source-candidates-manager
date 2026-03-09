# HEARTBEAT.md

# Active project queue is kept minimal. Completed items are archived in memory/90_inbox.

# Current work queue: none — heartbeat will be idle until new tasks are added.

# To add work: append a single-line task under this file. The agent will auto-advance completed items and write a progress note to memory/90_inbox.

# Rules
- The agent will perform one focused work block per heartbeat and then remove the completed item from this file and write a dated progress note to memory/90_inbox.
- The agent will not use the Reason Agent unless you explicitly approve in the session.
- If a task requires privileged actions (sudo, external installs, secrets), the agent will pause and ask for approval.

# If nothing needs attention, the agent replies exactly:
HEARTBEAT_OK

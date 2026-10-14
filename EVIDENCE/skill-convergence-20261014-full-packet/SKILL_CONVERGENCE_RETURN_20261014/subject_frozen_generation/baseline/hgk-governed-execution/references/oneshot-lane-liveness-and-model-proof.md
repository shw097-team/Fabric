# Proving a pinned one-shot VERIFY lane is alive and on-model

## Why
A VERIFY lane is dispatched as a separate `hermes_cli/main.py -z ...` process so it can carry a
model pin that `delegate_task` children cannot. Its stdout is buffered until completion, so for the
whole run the redirect file (`glm-verify.log`) stays 0 bytes. That looks identical to a hung
process. Two misreadings follow, and both cost real work:

- "0-byte log + idle parent = stalled" -> wrongly kill a lane that is working.
- "grep agent.log for the model name = proof of the pin" -> silently wrong: **log lines written by
a oneshot session carry NO `[session_id]` tag**, so a session-tagged grep returns 0 lines even
while the lane is making dozens of tool calls.

## Rules

1. **Do not judge lane liveness from its own stdout/log file.** The redirect is 0 bytes by design
   until exit.
2. **Do not judge the model pin by grepping `logs/agent.log`.** Oneshot lines are untagged. Grep
   for the model name alone and you will attribute another session's calls to your lane.
3. **Model pin proof** = read `sessions.model` for the lane's session id in the lane's HERMES_HOME
   `state.db`:
   ```
   sqlite3 state.db "SELECT id,source,model FROM sessions WHERE id='<session_id>'"
   ```
   Expect `source='oneshot'`. Get the session id from the lane child's environment
   (`HERMES_SINGLE_QUERY_SESSION=1` marks the one-shot; `HERMES_SESSION_ID` is its id) or from
   `sessions` rows created at launch time.
4. **Liveness proof** = the lane's own progress rows, not the log:
   ```
   SELECT count(*), max(timestamp) FROM messages WHERE session_id='<session_id>'
   ```
   A rising count of `tool` rows (read_file / execute_code / terminal / write_file) is progress.
   Cross-check with child-process CPU/IO delta (`cpu_delta` alone can look idle while children
   work) and the child's TCP connections.
5. **Distinguish a slow start from a stall.** A fresh one-shot can sit for minutes before its first
   model response while the provider/relay warms; that is one slow-start episode, not a block.
   Only treat it as a block when progress rows stop advancing too.

## Redaction note
These probes read `state.db` and process environment. Report counts, session ids and model names;
never paste environment values that carry secrets (RPC tokens, credentials) into a report.

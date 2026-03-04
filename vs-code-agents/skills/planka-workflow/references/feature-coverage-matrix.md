````markdown
# Planka Feature Coverage Matrix

This matrix ensures workflow tooling leverages every Planka feature category.

| Feature Category | MCP Tools | `planka_ops.py` Operations | Workflow Usage |
|---|---|---|---|
| Projects | `list_projects`, `get_project`, `create_project`, `update_project`, `delete_project` | `projects:list`, `project:get`, `project:create`, `project:update`, `project:delete` | Project discovery, setup, cleanup |
| Boards | `list_boards`, `get_board`, `create_board`, `update_board`, `delete_board` | `boards:list`, `board:get`, `board:create`, `board:update`, `board:delete` | One board per workflow process |
| Lists | `create_list`, `update_list`, `delete_list` | `list:create`, `list:update`, `list:delete` | Agent-stage columns |
| Cards | `get_card`, `create_card`, `update_card`, `move_card`, `delete_card` | `card:get`, `card:create`, `card:update`, `card:move`, `card:delete` | Primary workflow card lifecycle |
| Labels | `create_label`, `add_label_to_card`, `remove_label_from_card` | `label:create`, `label:add`, `label:remove` | Tagging (blocked, risk, feature type) |
| Task lists & tasks | `create_task_list`, `update_task_list`, `delete_task_list`, `create_task`, `update_task`, `delete_task` | `tasklist:create`, `tasklist:update`, `tasklist:delete`, `task:create`, `task:update`, `task:delete` | Acceptance checklist tracking |
| Comments | `get_comments`, `add_comment`, `delete_comment` | `comments:get`, `comment:add`, `comment:delete` | Structured handoffs and audit trail |
| Attachments | `upload_attachment`, `delete_attachment` | `attachment:upload`, `attachment:upload-file`, `attachment:delete` | Evidence/log attachments |
| Card members | `add_card_member`, `remove_card_member` | `member:add`, `member:remove` | Ownership assignment |
| Stopwatch | `update_card` with `stopwatch` payload | `stopwatch:start`, `stopwatch:stop` | Time tracking for implementation/testing |
| Custom fields | `create_custom_field_group`, `update_custom_field_group`, `delete_custom_field_group`, `create_custom_field`, `update_custom_field`, `delete_custom_field`, `set_custom_field_value`, `delete_custom_field_value` | `customgroup:create`, `customgroup:update`, `customgroup:delete`, `customfield:create`, `customfield:update`, `customfield:delete`, `customvalue:set`, `customvalue:delete` | Structured metadata (status, workflow ID, artifact path) |
| Subscribe | `update_card` with `isSubscribed` | `subscribe:set` | Notification management by active owner |

## Validation Rule

Before claiming workflow-complete integration, verify:
1. The operation catalog exposes all rows above.
2. At least one workflow playbook/example uses each category.
3. Agent sync procedures reference the full-feature operations layer.

````

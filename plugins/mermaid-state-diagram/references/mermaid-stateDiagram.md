# Mermaid stateDiagram-v2 quick reference

Source: https://mermaid.js.org/syntax/stateDiagram.html

## Basics
- Start a diagram with `stateDiagram-v2`.
- Transitions use `-->`. You can add a label with `: label`.
- If a state appears only in a transition, Mermaid creates it implicitly.

## Start/End
- Start and end are `[*]`.
- `[*] --> Idle` declares a start transition.
- `Success --> [*]` declares an end transition.

## State declarations
- Simple id: `Idle`
- With display name:
  - `state "Long Name" as LongName`
  - `LongName: Long Name`

## Composite states
- Use `state Parent { ... }` for nested states.
- You can nest multiple levels.
- Transitions can target composite states, but not internal states across different composites.

## Choice and fork/join
- Choice: declare `state Choice <<choice>>` and branch with transitions.
- Fork/join: declare `state Fork <<fork>>` and `state Join <<join>>` to split/merge flows.

## Concurrency
- Mermaid supports concurrency using the `--` separator inside a composite state.
- Refer to the source link for the exact layout when you need parallel regions.

## Direction and comments
- Set direction with `direction LR`, `direction TB`, etc.
- Comments must be on their own line and start with `%%`.

## Styling (optional)
- Use `classDef` plus `class` or `:::` to style states.
- Start/end states cannot receive `classDef` styling.

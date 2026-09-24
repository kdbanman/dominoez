---
name: review-doc
description: Build the review doc for a batch of motifs, a single published page showing every render at the SVG stage with approve-by-default review controls, notes, local persistence, and a copy-to-clipboard field that sends the page's state back into chat.
---

# Review doc

One page per batch. Highly visual, text minimal, lightly interactive. The reviewer sees every motif at once, marks the ones that need work, and pastes the result back into chat. Claude cannot see the page, so the page must be able to describe its own state as text.

## Inputs

- The batch's motif names, grouped by category, in registry order.
- `png/<name>.png` for each, rendered by `uv run dominoez render <names>`.
- For a redo, the previous render as well, so the old and new sit side by side.
- The GitHub issue number of each motif and each category.

## The page

- One section per category, headed by the category name and a link to its issue.
- A grid of cards, each card one motif: the render as an inline `data:` PNG at a size where the motif box reads (three to four cards across on a laptop, one at phone width), the motif name, the issue number as a link. No other text on the card. A redo card shows the old render faded beside the new one.
- Every card starts **approved**. Two buttons on the card: **redo** and **drop**. Clicking one selects it and shows a note field; clicking it again returns to approved. The card's border colour states its verdict.
- A sticky bar with the counts (approved, redo, drop) and a link to the send box.
- The send box at the bottom: one button, **Fill and copy**, that writes the state into a read-only textarea and copies it to the clipboard, with a status line saying it copied. A **Reset** button clears every verdict.
- Every verdict and note is written to `localStorage` on change, under a key that includes the batch name and the round number, and restored on load, so a republished round starts clean instead of showing the previous round's marks. Wrap every storage access in try/catch and let the page work without it.
- Comment threads on the artifact are a second feedback channel. When a thread is sent to Claude it wakes the session; read it with the Artifact tool's `comments` action and reply on the thread once acted on.

## The copied text

```
dominoez batch <name>: <a> approved, <r> redo, <d> drop of <n>

## <Category>
ok    otter
redo  penguin: flippers too short, and it leans left
drop  sloth
```

One line per motif, verdict first, note after a colon when there is one. Every motif is listed, including the approved ones, so nothing is lost if the reviewer skims.

## Building it

- Follow the `artifact-design` skill: real type pairing, tokens for light and dark, a chosen neutral ground. The page is a tool, so keep it quiet; the renders are the content.
- Inline the PNGs as base64 `data:` URIs. Fifty renders at about 15 KB each is well under the 16 MB page limit.
- Publish with the Artifact tool. Republish to the same path so the link stays fixed across redo rounds; the platform carries form state across a republish where it can, and `localStorage` covers the rest.
- Title the page after the batch, like "Batch One Review".

## After the paste

Parse each line by its leading verdict. Redraw every redo with its note as the brief, republish, and repeat. Close each drop's issue as not planned. When no redo remains, build the STLs and open the batch PR.

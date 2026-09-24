# Motifs are reviewed in batches through a review doc

Round two was seventeen motifs approved one PNG at a time in chat. It worked, but every render cost a turn of the reviewer's attention, redraws lost their before-and-after, and the flow could not scale to the two hundred motifs of round three. We now draw a batch of up to fifty at once, with up to three drawing agents in parallel, and review all of them on one published page: every motif approved by default, redo or drop marked with a note, the page copying its own state back into chat. Nothing is committed until the page has no redo left.

The alternative kept was the PR itself as the review surface, with the reviewer commenting on committed PNGs. Rejected because CI checks every committed output against the code, so draft churn would be a stream of red builds, and because a PR review reads one file at a time, which is the problem being solved.

## Consequences

- A batch's branch carries no commits until review is clear, so the branch is short-lived and there is nothing to revert when a motif is dropped.
- The review doc is an artifact outside the repo. What lives in the repo is the skill that builds it, so the page can be regenerated for any batch.
- Dropped motifs close their issue as not planned rather than lingering.

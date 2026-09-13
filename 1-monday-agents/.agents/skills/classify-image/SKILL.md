---
name: classify-image
description: Ask the CLIP model from Monday morning which of a list of labels best fits a photograph, by running scripts/clip_classify.py. Use when the user asks what an object in a photograph is, asks to sort or tag images against a set of categories, or wants a first guess at an artefact type from a picture. Also use to demonstrate that a skill can call a model.
---

# Classify a photograph with CLIP

This wraps the model from `1-monday-intro/clip_zero_shot.ipynb` — the same
weights, pinned to the same revision, so an answer here matches an answer
there. It runs on CPU and takes a few seconds.

## Running it

```bash
python scripts/clip_classify.py --image <path> --labels "label one,label two,label three"
```

Give it **at least three labels**. CLIP does not recognise objects; it scores
your labels against each other, so two labels make the result a coin toss
dressed as a measurement.

It prints a table for the human and one line of JSON with `scores`, `best` and
`margin`.

## Reading the answer — this is the part that matters

Three things are true of every answer it gives, and the user needs to hear
them alongside the number:

1. **The percentages are over the labels you supplied, and nothing else.**
   They add up to 100% whatever the photograph contains. A photograph of a
   bicycle scored against three artefact labels still returns a confident
   winner.
2. **There is no “none of the above”.** If you suspect the object may not be in
   the list, add a plain label such as `"something else entirely"` and see how
   much it takes.
3. **Rewording a label changes the answer.** `"a brooch"`, `"a bronze brooch"`
   and `"a photograph of a bronze brooch on a grey background"` are three
   different questions. If the wording matters to the conclusion, try two or
   three and report that it moved.

Always report the **margin** as well as the winner. A 4-point gap between first
and second is a guess; a 60-point gap is a result.

## Stop and ask

- The user gave **fewer than three labels** — ask for more, and say why.
- The user wants to **classify a whole folder** — say how many images and how
  long it will take before starting, and write the results to a CSV rather than
  into the conversation.
- The user treats the output as **ground truth** — say once, plainly, that it
  is a first guess against their own label list.

## Afterwards

If the user wants to see the results, use the **visualize** skill: a sorted bar
chart of the scores, with the margin called out and the label list printed on
the page.

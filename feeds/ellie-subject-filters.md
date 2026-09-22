# Ellie (7C) subject filters — Veckobrev / Vklass

**Authoritative rules** for every school homework refresh. Ellie (Eleanor Katherine, class **7C**) only studies **Spanish** as modern language. When parsing Veckobrev, Vklass news, or calendar items for Eleanor/Ellie, apply these filters **before** adding Spanish, Maths, or English material.

Anything that does **not** match the teacher/group tags below does **not** apply to Ellie — ignore it even if it looks like year 7 / åk 7 content.

## Spanish (Spanska)

| Field | Include only |
|-------|----------------|
| Teacher | **Sebastian** (ICS code **SEBTOR**) |
| Group | Often **M2SP71** / **7C** |

**Ignore:** French, German, and Spanish sections for other teachers or other groups.

Item fields to set when including: `teacher`: `"Sebastian"`, `group`: `"7C"` (or `"M2SP71"`). Prefer a short note that names Sebastian / the group when the source letter does.

## Maths (Matematik)

| Field | Include only |
|-------|----------------|
| Teacher | **Aleyna Bulduk** (ICS code **ALEBUL**) |
| Group | **7B–7D** |

**Ignore:** Maths labelled for other teachers, or other year-7 groupings that are not 7B–7D / Aleyna.

Item fields: `teacher`: `"Aleyna Bulduk"`, `group`: `"7B–7D"`. Notes should keep the 7B–7D attribution when present in the letter.

## English (Engelska)

| Field | Include only |
|-------|----------------|
| Teacher | **Emilia Isaksson** (ICS code **EMIISA**) |
| Group | **7C+7D** |

**Ignore:** English for other teachers or for 7A/7B-only groups.

Item fields: `teacher`: `"Emilia Isaksson"`, `group`: `"7C+7D"`. Prefer a short note naming Emilia / 7C+7D when missing.

## Refresh checklist

1. Identify subject (Spanish / Maths / English / other).
2. For Spanish, Maths, English: match **both** teacher (name or ICS code) **and** group as above.
3. If teacher/group is unclear and the item was already on Ellie’s list from a prior correct parse, **keep** it and tag with the correct `teacher` / `group`.
4. Remove an existing Ellie item only if notes clearly attribute it to a different teacher/group that fails these filters.
5. Do **not** invent new homework/tests. Do **not** change Ollie items.
6. Keep `data.json` and the embedded school data in `index.html` in sync (app embeds data for `file://`).

## Related

- School data: `../data.json` + embedded block in `../index.html`
- Feed overview: `README.md`

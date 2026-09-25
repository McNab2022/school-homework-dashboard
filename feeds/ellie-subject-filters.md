# Ellie (7C) subject filters — Veckobrev / Vklass

**Authoritative rules** for every school homework refresh. Ellie (Eleanor Katherine, class **7C**) only studies **Spanish** as modern language. When parsing Veckobrev, Vklass news, or calendar items for Eleanor/Ellie, apply these filters **before** adding Spanish, Maths, or English material.

Anything that does **not** match the teacher/group tags below does **not** apply to Ellie — ignore it even if it looks like year 7 / åk 7 content.

## Spanish (Spanska)

| Field | Include only |
|-------|----------------|
| Teacher | **Sebastian** (ICS code **SEBTOR**) |
| Group | Often **M2SP71** / **7C** |

**Ignore:** French, German, and Spanish sections for other teachers or other groups.

**Never include** Spanish homework or tests attributed to **Gabriella** (or any teacher other than Sebastian / SEBTOR). Chapter/glosor läxförhör under Gabriella must be **excluded** even if the same letter also mentions **7C** elsewhere — 7C alone is not enough; the Spanish teacher must be Sebastian.

Item fields to set when including: `teacher`: `"Sebastian"`, `group`: `"7C"` (or `"M2SP71"`). Prefer a short note that names Sebastian / the group when the source letter does.

## Spanish example (v.39)

Veckobrev sections look like:

```
Spanska
Sebastian:
Nästa vecka kommer vi att jobba vidare med berätta om en själv. Vi kommer också jobba med genitiv (ägande).
Prov:14/10, skriftlig framställning. Mer info i v klass och classroom.
sebastian.torres-villagran@huddinge.se
```

Only include blocks under **Sebastian:** — never Gabriella (or other Spanish teachers).

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

## Test revision items (standing rule)

For every known Ellie test, add a **Test revision** homework item referencing the test, date, topics and Veckobrev resources, dated from the start of the week before or of the test week.

- `type`: `"homework"` (shows under the Homework filter), `id` prefixed `el-rev-`, `related_tests`: list of the test item id(s).
- Title e.g. `Test revision: Maths (Tal, parts 1 & 2)` / `title_sv` `Repetition inför prov: Matematik (Tal, del 1 & 2)`.
- `date`: the Monday of the week before the test, or the Monday of the test week (e.g. 2026-09-28 for week-40/41 tests).
- `notes` + `notes_sv`: test date(s), what it covers, and the resources named in the Veckobrev (book, Magma, Classroom, Vklass…). Set `on_classroom: true` when Classroom material is mentioned.
- Only use topics from the letter or the existing test item — do not invent topics. If the test date is unconfirmed, say so (e.g. `Test revision: NO (date TBC)`).
- When a test moves or is removed, update or remove its revision item too.

## Refresh checklist

1. Identify subject (Spanish / Maths / English / other).
2. For Spanish, Maths, English: match **both** teacher (name or ICS code) **and** group as above.
3. If teacher/group is unclear and the item was already on Ellie’s list from a prior correct parse, **keep** it and tag with the correct `teacher` / `group`.
4. Remove an existing Ellie item only if notes clearly attribute it to a different teacher/group that fails these filters.
5. Do **not** invent new homework/tests (Test revision items for known tests are required, see above). Do **not** change Ollie items.
6. Make sure every Ellie test has a matching `el-rev-` Test revision homework item.
7. Keep `data.json` and the embedded school data in `index.html` in sync (app embeds data for `file://`).

## Related

- School data: `../data.json` + embedded block in `../index.html`
- Feed overview: `README.md`

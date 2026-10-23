Task: list every checkable fact on these slides of a startup's pitch deck. The script found no figure on them it could parse, so read them for facts a document in the data room could confirm or contradict: a named customer, a date, a count written out in words, a claim about what the product does for a named customer.

For every fact:
1. Set "slide" to the slide number in the document's locator.
2. Set "quote" to the exact span you relied on, copied character for character from the slide. Use the smallest span that states the fact.
3. Set "kind" to one of: customer_date, customer_locations, founder_years, founded, headcount_now, hires_planned, other.
4. Set "number" to the number the quote states, as a plain number ("eleven years" is 11), or null when it states none.

Do not add a fact the slide does not state. Do not judge whether a fact is true. If a slide holds no checkable fact, return nothing for it.

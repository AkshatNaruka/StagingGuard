# Public schema guidance

The user-supplied `schema` skill was reviewed. This workspace currently contains
tools and Markdown documentation, with no public event or product webpage, so
no JSON-LD is injected or claimed to be rich-result validated.

If a public page is added, choose markup that represents its visible content:

| Page | Candidate type | Required accuracy checks |
| --- | --- | --- |
| Your actual app page | `SoftwareApplication` | Actual name, category, operating system; truthful visible offer if present |
| Your project write-up | `Article` or `BlogPosting` | Real author, headline, image, publication date, canonical URL |
| An event information page you maintain | `Event` | Confirmed date/time, attendance mode, venue, organizer and page content |

An event-page candidate needs the organizer's conflicting schedule/online/team
metadata resolved first; see EVENT.md. The project must not imply that you host
the official AgntID event or fabricate pricing, ratings, reviews, availability,
offers, affiliation, or details not present on the page.

Use JSON-LD, escape serialization safely, and validate the rendered page in
[Schema.org Validator](https://validator.schema.org/) and, for currently
supported Google result types, [Rich Results Test](https://search.google.com/test/rich-results).
Check Google's current eligibility documentation at implementation time.

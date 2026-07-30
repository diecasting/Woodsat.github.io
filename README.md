# Industrial Manufacturer Hugo Template (v2.1)

A reusable, production-ready [Hugo](https://gohugo.io/) static-site template for
**precision-manufacturing / industrial B2B companies** (casting, CNC machining,
fabrication, contract manufacturing, etc.).

It ships with a premium, high-conversion industrial UI, a **data-driven GEO/Schema
engine** (Organization, Service, Product, Article, FAQ, Breadcrumb, Manufacturing,
Geo entity), a landing-page **section engine**, multilingual support
(EN/DE/JA/FR/ES), and a robust **Request-a-Quote (RFQ)** workflow.

> **This is a template, not a finished site.** All brand-specific content has been
> removed and replaced with configurable placeholders. Brand your site by editing
> `config/_default/params.toml` and the example pages under `content/`.

---

## Features

- **Premium industrial B2B UI** — sticky 1200px header, hero sections, alternating
  content bands, styled specification/comparison tables, FAQ accordion, dark CTA
  band, fully responsive.
- **Section engine** — landing pages are composed from a `sections:` array in
  front matter (no layout editing required).
- **Data-driven schema engine** — 5 JSON-LD schema types generated from
  `data/schema/*.toml`, localized per language.
- **Multilingual** — EN at root, `/de/ /ja/ /fr/ /es/` prefixes. Add or remove
  languages in `config/_default/languages.toml`.
- **RFQ, with graceful fallback** — a single `params.contact.form_action` setting
  controls the quote form. If it is **empty, the form is replaced by an email CTA**
  instead of a broken submission. See [RFQ form](#rfq-form--graceful-fallback).
- **SEO checks** — `scripts/seo-check.py` and `scripts/schema-check.py` validate
  every built page (run in CI before deploy).
- **GitHub Pages ready** — `.github/workflows/hugo.yml` builds, validates and
  deploys on push to `main`.

---

## Requirements

- **Hugo 0.163.3 (extended)** — the build uses extended features (SCSS pipeline
  via `resources`). `enableGitInfo = true` requires the site to be a **git repo**
  (`git init` if you start fresh).
- Python 3.12+ (only for the optional local SEO/schema checks).

---

## Quick start

```bash
# 1. Clone / copy this template into your project
git clone <your-repo> my-site
cd my-site

# 2. Initialise git (required for enableGitInfo)
git init -q && git add -A && git commit -m "init"

# 3. Build (or run `hugo server -D` to preview)
hugo --gc --minify

# 4. (optional) run the quality gates locally
python scripts/seo-check.py ./public
python scripts/schema-check.py ./public
```

Preview with `hugo server` and open `http://localhost:1313/`.

---

## Branding your site

**All branding lives in `config/_default/params.toml`.** You do **not** need to
touch any layout or partial.

| Key | Purpose |
| --- | --- |
| `companyName` | Site title + header/footer wordmark |
| `companyTagline` | Shown under the wordmark (and as logo subtitle fallback) |
| `branding.logo` | Logo image URL. **Empty = text wordmark** (first 2 letters of `companyName`). |
| `branding.logo_mark` | 1–3 letter monogram. Empty = first 2 letters of `companyName`. |
| `branding.logo_subtitle` | Small text under wordmark. Empty = `companyTagline`. |
| `description` | **Site-wide default meta description** (multilingual fallback). |
| `keywords` | Default meta keywords. |
| `Author.name` / `Author.email` | Author meta + schema contact. |
| `contact.email` | Used by RFQ email fallback, footer, schema. |
| `contact.phone` / `contact.address` | Footer + schema. |
| `contact.form_action` | RFQ form endpoint — see below. |
| `social.*` | Organization schema `sameAs`. |
| `features.*` | Enable/disable search, blog, RFQ, multilingual. |
| `homepage.*` | Toggle homepage sections. |
| `footer.copyright` | Footer copyright line. |
| `cta.*` | Conversion band title/subtitle before the footer. |

```toml
companyName = "Acme Precision Castings"
description  = "Acme Precision Castings provides investment casting and CNC machining for pump, valve and mobility customers worldwide."
[contact]
  email = "sales@acme.example"
  form_action = "https://formspree.io/f/your-form-id"   # or leave "" for email fallback
```

> **Note on `description` / `keywords`:** these keys MUST stay at the **top level**
> of `params.toml`, **above** any `[table]` header. Placing them after a table
> (e.g. `[branding]`) causes TOML to nest them (`branding.description`), which
> breaks the site-wide meta-description fallback on taxonomy and non-English pages.

Also set the real domain in `config/_default/hugo.toml` → `baseURL`.

### Menus

Menus are **fully editable** through language-specific files
(`config/_default/menus.en.toml`, `menus.de.toml`, …). The default set is:
**Home, Services, Materials, Industries, Processes, Resources, Contact.** No menus
are hardcoded in layouts. To add/remove items, edit these TOML files only.

---

## RFQ form — graceful fallback

The RFQ form (`layouts/partials/sections/rfq.html` and the `rfq_form` shortcode)
reads a **single** setting: `params.contact.form_action`.

- **If `form_action` is set** (e.g. a Formspree/HubSpot URL), a working form is
  rendered that POSTs to that endpoint.
- **If `form_action` is empty**, the template does **not** render a broken form.
  Instead it shows an **email CTA** (mailto to `contact.email`) so visitors can
  still request a quote. This prevents dead/broken submissions on a fresh clone.

> **Requirement:** never ship a default third-party form ID. The template ships
> with `form_action = ""` and the email fallback. Set your own endpoint in
> `params.toml`.

---

## Content structure

Example pages are provided so the site builds out-of-the-box. Replace them with
your own; the folder structure maps to the navigation:

```
content/
  _index.md                      # Homepage (layout: landing, section engine)
  services/example-service/      # Service page (layout: single)
  materials/example-material/    # Material page
  industries/example-industry/   # Industry page
  processes/example-process/     # Process page
  resources/example-resource/    # Resource / guide (uses capability_table)
  contact/                       # Contact page (RFQ)
  services/_index.md             # Section listing
  materials/_index.md
  industries/_index.md
  processes/_index.md
  resources/_index.md
```

### Creating a new service (or material/industry/process) page

1. Copy `content/services/example-service/index.md` to
   `content/services/my-part/index.md`.
2. Update front matter: `title`, `description`, `slug` (optional), and the
   `schema:` block.
3. Replace the body copy, image shortcodes, `process_flow`,
   `capability_table` and `rfq_form` / `faq_accordion` shortcodes.
4. Rebuild. The new page appears automatically in the section listing and menu.

> **Shortcodes:** `{{< image src title >}}`, `{{< process_flow steps >}}`,
> `{{< capability_table ... >}}…{{< /capability_table >}}` (must be closed),
> `{{< faq_accordion >}}`, `{{< rfq_form >}}`.

---

## Multilingual

- Languages are defined in `config/_default/languages.toml` (EN is the default
  content language at the site root).
- Each language has its own menu file (`menus.<lang>.toml`) and its own content
  tree (`content/<lang>/…`) created via `hugo new` / translation folders.
- `translationKey` links equivalent pages across languages (omit it on example
  pages; add it when you create real translated pairs).
- Schema strings are localized in `data/schema/*.toml` under `[en.<id>]`,
  `[de.<id>]`, `[ja.<id>]`, `[fr.<id>]`, `[es.<id>]` maps.

To **add a language**: add a block to `languages.toml`, create
`menus.<lang>.toml`, and add a `<lang>.<id>` map to every relevant
`data/schema/*.toml`.

---

## Schema engine

JSON-LD is generated from `data/schema/*.toml` and injected by
`layouts/partials/schema/render.html`. All brand fields fall back to
`params.toml` (so the generic template still produces valid Organization schema).

| File | Schema type |
| --- | --- |
| `organization.toml` | Organization (site-wide, in every page head) |
| `services.toml` | Service (matched by `url_path`) |
| `products.toml` | Product |
| `industries.toml` | (industry context) |
| `manufacturing.toml` | ManufacturingBusiness (knowsAbout / makesOffer) |
| `locations.toml` | GeoCoordinates / PostalAddress |
| `certifications.toml` | certifications (ISO 9001 / IATF 16949) |

Match a page to a schema entry by setting `url_path` in the schema file equal to
the page’s `.Dir` (e.g. `/services/example-service/`).

---

## SEO & schema validation

```bash
python scripts/seo-check.py ./public     # every page needs a meta description
python scripts/schema-check.py ./public   # JSON-LD well-formed & linked
```

Both scripts run automatically in the GitHub Actions deploy and will **fail the
build** if any page is missing a meta description or a schema block is malformed.

---

## Deployment (GitHub Pages)

1. Push the template to a GitHub repo (e.g. `industrial-manufacturer-hugo-template-2.1`).
2. In **Settings → Pages → Build and deployment**, set Source = **GitHub Actions**.
3. Push to `main`. `.github/workflows/hugo.yml` will build, run the SEO/schema
   checks, and deploy to GitHub Pages.

The workflow uses Hugo `0.163.3` (extended) and uploads `./public` as the Pages
artifact. To deploy elsewhere (Netlify, Cloudflare Pages, S3), just run
`hugo --gc --minify` and serve the `public/` folder.

---

## Project structure

```
config/_default/      # hugo.toml, languages.toml, params.toml, menus.*.toml
content/              # example pages (replace with your content)
data/schema/          # schema engine data (localized)
layouts/
  _default/           # baseof, landing, single, list, markup render hooks
  partials/           # head, header, footer, cta-band, sections/*, schema/*
  shortcodes/         # image, rfq_form, faq_accordion, process_flow, capability_table
assets/css/main.css   # design system
static/               # favicon, robots.txt, etc.
scripts/              # seo-check.py, schema-check.py
.github/workflows/    # hugo.yml (build + deploy)
```

---

## License

See `LICENSE`.

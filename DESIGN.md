# Design language

Clean, flat, quiet. One accent. Lines, not shadows. Few words.

`python3 build.py` checks the rules marked **checked**. A page that breaks one does not build.

## Rules

| Rule | Checked |
|---|---|
| Colours come from `--color-*` tokens. No raw hex or rgb in `styles.css`. | Yes |
| Type sizes, weights, and radii come from tokens. | Yes |
| Pages use only classes defined in `styles.css`. No inline styles. | Yes |
| No unused classes in `styles.css`. | Yes |
| One `h1` per page, 60 characters or fewer. | Yes |
| No paragraph, list item, or definition over 28 words. | Yes |
| Title 65 characters or fewer. Description 160 or fewer. | Yes |
| No shadows, gradients, or glows. The one exception: the stage hero fades its backdrop with a mask. | No |
| One primary button per view. | No |
| Sell the benefit. Leave the mechanism to Resources. | No |

## Tokens (`assets/tokens.css`)

| Tier | Example | Use |
|---|---|---|
| Primitive | `--gray-800` | Raw values. Only tokens.css uses them. |
| Semantic | `--color-border` | What styles.css uses. Change these to retheme. |
| Scale | `--space-5`, `--text-l`, `--radius-m` | Spacing, type, radius, weight. |

Themes: dark is the default. `data-theme="light"` on `<html>` switches. Add a theme by adding one `[data-theme]` block.

Scales: 6 type sizes, 3 weights, 9 spaces, 3 radii. Do not add a step without removing one.

## Components (`assets/styles.css`)

| Component | Use it for |
|---|---|
| `nav`, `menu` | Top bar and its menus. Defined once, in `build.py`. |
| `hero` | The top of every page. `--center` on home, `--end` when a control sits beside it. |
| `chapter` | One idea on one screen. Home page only. |
| `section`, `section__head` | Every block below the hero. |
| `grid`, `cell` | The one card. Cells share dividers. `--2`, `--3`, `--4` columns. |
| `cell--tall`, `cell__icon` | A cell with an icon above the words. |
| `cell--link` | A whole cell that is a link. |
| `cell--span` | A cell two columns wide and two rows tall. |
| `plan`, `price` | A cell on the pricing grid. |
| `segmented` | Choose one of two. Billing. |
| `split` | Words beside a product panel. |
| `mock`, `stats`, `entry` | The product, drawn in HTML. |
| `list` | Checked list. `--no` for what is excluded. |
| `tag` | A status word. `--good`, `--late`. |
| `button` | `--quiet`, `--small`, `--block`. |
| `form`, `field` | The Enterprise form. |
| `cta` | The band that closes a page. One partial: `src/partials/cta.html`. |
| `lede`, `note`, `eyebrow`, `link` | Text roles. |

Need something new? Reuse a component first. If nothing fits, add one component here and in `styles.css`, not a one-off.

## Words

- Headline: what the reader gets.
- One short line under it. Often none.
- Cells: a title and one sentence.
- No story-telling. No "we believe". No feature tours.
- Name the link's destination. Never "learn more".
- Same word for the same thing: Sign in, Sign up, Request a demo.

## Navigation

| Menu | Holds |
|---|---|
| Platform | What it is: Objectives, Knowledge, the three views, Actions, Integrations. |
| Solutions | Who it is for, and which need. |
| Resources | Help, learning, trust. Privacy lives here and in the footer. |
| Enterprise, Pricing | Direct links. |

## Motion

Scroll-driven, CSS only, home page only. Off under `prefers-reduced-motion`, and in browsers without `animation-timeline`.

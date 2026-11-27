# coremode.ai

The marketing site for coremode, served at **coremode.ai** by GitHub Pages.

Plain HTML and CSS. No JavaScript. No third parties: no analytics, hosted fonts, or trackers.

| To | Do |
|---|---|
| Edit a page | Change `src/pages/<name>.html`, then run `python3 build.py` |
| Edit the menus | Change `NAV` in `build.py` |
| Edit colours or sizes | Change `assets/tokens.css` |
| Add a component | See `DESIGN.md` |
| Preview | `./preview.sh`, then open http://localhost:8000/ |

The `.html` files at the root are built. Do not edit them; commit them with the source.

`build.py` needs Python 3 and nothing else. It fails if a page breaks the design rules in `DESIGN.md`.

The product lives in the private `coremodeai/coremode` repository.

## Deploy (GitHub Pages)

1. Push to `main` on `coremodeai/coremodeai.github.io`.
2. Repository settings, Pages: source `main` branch, `/ (root)`.
3. Custom domain `coremode.ai` (the `CNAME` file declares it). Enforce HTTPS.
4. DNS at the registrar:
   - `coremode.ai` A records: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - `www` CNAME: `coremodeai.github.io`

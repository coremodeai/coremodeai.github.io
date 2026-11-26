# coremode.ai

The marketing site for coremode, served at **coremode.ai** by GitHub Pages.

Plain HTML and CSS. No build step, no JavaScript, and no requests to any
third party: no analytics, hosted fonts, or trackers. The one web font, Mr
Dafoe (SIL Open Font License, in `assets/fonts`), is served from this site.

- Preview locally: `./preview.sh` then open http://localhost:8000/
- The product itself lives in the private `coremodeai/coremode` repository.

## Deploy (GitHub Pages)

1. Push this folder to the public repository `coremodeai/coremodeai.github.io`.
2. Repository settings, Pages: source `main` branch, `/ (root)`.
3. Custom domain `coremode.ai` (the `CNAME` file already declares it), then
   enforce HTTPS once the certificate is issued.
4. DNS at the registrar:
   - `coremode.ai` A records: 185.199.108.153, 185.199.109.153,
     185.199.110.153, 185.199.111.153
   - `www` CNAME: `coremodeai.github.io`

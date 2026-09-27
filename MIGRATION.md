# al-folio v1.2 migration

Prepared 2026-09-27 from personal-site commit `fe53f07` (v0.12.1 base), using
upstream al-folio v1.2 and `al_folio_core` 1.0.15.

The migration was prepared and validated in an isolated worktree on branch
`test/al-folio-v1.2` before integration into `main`. The local preview was stopped
after review; the commands below can restart it from this repository.

## Start or stop the preview

From this directory, with Docker Desktop running:

```sh
docker compose -p al-folio-v12 -f docker-compose.local.yml up -d
docker compose -p al-folio-v12 -f docker-compose.local.yml logs --tail 30
# Stop when finished:
docker compose -p al-folio-v12 -f docker-compose.local.yml down
```

Open <http://127.0.0.1:4000/>. The port is bound only to localhost. The image is
pinned by digest; it contains the tested Ruby 4.0.6/Bundler 4.0.6 and locked gems.
The local compose file overrides the image's default startup script so it does
not reset the lockfile in this worktree. Generated output stays in the container.

## Changes and retained customizations

- Replaced copied v0 layouts, includes, Sass, plugins, JavaScript, CSS and fonts
  with the v1 gem-owned runtime and Tailwind wiring.
- Kept all bibliography, blog post, news, image and PDF files byte-for-byte.
  The about-page prose is unchanged; only its news/latest-post flags use v1 keys.
- Kept original public routes, archive permalinks, navigation, profile, social
  links and personal configuration. Disabled the upstream books archive because
  this site has no books collection. Did not import upstream demo content.
- Rebased `_layouts/bib.liquid` on the current gem: show authors through Chaoyi
  Ruan, retain Project links, and retain author annotations as native tooltips.
- Rebased `assets/css/main.scss` on the current gem: warm light background, blue
  links, 220px proportional portrait, custom blog heading sizing, and no empty
  contact-note gap. Dark styling comes from the new theme.
- Recorded both intentional overrides in `.al-folio-overrides.yml`.
- Updated Docker/build dependency files and the deployment workflow for v1.2.
  The remote deployment workflow has not been exercised or deployed in this trial.
- Adapted the upstream style-contract check to allow the intentional bibliography
  layout. The override audit independently checks its reviewed gem checksum.

## Validation

Passed:

```sh
npm ci
npm run lint:style-contract
npm run lint:prettier
docker exec al-folio-v12-preview bundle exec al-folio upgrade audit --no-fail
docker exec al-folio-v12-preview bundle exec al-folio upgrade overrides audit
docker exec -e JEKYLL_ENV=production al-folio-v12-preview bundle exec jekyll build --destination /tmp/production-site --disable-disk-cache
docker exec al-folio-v12-preview python3 test/site_smoke.py /tmp/production-site
```

The upgrade audit reports zero blocking and zero non-blocking findings. Both
local overrides are acknowledged. Production output validates eight routes,
local HTML links and assets, 13 selected and 19 total publications, author
visibility, selected-publication order (Hold On Loosely, ATP, Holon), absence of
Accepted labels, and an exact resume PDF copy.

These upstream integration checks also passed inside the same container:

```sh
for check in test/integration_plugin_toggles.sh test/integration_bootstrap_compat.sh test/integration_upgrade_cli.sh test/integration_css_minify.sh; do
  docker exec al-folio-v12-preview bash "$check" || break
done
```

Browser checks passed at desktop size and 390px mobile width: home and portrait
sizing, publication filtering, expanding authors, global search and navigation
to the AuroraRL post, blog listing, mobile menu, dark/light theme switching, and
no horizontal overflow on the mobile homepage. No console errors were observed.
The browser viewport and theme were restored to their initial settings.

No material visual regression was observed on those pages. v1's standard theme
styling remains in effect where this site has no override (for example, publication
button labels use the new theme's capitalization).

### Test scope and notes

The upstream comments test was tried but requires a removed demo post at
`/blog/2022/giscus-comments/`; it is not applicable to this personal site.
The Distill and new-plugin demo tests, and upstream demo screenshot baselines,
were likewise not used as personal-site acceptance checks. Hidden CV, projects
and repositories pages remain excluded as before.

Notebook conversion emits a non-fatal warning that the IPython3 lexer is absent;
nbconvert falls back to Python 3. This does not affect the personal pages.
The GitHub Actions CSS-purge/deployment stage and external links were not tested.

Local logs: `/private/tmp/al-folio-v12-build.log` and
`/private/tmp/al-folio-v12-integration.log`.

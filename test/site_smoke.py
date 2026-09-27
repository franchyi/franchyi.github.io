"""Validate the migrated personal site after `jekyll build`. Requires bs4 (nbconvert dependency)."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys
from bs4 import BeautifulSoup

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
pages = ["index.html", "publications/index.html", "blog/index.html",
         "blog/2026/aurora-rl/index.html", "blog/2026/index.html",
         "blog/tag/ml-systems/index.html", "blog/category/project/index.html", "404.html"]
missing = set()
for page in pages:
    path = root / page
    assert path.exists(), page
    soup = BeautifulSoup(path.read_text(), "html.parser")
    for node in soup.select("[src], [href], object[data]"):
        value = node.get("src") or node.get("href") or node.get("data")
        url = urlsplit(value)
        if url.scheme or url.netloc or not url.path:
            continue
        target = root / unquote(url.path).lstrip("/") if url.path.startswith("/") else path.parent / unquote(url.path)
        if not target.is_file() and not (target / "index.html").is_file():
            missing.add((page, value))
assert not missing, sorted(missing)
home = BeautifulSoup((root / "index.html").read_text(), "html.parser")
pubs = BeautifulSoup((root / "publications/index.html").read_text(), "html.parser")
assert [n.get("id") for n in home.select(".bibliography div[id]")][:3] == ["ruan2027holdon", "chen2026atp", "song2027holon"]
assert len(home.select(".bibliography .title")) == 13
assert len(pubs.select(".bibliography .title")) == 19
for page in (home, pubs):
    assert "Accepted" not in page.get_text()
    for author in page.select(".bibliography .author"):
        assert "Chaoyi Ruan" in " ".join(author.get_text().split()), author.get_text()
assert (root / "assets/pdf/cv.pdf").read_bytes() == Path("assets/pdf/cv.pdf").read_bytes()
print("PASS: 8 routes; local HTML links/assets; 13 selected / 19 total publications; author visibility; order; no Accepted labels; resume bytes.")

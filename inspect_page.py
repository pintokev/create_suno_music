"""Dump des éléments interactifs de la page Suno ouverte (pour trouver les sélecteurs)."""
from playwright.sync_api import sync_playwright

JS = """
() => [...document.querySelectorAll('textarea, input, button, [role=slider], [role=switch], [role=tab], [contenteditable=true], [role=combobox], [role=checkbox]')]
  .filter(e => e.offsetParent !== null)
  .map(e => ({
    tag: e.tagName.toLowerCase(),
    type: e.getAttribute('type'),
    role: e.getAttribute('role'),
    aria: e.getAttribute('aria-label'),
    ph: e.getAttribute('placeholder'),
    testid: e.getAttribute('data-testid'),
    name: e.getAttribute('name'),
    pressed: e.getAttribute('aria-pressed') || e.getAttribute('aria-checked') || e.getAttribute('aria-selected') || e.getAttribute('data-state'),
    val: e.getAttribute('aria-valuenow') || (e.value !== undefined ? String(e.value).slice(0, 40) : null),
    text: (e.innerText || '').trim().replace(/\\s+/g, ' ').slice(0, 60),
  }))
"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        page = next(pg for ctx in browser.contexts for pg in ctx.pages if "suno.com" in pg.url)
        print("URL:", page.url)
        for el in page.evaluate(JS):
            print({k: v for k, v in el.items() if v})
        page.screenshot(path="screenshot.png", full_page=False)
        print("screenshot -> screenshot.png")


if __name__ == "__main__":
    main()

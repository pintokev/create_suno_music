"""Remplit le formulaire Suno (mode Advanced) à partir d'un fichier JSON.

Usage : .venv/bin/python fill.py songs/ma_chanson.json

Ne clique JAMAIS sur Create : c'est toi qui valides.
Toutes les clés sont optionnelles (une clé absente = champ laissé tel quel) :
{
  "model": "v6" | "v6-wild" | "v6-mini",
  "title": "...",
  "lyrics": "...",            # "" = instrumental
  "styles": "...",
  "exclude": "...",
  "vocal_gender": "male" | "female" | null,
  "max_mode": true | false,
  "weirdness": 0-100,
  "style_influence": 0-100,
  "variety": 0-4,
  "my_taste": true | false
}
"""
import json
import sys

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"

PASTE_JS = """(el, text) => {
  el.focus();
  const dt = new DataTransfer();
  dt.setData('text/plain', text);
  el.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
}"""


def get_page(browser):
    for ctx in browser.contexts:
        for pg in ctx.pages:
            if "suno.com" in pg.url:
                return pg
    raise SystemExit("Aucun onglet suno.com trouvé — lance d'abord launch.py")


def row(page, label):
    """Conteneur le plus proche (contenant des boutons) du libellé `label`."""
    return page.locator(
        f"xpath=//*[normalize-space(text())='{label}']/ancestor::*[.//button[@data-selected]][1]"
    ).locator("visible=true").first


def is_selected(btn):
    return btn.get_attribute("data-selected") == "true"


def choose(page, label, option):
    btn = row(page, label).get_by_role("button", name=option, exact=True).first
    if not is_selected(btn):
        btn.click()


def set_slider(page, label, value):
    s = page.locator(f'[role=slider][aria-label="{label}"]:visible').first
    s.focus()
    for _ in range(3):
        cur = float(s.get_attribute("aria-valuenow"))
        if cur == value:
            return
        key = "ArrowRight" if value > cur else "ArrowLeft"
        steps = abs(value - cur)
        # on mesure la taille d'un pas sur le premier appui
        page.keyboard.press(key)
        step = abs(float(s.get_attribute("aria-valuenow")) - cur) or 1
        for _ in range(int(round(steps / step)) - 1):
            page.keyboard.press(key)
    print(f"  ! {label} = {s.get_attribute('aria-valuenow')} (voulu {value})")


def set_model(page, model):
    trigger = page.locator("button:visible").filter(has_text="v6").first
    if trigger.inner_text().strip() == model:
        return
    trigger.click()
    page.wait_for_timeout(400)
    page.evaluate(
        """(name) => {
          const els = [...document.querySelectorAll('body *')].filter(e => e.offsetParent &&
            [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim() === name) &&
            !e.closest('button[aria-haspopup], button[aria-expanded]'));
          const target = els.find(e => e.closest('[role=menuitem],[role=option],[role=menuitemradio]')) || els[els.length - 1];
          (target.closest('[role=menuitem],[role=option],[role=menuitemradio],button') || target).click();
        }""",
        model,
    )
    page.wait_for_timeout(400)


def set_lyrics(page, text):
    ed = page.get_by_role("textbox", name="Lyrics editor").first
    ed.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    if text:
        ed.evaluate(PASTE_JS, text)
        page.wait_for_timeout(300)
        got = ed.inner_text().strip()
        if len(got) < len(text.strip()) * 0.9:  # le paste n'a pas pris → frappe ligne par ligne
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            for i, line in enumerate(text.split("\n")):
                if i:
                    page.keyboard.press("Shift+Enter")
                page.keyboard.insert_text(line)


def styles_box(page):
    # Le champ Styles est le seul textarea sans aria-label limité à 1000 caractères
    # (≠ « Cowriter prompt » du Lyricist, ≠ prompt de l'onglet Sounds).
    boxes = page.locator(
        'textarea[maxlength="1000"]:not([aria-label])'
        ':not([placeholder="Describe the sound you want"]):visible'
    )
    if boxes.count() != 1:
        raise SystemExit(f"Champ Styles introuvable ou ambigu ({boxes.count()} candidats)")
    return boxes.first


def fill(page, spec):
    page.get_by_role("tab", name="Songs").click()
    page.get_by_role("tab", name="Advanced").click()
    page.wait_for_timeout(500)

    if "model" in spec:
        set_model(page, spec["model"])
    if "title" in spec:
        page.locator('input[placeholder="Song Title (Optional)"]:visible').first.fill(spec["title"])
    if "lyrics" in spec:
        set_lyrics(page, spec["lyrics"])
    if "styles" in spec:
        box = styles_box(page)
        box.fill(spec["styles"])
        if box.input_value() != spec["styles"]:
            raise SystemExit("Le champ Styles n'a pas pris la valeur demandée")

    opts = {"exclude", "vocal_gender", "max_mode", "weirdness", "style_influence", "variety", "my_taste"}
    if opts & spec.keys():
        if not page.get_by_text("Vocal Gender", exact=True).locator("visible=true").count():
            page.get_by_text("More Options", exact=True).locator("visible=true").first.click()
            page.wait_for_timeout(400)
    if "exclude" in spec:
        page.locator('input[placeholder="Exclude styles"]:visible').first.fill(spec["exclude"])
    if "vocal_gender" in spec:
        g = spec["vocal_gender"]
        for opt in ("Male", "Female"):
            btn = row(page, "Vocal Gender").get_by_role("button", name=opt, exact=True).first
            want = g is not None and g.lower() == opt.lower()
            if is_selected(btn) != want:
                btn.click()
    if "max_mode" in spec:
        choose(page, "Max Mode", "On" if spec["max_mode"] else "Off")
    if "my_taste" in spec:
        choose(page, "Personalize", "On" if spec["my_taste"] else "Off")
    if "weirdness" in spec:
        set_slider(page, "Weirdness", spec["weirdness"])
    if "style_influence" in spec:
        set_slider(page, "Style Influence", spec["style_influence"])
    if "variety" in spec:
        set_slider(page, "Variety", spec["variety"])


def report(page):
    return page.evaluate("""() => {
      const v = s => document.querySelector(s);
      const sl = l => [...document.querySelectorAll(`[role=slider][aria-label="${l}"]`)].find(e => e.offsetParent)?.getAttribute('aria-valuenow');
      const sel = l => { const x = [...document.querySelectorAll('*')].find(e => e.offsetParent && e.childNodes.length===1 && e.textContent.trim()===l);
        if (!x) return null; let c = x; while (c && !c.querySelector('button[data-selected]')) c = c.parentElement;
        return [...c.querySelectorAll('button[data-selected=true]')].map(b => b.innerText.trim()); };
      return {
        title: [...document.querySelectorAll('input[placeholder="Song Title (Optional)"]')].find(e=>e.offsetParent)?.value,
        lyrics_chars: document.querySelector('[aria-label="Lyrics editor"]')?.innerText.trim().length,
        exclude: [...document.querySelectorAll('input[placeholder="Exclude styles"]')].find(e=>e.offsetParent)?.value,
        vocal_gender: sel('Vocal Gender'), max_mode: sel('Max Mode'), my_taste: sel("Personalize"),
        weirdness: sl('Weirdness'), style_influence: sl('Style Influence'), variety: sl('Variety'),
      };
    }""") | {"styles": styles_box(page).input_value()}


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = get_page(browser)
        page.bring_to_front()
        fill(page, spec)
        for k, v in report(page).items():
            print(f"  {k}: {v}")
        page.screenshot(path="screenshot.png")
        print("Formulaire rempli — vérifie et clique sur Create.")


if __name__ == "__main__":
    main()

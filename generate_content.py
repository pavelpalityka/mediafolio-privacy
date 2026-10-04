#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate privacy JSON for locales without a hand-written translation."""
from __future__ import annotations

import html
import json
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
EN_PATH = CONTENT / "en.json"

HAND_MAINTAINED = {"en", "ru", "uk", "zh_CN"}

FALLBACK_NOTICE = {
    "by": "Поўны тэкст паказаны на англійскай мове. Актуальная версія — англійская.",
    "de": "Der vollständige Text wird auf Englisch angezeigt. Die maßgebliche Version ist Englisch.",
    "fr": "Le texte intégral est affiché en anglais. La version faisant foi est la version anglaise.",
    "es": "El texto completo se muestra en inglés. La versión vinculante es la versión en inglés.",
    "it": "Il testo completo è mostrato in inglese. La versione fa fede è quella in inglese.",
    "pt": "O texto completo é apresentado em inglês. A versão vinculativa é a versão em inglês.",
    "nl": "De volledige tekst wordt in het Engels weergegeven. De bindende versie is Engels.",
    "pl": "Pełny tekst jest wyświetlany po angielsku. Wiążąca wersja to wersja angielska.",
    "cs": "Úplný text je zobrazen v angličtině. Závazná je anglická verze.",
    "sk": "Úplný text je zobrazený v angličtine. Záväzná je anglická verzia.",
    "hu": "A teljes szöveg angolul jelenik meg. A mérvadó verzió az angol.",
    "ro": "Textul complet este afișat în engleză. Versiunea obligatorie este cea în engleză.",
    "bg": "Пълният текст е на английски. Обвързващата версия е на английски.",
    "el": "Το πλήρες κείμενο εμφανίζεται στα αγγλικά. Η δεσμευτική έκδοση είναι η αγγλική.",
    "tr": "Tam metin İngilizce gösterilir. Bağlayıcı sürüm İngilizce sürümdür.",
    "sv": "Fullständig text visas på engelska. Den bindande versionen är engelska.",
    "da": "Den fulde tekst vises på engelsk. Den bindende version er den engelske.",
    "nb": "Full tekst vises på engelsk. Den bindende versjonen er engelsk.",
    "fi": "Koko teksti näytetään englanniksi. Sitova versio on englanninkielinen.",
    "et": "Täistekst kuvatakse inglise keeles. Siduv versioon on inglise keeles.",
    "lv": "Pilns teksts tiek rādīts angļu valodā. Saistošā versija ir angļu valodā.",
    "lt": "Visas tekstas rodomas angliškai. Privaloma versija – angliška.",
    "hr": "Cijeli tekst prikazan je na engleskom. Obvezujuća verzija je engleska.",
    "sl": "Celotno besedilo je prikazano v angleščini. Zavezujoča različica je angleška.",
    "sr_Latn": "Ceo tekst je prikazan na engleskom. Obavezujuća verzija je engleska.",
    "bs": "Cijeli tekst prikazan je na engleskom. Obavezujuća verzija je engleska.",
    "mk": "Целосниот текст е на англиски. Обврзувачката верзија е на англиски.",
    "sq": "Teksti i plotë shfaqet në anglisht. Versioni ligjërisht vlenës është ai anglisht.",
    "is": "Fullur texti birtist á ensku. Gildandi útgáfa er enska.",
    "ca": "El text complet es mostra en anglès. La versió vinculant és l’anglesa.",
    "ga": "Taispeántar an téacs iomlán i mBéarla. Is í an leagan Béarla an ceann ceangailteach.",
    "mt": "It-test kollu jintwera bl-Ingliż. Il-verżjoni vincolanti hija l-Ingliża.",
    "ja": "全文は英語で表示されます。拘束力のある版は英語版です。",
    "ko": "전체 텍스트는 영어로 표시됩니다. 구속력 있는 버전은 영어 버전입니다.",
    "vi": "Toàn văn hiển thị bằng tiếng Anh. Phiên bản ràng buộc là bản tiếng Anh.",
}

TITLE = {
    "de": "Datenschutzerklärung — MediaFolio",
    "fr": "Politique de confidentialité — MediaFolio",
    "es": "Política de privacidad — MediaFolio",
    "it": "Informativa sulla privacy — MediaFolio",
    "pt": "Política de privacidade — MediaFolio",
    "nl": "Privacybeleid — MediaFolio",
    "pl": "Polityka prywatności — MediaFolio",
    "by": "Палітыка прыватнасці — MediaFolio",
}


def main() -> None:
    en = json.loads(EN_PATH.read_text(encoding="utf-8"))
    for lang, notice in FALLBACK_NOTICE.items():
        if lang in HAND_MAINTAINED:
            continue
        data = deepcopy(en)
        data["fallbackNotice"] = notice
        if lang in TITLE:
            data["title"] = TITLE[lang]
        out = CONTENT / f"{lang}.json"
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("wrote", out.name)


STATIC_LANGS = {
    "en": "en",
    "zh_CN": "zh-CN",
}

PAGE = """<!DOCTYPE html>
<html lang="{html_lang}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{title}">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <div class="header-inner">
            <a class="brand" href="index.html">MediaFolio</a>
            <div class="lang-select">
                <a href="index.html">{more}</a>
            </div>
        </div>
    </header>
    <main>
        <h1>{title}</h1>
        <p class="updated">{updated}</p>
        <article id="body">
{sections}
        </article>
    </main>
    <footer>{footer}</footer>
</body>
</html>
"""

LABELS = {
    "en": "Other languages",
    "zh_CN": "其他语言 / Other languages",
}


def render_static(data: dict, lang: str) -> Path:
    parts = []
    for section in data["sections"]:
        parts.append("            <section>")
        parts.append("                <h2>%s</h2>" % html.escape(section["title"]))
        for block in section["blocks"]:
            if block["type"] == "p":
                parts.append("                <p>%s</p>" % block["html"])
            elif block["type"] == "ul":
                parts.append("                <ul>")
                for item in block["items"]:
                    parts.append("                    <li>%s</li>" % item)
                parts.append("                </ul>")
        parts.append("            </section>")
    page = PAGE.format(
        html_lang=STATIC_LANGS[lang],
        title=html.escape(data["title"]),
        updated=html.escape(data.get("updatedLabel", "")),
        footer=html.escape(data.get("footer", "")),
        more=html.escape(LABELS[lang]),
        sections="\n".join(parts),
    )
    out = ROOT / f"{lang}.html"
    out.write_text(page, encoding="utf-8")
    return out


def static() -> None:
    for lang in STATIC_LANGS:
        data = json.loads((CONTENT / f"{lang}.json").read_text(encoding="utf-8"))
        print("wrote", render_static(data, lang).name)


if __name__ == "__main__":
    if "--static" in sys.argv:
        static()
    else:
        main()

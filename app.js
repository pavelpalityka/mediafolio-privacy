const SUPPORTED_FULL = new Set([
    "en", "ru", "uk", "by", "de", "fr", "es", "it", "pt", "nl", "pl", "cs", "sk",
    "hu", "ro", "bg", "el", "tr", "sv", "da", "nb", "fi", "et", "lv", "lt", "hr",
    "sl", "sr_Latn", "bs", "mk", "sq", "is", "ca", "ga", "mt", "zh_CN", "ja", "ko", "vi",
]);

const LANG_OPTIONS = [
    ["en", "English"],
    ["ru", "Русский"],
    ["uk", "Українська"],
    ["by", "Беларуская"],
    ["de", "Deutsch"],
    ["fr", "Français"],
    ["es", "Español"],
    ["it", "Italiano"],
    ["pt", "Português"],
    ["nl", "Nederlands"],
    ["pl", "Polski"],
    ["cs", "Čeština"],
    ["sk", "Slovenčina"],
    ["hu", "Magyar"],
    ["ro", "Română"],
    ["bg", "Български"],
    ["el", "Ελληνικά"],
    ["tr", "Türkçe"],
    ["sv", "Svenska"],
    ["da", "Dansk"],
    ["nb", "Norsk Bokmål"],
    ["fi", "Suomi"],
    ["et", "Eesti"],
    ["lv", "Latviešu"],
    ["lt", "Lietuvių"],
    ["hr", "Hrvatski"],
    ["sl", "Slovenščina"],
    ["sr_Latn", "Srpski"],
    ["bs", "Bosanski"],
    ["mk", "Македонски"],
    ["sq", "Shqip"],
    ["is", "Íslenska"],
    ["ca", "Català"],
    ["ga", "Gaeilge"],
    ["mt", "Malti"],
    ["zh_CN", "简体中文"],
    ["ja", "日本語"],
    ["ko", "한국어"],
    ["vi", "Tiếng Việt"],
];

function normalizeLang(code) {
    if (!code) return "en";
    const c = code.replace("-", "_").toLowerCase();
    if (c === "be") return "by";
    if (c.startsWith("zh")) return "zh_CN";
    if (c.startsWith("nb") || c.startsWith("no")) return "nb";
    if (c.startsWith("sr")) return "sr_Latn";
    const base = c.split("_")[0];
    for (const [id] of LANG_OPTIONS) {
        if (id.toLowerCase() === c || id.toLowerCase() === base)
            return id;
    }
    return "en";
}

function queryLang() {
    const params = new URLSearchParams(window.location.search);
    const raw = params.get("lang");
    return raw ? normalizeLang(raw) : null;
}

function pickLang() {
    const fromQuery = queryLang();
    if (fromQuery) return fromQuery;
    const nav = navigator.languages || [navigator.language || "en"];
    for (const l of nav) {
        const n = normalizeLang(l);
        if (LANG_OPTIONS.some(([id]) => id === n))
            return n;
    }
    return "en";
}

async function loadContent(lang) {
    const tryLangs = [lang];
    if (!SUPPORTED_FULL.has(lang))
        tryLangs.push("en");
    else if (lang !== "en")
        tryLangs.push("en");

    for (const code of tryLangs) {
        try {
            const res = await fetch(`content/${code}.json`, { cache: "no-cache" });
            if (res.ok)
                return { data: await res.json(), requested: lang, loaded: code };
        } catch (_) { /* next */ }
    }
    throw new Error("Failed to load privacy policy");
}

function render(data, requested, loaded) {
    document.documentElement.lang = loaded;
    document.title = data.title;

    const notice = document.getElementById("notice");
    if (requested !== loaded && data.fallbackNotice) {
        notice.hidden = false;
        notice.textContent = data.fallbackNotice;
    } else {
        notice.hidden = true;
    }

    document.getElementById("title").textContent = data.title;
    document.getElementById("updated").textContent = data.updatedLabel;
    document.getElementById("footer").textContent = data.footer;

    const body = document.getElementById("body");
    body.innerHTML = "";
    for (const section of data.sections) {
        const el = document.createElement("section");
        const h2 = document.createElement("h2");
        h2.textContent = section.title;
        el.appendChild(h2);
        for (const block of section.blocks) {
            if (block.type === "p") {
                const p = document.createElement("p");
                p.innerHTML = block.html;
                el.appendChild(p);
            } else if (block.type === "ul") {
                const ul = document.createElement("ul");
                for (const item of block.items) {
                    const li = document.createElement("li");
                    li.innerHTML = item;
                    ul.appendChild(li);
                }
                el.appendChild(ul);
            }
        }
        body.appendChild(el);
    }
}

function fillLangSelect(current) {
    const select = document.getElementById("lang");
    select.innerHTML = "";
    for (const [code, name] of LANG_OPTIONS) {
        const opt = document.createElement("option");
        opt.value = code;
        opt.textContent = name;
        if (code === current) opt.selected = true;
        select.appendChild(opt);
    }
    select.addEventListener("change", () => {
        const url = new URL(window.location.href);
        url.searchParams.set("lang", select.value);
        window.location.href = url.toString();
    });
}

async function init() {
    const lang = pickLang();
    fillLangSelect(lang);
    try {
        const { data, requested, loaded } = await loadContent(lang);
        render(data, requested, loaded);
    } catch (e) {
        document.getElementById("body").innerHTML =
            "<p class=\"loading\">Unable to load privacy policy. Please try again later.</p>";
        console.error(e);
    }
}

init();

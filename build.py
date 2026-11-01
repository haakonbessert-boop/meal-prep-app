# Baut die App aus src/ und data/.
#   index.html  -> Einzeldatei für den Claude-Artifact-Prototyp
#   docs/       -> fertige PWA für GitHub Pages (Manifest, Offline, Icons)
import json, pathlib, shutil
root = pathlib.Path(__file__).parent
VERSION = "0.10.0"

# Profile: Haakons App (data/ -> docs/) und das Aufbau-Profil (data-aufbau/ -> docs/aufbau/).
# Das Aufbau-Profil bringt in rezepte.json unter "ui" eigene Texte, Namen und Speicher-Präfix mit.
def build(data, dist, artifact=False):
    rez = json.loads((root/data/"rezepte.json").read_text())
    ui = rez.get("ui", {})
    name = ui.get("app_name", "Meal Prep")
    t = (root/"src/index.template.html").read_text().replace("__APPVERSION__", VERSION)
    for k, f in [("REZEPTE", "rezepte.json"), ("ZUTATEN", "zutaten.json")]:
        t = t.replace(f"/*{k}*/", json.dumps(json.loads((root/data/f).read_text()), ensure_ascii=False))
    if ui:
        t = (t.replace("<title>Meal Prep Woche</title>", f"<title>{name}</title>")
              .replace("<h2>Meal Prep</h2>", f"<h2>{name}</h2>")
              .replace("Salat und Abendessen selbst kombinieren", ui.get("frei_text", "Salat und Abendessen selbst kombinieren"))
              .replace("Salat (15 Uhr, 5 Portionen)", ui.get("frei_salat", "Salat (15 Uhr, 5 Portionen)")))
    if artifact:
        (root/"index.html").write_text(t)

    # PWA: Kopf und Körper trennen, Grundgerüst drumherum
    split = t.index('<header class="top">')
    head, body = t[:split], t[split:]
    body = body.replace("render();\n</script>", """render();
if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js");
</script>""")
    page = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#faf9f5" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#262624" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="{name}">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" href="icons/icon-192.png">
<style>html{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);color-scheme:light}}body{{margin:0}}img{{max-width:100%}}</style>
{head}</head>
<body>
{body}</body>
</html>
"""
    (dist/"icons").mkdir(parents=True)
    (dist/"index.html").write_text(page)
    for p in (root/"src/icons").iterdir(): shutil.copy(p, dist/"icons"/p.name)
    (dist/"manifest.webmanifest").write_text(json.dumps({
      "name": name, "short_name": name, "lang": "de",
      "start_url": "./", "scope": "./", "display": "standalone",
      "background_color": "#faf9f5", "theme_color": "#faf9f5",
      "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
      ]}, ensure_ascii=False, indent=1))
    (dist/"sw.js").write_text((root/"src/sw.js").read_text().replace("meal-prep-v", ui.get("cache", "meal-prep-v")).replace("__VERSION__", VERSION))
    (dist/".nojekyll").write_text("")

shutil.rmtree(root/"docs", ignore_errors=True)
build("data", root/"docs", artifact=True)
build("data-aufbau", root/"docs"/"aufbau")
print(f"index.html, docs/ und docs/aufbau/ gebaut (v{VERSION})")

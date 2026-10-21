# Baut die App aus src/ und data/.
#   index.html  -> Einzeldatei für den Claude-Artifact-Prototyp
#   docs/       -> fertige PWA für GitHub Pages (Manifest, Offline, Icons)
import json, pathlib, shutil
root = pathlib.Path(__file__).parent
VERSION = "0.9.3"

t = (root/"src/index.template.html").read_text().replace("__APPVERSION__", VERSION)
for name, f in [("REZEPTE", "rezepte.json"), ("ZUTATEN", "zutaten.json")]:
    t = t.replace(f"/*{name}*/", json.dumps(json.loads((root/"data"/f).read_text()), ensure_ascii=False))
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
<meta name="apple-mobile-web-app-title" content="Meal Prep">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" href="icons/icon-192.png">
<style>html{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);color-scheme:light}}body{{margin:0}}img{{max-width:100%}}</style>
{head}</head>
<body>
{body}</body>
</html>
"""
dist = root/"docs"
shutil.rmtree(dist, ignore_errors=True)
(dist/"icons").mkdir(parents=True)
(dist/"index.html").write_text(page)
for p in (root/"src/icons").iterdir(): shutil.copy(p, dist/"icons"/p.name)
(dist/"manifest.webmanifest").write_text(json.dumps({
  "name": "Meal Prep", "short_name": "Meal Prep", "lang": "de",
  "start_url": "./", "scope": "./", "display": "standalone",
  "background_color": "#faf9f5", "theme_color": "#faf9f5",
  "icons": [
    {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
    {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ]}, ensure_ascii=False, indent=1))
(dist/"sw.js").write_text((root/"src/sw.js").read_text().replace("__VERSION__", VERSION))
(dist/".nojekyll").write_text("")
print(f"index.html und docs/ gebaut (v{VERSION})")

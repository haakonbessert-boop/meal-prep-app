# Erzeugt zutaten.json und berechnet die Makros in rezepte.json (Aufbau-Profil).
import json, pathlib
root = pathlib.Path(__file__).parent
def Z(name, abt, einheit, menge, kcal, p, f, basis="100 g", **kw):
    d = {"name": name, "abteilung": abt, "packung": {"einheit": einheit, "menge": menge},
         "naehrwerte": {"basis": basis, "kcal": kcal, "protein": p, "fett": f}}
    d.update(kw); return d
O, K, T, V = "Obst & Gemüse", "Kühltheke", "Konserven & Trocken", "Vorrat"
ZUT = {
 "_info": "Zutaten-Stammdaten Aufbau-Profil. Nährwerte = Standardwerte pro 100 g/ml bzw. pro Stück, vor dem Start mit der Tracking-App abgleichen. Kein Tiefkühler: nichts aus der Tiefkühltruhe.",
 "paprika": Z("Paprika", O, "Stück", 180, 31, 1, 0.3),
 "fruehlingszwiebel": Z("Frühlingszwiebeln", O, "Bund", 1, 32, 1.8, 0.2, basis="Bund"),
 "cocktailtomaten": Z("Cocktailtomaten", O, "Schale 250 g", 250, 19, 0.9, 0.3),
 "roemersalat": Z("Römersalatherzen", O, "Pck.", 200, 17, 1.2, 0.3),
 "limette": Z("Limette", O, "Stück", 1, 6, 0.1, 0, basis="Stück", stueck=True),
 "haehnchen": Z("Hähnchenbrust frisch", K, "× 500 g", 500, 105, 23.5, 1.2),
 "haehnchen_gegart": Z("Hähnchenbrust-Streifen gegart (vakuumiert)", K, "× 150 g", 150, 115, 22, 2.5),
 "kochschinken": Z("Kochschinken-Würfel", K, "× 200 g", 200, 110, 19, 3.5),
 "speck": Z("Speckwürfel", K, "× 150 g", 150, 310, 15, 28),
 "eier": Z("Eier", K, "Stück", 1, 81, 7.5, 5.5, basis="Stück", haltbar=True, stueck=True),
 "gouda": Z("Gouda am Stück", K, "× 200 g", 200, 360, 25, 28),
 "mozzarella_mini": Z("Mini-Mozzarella", K, "× 125 g", 125, 250, 18, 19),
 "cheddar": Z("Cheddar gerieben", K, "× 200 g", 200, 400, 25, 33),
 "emmentaler": Z("Emmentaler gerieben", K, "× 200 g", 200, 380, 28, 30),
 "pizzakaese": Z("Pizzakäse gerieben", K, "× 250 g", 250, 320, 23, 25),
 "parmesan": Z("Parmesan/Grana am Stück", K, "× 150 g", 150, 390, 33, 28, haltbar=True),
 "griech_joghurt": Z("Griechischer Joghurt 10 %", K, "× 500 g", 500, 120, 5.5, 10),
 "schmand": Z("Schmand", K, "× 200 g", 200, 240, 2.7, 24),
 "kochsahne": Z("Kochsahne 15 % (H)", K, "× 200 ml", 200, 165, 3, 15),
 "sahne": Z("Schlagsahne", K, "× 200 ml", 200, 290, 2.4, 30),
 "tortellini": Z("Tortellini mit Käse (Kühlregal)", K, "× 250 g", 250, 280, 11, 7),
 "spaetzle": Z("Spätzle (Kühlregal)", K, "× 500 g", 500, 165, 6, 2),
 "nudeln": Z("Nudeln (Spirelli, Fusilli, Farfalle)", T, "× 500 g", 500, 355, 12, 1.5, haltbar=True),
 "wraps": Z("Weizen-Wraps", T, "Pck. à 6", 6, 185, 5, 4.5, basis="Stück", stueck=True),
 "mais": Z("Mais (Dose)", T, "Dose", 285, 80, 2.5, 1.2),
 "kidneybohnen": Z("Kidneybohnen (Dose)", T, "Dose", 250, 108, 7.5, 0.6),
 "gewuerzgurken": Z("Gewürzgurken", T, "Glas", 15, 5, 0.2, 0, basis="Stück", haltbar=True, stueck=True),
 "pesto": Z("Pesto Genovese", T, "Glas", 190, 450, 5, 45),
 "getr_tomaten": Z("Getrocknete Tomaten in Öl", T, "Glas", 170, 200, 4, 15),
 "pinienkerne": Z("Pinienkerne", T, "× 50 g", 50, 670, 14, 68, haltbar=True),
 "salsa": Z("Salsa-Dip", T, "Glas", 300, 35, 1.5, 0.3),
 "tortilla_chips": Z("Tortilla-Chips", T, "Beutel", 175, 490, 7, 24),
 "caesar_dressing": Z("Caesar-Dressing", T, "Flasche", 250, 380, 2, 38),
 "mayo": Z("Salatmayonnaise", T, "Glas", 250, 480, 1, 50, haltbar=True),
 "passierte_tomaten": Z("Passierte Tomaten", T, "× 500 g", 500, 25, 1.3, 0.2),
 "milch": Z("H-Milch 3,5 %", T, "× 1 l", 1000, 64, 3.4, 3.5),
 "roestzwiebeln": Z("Röstzwiebeln", T, "Becher", 150, 600, 6, 42, haltbar=True),
 "mehl": Z("Mehl", V, "g", 1, 340, 10, 1, vorrat=True),
 "oel": Z("Öl", V, "g", 1, 900, 0, 100, vorrat=True),
 "gewuerze": {"name": "Gewürze (Salz, Pfeffer, Paprika, Oregano, Taco)", "abteilung": V, "vorrat": True},
}
(root/"zutaten.json").write_text(json.dumps(ZUT, ensure_ascii=False, indent=1))

r = json.loads((root/"rezepte.json").read_text())
def makros(rez):
    k = p = f = 0
    for e in rez["zutaten"]:
        key, m = e[0], e[1]
        if len(e) > 2 and e[2] < rez["portionen"] and key.endswith("_gegart"): continue  # Freitags-Ersatz zählt nicht doppelt
        n = ZUT[key].get("naehrwerte")
        if not n or not m: continue
        fac = m if n["basis"] in ("Stück", "Bund") else m / 100
        k += n["kcal"]*fac; p += n["protein"]*fac; f += n["fett"]*fac
    return {"kcal": round(k/10)*10, "protein": round(p), "fett": round(f)}
for rez in r["rezepte"]: rez["makros"] = makros(rez)
(root/"rezepte.json").write_text(json.dumps(r, ensure_ascii=False, indent=1))
byid = {x["id"]: x for x in r["rezepte"]}
for w in r["rotation"]:
    a, b = byid[w["salat"]]["makros"], byid[w["abend"]]["makros"]
    print(w["woche"], a, b, "Tag:", a["kcal"]+b["kcal"], a["protein"]+b["protein"])

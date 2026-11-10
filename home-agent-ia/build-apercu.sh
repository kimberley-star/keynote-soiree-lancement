#!/usr/bin/env bash
# Régénère apercu.html (page de prévisualisation) à partir de encart-agent-ia.html
cd "$(dirname "$0")"
{
cat <<'HEAD'
<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aperçu encart agent IA</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Poppins:wght@500;600;700;800&display=swap">
<style>body{margin:0;font-family:Lato,sans-serif;background:#fff;color:#182534}
.mock{padding:56px 16px;text-align:center;background:#F1F4F8;color:#768EA6;font:600 14px Poppins,sans-serif;border-bottom:1px dashed #CAD6E2}
.mock h1{margin:0 0 8px;color:#182534;font-size:32px}.mock .b{display:inline-block;margin:16px 6px 0;padding:12px 22px;border-radius:999px;background:#01AEC8;color:#fff;text-decoration:none}
.mock .b.o{background:#fff;color:#016D7D;border:1.5px solid #01AEC8}</style></head><body>
<div class="mock"><p>[ Hero existant ]</p><h1>L'outil de recrutement version terrain</h1>
<a class="b" href="#">Demander une démo</a><a class="b o" href="#agent-ia">Rencontrer notre agent IA</a></div>
HEAD
cat encart-agent-ia.html
echo '<div class="mock">[ Suite de la home : parcours en 4 étapes, témoignages… ]</div></body></html>'
} > apercu.html

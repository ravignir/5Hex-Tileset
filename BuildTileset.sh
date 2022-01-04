#!/usr/bin/env bash

# This can be the "build script" for the tileset.
# Alternatively, you could rewrite it entirely in Python.
# Based on 5Hex.

# ===LICENSE===
# By https://github.com/will-ca/, https://github.com/Intralexical.
# http://creativecommons.org/publicdomain/zero/1.0/
# To the extent possible under law, the person who associated CC0 with this work has waived all copyright and related or neighboring rights to this work.

set -eu


DIR="$(dirname "$(readlink -f "$0")")"

target="$DIR/Images/TileSets/5Hex"
echo && echo "Deleting previous build: $target"
sleep 1
rm -rfv "$target"

source="$DIR/src/5Hex"
echo && echo "Copying source to target: $source → $target"
sleep 1
cp -r "$source" "$target"


transformer="$DIR/TileTransformer.py"
echo && echo "Using TileTransformer.py at $transformer."
sleep 2


cd "$target"


SCALE=1.5
FUZZEDSCALE=1.5
#FUZZEDSHIFT=-0.125
#RIVERSHIFT=0.125

FUZZ_TILES=("Tiles/Ocean.png" "Tiles/Coast.png" "Tiles/Grassland.png" "Tiles/Grassland+Marsh.png" "Tiles/Great Barrier Reef.png" "Tiles/Plains.png" "Tiles/Tundra.png" "Tiles/Desert.png" "Tiles/Lakes.png" "Tiles/Snow.png" "Tiles/Fallout.png" "Tiles/Flood plains.png")

#BASE_TILES=("${FUZZ_TILES[@]}" "Tiles/Mountain.png")

BACKGROUND_GRASSLAND_TILES=("Tiles/El Dorado.png" "Tiles/Fountain of Youth.png" "Tiles/Mount Kilimanjaro.png" "Tiles/Rock of Gibraltar.png" "Tiles/Sri Pada.png" "Tiles/Mountain.png")
BACKGROUND_DESERT_TILES=("Tiles/Mount Sinai.png")
BACKGROUND_PLAINS_TILES=("Tiles/Barringer Crater.png" "Tiles/Grand Mesa.png" "Tiles/King Solomon's Mines.png" "Tiles/Lakes+Lake Victoria.png" "Tiles/Mount Kailash.png" "Tiles/Old Faithful.png" "Tiles/Uluru.png")
GRASSLAND="Tiles/Grassland.png"; DESERT="Tiles/Desert.png"; PLAINS="Tiles/Plains.png"

RIVER_TILES=("Tiles/River-Bottom.png" "Tiles/River-BottomLeft.png" "Tiles/River-BottomRight.png")

SHEARSHADOW_TILES=("Tiles/Academy.png" "Tiles/AcademySnowy.png" "Tiles/Aluminum+Mine.png" "Tiles/Ancient ruins.png" "Tiles/Ancient ruins2.png" "Tiles/AncientRuinsDesert.png" "Tiles/AncientRuinsForests.png" "Tiles/AncientRuinsSnowTundra.png" "Tiles/Antiquity Site.png" "Tiles/Cerro de Potosi.png" "Tiles/Chateau.png" "Tiles/Citadel.png" "Tiles/Coal+Mine.png" "Tiles/Copper+Mine.png" "Tiles/Feitoria.png" "Tiles/Iron+Mine.png" "Tiles/Krakatoa.png" "Tiles/Mountain.png" "Tiles/Mount Fuji.png" "Tiles/Silver+Mine.png" "Tiles/Sri Pada.png" "Tiles/Uluru.png" "Tiles/Uranium+Mine.png")

DROPSHADOW_TILES=("Tiles/Aluminum.png" "Tiles/Archaeological Dig.png" "Tiles/Bananas.png" "Tiles/Bananas+Plantation.png" "Tiles/Barbarian encampment.png" "Tiles/Bison.png" "Tiles/Bison+Camp.png" "Tiles/Cattle.png" "Tiles/Cattle+Pasture.png" "Tiles/Citrus.png" "Tiles/Citrus+Plantation.png" "Tiles/City center.png" "Tiles/City center-Ancient era.png" "Tiles/City center-Atomic era.png" "Tiles/City center-Classical era.png" "Tiles/City center-Future era.png" "Tiles/City center-Industrial era.png" "Tiles/City center-Information era.png" "Tiles/City center-Medieval era.png" "Tiles/City center-Modern era.png" "Tiles/City center-Renaissance era.png" "Tiles/City ruins.png" "Tiles/Coal.png" "Tiles/Cocoa.png" "Tiles/Cocoa+Plantation.png" "Tiles/Colossal Head.png" "Tiles/Copper.png" "Tiles/Cotton.png" "Tiles/Cotton+Plantation.png" "Tiles/Crab.png" "Tiles/Crab+Fishing Boats.png" "Tiles/Customs house.png" "Tiles/Deer.png" "Tiles/Deer+Camp.png" "Tiles/Dyes.png" "Tiles/Dyes+Plantation.png" "Tiles/Farm.png" "Tiles/Fish+Fishing Boats.png" "Tiles/Fishing Boats.png" "Tiles/Flood plains.png" "Tiles/Forest.png" "Tiles/Forest+Citrus.png" "Tiles/Forest+Deer.png" "Tiles/Forest+Deer+Camp.png" "Tiles/Forest+Dyes.png" "Tiles/Forest+Furs.png" "Tiles/Forest+Furs+Camp.png" "Tiles/Forest+Lumber mill.png" "Tiles/Forest+Sacred Grove.png" "Tiles/Forest+Silk.png" "Tiles/Forest+Spices.png" "Tiles/Forest +Trading post.png" "Tiles/Forest+Truffles.png" "Tiles/Forest+Truffles+Camp.png" "Tiles/Fort.png" "Tiles/Fountain of Youth.png" "Tiles/Furs.png" "Tiles/Furs+Camp.png" "Tiles/Gems.png" "Tiles/Gems+Mine.png" "Tiles/Gold Ore.png" "Tiles/Gold Ore+Mine.png" "Tiles/HF.png" "Tiles/HF+Citrus.png" "Tiles/HF+Deer.png" "Tiles/HF+Deer+Camp.png" "Tiles/HF+Dyes.png" "Tiles/HF+Furs.png" "Tiles/HF+Furs+Camp.png" "Tiles/HF+Lumber mill.png" "Tiles/HF+Sacred Grove.png" "Tiles/HF+Silk.png" "Tiles/HF+Spices.png" "Tiles/HF+Trading post.png" "Tiles/HF+Truffles.png" "Tiles/HF+Truffles+Camp.png" "Tiles/Holy Place.png" "Tiles/Holy site.png" "Tiles/Horses.png" "Tiles/Horses+Pasture.png" "Tiles/Ice.png" "Tiles/Incense.png" "Tiles/Incense+Plantation.png" "Tiles/Iron.png" "Tiles/Ivory.png" "Tiles/Ivory+Camp.png" "Tiles/Jungle.png" "Tiles/Jungle+Ancient ruins.png" "Tiles/Jungle+Bananas.png" "Tiles/Jungle+Brazilwood camp.png" "Tiles/Jungle+Citrus.png" "Tiles/Jungle+Cocoa.png" "Tiles/Jungle+Dyes.png" "Tiles/Jungle+Sacred Grove.png" "Tiles/Jungle+Spices.png" "Tiles/Jungle+Trading post.png" "Tiles/Jungle+Truffles.png" "Tiles/Jungle+Truffles+Camp.png" "Tiles/Kasbah.png" "Tiles/Kurgan.png" "Tiles/Landmark.png" "Tiles/Land Trade Route (Food).png" "Tiles/Land Trade Route (Gold).png" "Tiles/Land Trade Route (Production).png" "Tiles/Manufactory.png" "Tiles/Marble.png" "Tiles/Marble+Quarry.png" "Tiles/Mine.png" "Tiles/Moai.png" "Tiles/Oasis.png" "Tiles/Offshore platform.png" "Tiles/Oil well.png" "Tiles/Pasture.png" "Tiles/Pearls.png" "Tiles/Pearls+Fishing Boats.png" "Tiles/Polder.png" "Tiles/Sacred Place.png" "Tiles/Salt.png" "Tiles/Salt+Mine.png" "Tiles/Seaside Stall.png" "Tiles/Sea Trade Route (Food).png" "Tiles/Sea Trade Route (Gold).png" "Tiles/Sea Trade Route (Production).png" "Tiles/Sheep.png" "Tiles/Sheep+Pasture.png" "Tiles/Silk.png" "Tiles/Silk+Plantation.png" "Tiles/Silver.png" "Tiles/Spices.png" "Tiles/Spices+Plantation.png" "Tiles/Stone.png" "Tiles/Stone+Quarry.png" "Tiles/Sugar.png" "Tiles/Sugar+Plantation.png" "Tiles/Terrace farm.png" "Tiles/TF.png" "Tiles/TF+Citrus.png" "Tiles/TF+Deer.png" "Tiles/TF+Deer+Camp.png" "Tiles/TF+Dyes.png" "Tiles/TF+Furs.png" "Tiles/TF+Furs+Camp.png" "Tiles/TF+Lumber mill.png" "Tiles/TF+Sacred Grove.png" "Tiles/TF+Silk.png" "Tiles/TF+Spices.png" "Tiles/TF+Trading post.png" "Tiles/TF+Truffles.png" "Tiles/TF+Truffles+Camp.png" "Tiles/Trading post.png" "Tiles/Truffles.png" "Tiles/Truffles+Camp.png" "Tiles/Uranium.png" "Tiles/Whales.png" "Tiles/Whales+Fishing Boats.png" "Tiles/Wheat.png" "Tiles/Wheat+Farm.png" "Tiles/Wine.png" "Tiles/Wine+Plantation.png")


"$transformer" "expand(scale=$SCALE, topmargin=1.0)" Tiles/*.png

"$transformer" "shearShadow(scale=$SCALE, base=0.5, opacity=0.7, blur=0.05, length=1.15, shear=0.6)" "${SHEARSHADOW_TILES[@]}"
"$transformer" "dropShadow(scale=$SCALE, opacity=0.5, blur=0.01, x=0.05, y=0.05)" "${DROPSHADOW_TILES[@]}"

"$transformer" "tesselate($SCALE)" "${FUZZ_TILES[@]}"
"$transformer" "fuzzPolygonalFeather($SCALE, $FUZZEDSCALE)" "${FUZZ_TILES[@]}"

"$transformer" "addBackground('$GRASSLAND')" "${BACKGROUND_GRASSLAND_TILES[@]}"
"$transformer" "addBackground('$DESERT')" "${BACKGROUND_DESERT_TILES[@]}"
"$transformer" "addBackground('$PLAINS')" "${BACKGROUND_PLAINS_TILES[@]}"

#"$transformer" "shift($SCALE, y=$FUZZEDSHIFT)" "${BASE_TILES[@]}"
#"$transformer" "shift($SCALE, y=$RIVERSHIFT)" "${RIVER_TILES[@]}"


"$transformer" "expand(scale=$SCALE, topmargin=1.0)" Units/*.png
"$transformer" "shearShadow(scale=$SCALE, base=0.1, opacity=0.5, blur=0.015)" Units/*.png


"$transformer" "expand(scale=$SCALE, topmargin=0)" Hexagon.png
"$transformer" "expand(scale=$SCALE, topmargin=0)" Borders/*.png
"$transformer" "expand(scale=$SCALE, topmargin=0)" Crosshair.png CrosshatchHexagon.png Highlight.png

echo && echo "Tileset build complete."


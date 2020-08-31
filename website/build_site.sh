#!/bin/sh

cp -r ../documentation content/
jupyter nbconvert ../source/Mlos.Notebooks/*.ipynb --to markdown --output-dir content/notebooks

cp ../*.md content/
cp ../LICENSE content/
cp ../README.md content/_index.md
mv content/documentation/README.md content/documentation/_index.md

# replace markdown links
# this allows the original files to link on github directly
# while also rendering properly in hugo (which requires no .md in the links)
sed -i 's/\.md/\//g' content/*.md
sed -i 's/\.md/\//g' content/documentation/*.md


if [ ! -d "themes/book" ]; then
    git clone --depth 1 --branch v8 https://github.com/alex-shpak/hugo-book.git themes/book/
fi

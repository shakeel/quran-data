import sys
import glob
import os
from jinja2 import Template

htmlTemplate = Template("""<!DOCTYPE html>
<html lang="ar">
  <head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri+Quran&display=swap">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Reem+Kufi&display=swap">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri+Quran&family=Amiri">
    <title>{{name}}</title>
    <style>
    body {
      direction: rtl;
      text-align: justify;
      text-align-last: center;
      font-family: sans-serif;
      padding: 0 26px;
    }
    article {
    }
    .basmala {
      font-family: 'Amiri Quran', serif;
      font-size: xxx-large;
      font-weight: bold;
      text-align: center;
    }
    .sura-name {
      font-family: 'Reem Kufi', serif;
      font-size: xxx-large;
      text-align: center;
    }
    .sura {
      font-family: 'Amiri Quran', serif;
      font-size: xx-large;
      font-weight: bold;
    }
    </style>
  </head>
  <body>
    <article>
      <div class="sura-name">سورة {{name}}\t{{place}}</div>
      {%- if basmala %}
      <p class="basmala">&#xfdfd;</p>
      {% endif -%}
      <p class="sura">
      {{text}}
      </p>
    </article>
  </body>
</html>
""")

def build_page(textfile, metadata):
    text = textfile.read().strip()
    num = int(os.path.splitext(os.path.basename(textfile.name))[0])
    name, place, basmala = metadata[num]
    html = htmlTemplate.render(text=text, name=name, place=place, basmala=basmala)

    return html

def read_metadata(filename):
    metadata = {}
    with open(filename) as metafile:
        lines = [l.strip().split("\t") for l in metafile.readlines()]
        for num, line in enumerate(lines):
            num = num + 1
            metadata[num] = [line[0], line[1], True]
            if len(line) == 3:
                metadata[num][2] = False
    return metadata

def main():
    dirname = sys.argv[1]
    filenames = glob.glob(os.path.join(dirname,"???.txt"))
    metadata = read_metadata(os.path.join(dirname, "meta.txt"))
    for filename in filenames:
        with open(filename, "r") as textfile:
            html = build_page(textfile, metadata)
            with open(filename.replace(".txt", ".html"), "w") as htmlfile:
                htmlfile.write(html)

if __name__ == "__main__":
    main()

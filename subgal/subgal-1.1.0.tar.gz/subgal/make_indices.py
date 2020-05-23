#!/usr/bin/env python3

import sys
import os
import json
import collections

DEFAULT_BASE_URL = "http://localhost:8080/"

__doc__ = """Usage: subgal make-indices [options] [-v ...] <correlations.json>
       subgal make-indices --help

Options:
-h, --help                       This help
-i, --index-root=<path>          Where the index_....html files will be created
                                 [DEFAULT: .]
-v, --verbosity                  Number of v's is level of verbosity
                                 (No -v results in silence, -vvvv is
                                 super verbose)
-b, --base-url=<url>             All images and indices will have <url> at the beginning
                                 [DEFAULT: {1}]
""".format(sys.argv[0], DEFAULT_BASE_URL)


from docopt import docopt


def vprint(given_verbosity, verbosity, string):
  if given_verbosity <= verbosity:
    print(string)


def directories_to_original_filenames(correlation):
  to_return = collections.defaultdict(list)
  for original_filename in correlation.keys():
    directory = os.path.dirname(original_filename)
    to_return[directory].append(original_filename)
  return to_return


def create_main_index(main_index_filename, index_filenames):
  with open(main_index_filename, 'w') as f:
    f.write("""
<html>
  <head>
    <meta name="viewport" content="user-scalable=no, width=device-width, initial-scale=1, maximum-scale=1">

    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>

    <link href="https://unpkg.com/nanogallery2/dist/css/nanogallery2.min.css" rel="stylesheet" type="text/css">
    <script type="text/javascript" src="https://unpkg.com/nanogallery2/dist/jquery.nanogallery2.min.js"></script>

<style>
.myButton {
  box-shadow:inset 0px 1px 0px 0px #9acc85;
  background:linear-gradient(to bottom, #74ad5a 5%, #68a54b 100%);
  background-color:#74ad5a;
  border:1px solid #3b6e22;
  display:inline-block;
  cursor:pointer;
  color:#ffffff;
  font-family:Arial;
  font-size:13px;
  font-weight:bold;
  padding:6px 12px;
  text-decoration:none;
  margin: .2em;
}
.myButton:hover {
  background:linear-gradient(to bottom, #68a54b 5%, #74ad5a 100%);
  background-color:#68a54b;
}
.myButton:active {
  position:relative;
  top:1px;
}
</style>

  </head>
  <body>
    <ul>
    """)
    for index_filename in index_filenames:

      # Don't show index_ or .html
      f.write(f'<li><a class="myButton" href="{index_filename}">{os.path.splitext(index_filename)[0][6:]}</a></li>')
    f.write("""
    </ul>
    </div>

  </body>
</html>
    """)


def create_index(index_filename, directory, correlations, verbosity=0,
    thumb_key="300x300", big_key="1000x1000", main_index_filename="index.html"):
  v = verbosity
  vprint(1, v, f"Creating {index_filename}")
  with open(index_filename, 'w') as f:

    # The before-images part
    f.write("""
<html>
  <head>
    <meta name="viewport" content="user-scalable=no, width=device-width, initial-scale=1, maximum-scale=1">

    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>

    <link href="https://unpkg.com/nanogallery2/dist/css/nanogallery2.min.css" rel="stylesheet" type="text/css">
    <script type="text/javascript" src="https://unpkg.com/nanogallery2/dist/jquery.nanogallery2.min.js"></script>

<style>
.myButton {
  box-shadow:inset 0px 1px 0px 0px #9acc85;
  background:linear-gradient(to bottom, #74ad5a 5%, #68a54b 100%);
  background-color:#74ad5a;
  border:1px solid #3b6e22;
  display:inline-block;
  cursor:pointer;
  color:#ffffff;
  font-family:Arial;
  font-size:13px;
  font-weight:bold;
  padding:6px 12px;
  text-decoration:none;
  margin: .2em;
}
.myButton:hover {
  background:linear-gradient(to bottom, #68a54b 5%, #74ad5a 100%);
  background-color:#68a54b;
}
.myButton:active {
  position:relative;
  top:1px;
}
</style>

  </head>
  <body>
    <h3>""")
    f.write(directory)
    f.write("""</h3>
  <a class="myButton" href=""")
    f.write(main_index_filename)
    f.write(""">Index</a>
    <div ID="ngy2p" data-nanogallery2='{
        "itemsBaseURL": "./",
        "thumbnailWidth": "auto",
        "galleryDisplayMode": "pagination",
        "thumbnailAlignment": "center",
        "galleryMaxRows": 20,
        "galleryPaginationMode": "numbers",
        "gallerySorting": "random"
      }'>
    """)
    for original_filename in correlations:
      if os.path.dirname(original_filename) == directory:
        vprint(2, v, f"  {original_filename}")
        basename = os.path.basename(original_filename)

        # Here's where there are choices  I'm mapping one thumbnail to
        # another because originals are always so big
        try:
          thumb = correlations[original_filename][thumb_key]
          big = correlations[original_filename][big_key]
        except KeyError as e:
          message = f"Either {thumb_key} or {big_key} doesn't exist " \
              + f"for {original_filename}"
          vprint(1, v, message)
          raise ValueError(message)

        f.write(f'<a href="{big}" data-ngthumb="{thumb}" data-ngdesc="">{basename}</a>')

    # After the images part
    f.write("""
    </div>

  </body>
</html>
    """)


def main(argv):
  args = docopt(__doc__, argv=argv)

  base_url = args['--base-url']
  index_root = args['--index-root']
  json_filename = args['<correlations.json>']
  verbosity = args['--verbosity']
  v = verbosity

  with open(json_filename) as f:
    correlations = json.load(f)

  dtoof = directories_to_original_filenames(correlations)

  index_filenames = []
  for directory in dtoof.keys():
    index_filename = "index_" + directory.replace(os.path.sep, "__") + ".html"
    index_filenames.append(index_filename)
    try:
      create_index(index_filename, directory, correlations,
          verbosity=verbosity)
    except ValueError as e:
      vprint(1, v, "Missing some thumbs")
  create_main_index(os.path.join(index_root, "index.html"), index_filenames)


if __name__ == "__main__":
  main(sys.argv)

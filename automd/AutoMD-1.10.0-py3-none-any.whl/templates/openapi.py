# Adapted from python made by Otto Seiskary
#
#  Copyright 2017 Otto Seiskari
#  Licensed under the Apache License, Version 2.0.
#  See http://www.apache.org/licenses/LICENSE-2.0 for the full text.
#
#  This file is based on
#  https://github.com/swagger-api/swagger-ui/blob/4f1772f6544699bc748299bd65f7ae2112777abc/dist/index.html
#  (Copyright 2017 SmartBear Software, Licensed under Apache 2.0)
#
import yaml
import json
import sys

from typing import Dict

SWAGGER_UI_TEMPLATE_old: str = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Swagger UI</title>
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700|Source+Code+Pro:300,600|Titillium+Web:400,600,700" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/swagger-ui.css" >
  <style>
    html
    {
      box-sizing: border-box;
      overflow: -moz-scrollbars-vertical;
      overflow-y: scroll;
    }
    *,
    *:before,
    *:after
    {
      box-sizing: inherit;
    }
    body {
      margin:0;
      background: #fafafa;
    }
  </style>
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/swagger-ui-bundle.js"> </script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/swagger-ui-standalone-preset.js"> </script>
<script>
window.onload = function() {
  var spec = %s;
  // Build a system
  const ui = SwaggerUIBundle({
    spec: spec,
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [
      SwaggerUIBundle.presets.apis,
      //SwaggerUIStandalonePreset
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl
    ],
    //layout: "StandaloneLayout"
  })
  window.ui = ui
}
</script>
</body>
</html>
"""
SWAGGER_UI_TEMPLATE: str = """
<!-- HTML for static distribution bundle build -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Swagger UI</title>
    <link rel="icon" type="image/png" href="./favicon-32x32.png" sizes="32x32" />
    <link rel="icon" type="image/png" href="./favicon-16x16.png" sizes="16x16" />
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.25.3/swagger-ui.css" >
    <style>
      html
      {
        box-sizing: border-box;
        overflow: -moz-scrollbars-vertical;
        overflow-y: scroll;
      }

      *,
      *:before,
      *:after
      {
        box-sizing: inherit;
      }

      body
      {
        margin:0;
        background: #fafafa;
      }
    </style>
  </head>

  <body>
    <div id="swagger-ui"></div>

    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.25.3/swagger-ui-bundle.js"> </script>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.25.3/swagger-ui-standalone-preset.js"> </script>
    <script>
    window.onload = function() {
      // Begin Swagger UI call region
      var spec = %s;
      const ui = SwaggerUIBundle({  
        spec: spec,
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        plugins: [
          SwaggerUIBundle.plugins.DownloadUrl
        ],
        layout: "StandaloneLayout"
      })
      // End Swagger UI call region

      window.ui = ui
    }
  </script>
  </body>
</html>
"""
REDOC_TEMPLATE: str = """
<!DOCTYPE html>
<html>
  <head>
    <title>ReDoc</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">

    <!--
    ReDoc doesn't change outer page styles
    -->
    <style>
      body {
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div id='redoc-container'></div>
    <script>
      window.onload = function() {
        var spec = %s;
        Redoc.init(spec,
                   {},
                   document.getElementById('redoc-container')
        )
      }
    </script>
    <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
  </body>
</html>
"""


def generate_template_from_yaml(spec_yaml: str) -> str:
    """
    Creates the OpenAPI HTML page from a YAML input
    :param spec_yaml:
    :return:
    """
    spec: Dict = yaml.load(spec_yaml, Loader=yaml.FullLoader)
    return generate_template_from_dict(spec)


def generate_template_from_dict(spec_dict: Dict) -> str:
    """
        Creates the OpenAPI HTML page from a JSON input
        :param spec_dict:
        :return:
        """
    return REDOC_TEMPLATE % json.dumps(spec_dict)


def main():
    spec_yaml: str = sys.stdin.read()
    html_template: str = generate_template_from_yaml(spec_yaml)
    print(html_template)


if __name__ == "__main__":
    """
    Usage:
        python openapi.py < /path/to/api.yaml > doc.html
    """
    main()

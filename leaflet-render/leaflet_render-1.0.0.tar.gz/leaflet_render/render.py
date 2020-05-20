import subprocess
import os
import logging
import tempfile
import string
import pkgutil

logger = logging.getLogger(__name__)

leaflet_js = pkgutil.get_data('leaflet_render', 'leaflet.js').decode()
leaflet_css = pkgutil.get_data('leaflet_render', 'leaflet.css').decode()

# language=HTML
TEMPLATE = string.Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
   <style>$css</style>
   <script>$js</script>
    <!-- 
   <link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
   integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
   crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js"
   integrity="sha512-gZwIG9x3wUXg2hdXF6+rVkLF/0Vi9U8D2Ntg4Ga5I5BZpVkVxlJWbSQtXPSiUTtC0TjtGOmxa1AJPuV0CPthew=="
   crossorigin=""></script>
   -->
   <style>
    body {
        margin: 0;
        padding: 0;
    }
   </style>
</head>
<body>
    <div id="map" style="width: 100%; height: 100vh"></div>
    <script id="geojson" type="application/json">$geojson</script>
    <script>
    
    const geojson = JSON.parse(document.getElementById('geojson').textContent)
    const map = L.map('map', { zoomControl:false })

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map)

    const layer = L.geoJSON(geojson)
        .addTo(map)
    
    map.setView([-27, 25], 5)
    map.fitBounds(layer.getBounds())    
    
    </script>
</body>
</html>
""")


def render_geojson(geojson: str, width=800, height=600, chromium_path=None):
    if chromium_path is None:
        chromium_path = os.environ.get('CHROMIUM_PATH')
    if chromium_path is None:
        logger.warning('CHROMIUM_PATH not configured')
        return b''

    markup = tempfile.NamedTemporaryFile(mode='wb', suffix='.html')
    print(markup.name)
    markup.write(TEMPLATE.substitute(geojson=geojson, js=leaflet_js, css=leaflet_css).encode('utf-8'))

    # url = 'data:text/html;base64,' + base64.b64encode(
    #     TEMPLATE.substitute(geojson=geojson).encode('utf-8')
    # ).decode()

    with tempfile.NamedTemporaryFile(mode='rb') as tmp:
        try:
            subprocess.run([
                chromium_path,
                '--headless',
                f'file://{markup.name}',
                f'--window-size={width},{height}'
                '--hide-scrollbars',
                f'--screenshot={tmp.name}',
            ], check=True)
        except (subprocess.CalledProcessError, OSError) as e:
            logger.warning(f'error calling chromium: {e}')
            return b''
        tmp.seek(0)
        content = tmp.read()

    return content

import os
from os import listdir
from os.path import isfile, join
import re

class Reader:
  def __init__(self, lines):
    self._lines = lines
    self._position = -1
    self.current_line = None
    
    self.move()
  
  def move(self):
    while True:
      self._position += 1
      
      if self._position >= len(self._lines):
        self._position = len(self._lines)
        self.current_line = None
        break
      
      self.current_line = self._lines[self._position].strip()
      
      if len(self.current_line) != 0 and self.current_line[0] != '#':
        break

HTML_TEMPLATE = '''
<html>

<head>
    <title>Postprocessing</title>
    <style>
        body {
            margin: 0;
        }

        canvas {
            display: block;
        }
        
        #loadcase {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
        }
        
        #loadcase input {
            width: 500px;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/85/three.min.js"></script>
    <script src="https://unpkg.com/three@0.85.0/examples/js/controls/OrbitControls.js"></script>
</head>

<body>
    <script>
        var vertices = %VERTICES%;
        var faces = %FACES%;
        var displacements = %DISPLACEMENTS%;
        
        var scene = new THREE.Scene();
        scene.background = new THREE.Color(0xffffff);

        let width = window.innerWidth;
        let height = window.innerHeight;

        let fov = 45;
        let aspect = width / height;
        let near = 0.1;
        let far = 1000;

        let camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
        camera.position.set(-8, 8, -8)
        camera.lookAt(new THREE.Vector3(0, 0, 0));

        var renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        renderer.setSize(width, height);
        renderer.setPixelRatio(devicePixelRatio);

        controls.addEventListener('change', () => renderer.render(scene, camera));

        document.body.appendChild(renderer.domElement);
        
        function update(timestep) {
            while (scene.children.length > 0) { 
                scene.remove(scene.children[0]); 
            }

            var displacement = displacements[timestep];

            var ambientLight = new THREE.AmbientLight(0x0c0c0c);
            scene.add(ambientLight);
            
            var spotLight = new THREE.SpotLight(0xffffff);
            spotLight.position.set(-40, 60, -10);

            spotLight.castShadow = true;

            scene.add(spotLight);

            var geometry = new THREE.Geometry();

            for (let [key, x, y, z] of vertices) {
                var d = displacement[key];
                geometry.vertices.push(new THREE.Vector3(x + d[0], z + d[2], y + d[1]));
            }

            for (let [_, a, b, c, d] of faces) {
                geometry.faces.push(new THREE.Face3(a, b, c));
                geometry.faces.push(new THREE.Face3(c, d, a));
            }
            geometry.computeFaceNormals();
            geometry.computeVertexNormals();

            var material = new THREE.MeshLambertMaterial({
                side: THREE.DoubleSide,
                color: 0x999999,
                opacity: 0.5,
                transparent: true,
            });
            var mesh = new THREE.Mesh(geometry, material);
            scene.add(mesh);

            renderer.render(scene, camera);

            document.getElementById("currenttimestep").innerText = timestep;
        }

        update(0);
    </script>
    <div id="loadcase">
      <input type="range" min="0" max="%NB_TIMESTEPS%" value="0" step="1" class="slider" id="timestep" oninput="update(this.value)">
      <span id="currenttimestep">0</span>
    </div>
</body>

</html>
'''

def main():
    cwd = os.getcwd()

    for filename in listdir(cwd):
        path = join(cwd, filename)
        
        if not isfile(path):
            continue

        if not path.endswith('.msh'):
            continue

        post_msh_path = path
        post_res_path = path[:-3] + 'res'

        if not isfile(post_res_path):
            continue

        print(f'Process "{filename[:-4]}"...')

        with open(post_msh_path) as f:
            post_msh = f.readlines()

        with open(post_res_path) as f:
            post_res = f.readlines()

        # ---

        res_reader = Reader(post_res)
        
        if res_reader.current_line != 'GiD Post Results File 1.0':
            raise RuntimeError('Invalid file!')
        
        results = []
        
        def try_read_results():
            result_data = re.match(r'Result\s+"(?P<result_name>[\w\s,]+)"\s+"Load Case"\s+(?P<step_value>\d+)\s+(?P<type>(Vector|Scalar))\s+(?P<location>(OnNodes|OnGaussPoints))(\s+"(?P<locationName>[\w\s]+)")?', res_reader.current_line)
            
            if result_data is None:
                return False
            
            result_name = result_data.group('result_name')
            step_value = int(result_data.group('step_value'))
            result_type = result_data.group('type')
            location = result_data.group('location')
            
            res_reader.move()
            
            if res_reader.current_line != 'Values':
                raise RuntimeError('Invalid file!')
            
            res_reader.move()
            
            values = {}
            
            def read_scalar():
                scalarData = re.match(r'(?P<node>\d+)\s+(?P<value>-?[\d.]+(?:e[-+]?\d+)?)', res_reader.current_line)
                
                if scalarData is None:
                    raise RuntimeError(f'Invalid file! {res_reader.current_line}')
                
                node = int(scalarData.group('node'))
                vals = [float(scalarData.group('value'))]
                
                res_reader.move()
                vals.append(float(res_reader.current_line))
                res_reader.move()
                vals.append(float(res_reader.current_line))
                res_reader.move()
                vals.append(float(res_reader.current_line))
                
                values[node] = vals
            
            def read_vector():
                vectorData = re.match(r'(?P<node>\d+)\s+(?P<x>-?[\d.]+(?:e[-+]?\d+)?)\s+(?P<y>-?[\d.]+(?:e[-+]?\d+)?)\s+(?P<z>-?[\d.]+(?:e[-+]?\d+)?)', res_reader.current_line)
                
                if vectorData is None:
                    raise RuntimeError(f'Invalid file! {res_reader.current_line}')
                
                node = int(vectorData.group('node'))
                x = float(vectorData.group('x'))
                y = float(vectorData.group('y'))
                z = float(vectorData.group('z'))
                
                values[node] = [x, y, z]
            
            read_value = read_scalar if result_type == 'Scalar' else read_vector
            
            while res_reader.current_line is not None:
                if res_reader.current_line == 'End Values':
                    res_reader.move()
                    break
                
                read_value()
                
                res_reader.move()
            
            results.append({
                'result_name': result_name,
                'step_value': step_value,
                'values': values,
            })
            
            return True
        
        res_reader.move()
        
        while res_reader.current_line is not None:
            if try_read_results():
                continue
            
            res_reader.move()

        displacements = {}

        for result in results:
            if result['result_name'] != 'Displacement':
                continue
            displacements[result['step_value']] = result['values']

        # ---
        
        msh_reader = Reader(post_msh)

        msh_reader.move()

        if msh_reader.current_line != 'Coordinates':
            raise RuntimeError('invalid file!')
            
        nodes = {}
        nnodes = 0

        node_results = []

        vertices = []


        while True:
            msh_reader.move()

            if msh_reader.current_line == 'End Coordinates':
                msh_reader.move()
                break
            
            node_data = re.match(r'(?P<id>\d+)\s+(?P<x>-?[\d.]+(?:e[-+]?\d+)?)\s+(?P<y>-?[\d.]+(?:e[-+]?\d+)?)\s+(?P<z>-?[\d.]+(?:e[-+]?\d+)?)', msh_reader.current_line)

            if node_data is None:
                raise RuntimeError('Invalid file!')

            key = int(node_data.group('id'))
            x = float(node_data.group('x'))
            y = float(node_data.group('y'))
            z = float(node_data.group('z'))
            
            vertices.append([key, x, y, z])
            
            nodes[key] = nnodes
            nnodes += 1
            
        if re.match(r'MESH\s+"[\w\s]+"\s+dimension\s+2\s+ElemType\s+Quadrilateral\s+Nnode\s+4', msh_reader.current_line) is None:
            raise RuntimeError('Invalid file!')
        
        msh_reader.move()
        
        if msh_reader.current_line != 'Elements':
            raise RuntimeError('Invalid file!')
        
        faces = []
        
        while True:
            msh_reader.move()

            if msh_reader.current_line == 'End Elements':
                msh_reader.move()
                break

            element_data = re.match(r'(?P<id>\d+)\s+(?P<a>\d+)\s+(?P<b>\d+)\s+(?P<c>\d+)\s+(?P<d>\d+)\s+(?P<properties>\d+)', msh_reader.current_line)

            if element_data is None:
                raise RuntimeError('Invalid file!')

            key = int(element_data.group('id'))
            a = float(element_data.group('a'))
            b = float(element_data.group('b'))
            c = float(element_data.group('c'))
            d = float(element_data.group('d'))

            idx_a = nodes[a]
            idx_b = nodes[b]
            idx_c = nodes[c]
            idx_d = nodes[d]

            faces.append([key, idx_a, idx_b, idx_c, idx_d])

        result_path = path[:-9] + '-results.html'

        result = HTML_TEMPLATE.replace('%VERTICES%', str(vertices)) \
                              .replace('%FACES%', str(faces)) \
                              .replace('%DISPLACEMENTS%', str(displacements)) \
                              .replace('%NB_TIMESTEPS%', str(len(displacements)))
        
        with open(result_path, 'w') as f:
            f.write(result)

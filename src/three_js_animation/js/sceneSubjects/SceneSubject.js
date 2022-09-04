import { BufferGeometryLoader } from 'https://cdn.rawgit.com/mrdoob/three.js/master/src/loaders/BufferGeometryLoader.js';
import { GUI } from 'https://cdn.rawgit.com/mrdoob/three.js/master/examples/jsm/libs/lil-gui.module.min.js';


const gui = new GUI();
const amount = parseInt(window.location.search.slice(1)) || 10;
const count = Math.pow( amount, 3 );
const dummy = new THREE.Object3D();

// Geometries
const sphereGeometry = new THREE.SphereGeometry(0.4, 16, 8);
const boxGeometry = new THREE.BoxGeometry(0.5, 0.5, 0.5);
const torusGeometry = new THREE.TorusGeometry(0.3, 0.1, 8, 25);
const torusNotGeometry = new THREE.TorusKnotGeometry(0.3, 0.1, 100, 16);
const capsuleGeometry = new THREE.CapsuleGeometry(0.3, 0.3, 4, 8);
const circleGeometry = new THREE.CircleGeometry(0.3, 32);
const coneGeometry = new THREE.ConeGeometry(0.3, 0.7, 32);
const cylinderGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.7, 32);
const tubeGeometry = getTubeGeometry();
const GEOMETRIES = [
    boxGeometry,
    sphereGeometry,
    torusGeometry,
    torusNotGeometry,
    capsuleGeometry,
    circleGeometry,
    coneGeometry,
    cylinderGeometry,
    tubeGeometry,
];

// Texture
const TEXTURE_PATHS = [
    'js/textures/land_ocean_ice_cloud_2048.jpg',
    'js/textures/brick_wall.png',
    'js/textures/horse.jpeg',
    'js/textures/crate.gif',
    'js/textures/best-teacher-4ever.jpeg',
    'js/textures/confia.jpeg',
    'js/textures/cat-sad.jpeg',
    'js/textures/serjao.jpeg',
    'js/textures/kid-looking-weird.jpeg',
    'js/textures/huehue.png',
];


function getTubeGeometry(){
    class CustomSinCurve extends THREE.Curve {
        constructor( scale = 1 ) {
            super();
            this.scale = scale;
        }

        getPoint( t, optionalTarget = new THREE.Vector3() ) {
            const tx = t * 3 - 1.5;
            const ty = Math.sin( 2 * Math.PI * t );
            const tz = 0;

            return optionalTarget.set( tx, ty, tz ).multiplyScalar( this.scale );
        }
    }

    const path = new CustomSinCurve( 0.5 );
    const geometry = new THREE.TubeGeometry(path, 5, 0.5, 2, false);
    return geometry;
}


function plotObject(mesh) {
    if ( mesh ) {
        const time = Date.now() * 0.001;
        mesh.rotation.x = Math.sin( time / 4 );
        mesh.rotation.y = Math.sin( time / 2 );

        let i = 0;
        const offset = ( amount - 1 ) / 2;
        for (let x = 0; x < amount; x++) {
            for (let y = 0; y < amount; y++) {
                for (let z = 0; z < amount; z++) {
                    dummy.position.set(offset - x, offset - y, offset - z);
                    dummy.rotation.y = (Math.sin(x / 4 + time)
                        + Math.sin(y / 4 + time)
                        + Math.sin(z / 4 + time));
                    dummy.rotation.z = dummy.rotation.y * 2;
                    dummy.updateMatrix();
                    mesh.setMatrixAt(i++, dummy.matrix);
                }
            }
        }
        mesh.instanceMatrix.needsUpdate = true;
    }
}


function choice(choices) {
    const index = Math.floor(Math.random() * choices.length);
    return choices[index];
}


function getRandomGeometry() {
    return choice(GEOMETRIES);
}


function getRandomTexture() {
    const texturePath = choice(TEXTURE_PATHS);
    const texture = new THREE.TextureLoader().load(texturePath);
    return texture
}


function getRandomMaterial() {
    const texture = getRandomTexture();
    const basicMaterial = new THREE.MeshBasicMaterial({ map: texture});
    const toonMaterial = new THREE.MeshToonMaterial({ map: texture});
    const physicalMaterial = new THREE.MeshPhysicalMaterial({ map: texture, flatShading: true})
    const MATERIALS = [
        basicMaterial,
        toonMaterial,
        physicalMaterial,
    ];
    return choice(MATERIALS);
}


export function SceneSubject(scene) {

    function loadMesh() {
        function loadMonkey() {
            const loader = new BufferGeometryLoader();
            loader.load(
                // resource URL
                'js/models/json/monkey.json',
                // onLoad callback
                function (geometry) {
                    geometry.computeVertexNormals();
                    geometry.scale(0.5, 0.5, 0.5);
                    const material = new THREE.MeshNormalMaterial();
                    mesh = new THREE.InstancedMesh(geometry, material, count);
                    mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
                    scene.add(mesh);
                    gui.add(mesh, 'count', 0, count);
                    return mesh;
                },
                // onProgress callback
                function ( xhr ) {
                    let loadingProgress = (xhr.loaded / xhr.total * 100);
                    console.log(loadingProgress.toFixed(2) + '% loaded');
                },
                // onError callback
                function ( err ) {
                    console.log('An error happened. ' + err);
                }
            );
        }

        function createMesh() {
            const geometry = getRandomGeometry();
            const material = getRandomMaterial();
            mesh = new THREE.InstancedMesh(geometry, material, count);
            scene.add(mesh);
            gui.add(mesh, 'count', 0, count);
            return mesh;
        }

        // Get model or create mesh: 0 creates a mesh, 1 loads from external model.
        const index = choice([0, 0, 1])  // 1/3 %
        const function_ = [createMesh, loadMonkey][index];
        mesh = function_();
        return mesh
    }

    let mesh = undefined;
    loadMesh();

    this.update = function(time) {
        plotObject(mesh);
    }
}

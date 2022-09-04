import { SceneSubject } from './sceneSubjects/SceneSubject.js';


export function SceneManager(canvas) {
    const clock = new THREE.Clock();

    const screenDimensions = {
        width: canvas.width,
        height: canvas.height
    }

    const scene = buildScene();
    const renderer = buildRender(screenDimensions);
    const camera = buildCamera(screenDimensions);
    const sceneSubjects = createSceneSubjects(scene);

    function buildScene() {
        function buildSky() {
            // LIGHTS
            const light = new THREE.DirectionalLight( 0xaabbff, 0.3 );
            light.position.x = 300;
            light.position.y = 250;
            light.position.z = - 500;
            scene.add( light );

            // SKYDOME
            const vertexShader = document.getElementById( 'vertexShader' ).textContent;
            const fragmentShader = document.getElementById( 'fragmentShader' ).textContent;
            const uniforms = {
                topColor: { value: new THREE.Color( 0x0077ff ) },
                bottomColor: { value: new THREE.Color( 0xffffff ) },
                offset: { value: 400 },
                exponent: { value: 0.6 }
            };
            uniforms.topColor.value.copy( light.color );

            const skyGeo = new THREE.SphereGeometry( 4000, 32, 15 );
            const skyMat = new THREE.ShaderMaterial( {
                uniforms: uniforms,
                vertexShader: vertexShader,
                fragmentShader: fragmentShader,
                side: THREE.BackSide
            } );

            const sky = new THREE.Mesh( skyGeo, skyMat );
            scene.add( sky );
        }

        const scene = new THREE.Scene();
        buildSky();
        return scene;
    }

    function buildRender({ width, height }) {
        const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
        const DPR = (window.devicePixelRatio) ? window.devicePixelRatio : 1;
        renderer.setPixelRatio(DPR);
        renderer.setSize(width, height);

        renderer.gammaInput = true;
        renderer.gammaOutput = true;

        return renderer;
    }

    function buildCamera({ width, height }) {
        const aspectRatio = width / height;
        const fieldOfView = 2; // 40
        const nearPlane = 1;
        const farPlane = 10000;
        const camera = new THREE.PerspectiveCamera(
                fieldOfView, aspectRatio, nearPlane, farPlane);

        camera.position.set(700, 200, -500);

        // CONTROLS
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.maxPolarAngle = 0.9 * Math.PI / 2;
        controls.enableZoom = true;

        return camera;
    }

    function createSceneSubjects(scene) {
        const sceneSubjects = [
                new GeneralLights(scene),
                new SceneSubject(scene)
                ];
        return sceneSubjects;
    }

    this.update = function() {
        const elapsedTime = clock.getElapsedTime();

        for(let i=0; i<sceneSubjects.length; i++)
            sceneSubjects[i].update(elapsedTime);

        renderer.render(scene, camera);
    }

    this.onWindowResize = function() {
        const { width, height } = canvas;

        screenDimensions.width = width;
        screenDimensions.height = height;

        camera.aspect = width / height;
        camera.updateProjectionMatrix();

        renderer.setSize(width, height);
    }
}

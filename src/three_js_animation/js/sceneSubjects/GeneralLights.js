function GeneralLights(scene) {
    const color = "#fff";
    const intensity = 1;
    const distance = 0;
    const light = new THREE.PointLight(color, intensity, distance);
    const light2 = new THREE.AmbientLight(0x404040, intensity); // soft white light
    scene.add(light, light2);

    this.update = function(time) {
        light.intensity = (Math.sin(time) + 1.5) / 1.5;
        light.color.setHSL(Math.sin(time), 0.5, 0.5);
    }
}
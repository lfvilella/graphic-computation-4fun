# Playing with Three JS

## Requirements (pt-br)

Criar uma animação utilizando WebGL e a biblioteca Three.js que siga os seguintes critérios:

- [x] Utilizar animação com RequestAnimationFrame
  - [requestAnimationFrame(render);](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/three_js_animation/js/main.js#L33)
- [x] Utilize pelo menos 3 tipos diferentes de geometrias
  - [geometrias usadas](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/three_js_animation/js/sceneSubjects/SceneSubject.js#L20)
- [x] Utilize pelo menos 2 tipos de materiais
  - [materiais usados](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/three_js_animation/js/sceneSubjects/SceneSubject.js#L118)
- [x] Carregue pelo menos 1 textura
  - [texturas usadas | code](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/three_js_animation/js/sceneSubjects/SceneSubject.js#L106)
  - [texturas usadas | imagens](https://github.com/lfvilella/graphic-computation-4fun/tree/main/src/three_js_animation/js/textures)
- [x] Possua pelo menos 2 fontes de iluminação
  - [fonte 1](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/three_js_animation/js/sceneSubjects/GeneralLights.js#L5)
  - [fonte 2](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/three_js_animation/js/sceneSubjects/GeneralLights.js#L6)
- [x] Carregue pelo menos um modelo externo
  - [usado o BufferGeometryLoader](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/three_js_animation/js/sceneSubjects/SceneSubject.js#L130)
- [x] Realize a criação de objetos dinâmicos
  - [cria dinamicamente baseado no input do usuário](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/three_js_animation/js/sceneSubjects/SceneSubject.js#L69)
- [x] Possua algum tipo de interação com o usuário (mouse ou teclado)
  - [movimentos com camera](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/three_js_animation/js/SceneManager.js#L77)
  - [GUI](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/three_js_animation/js/sceneSubjects/SceneSubject.js#L5)
  - [gui.add](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/three_js_animation/js/sceneSubjects/SceneSubject.js#L143)

# Context

This project shows a little about the Three JS library. The main usage flow here is a mesh of small meshes that are rotating and the user can control the camera and the number of plots.

**Reload your page to get a random mesh with random texture, material and geometry.**

> *Tip: You have a 1/3 chance to load an external model (monkey model) instead of creating a random mesh.*

# Run locally

With python http.server:

```sh
$ python3 -m http.server
```

# Examples

![ezgif com-gif-maker](https://user-images.githubusercontent.com/45940140/188335165-e99689fe-16dc-4ed5-a0e7-ff723a524065.gif)
<img width="939" alt="Screen Shot 2022-09-04 at 18 38 56" src="https://user-images.githubusercontent.com/45940140/188335191-e4a06587-112c-43b6-af19-c35134686aa2.png">
<img width="940" alt="Screen Shot 2022-09-04 at 18 39 11" src="https://user-images.githubusercontent.com/45940140/188335192-0f23863d-84c6-434c-82cf-28a6196880f6.png">
<img width="938" alt="Screen Shot 2022-09-04 at 18 39 21" src="https://user-images.githubusercontent.com/45940140/188335193-456a446b-c557-4dc2-9e6f-4d9c00bdec55.png">
<img width="941" alt="Screen Shot 2022-09-04 at 18 39 48" src="https://user-images.githubusercontent.com/45940140/188335194-73afa9e5-23c9-49a3-b464-cadf7a6a73d8.png">
<img width="943" alt="Screen Shot 2022-09-04 at 18 40 08" src="https://user-images.githubusercontent.com/45940140/188335195-24842a30-212b-4e3f-a77f-27f7b9249b6b.png">
<img width="939" alt="Screen Shot 2022-09-04 at 18 42 15" src="https://user-images.githubusercontent.com/45940140/188335205-123dddb9-9dc1-4152-8732-6dcd83664dce.png">
<img width="940" alt="Screen Shot 2022-09-04 at 18 44 07" src="https://user-images.githubusercontent.com/45940140/188335206-7c7537cc-cd36-4e32-8215-290ba82f27c9.png">
<img width="939" alt="Screen Shot 2022-09-04 at 18 45 19" src="https://user-images.githubusercontent.com/45940140/188335207-692fe8de-6373-4bde-8c65-94c031c11837.png">
<img width="939" alt="Screen Shot 2022-09-04 at 18 41 02" src="https://user-images.githubusercontent.com/45940140/188335208-fd57849e-ef23-4ea8-8ce1-be1c9cb53a1e.png">
<img width="941" alt="Screen Shot 2022-09-04 at 18 40 31" src="https://user-images.githubusercontent.com/45940140/188335209-e015e1dd-b483-4a55-b377-1e8181890dfe.png">

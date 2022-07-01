# Protocolo de processamento e interpretação de imagens

## Objetivo

---

São dois objetivos a princípio, um identificar e contar a quantidade de placas 
memoriais nas paredes do bloco de CCT da UENP (Campus Luiz Meneghel, Bandeirantes-PR), 
e o outro objetivo é contar a quantidade de caracteres nessas placas. 

## Ferramentas Utilizadas

---

Foi utilizado Python + OpenCV + Tesseract para atingir o objetivo, todas 
bibliotecas requeridas podem ser encontrados em `requirements.txt`, 
porém uma lista breve das ferramentas utilizadas são:

- OS based on Unix (Linux or MacOS)
- Python
- OpenCV
- opencv-python
- pytesseract
- Pillow
- matplotlib

## Desafios

---

Não houve muito desafio para **contar as placas na parade**, pois a parade era da cor branca 
tendo um alto contraste com o objeto alvo, porém na **contagem dos caracteres da placa** a
parede no fundo e a iluminação que refletia nas letras foram os principais desafios.

## Protocolo - Find plates

---

### 1. Aquisição das imagens

O equipamento utilizado para coletar as imagens foi um smartphone (Xiaomi POCO F3),
não teve nenhum parâmentro crítico ou formato utilizado, simplesmente chegar no local
em uma distancia onde a parade fique como fundo, ou seja, não tirar foto de pessoas
passando na frente ou janelas ao redor. 

### 2. Pré-processamento

Os filtros utilizados em ordem foram:
- [medianBlur](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/uenp_plates/__init__.py#L127)
- [gray](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/uenp_plates/__init__.py#L128)

Primeiramente borramos a imagem usando um valor de `35` para remove o ruído, 
pois o intuíto é contar placas, em seguida aplicamos o filtro de cinza.

### 3. Segmentação

O filtro utilizado foi:

- [thresh](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/uenp_plates/__init__.py#L139)

Não foi necessário aplicar nenhuma erosão ou dilatação, pois o espaçamento entre
as placas na parede era de uma boa distancia, e sendo assim foi necessário apenas
aplicar uma limiarização, onde basicamente destaca as placas do fundo branco da parede.

### 4. Interpretação

A estratégia para contar as placas foi usar o [`findCountours`](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/uenp_plates/__init__.py#L147) 
para encontrar os contornos, passando [`cv2.RETR_EXTERNAL`](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html#ga819779b9857cc2f8601e6526a3a5bc71)
(para recuperar apenas os contornos externos extremos) e [`cv2.CHAIN_APPROX_SIMPLE`](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html#ga4303f45752694956374734a03c54d5ff)
(para comprimir os segmentos horizontais, verticais e diagnonais, deixando apenas
os pontos finais). Para finalizar utiliza do [`imutils.grab_contours`](https://github.com/PyImageSearch/imutils/blob/9f740a53bcc2ed7eba2558afed8b4c17fd8a1d4c/imutils/convenience.py#L154)
para "agarrar" os contornous, onde basicamente ele faz um `get` dos contornos 
mantendo *backward compatibilities* com as versões do OpenCV. 

### Experimento para a validação do método

| <img width="1207" alt="Screen Shot 2022-07-01 at 16 46 29" src="https://user-images.githubusercontent.com/45940140/176960046-05de190b-7148-4ee1-bb9c-1456cddd9d97.png">                                                                    |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Exemplo do resultado sendo afetado pela luminosidade do local <br/><img width="1205" alt="Screen Shot 2022-07-04 at 20 05 40" src="https://user-images.githubusercontent.com/45940140/177224487-c614470e-1c82-46d4-8bf3-667be6eecbbe.png"> |

Essa é uma imagem dos passos executados em ordem numérica pelo algoritmo. Para executar
o algoritmo em outras apenas mude o `filepath`.

### [CLI Usage:](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/uenp_plates/__main__.py#L27)

*Certifique-se que esteja dentro de src (`cd src`) antes de rodar os comandos.*

```sh
python -m uenp_plates --module find_plates --filepath ./uenp_plates/images/plates1.jpeg --debug --export
```

[`--module`](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/uenp_plates/__main__.py#L11)

- find_plates
- read_plates

`--filepath`: O caminho da imagem a ser processada.

`--debug`: Flag para ver passos executados na imagem com matplotlib

`--export`: Flag para exporta os passos em imagens. Exemplo:

![Screen Shot 2022-07-01 at 16 35 41](https://user-images.githubusercontent.com/45940140/176960053-88cd6884-86b6-4cf9-89f6-573383c21f74.png)

`--language`: Linguagem utilizada pelo tesseract

## Protocolo - Read plates

---

#### 1. Aquisição das imagens

O equipamento utilizado para coletar as imagens foi o smartphone (Xiaomi POCO F3),
não teve nenhum parâmentro crítico ou formato utilizado, simplesmente chegar no local
em uma distancia onde as letras da placa fique legível (isso está ligado a
resolução da imagem). Também é sugerível controlar a luminosidade para não afetar
o resultado final, ou seja, não deixar feichos de luz atingir a placa.

### 2. Pré-processamento

Os filtros utilizados em ordem foram:
- [FindPlates](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/uenp_plates/__init__.py#L179)
- [crop images](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/uenp_plates/__init__.py#L186)

Aqui podemos reaproveitar o processamento de imagem do `FindPlates`, onde a ideia
é encontrar a placa e fazer um recorte dela para continuar processando na segmentação
e interpretação.

### 3. Segmentação

O filtro utilizado foi:
- [thresh](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/uenp_plates/__init__.py#L201)

Como a letra da placa é bem diferente do fundo apenas aplicamos uma limiarização 
por placa.

### 4. Interpretação

A estratégia para contar as placas foi usar o [`findCountours`](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/uenp_plates/__init__.py#L147)
para encontrar os contornos, passando [`cv2.RETR_EXTERNAL`](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html#ga819779b9857cc2f8601e6526a3a5bc71)
(para recuperar apenas os contornos externos extremos) e [`cv2.CHAIN_APPROX_NONE`](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html#ga4303f45752694956374734a03c54d5ff)
(para armazenar todos os pontos do contorno). Para finalizar iteramos sobre esses
contornos (bloco de textos) e utilizamos o [pytesseract](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/uenp_plates/__init__.py#L223)
para converter o conteudo das image em texto.

### Experimento para a validação do método

| ![Screen Shot 2022-07-01 at 16 59 40](https://user-images.githubusercontent.com/45940140/176961321-bf7d2428-174f-4f8d-8683-fdc95934a103.png)                                                                                                 | ![Screen Shot 2022-07-01 at 17 14 18](https://user-images.githubusercontent.com/45940140/176962739-94d4a2a5-250b-4f11-b6bc-741fc4c59438.png) |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| Exemplo 1 do resultado sendo afetado pela luminosidade do local <br/><img width="1221" alt="Screen Shot 2022-07-04 at 20 07 06" src="https://user-images.githubusercontent.com/45940140/177224511-615e0912-d52f-4e3f-a237-6341be86e78c.png"> | ![Screen Shot 2022-07-04 at 20 09 00](https://user-images.githubusercontent.com/45940140/177224514-caa237be-889f-4c93-ab39-468cc9dbdb39.png) | 
| ![Screen Shot 2022-07-04 at 20 09 40](https://user-images.githubusercontent.com/45940140/177224526-ad55767f-1b99-4be1-8d40-13ab968e0754.png)                                                                                                 | ![Screen Shot 2022-07-04 at 20 11 26](https://user-images.githubusercontent.com/45940140/177224532-d920b7ac-9d5c-491f-ac42-b5ef284f0a00.png) |
| ![Screen Shot 2022-07-04 at 20 12 00](https://user-images.githubusercontent.com/45940140/177224540-93f8219d-62fe-4a2f-a53c-a5f2ffcaecd2.png)                                                                                                 | ![Screen Shot 2022-07-04 at 20 12 55](https://user-images.githubusercontent.com/45940140/177224548-30e0a771-99f9-4b82-bbf8-d6fd1ac127e3.png) |

Essa é uma imagem dos passos executados em ordem numérica pelo algoritmo. Para executar
o algoritmo em outras apenas mude o `filepath`.


### [CLI Usage:](https://github.com/lfvilella/graphic-computation-4fun/blob/main/src/uenp_plates/__main__.py#L27)

*Certifique-se que esteja dentro de src (`cd src`) antes de rodar os comandos.*

```sh
python -m uenp_plates --module read_plates --filepath ./uenp_plates/images/letters1.jpeg --debug --export
```

Apenas foi alterado o `module` e o `filepath` é o mesmo CLI previamente documentado.
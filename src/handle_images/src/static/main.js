class RGBColor {
    constructor(r, g, b) {
        this.red = r;
        this.green = g;
        this.blue = b;
    }
}

class RGBAColor extends RGBColor{
    constructor(r, g, b, a) {
        super(r, g, b);
        this.alpha = a;
    }
}

class MatrixImage {
    constructor(imageData) {
        this.imageData = imageData;
        this.height = imageData.height;
        this.width = imageData.width;
    }

    getPixel(x, y) {
        let position = ((y * (this.width * 4)) + (x * 4));
        return new RGBAColor(
            this.imageData.data[position],  // red
            this.imageData.data[position + 1],  // green
            this.imageData.data[position + 2],  // blue
            this.imageData.data[position + 3],  // alpha
        );
    }

    setPixel(x, y, color) {
        let position = ((y * (this.width * 4)) + (x * 4));
        this.imageData.data[position] = color.red;
        this.imageData.data[position + 1] = color.green;
        this.imageData.data[position + 2] = color.blue;
        if (color.alpha !== undefined){
            this.imageData.data[position + 3] = color.alpha;
        }
    }
}


let IMAGE = document.getElementById('image');
// IMAGE.setAttribute('crossOrigin', 'Anonymous');
let CANVAS = document.getElementById('image-canvas');
let CONTEXT;


let drawImage = function(cv, ctx, img, buildSquare = false) {
    let _width = img.width;
    let _height = img.height;
    if (buildSquare) {
        const higherDimension = Math.max(_width, _height);
        _width = higherDimension;
        _height = higherDimension;
    }
    cv.width = _width;
    cv.height = _height;
    ctx.drawImage(img, 0, 0);
}


let load = function (){
    CONTEXT = CANVAS.getContext('2d');
    drawImage(CANVAS, CONTEXT, IMAGE);
}


let redScale = function() {
    const imageData = CONTEXT.getImageData(
            0, 0, CANVAS.width, CANVAS.height);
    const data = imageData.data;
    for (let i = 0; i < data.length; i+=4) {
        data[i+1] = 0;
        data[i+2] = 0;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}


let cyanScale = function() {
    const imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    const data = imageData.data;
    for (let i = 0; i < data.length; i+=4) {
        data[i+1] = 255;
        data[i+2] = 255;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}


let greenScale = function() {
    const imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    const data = imageData.data;
    for (let i = 0; i < data.length; i+=4) {
        data[i] = 0;
        data[i+2] = 0;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}


let magentaScale = function() {
    const imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    const data = imageData.data;
    for (let i = 0; i < data.length; i+=4) {
        data[i] = 255;
        data[i+2] = 255;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}


let blueScale = function() {
    const imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    const data = imageData.data;
    for (let i = 0; i < data.length; i+=4) {
        data[i] = 0;
        data[i+1] = 0;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}


let yellowScale = function() {
    const imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    const data = imageData.data;
    for (let i = 0; i < data.length; i+=4) {
        data[i] = 255;
        data[i+1] = 255;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}


let grayScale = function() {
    const imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    const data = imageData.data;
    for (let i = 0; i < data.length; i+=4) {
        const red = data[i];
        const green = data[i + 1];
        const blue = data[i+2];
        const gray = (red + green + blue) / 3;
        data[i] = data[i+1] = data[i+2] = gray;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}


let _pushPixel = function (pixels, pixel) {
    pixels.push(pixel.red);
    pixels.push(pixel.green);
    pixels.push(pixel.blue);
}


let grayMeanScale = function() {
    let imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    let img = new MatrixImage(imageData);
    for (let i = 2; i < img.width - 2; i++) {
        for (let j = 2; j < img.height - 2; j++) {
            const pixels = Array();
            const pixel1 = img.getPixel(i - 1, j - 1);
            _pushPixel(pixels, pixel1);
            const pixel2 = img.getPixel(i - 1, j);
            _pushPixel(pixels, pixel2);
            const pixel3 = img.getPixel(i, j - 1);
            _pushPixel(pixels, pixel3);
            const pixel4 = img.getPixel(i + 1, j - 1);
            _pushPixel(pixels, pixel4);
            const pixel5 = img.getPixel(i, j);
            _pushPixel(pixels, pixel5);
            const pixel6 = img.getPixel(i - 1, j + 1);
            _pushPixel(pixels, pixel6);
            const pixel7 = img.getPixel(i, j + 1);
            _pushPixel(pixels, pixel7);
            const pixel8 = img.getPixel(i + 1, j);
            _pushPixel(pixels, pixel8);
            const pixel9 = img.getPixel(i + 1, j + 1);
            _pushPixel(pixels, pixel9);
            const gray = pixels.reduce((a, b) => a + b, 0) / pixels.length;
            img.setPixel(i, j, new RGBColor(gray, gray, gray));
        }
    }
    CONTEXT.putImageData(img.imageData, 0, 0);
}


const median = arr => {
    let middle = Math.floor(arr.length / 2);
    arr = [...arr].sort((a, b) => a - b);
    return arr.length % 2 !== 0 ? arr[middle] : (arr[middle - 1] + arr[middle]) / 2;
};


let grayMedianScale = function() {
    let imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    let img = new MatrixImage(imageData);
    for (let i = 2; i < img.width-2; i++) {
        for (let j = 2; j < img.height-2; j++) {
            const pixels = Array();
            const pixel1 = img.getPixel(i - 1, j - 1);
            _pushPixel(pixels, pixel1);
            const pixel2 = img.getPixel(i - 1, j);
            _pushPixel(pixels, pixel2);
            const pixel3 = img.getPixel(i, j - 1);
            _pushPixel(pixels, pixel3);
            const pixel4 = img.getPixel(i + 1, j - 1);
            _pushPixel(pixels, pixel4);
            const pixel5 = img.getPixel(i, j);
            _pushPixel(pixels, pixel5);
            const pixel6 = img.getPixel(i - 1, j + 1);
            _pushPixel(pixels, pixel6);
            const pixel7 = img.getPixel(i, j + 1);
            _pushPixel(pixels, pixel7);
            const pixel8 = img.getPixel(i + 1, j);
            _pushPixel(pixels, pixel8);
            const pixel9 = img.getPixel(i + 1, j + 1);
            _pushPixel(pixels, pixel9);
            const gray = median(pixels);
            img.setPixel(i, j, new RGBColor(gray, gray, gray));
        }
    }
    CONTEXT.putImageData(img.imageData, 0, 0);
}


let thresholdingScale = function() {
    const imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    const data = imageData.data;
    const grayScale = [];
    for (let i = 0; i < data.length; i+=4) {
        const red = data[i];
        const green = data[i + 1];
        const blue = data[i + 2];
        const gray = (red + green + blue) / 3;
        grayScale.push(gray);
    }
    const threshold = grayScale.reduce(
            (a, b) => a + b, 0) / grayScale.length;  // mean

    for (let i = 0; i < data.length; i+=4) {
        const red = data[i];
        const green = data[i+1];
        const blue = data[i+2];
        // TODO: should be a flow/way to invert it
        const gray = ((red + green + blue) / 3) <= threshold ? 0: 255;
        data[i] = data[i+1] = data[i+2] = gray;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}


let grayScaleCIE = function() {
    const imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    const data = imageData.data;
    for (let i = 0; i < data.length; i+=4) {
        const red = data[i];
        const green = data[i+1];
        const blue = data[i+2];
        const gray = (red * 0.2126 + green * 0.7152 + blue * 0.0722);
        data[i] = data[i+1] = data[i+2] = gray;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}


let grayScaleNTSC = function() {
    const imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    const data = imageData.data;
    for (let i = 0; i < data.length; i+=4) {
        const red = data[i];
        const green = data[i+1];
        const blue = data[i+2];
        const gray = (red * 0.299 + green * 0.587 + blue * 0.144);
        data[i] = data[i+1] = data[i+2] = gray;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}


let blurGaussian = function() {
    const radius = 8;
    const blur = radius;
    const blurRange = blur * 3;
    const gaussParam = new Array;
    for (let i = 0; i <= blurRange; i++){
      gaussParam[i] = Math.exp(-i * i / (2 * blur * blur));
    }

    const imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    const img = new MatrixImage(imageData);
    const width = img.width;
    const height = img.height;

    const data = imageData.data;
    let ox, oy, gauss, count, R, G, B, A;
    for(let i = 0, len = width * height; i<len; i++){
        gauss = count = R = G = B = A = 0;
        ox = i % width;
        oy = (i / width)|0;  // = Math.floor(i / width);
        for (let x = -1 * blurRange; x <= blurRange; x++){
            const tx = ox + x;
            if ((0 <= tx) && (tx < width)){
                gauss = gaussParam[x<0?-x:x];  // = [Math.abs(x)]
                const k = i + x;
                R += data[k*4 + 0] * gauss;
                G += data[k*4 + 1] * gauss;
                B += data[k*4 + 2] * gauss;
                A += data[k*4 + 3] * gauss;
                count += gauss;
            }
        }
        data[i*4 + 0] = (R / count)|0;
        data[i*4 + 1] = (G / count)|0;
        data[i*4 + 2] = (B / count)|0;
        data[i*4 + 3] = (A / count)|0;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}


let contrast = function() {
    const imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    const data = imageData.data;

    let redFactor = 0;
    let greenFactor = 0;
    let blueFactor = 0;
    // let alphaFactor = 0;
    for (let i = 0; i < data.length; i+=4) {
        redFactor += data[i];
        greenFactor += data[i+1];
        blueFactor += data[i+2];
        // alphaFactor += data[i+3];
    }
    redFactor = redFactor % 255 * 0.05;
    greenFactor = greenFactor % 255 * 0.05;
    blueFactor = blueFactor % 255 * 0.05;
    // alphaFactor = alphaFactor % 255 * 0.05;

    for (let i = 0; i < data.length; i+=4) {
        data[i] *= redFactor;
        data[i+1] *= greenFactor;
        data[i+2] *= blueFactor;
        // data[i+3] *= alphaFactor;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}


let brightness = function() {
    const imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    const data = imageData.data;
    for (let i = 0; i < data.length; i+=4) {
        data[i] *= 1.75;
        data[i+1] *= 1.75;
        data[i+2] *= 1.75;
    }
    CONTEXT.putImageData(imageData, 0, 0);
}

let horizontalFlip = function() {
    let imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    let img = new MatrixImage(imageData);
    for (let i = 0; i < img.width / 2; i++) {
        for (let j = 0; j < img.height; j++) {
            const pixel= img.getPixel(i, j);
            const columnToFlip = (img.width - 1) - i
            const pixelInverted = img.getPixel(columnToFlip, j);
            img.setPixel(i, j, pixelInverted);
            img.setPixel(columnToFlip, j, pixel);
        }
    }
    CONTEXT.putImageData(img.imageData, 0, 0);
}


let verticalFlip = function() {
    let imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    let img = new MatrixImage(imageData);
    for (let i = 0; i < img.width; i++) {
        for (let j = 0; j < img.height / 2; j++) {
            const pixel= img.getPixel(i, j);
            const lineToFlip = (img.height - 1) - j
            const pixelInverted = img.getPixel(i, lineToFlip);
            img.setPixel(i, j, pixelInverted);
            img.setPixel(i, lineToFlip, pixel);
        }
    }
    CONTEXT.putImageData(img.imageData, 0, 0);
}


let _ALREADY_ROTATED = false;


let rotate90Degree = function() {
    let drawHorizontally = _ALREADY_ROTATED;
    if (!_ALREADY_ROTATED){
        drawImage(CANVAS, CONTEXT, IMAGE, true);
        _ALREADY_ROTATED = true;
    }
    let imageData = CONTEXT.getImageData(0, 0, CANVAS.width, CANVAS.height);
    let img = new MatrixImage(imageData);
    let imageDataRotate = CONTEXT.getImageData(
            0, 0, CANVAS.width, CANVAS.height);
    let imgRotate = new MatrixImage(imageDataRotate);
    for (let i = 0; i < img.width; i++) {
        for (let j = 0; j < img.height; j++) {
            const pixel= img.getPixel(i, j);
            imgRotate.setPixel(j, i, pixel);
        }
    }
    if (drawHorizontally) {
        drawImage(CANVAS, CONTEXT, IMAGE);
        _ALREADY_ROTATED = false;
    }
    CONTEXT.putImageData(imgRotate.imageData, 0, 0);
}


document.getElementById('btnLoad').addEventListener('click', load);
document.getElementById('btnGray').addEventListener('click', grayScale);
document.getElementById('btnGrayMean').addEventListener(
        'click', grayMeanScale);
document.getElementById('btnGrayMedian').addEventListener(
        'click', grayMedianScale);
document.getElementById('btnThresholding').addEventListener(
        'click', thresholdingScale);
document.getElementById('btnGrayCIE').addEventListener(
        'click', grayScaleCIE);
document.getElementById('btnGrayNTSC').addEventListener(
        'click', grayScaleNTSC);
document.getElementById('btnBlurGaussian').addEventListener(
    'click', blurGaussian);
document.getElementById('btnRed').addEventListener('click', redScale);
document.getElementById('btnCyan').addEventListener('click', cyanScale);
document.getElementById('btnGreen').addEventListener('click', greenScale);
document.getElementById('btnMagenta').addEventListener('click', magentaScale);
document.getElementById('btnBlue').addEventListener('click', blueScale);
document.getElementById('btnYellow').addEventListener('click', yellowScale);
document.getElementById('btnBrightness').addEventListener('click', brightness);
document.getElementById('btnContrast').addEventListener('click', contrast);
document.getElementById('btnHorizontalFlip').addEventListener(
        'click', horizontalFlip);
document.getElementById('btnVerticalFlip').addEventListener(
        'click', verticalFlip);
document.getElementById('btnRotate90Degree').addEventListener(
        'click', rotate90Degree);

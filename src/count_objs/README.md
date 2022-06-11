# Running locally

## Coins counter

Algorithm steps:

1. Load image
2. Apply median blur with value 25 of rating
3. Apply gray scale
4. Apply `THRESH_BINARY_INV` to binarize the image
5. Create 3x3 kernel
6. Apply `morphologyEx` to fix some remain noises
7. Apply `distanceTransform` to replace the value of each pixel to the nearest background pixel
8. Convert the last result for `uint8`
9. Apply `findCountours` to detect the objs and `grap_counters` to normalize our array

```
python3 -m coins --filepath ./images/coins3.jpeg --debug
```

Pass `--debug` flag to see the images results.


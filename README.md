# image-worker
Resizing images with Python using Multiprocessing 🐍

## Test

```bash
# Run on a Intel(R) Core(TM) i5-5200U CPU @ 2.20GHz

$ time ./main.py -s=/cdn_squarebreak -d=/cdn2_squarebreak/ -q=80 -si 100 200 300 600
SOURCE: /cdn_squarebreak
DESTINATION : /cdn2_squarebreak/
#####################################
Resizing 762 images in 4 dimensions
TOTAL:  3048 images to create

real	4m34.680s
user	17m12.924s
sys	0m41.028s
```

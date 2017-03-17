[![Build Status](https://travis-ci.org/bourdeau/image-worker.svg?branch=master)](https://travis-ci.org/bourdeau/image-worker)
# image-worker
Resizing images with Python using Multiprocessing 🐍

## Install

```bash
git clone git@github.com:bourdeau/image-worker.git
cd image-worker
virtualenv -p /usr/bin/python3.5 venv --no-site-packages
source venv/bin/activate
pip3 install -r requirements.txt
```

## Run

```bash
# -s = source directory
# -d = destination directory
# -q = quality of the image (0 to 100)
# -si = sizes in pixel

python main.py -s=/home/bob/images -d=/home/bob/images-resized -q=80 -si 100 200 300 600
```


## Performance

```bash
# Run on a Intel(R) Core(TM) i5-5200U CPU @ 2.20GHz

$ time ./main.py -s=/home/bob/images -d=/home/bob/images-resized -q=80 -si 100 200 300 600
SOURCE: /home/bob/images
DESTINATION : /home/bob/images-resized
#####################################
Resizing 762 images in 4 dimensions
TOTAL:  3048 images to create

real	4m34.680s
user	17m12.924s
sys	0m41.028s
```

## Tests
```bash
python3 -m unittest tests/imageworker/worker.py
```

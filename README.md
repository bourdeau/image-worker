[![Build Status](https://travis-ci.org/bourdeau/image-worker.svg?branch=master)](https://travis-ci.org/bourdeau/image-worker)
# image-worker
Resizing images with Python using Multiprocessing with Pillow-SIMD 🐍

## Install

```bash
git clone git@github.com:bourdeau/image-worker.git && cd image-worker
pipenv install
```

In case of troubles compiling limImaging with gcc:
```bash
sudo apt-get install libjpeg-dev zlib1g-dev
sudo apt-get install python3.7-dev
```

## Run

```bash
# -s = source directory
# -d = destination directory
# -q = quality of the image (0 to 100)
# -si = sizes in pixel

pipenv run python main.py -s=/home/bob/images -d=/home/bob/images-resized -q=80 -si 100 200 300 600
```

## Tests
```bash
pipenv run python -m unittest tests/imageworker/worker.py
```

## Performance

```bash
# Run on a Intel(R) Core(TM) i5-5200U CPU @ 2.20GHz

SOURCE: /home/ph/Images-Original
DESTINATION : /home/ph/Images-Resized
#####################################
Resizing 300 images in 4 dimensions
TOTAL:  1200 images to create

real	1m51,182s
user	5m59,305s
sys	0m23,097s
```

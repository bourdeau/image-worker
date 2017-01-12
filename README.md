# image-worker
Resizing images in Python vs PHP 🐍

Resizing 354 images (539.6 Mo) in 6 width (1200, 800, 650, 400, 300, 250)

```bash
$ time php worker.php

real	2m24.383s
user	2m7.660s
sys	0m16.684s
```

```bash
$ time python3 worker.py

real	0m33.092s
user	1m48.532s
sys	0m12.292s
```

![Can't touch this](http://www.temptatz.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/t/0/t003.jpg)

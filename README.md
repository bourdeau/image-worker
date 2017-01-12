# image-worker
Resizing images in Python vs PHP 🐍

## Test
Resizing 354 images (539.6 Mb) in 6 widths (1200px, 800px, 650px, 400px, 300px, 250px)

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

![Can't touch this](http://www.tigerstrypes.com/wp-content/uploads/2016/04/hammer2.jpg)

## Explanations
I wrote almost the same code in both languages and they perform the same (2m20~)

But with Python Multiprocessing with 2 workers then they don't play in the same league.

*Note:* Python LIB seem to do better than PHP Imagick in term of image size.

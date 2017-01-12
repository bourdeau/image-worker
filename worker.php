<?php


class ImageWorker
{
    const CDN_PATH = '/home/ph/Bureau/cdn_squarebreak';
    const NEW_CDN = '/home/ph/Bureau/PHP_cdn_squarebreak';
    const QUALITY = 80;
    const IMAGE_SIZES = [
        1200,
        800,
        650,
        400,
        300,
        250,
    ];

    public function main()
    {
        $files = $this->getDirContents(self::CDN_PATH);
        $images = $this->filterImageFromFiles($files);

        foreach ($images as $image) {
            foreach (self::IMAGE_SIZES as $size) {
                $this->resize($image, $size, self::QUALITY);
            }
        }
    }

    private function getDirContents($dir, &$results = []): array
    {
        $files = scandir($dir);

        foreach($files as $value){
            $path = realpath($dir.DIRECTORY_SEPARATOR.$value);
            if (!is_dir($path)) {
                $results[] = $path;
            } elseif ($value != "." && $value != "..") {
                $this->getDirContents($path, $results);
                $results[] = $path;
            }
        }

        return $results;
    }

    private function filterImageFromFiles(array $files): array
    {
        $images = [];
        foreach ($files as $file) {
            // We filter on original images
            preg_match('/[a-zA-Z0-9]{3}\.jpg/', $file, $matches);

            if (count($matches) > 0) {
                $images[] = $file;
            }
        }

        return $images;
    }

    private function resize(string $imagePath, $width, $quality)
    {
        preg_match('/([a-f0-9]*)\.jpg/', $imagePath, $matches);
        $originalImageName = $matches[1];

        $imagick = new \Imagick($imagePath);
        $imagick->setImageCompression(\Imagick::COMPRESSION_JPEG);
        $imagick->setImageCompressionQuality($quality);
        $imagick->setImageFormat('jpg');

        // Remove metda-data
        $imagick->stripImage();
        // Resize Image
        $imagick->thumbnailImage($width, $width, true);

        $dirPath = self::NEW_CDN.'/'.$width;

        if (!file_exists($dirPath)) {
            mkdir($dirPath, 0777, true);
        }

        $imagick->writeImages($dirPath.'/'.$originalImageName.'.jpg', true);
    }
}

$worker = new ImageWorker();
$worker->main();

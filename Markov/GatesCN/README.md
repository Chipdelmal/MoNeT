
```bash
ffmpeg -start_number 1 -r 24 -f image2 -i map%04d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p 00_Trailer.mp4
```

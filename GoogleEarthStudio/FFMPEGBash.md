ffmpeg -start_number 1 -r 24 -f image2 -s 1920x1080 -i Comoros_%03d.jpeg -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p 00_Trailer.mp4


ffmpeg -i ArtStyleML.mp4 -i palette.png -r 15 -lavfi paletteuse image.gif
ffmpeg -ss 2.6 -i ArtStyleML.mp4 -i palette.png \
-filter_complex "fps=5,scale=500:-1:flags=lanczos[x];[x][1:v]paletteuse" sixthtry.gif


ffmpeg -i ArtStyleML.mp4 ArtStyleML.gif -hide_banner


ffmpeg -ss 2.6 -t 1.3 -i ArtStyleML.mp4 -vf \ fps=15,scale=320:-1:flags=lanczos,palettegen palette.png
ffmpeg -ss 30 -t 3 -i ArtStyleML.mp4 -i palette.png -filter_complex \ "fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif


## Remove black bars
ffmpeg -i MGDrivE.mp4 -vf 'scale=3840:2160:force_original_aspect_ratio=decrease,pad=3840:2160:x=(3840-iw)/2:y=(2160-ih)/2:color=white' MGDrivEPadded.mp4  



ffmpeg -start_number 1 -r 5 -f image2 -s 1920x1080 -i %06d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p 000000.mp4
ffmpeg -ss 2.6 -t 1.3 -i 000000.mp4 -vf \ fps=15,scale=320:-1:flags=lanczos,palettegen palette.png
ffmpeg -i 000000.mp4 -i palette.png -r 5 -lavfi paletteuse image.gif

ffmpeg -ss 2.6 -i 000000.mp4 -i palette.png \
-filter_complex "fps=5,scale=500:-1:flags=lanczos[x];[x][1:v]paletteuse" 000000.gif


ffmpeg -ss 61.0 -t 2.5 -i 000000.mp4 -filter_complex "[0:v] palettegen" palette.png
ffmpeg -ss 61.0 -t 2.5 -i 000000.mp4 -i palette.png -filter_complex "[0:v][1:v] paletteuse" 000000.gif

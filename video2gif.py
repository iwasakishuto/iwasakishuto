# coding: utf-8
# Converts video to gif.
# $ python video2gif.py -v bio.mov  \
#                       -gif bio.gif \
#                       --resize 800,400 \
#                       --loop 0 \
#                       --speed 8
import sys
import cv2
import argparse
from PIL import Image
try:
    from kerasy.utils import toGREEN, toBLUE
except ModuleNotFoundError:
    print(f"I recommend you to install `kerasy` (https://github.com/iwasakishuto/Kerasy)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="video2gif", add_help=True)
    parser.add_argument("-v",   "--video-path", type=str, help="URL of a page you want to create a pdf.", required=True)
    parser.add_argument("-gif", "--gif-path",   type=str, help="Gateway identifier, string name of a gateway")
    parser.add_argument("--resize", type=lambda x:list(map(int, x.split(","))), help="Enter size separated by a comma (width,height)")
    parser.add_argument("--loop",  type=int, default=0, help="How many times gif image loops.")
    parser.add_argument("--speed", type=int, default=5)
    args = parser.parse_args()

    video_path = args.video_path
    gif_path = args.gif_path
    resize = args.resize
    loop = args.loop
    speed = args.speed
    
    # === Load video & Get Video Information ===
    video = cv2.VideoCapture(video_path)
    width  = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps    = video.get(cv2.CAP_PROP_FPS)
    count  = video.get(cv2.CAP_PROP_FRAME_COUNT)
    second = count/fps

    # Arguments check.
    if gif_path is None:
        gif_path = video_path+".gif"
    if resize is None:
        re_width, re_height = (width, height)
    else:
        re_width, re_height = resize

    print(f"""=== VIDEO INFO ===
    * VIDEO_PATH   : {toBLUE(video_path)}
    * FRAME_WIDTH  : {toGREEN(width )} -> {toBLUE(re_width)} [px]
    * FRAME_HEIGHT : {toGREEN(height)} -> {toBLUE(re_height)} [px]
    * FRAME_COUNT  : {toGREEN(count )} [n]
    * FRAME_LENGTH : {toGREEN(second)} [s]
    * FPS          : {toGREEN(fps)} [n/s]
    """)

    print(f"Start converting video -> gif")
    images = []; i = 0
    while True:
        i+=1
        ret, img_bgr = video.read()
        if not ret: 
            sys.stdout.write(f"\r Frame No.{i} ({toGREEN('Finished.')}")
            break
        if i%speed==0:        
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            img_pillow = Image.fromarray(img_rgb).resize(size=(re_width, re_height)).quantize(method=0)
            images.append(img_pillow)
        sys.stdout.write(f"\r Frame No.{i}")
    print(f"Saving gif to {toBLUE(gif_path)}...")
    images[0].save(
        fp=gif_path, 
        format="gif", 
        save_all=True, 
        append_images=images[1:], 
        loop=0
    )
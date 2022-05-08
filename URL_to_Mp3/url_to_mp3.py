# Soundcloud Download (sdcl) https://github.com/flyingrub/scdl
# Youtube Download https://youtube-dl.org/
import os, subprocess
import sys

# rename file after download
def getFileFullpath(music_folder, stdout):
    escaped_chars = ['(',')'] #characters that must be escaped in filepath
    for line in stdout.split('\n'):
        rec = 0
        line = str(line[5:-4])
        file_loc = music_folder
        for word in line.split():
            if(rec == 1):
                if(word[0] in escaped_chars):
                    word = "\\" + word
                if(word[-1] in escaped_chars):
                    word= word[:-1] + "\\" + word[-1];

                file_loc = file_loc + str(word) + "\\ "

            if(word == "Downloading"):
                rec = 1
        if(rec == 1):
            return file_loc[:-2] + ".mp3"

def scdl_convert(line, title, music_folder):
    proc = subprocess.Popen(['scdl',
                             '-c',
                             '--onlymp3',
                             '--path', music_folder,
                             '-l', line[:-1]],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    mp3_fullpath = getFileFullpath(music_folder, \
            str(stdout.decode("utf-8")) + str(stderr.decode("utf-8")))
    if(mp3_fullpath != None):
        rename_cmd= "mv " + mp3_fullpath + " " + music_folder + title + ".mp3"
        print(title + ".mp3")
        os.system(rename_cmd)

def youtube_dl_convert(line, music_folder):
    proc = subprocess.Popen(['youtube-dl',
                             '--ignore-errors',
                             '--output', "\"" + music_folder + "%(title)s.%(ext)s\"",
                             '--extract-audio',
                             '--audio-format', 'mp3',
                             '-v',
                             line[:-1]],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    for line in stdout.decode("utf-8").split('\n'):
        if(line.find("[ffmpeg] Destination:") != -1):
            print(line[42:])


if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print("usage: python3 url_to_mp3.py <url_file.txt> <music_folder>")
        sys.exit(1)
    else:
        filename=sys.argv[1]
        music_folder= sys.argv[2]
        music_url_file= open(filename, "r")

        for line in music_url_file:
            title = line.split('/')[-1][:-1]
            platform = line.split('/')[2]
            if(platform == "soundcloud.com"):
                scdl_convert(line, title, music_folder)
            elif(platform == "www.youtube.com"):
                youtube_dl_convert(line, music_folder)

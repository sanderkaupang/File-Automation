from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging


# SETT PATH UNDER
# bruk \\ som vist her: "C:\\Users\\UserName\\Downloads"
source_dir = "C:\\Users\\sande\\Downloads"
dest_dir_sfx = "C:\\Users\\sande\\Music"
dest_dir_music = "C:\\Users\\sande\\Music"
dest_dir_video = "C:\\Users\\sande\\Videos"
dest_dir_image = "C:\\Users\\sande\\Bilder"
dest_dir_documents = "C:\\Users\\sande\\Documents"

# Bildetypere som er støttet
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# Videotyper som er støttet
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# Audiotyper som er støttet
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# Dokumenttyper som er støttet
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # Hvis filen eksisterer legges et tal bak bilder for og ikke duplisere filnavn
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

#flytter filen dit den skal etter og ha sjekket type på filen
def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    #Klassen vil kjøres når det skjer en endring i "source_dir"/Download folder
    #.upper for og ikke ødelegge filer som bruker store bokstaver i typen
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

#sjekker audio filer
    def check_audio_files(self, entry, name):  
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:  #10Megabytes
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

#sjekker video filer
    def check_video_files(self, entry, name):  
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

#sjekker bilde filer
    def check_image_files(self, entry, name):  
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

#sjekker dokument filer
    def check_document_files(self, entry, name):  
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")


# Ser etter endring i source_dir
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
    # Sander Kaupang 2022

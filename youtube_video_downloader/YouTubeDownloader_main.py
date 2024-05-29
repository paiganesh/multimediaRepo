from ytube import YouTube

utube_URL = 'https://www.youtube.com/playlist?list=PLR2yPNIFMlL9UUF6-syrVrNaRwHVJofZE'
download_dir = "G:\\Library\\Java"

utube_URL = 'https://www.youtube.com/watch?v=TU3Vq8MkNHk'
download_dir = "G:\\Library\\Java\\Spring Boot Tutorials - Code Java"


YouTube().download_videos(utube_URL, dest_dir=download_dir, playlist_autonumber=False)

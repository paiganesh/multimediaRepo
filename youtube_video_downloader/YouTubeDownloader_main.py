from ytube import YouTube

utube_URL = 'https://www.youtube.com/playlist?list=ABCDPQR'  # specify a valid playlist URL
download_dir = "D:\\Download_Dir"

utube_URL = 'https://www.youtube.com/watch?v=ABCDPQR'        # specify a valid video URL
download_dir = "D:\\Download_Dir"


YouTube().download_videos(utube_URL, dest_dir=download_dir, playlist_autonumber=False)

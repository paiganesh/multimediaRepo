from pytube import Playlist, YouTube as YT
import os

class YouTube:
    def __download_playlist(self, playlist_URL, dest_dir, playlist_autonumber=False, resolution=None):
        prefix = None
        
        playlist = Playlist(playlist_URL)
        print('Number of videos in playlist: %s' % len(playlist.video_urls))
        
        playlist_dir = "%s - %s" % (playlist.title, playlist.owner)
        dest_dir = os.path.join(dest_dir, playlist_dir)
        
        if os.path.exists(dest_dir): 
            if input(f'Directory "{dest_dir}" already exists. Do you want to overwrite? (y/n)').lower().startswith('n'):
                return
        else:
            os.mkdir(dest_dir)
        
        slno = 0
        failure_log = []
        
        for video_url in playlist.video_urls._elements:
            slno += 1
            print('*' * 50 + "\n" + str(slno) + '. Downloading ' + video_url)
            if playlist_autonumber: prefix = f'{slno}. '
            state = self.__download_video(video_url, dest_dir, printmsg=False, prefix=prefix, resolution=resolution)
            if state != None: failure_log.append(state)
    
        def print_failure_log(failure_log):
            print("\n\n" + "=" * 50 + "\n>>> Download Failure Report <<<")
            for i, video in enumerate(failure_log, start=1):
                if video[2] == None: #if prefix is None
                    print(f'{i}. {video[0]}  ==>  {video[1]}')
                else:
                    print(f'{i}. {video[0]}  ==>  {video[2]}. {video[1]}')
            print("="*50)
            
        failure_log2 = []
        if len(failure_log) > 0:
            print_failure_log(failure_log)
            
            print("\n--- Retrying failed downloads... ---")
            for video_url, title, prefix in failure_log:
                state = self.__download_video(video_url, dest_dir, printmsg=False, prefix=prefix, resolution=resolution)
                if state != None: failure_log2.append(state)
        
        if len(failure_log2) == 0:
            print("All downloads completed.")
        else:
            print_failure_log(failure_log2)
            
    
    def __download_video(self, video_url, dest_dir, printmsg=True, prefix=None, resolution=None):
            resolution_values = ['1080p', '720p', '480p', '360p', None]
            if resolution not in resolution_values:
                print(f"Invalid resolution {resolution} found. Possible values {resolution_values[:4]}. Aborting.")
                return
            
            if printmsg:
                if not os.path.exists(dest_dir): 
                    print(f"Destination directory '{dest_dir}' does not exist. Download aborting.")
                    return
                print('Downloading ' + video_url)
                
            video = YT(video_url, use_oauth=False, allow_oauth_cache=True)
            print("Title: " + video.title)
            stream = None
            try:
                if resolution != None:
                    stream = video.streams.filter(progressive=True, res=resolution).first()
                    if stream == None:
                        print(f"Video for selected resolution {resolution} not found. Trying for other available resolutions.")
                
                if stream == None:
                    resolution = resolution_values[0]
                    stream = video.streams.filter(progressive=True, res=resolution).first()
                if stream == None:
                    resolution = resolution_values[1]
                    stream = video.streams.filter(progressive=True, res=resolution).first()
                if stream == None:
                    resolution = resolution_values[2]
                    stream = video.streams.filter(progressive=True, res=resolution).first()
                if stream == None:
                    resolution = resolution_values[3]
                    stream = video.streams.filter(progressive=True, res=resolution).first()
                
                if stream == None:
                    print('No suitable resolution found.')
                else:
                    print('Download Resolution:', resolution, "\nDownloading...", end=" ")
                    stream.download(output_path=dest_dir, skip_existing=True, filename_prefix=prefix, max_retries=1)
                    print('Done.')
            except Exception as e:
                print('\nException:', e)
                return (video_url, video.title, prefix)
    
    
    def download_videos(self, utube_URL:str, dest_dir:str, playlist_autonumber:bool=False, resolution='720p'):
        """
        Downloads YouTube Videos or Playlist videos from *utube_URL* into the *dest_dir* directory.

        Parameters
        ----------
        utube_URL : str
            Video or Playlist URL.
        dest_dir : str
            Location where downloaded video will be stored. In case of playlist, a new directory will be created in *dest_dir* with the name '<Playlist Title - Owner>' 
        playlist_autonumber : bool, optional
            If True, serial number will be prefixed to the downloaded videos in the order of playlist. The default is False.
        resolution : str, optional
            Resolution of the video to be downloaded. Possible values are 1080p, 720p, 480p or 360p. The default is 720p.

        Returns
        -------
        None

        """
        def is_connected():
          import socket
          try:
            socket.create_connection((socket.gethostbyname("one.one.one.one"), 80), 2).close()
            return True
          except Exception:
             pass
          return False
      
        if not is_connected():
            print("No Internet!!!. Check your Internet connection and retry.")
            return
        
        import re
        video_pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        video_regex = re.compile(video_pattern)
        if video_regex.search(utube_URL):
            print(f"[{utube_URL}] is a Video URL\n")
            self.__download_video(utube_URL, dest_dir=dest_dir, resolution=resolution)
        else:
            print(f"[{utube_URL}] is a Playlist URL\n")
            self.__download_playlist(utube_URL, dest_dir=dest_dir, playlist_autonumber=playlist_autonumber, resolution=resolution)

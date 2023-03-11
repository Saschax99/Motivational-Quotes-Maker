from shorts_generator import ShortsFetcher, YoutubeShortsUploader
import config

text_title = '''
  ______ _                               _______                                                
 / _____) |                  _          (_______)                                _              
( (____ | |__   ___   ____ _| |_  ___    _   ___ _____ ____  _____  ____ _____ _| |_ ___   ____ 
 \____ \|  _ \ / _ \ / ___|_   _)/___)  | | (_  | ___ |  _ \| ___ |/ ___|____ (_   _) _ \ / ___)
 _____) ) | | | |_| | |     | |_|___ |  | |___) | ____| | | | ____| |   / ___ | | || |_| | |    
(______/|_| |_|\___/|_|      \__|___/    \_____/|_____)_| |_|_____)_|   \_____|  \__)___/|_|
'''


if __name__ == '__main__':
    print(text_title)
    print("Shorts Generator - By Saschax", "\nThe program automatically searches for videos to download and edit the videos with music that are in the /songs directory. These videos can then be uploaded to Youtube/Instagram/TikTok. Using pexels.com as reference")
    skip = str(input("just upload files? [yes/no]"))
    if skip.lower() == "no":
        keyword = str(input("insert keyword to search [default=nature]: "))
        type = int(input("downloading and edit by scratch = 1 | downloading by file in path = 2: "))
        fetcher = ShortsFetcher()
        fetcher.set_keyword(keyword)
        if type == 1:
            fetcher.get_browser()
            video_links = fetcher.get_video_links_from_keyword()
            print(video_links)
            fetcher.close()
        fetcher.download_video_series()


    amount = str(input("amount of videos to upload [new account limit=10]: "))
    try:
        user = config.USER
        password = config.PASSWORD
    except:
        user = str(input("username of youtube: "))
        password = str(input("password of youtube: "))
    ytUploader = YoutubeShortsUploader(amount, user, password)
    ytUploader.get_browser()
    ytUploader.upload_video_series()
    
    
    # print(video_links)

    # download all videos
    # download_video_series(video_links)
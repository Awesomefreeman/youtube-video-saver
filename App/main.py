import api
import helper


def main():
    favorites = api.Request().favorites()
    favorites_video = api.Request(playlist_id=favorites).get_video_id()
    helper.downloader("favorites", favorites_video)
    request = api.Request()
    for items in request.my_playlists().items():
        video_id = api.Request(playlist_id=items[1]).get_video_id()
        helper.downloader(items[0], video_id)


if __name__ == '__main__':
    main()

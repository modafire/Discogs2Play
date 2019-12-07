import discogs_client
from gmusicapi import Musicmanager
from gmusicapi import Mobileclient

d = discogs_client.Client('ExampleApplication/0.1', user_token = 'KPqrfKmxmnGoqyTHVjoVxcBYumJhRCDbmEsVPnqz')

api = Mobileclient()
mm = Musicmanager()
mm.login()
api.__init__(debug_logging=True, validate=True, verify_ssl=True)
# credentials below
api.oauth_login('000000000', "C:/users/file")

def trackdict(artist, track, year):
    #Puts track info into a dictionary
    dicx = {'artist': artist , 'track': track , 'year': year}
    return dicx

########################################
#         PROGRAM INPUTS               #
########################################
label_name = 'Altered reality records'
playlist_name = 'AutoARR'
how_many_releases = 0 #Leave at 0 for all release - Limit this for labels with lots of releases!
how_many_tracks = 20 
descending = True #True means reverse chronological order, eg. recent first
#======================================#

#Retrieve label from discogs search
results = d.search(label_name, type='label')
label = results[0]
if how_many_releases == 0:
    label_releases = label.releases
else:
    label_releases = [label.releases[n] for n in range(how_many_releases)]


#Creates lists of IDs, years, artists, tracklists and track artists (if compilations) for each album

release_ids = [release.id for release in label_releases]
release_tracklists_pre = [d.release(ID).tracklist for i, ID in enumerate(release_ids)]

# These are the key outputs
release_years= [release.year for release in label_releases]
release_artists = [release.artists[0].name for release in label_releases]
release_tracklists = [[track.title for j, track in enumerate(release_tracklists_pre[i])] for i, release in enumerate(release_tracklists_pre)]

track_artists = []
for i, album in enumerate(release_tracklists_pre):
    track_artists_album = []
    for track in release_tracklists_pre[i]:
        try:
            track_artists_album.append(track.artists[0].name)
        except:
            track_artists_album.append(release_artists[i])
    track_artists.append(track_artists_album)

# This creates a dictionary for each individual track, then puts them into a list
release_dicts = []
for i in range(len(release_ids)):
    year = release_years[i]
    for j in range(len(release_tracklists[i])):
        track = release_tracklists[i][j]

        try:
            artist = track_artists[i][j]
        except:
            artist = release_artists[i]

        release_dicts.append(trackdict(artist, track, year))

# Sorts the list
if descending ==True:
    release_dicts_sorted = (sorted(release_dicts, key=lambda i: i['year'], reverse=True))
else:
    release_dicts_sorted = (sorted(release_dicts, key=lambda i: i['year']))


def makeplaylist(track_dicts, playlist_name='Autoplaylist', size=20):
    playlist_id = api.create_playlist(playlist_name)
    shortlist = track_dicts[0:size]
    for i, dic in enumerate(shortlist):
        for j, name in enumerate(dic.values()):
            if j == 0:
                artist = name
                if artist[-1]==')':
                    artist = artist[0:-4]
            elif j==1:
                title = name
            else:
                play_search = api.search(title + ' ' + artist)
                print(title + ' ' + artist)
                try:
                    store_id=play_search['song_hits'][0]['track']['storeId']
                    api.add_songs_to_playlist(playlist_id, store_id)

                except:
                    print(artist + ' - ' + title + ' failed to add')
                    

makeplaylist(release_dicts_sorted, playlist_name, how_many_tracks)

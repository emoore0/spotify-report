import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credentials
import matplotlib.pyplot as plt


class Spotireport:

	track_table = ''
	artist_table = ''
	track_artist_ids = []
	term = ''
	#def __init__(self):
		
	def authenticate(self,scope=None):
		authentication = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials.client_id, client_secret= credentials.client_secret, redirect_uri=credentials.redirect_url, scope=scope))

		return authentication


	def top_tracks(self,time_range,number):
		scope = "user-top-read"
		sp = self.authenticate(scope)
		results = sp.current_user_top_tracks(number,time_range=time_range)
		#print(results['items'])
		self.term += str(time_range)
		album = []
		release_date = []
		artist = []
		track = []
		
		for idx, item in enumerate(results['items']):
			album.append(str(results['items'][idx]['album']['name']))
			release_date.append(str(results['items'][idx]['album']['release_date']))
			artist.append(str(results['items'][idx]['album']['artists'][0]['name']))
			track.append(str(results['items'][idx]['name']))
			self.track_artist_ids.append(results['items'][idx]['artists'][0]['id'])
		#return results['items'][0]

		if time_range == 'short_term':
			self.track_table += f'Your top {number} most listened to tracks on Spotify in the last 4 weeks are ready!\n'
		elif time_range == 'medium_term':
			self.track_table += f'Your top {number} most listened to tracks on Spotify in the last 6 months are ready!\n'
		elif time_range == 'long_term':
			self.track_table += f'Your top {number} most listened to tracks on Spotify over the last few years are ready!\n'
		self.track_table += '\n'

		numbers = []
		for x in range(number):
			numbers.append(str(x+1))

		lnumber = max(numbers,key=len)
		count = f'|No.'+ ' '*(len(lnumber)-len('No.'))+' '
		self.track_table += count

		ltrack = max(track,key=len)
		tracks = f'|Track' + ' '*(len(ltrack)-len('Track'))+'  '
		self.track_table += tracks

		lalbum = max(album,key=len)
		albums = f'|Album' + ' '*(len(lalbum)-len('Album'))+'  '
		self.track_table += albums

		lartist = max(artist,key=len)
		artists = f'|Artist' + ' '*(len(lartist)-len('Artist'))+ '  '
		self.track_table += artists

		ldate = max(release_date,key=len)
		date = f'|Release Date' + ' '*(len(ldate)-len('Release Date')) + '|'
		self.track_table += date
		self.track_table += '\n'
		self.track_table += '-'*(len(count)+len(tracks)+len(albums)+len(artists)+len(date))
		self.track_table += '\n'
		for z,a,b,c,d in zip(numbers,track,album,artist,release_date):
			self.track_table += f'|{z}. '
			self.track_table += ' '*(len(count)-len(z)-3)+f'| {a} '
			self.track_table += ' '*(len(tracks)-len(a)-3) + f'|{b} ' 
			self.track_table += ' '*(len(albums)-len(b)-2) + f'|{c} '
			self.track_table += ' '*(len(artists)-len(c)-2) + f'|{d} '+' '*(len(date)-len(ldate)-3) + '|'
			self.track_table += f'\n'
			
		return self.track_table

	def top_artists(self,time_range,number):
		scope = "user-top-read"
		sp = self.authenticate(scope)
		results = sp.current_user_top_artists(number,time_range=time_range)
		#print(results['items'][0]['genres'][0])
		genre = []
		artist = []
	
		for idx, item in enumerate(results['items']):
			artist.append(results['items'][idx]['name'])
			#genre.append(results['items'][idx]['genres'][0])
			genre_list = results['items'][idx]['genres'][0].split()
			if 'hip' in genre_list:
				genre.append('hip hop')
			elif 'rap' in genre_list:
				genre.append('rap')
			else:
				genre.append(results['items'][idx]['genres'][0])



		if time_range == 'short_term':
			self.artist_table += f'Your top {number} most listened to artists on Spotify in the last 4 weeks are ready!\n'
		elif time_range == 'medium_term':
			self.artist_table += f'Your top {number} most listened to artists on Spotify in the last 6 months are ready!\n'
		elif time_range == 'long_term':
			self.artist_table += f'Your top {number} most listened to artists on Spotify over the last few years are ready!\n'
		self.artist_table += '\n'

		numbers = []
		for x in range(number):
			numbers.append(str(x+1))
			
		lnumber = max(numbers,key=len)
		count = f'|No.'+ ' '*(len(lnumber)-len('No.'))+' '
		self.artist_table += count

		lartist = max(artist,key=len)
		artists = f'|Artist' + ' '*(len(lartist)-len('Artist'))+ '  '
		self.artist_table += artists

		lgenre = max(genre,key=len)
		genres = f'|Genre' + ' '*(len(lgenre)-len('Genre'))+ '  '
		self.artist_table += genres
		self.artist_table += '\n'
		self.artist_table += '-'*(len(count)+len(artists)+len(genres))
		self.artist_table += '\n'
		for a,b,c in zip(numbers,artist,genre):
			self.artist_table += f'|{a}. '
			self.artist_table += f' '*(len(count)-len(a)-3) + f'|{b} '
			self.artist_table += f' '*(len(artists)-len(b)-2) + f'|{c} '
			self.artist_table += f'\n'


		return self.artist_table

	def track_analysis(self):
		genres = dict()
		sp = self.authenticate()
		for i in self.track_artist_ids:
			results = sp.artist(i)
			#return sp.artist(self.track_artist_ids[25])['genres'] == []
			if results['genres'] == [] :
				genres['unavailable'] = genres.get('unavailable',0) + 1
			elif 'hip' in results['genres'][0]:
				genres['hip hop'] = genres.get('hip hop',0) + 1
			elif 'rap' in results['genres'][0]:
				genres['rap'] = genres.get('rap',0) + 1
			else:
				genres[results['genres'][0]] = genres.get(results['genres'][0],0) + 1
		
		total = sum(genres.values())
		for k,v in genres.items():
			genres[k] = (v/total)*100
		sorted_genres = dict(sorted(genres.items(), key=lambda item: item[1], reverse=True))
	#-----------------------------------------------------IMPORTANT!--------------------------------------------------
 	#A lambda function in Python is a compact, anonymous function defined using the lambda keyword. 
 	#It's designed for short, simple tasks and consists of input parameters and a single expression.
 	# For example, lambda x: x * 2 doubles a value x. Lambda functions are often used with functions like sorted() to define custom sorting keys. 
 	#In sorted(items, key=lambda item: item[1]), it sorts items based on the second element of each item.
 	#-----------------------------------------------------IMPORTANT!--------------------------------------------------
		genre_names = list(sorted_genres.keys())
		genre_percentages = list(sorted_genres.values())
		plt.figure(figsize=(10,6))
		plt.pie(genre_percentages,labels = genre_names)
		#plt.xlabel('Genres')
		#plt.ylabel('Percentage (%)')
		if self.term == 'short_term':
			plt.title('Genre Distribution in the Last 4 Weeks')
		elif self.term == 'medium_term':
			plt.title('Genre Distribution in the Last 6 Months')
		elif self.term == 'long_term':
			plt.title('Genre Distribution in the Last Several Years')

		plt.tight_layout()
		plt.show()
		#return sorted_genres

	def compare(self,time_range1,time_range2):
		comp_report = ''
		scope = "user-top-read"
		sp = self.authenticate(scope)
		results1 = sp.current_user_top_tracks(50,time_range=time_range1)
		results2 = sp.current_user_top_tracks(50,time_range=time_range2)
		track_id_1 = []
		track_id_2 = []
		for idx, item in enumerate(results1['items']):
			track_id_1.append(results1['items'][idx]['artists'][0]['id'])

		for idx, item in enumerate(results2['items']):
			track_id_2.append(results2['items'][idx]['artists'][0]['id'])

		genres1 = dict()
		genres2 = dict()

		sp = self.authenticate()
		for i in track_id_1:
			results_a = sp.artist(i)
			if results_a['genres'] == []:
				genres1['unavailable'] = genres1.get('unavailable',0) + 1
			elif 'hip' in results_a['genres'][0]:
				genres1['hip hop'] = genres1.get('hip hop',0) + 1
			elif 'rap' in results_a['genres'][0]:
				genres1['rap'] = genres1.get('rap',0) + 1
			else:
				genres1[results_a['genres'][0]] = genres1.get(results_a['genres'][0],0) + 1

		for i in track_id_2:
			results_b = sp.artist(i)
			if results_b['genres'] == []:
				genres2['unavailable'] = genres2.get('unavailable',0) + 1
			elif 'hip' in results_b['genres'][0]:
				genres2['hip hop'] = genres2.get('hip hop',0) + 1
			elif 'rap' in results_b['genres'][0]:
				genres2['rap'] = genres2.get('rap',0) + 1
			else:
				genres2[results_b['genres'][0]] = genres2.get(results_b['genres'][0],0) + 1
		
		comp_report += 'Your Comparison Report is ready\n'
		if time_range1 == 'short_term':
			comp_report += f'Last 4 Weeks'
		elif time_range1 == 'medium_term':
			comp_report += f'Last 6 Months'
		elif time_range1 == 'long_term':
			comp_report += f'Last Several Years'
		comp_report += ' VS '
		if time_range2 == 'short_term':
			frame = 'Last 4 Weeks'
			comp_report += f'{frame}'
		elif time_range2 == 'medium_term':
			frame = 'Last 6 Months'
			comp_report += f'{frame}'
		elif time_range2 == 'long_term':
			frame = 'Last Several Years'
			comp_report += f'{frame}'

		most_listened1 = max(genres1,key = lambda x:genres1[x])
		most_listened2 = max(genres2,key = lambda x:genres2[x])




		return comp_report

x = Spotireport()
#x.top_tracks('short_term',10)
#print(x.top_artists('short_term',10))
#x.track_analysis()
#print(x.compare('short_term','medium_term'))

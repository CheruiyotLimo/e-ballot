import googlemaps

API_KEY = 'AIzaSyDejfUwd965JEoSsBgKOZVrTunbxkdwfzE'

map_client = googlemaps.Client(API_KEY)

map_client.geocode()
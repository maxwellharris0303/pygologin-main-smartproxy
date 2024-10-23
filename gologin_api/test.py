from gologin import GoLogin


gl = GoLogin({
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWU2ODA4OGJlYmQ0ZGI5ZGVlODU2MDgiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NWU2ODI5YWJlYmQ0ZGI5ZGVlODk4YjcifQ.lySpRkH2TURQAV1SrxTbqcJQh9yMpDNOIVIBba7jPcU",
	})

profile_id = gl.create({
    "name": 'profile_mac',
    "os": 'mac',
    "navigator": {
        "language": 'en-US',
        "userAgent": 'random', # Your userAgent (if you don't want to change, leave it at 'random')
        "resolution": '1024x768', # Your resolution (if you want a random resolution - set it to 'random')
        "platform": 'mac',
    },
    'proxyEnabled': True, # Specify 'false' if not using proxy
    'proxy': {
        'mode': 'http',
        'autoProxyRegion': 'us' ,
        'host': 'us.smartproxy.com',
        'port': '12323',
        'username': 'user-spo8thgt4t-sessionduration-30',
        'password': '7=52dyzzl8FOMfVafk',
    },
    "webRTC": {
        "mode": "alerted",
        "enabled": True,
    },
})

print('profile id=', profile_id)

# gl.update({
#     "id": 'yU0Pr0f1leiD',
#     "name": 'profile_mac2',
# });

profile = gl.getProfile(profile_id)

print('new profile name=', profile.get("name"))

# gl.delete('yU0Pr0f1leiD')

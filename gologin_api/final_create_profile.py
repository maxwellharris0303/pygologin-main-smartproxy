import create_profile
import update_fingerprint_multiple_profiles
import add_proxy_to_profile
import start_profile
import stop_profile

profile_id = create_profile.create()
status_fingerprint = update_fingerprint_multiple_profiles.update_fingerprint(profile_id)
print(status_fingerprint)
proxy_port = add_proxy_to_profile.add_proxy(profile_id)
print(f"Proxy port: {proxy_port}")

start_profile.start(profile_id)
stop_profile.stop(profile_id)


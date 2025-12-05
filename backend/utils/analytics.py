import os
from posthog import Posthog

# Initialize PostHog client
posthog = Posthog(
    project_api_key=os.getenv('POSTHOG_API_KEY', ''),
    host=os.getenv('POSTHOG_HOST', 'https://eu.i.posthog.com')
)

def track_event(user_id: str, event_name: str, properties: dict = None):
    '''Track analytics event'''
    if not posthog.api_key:
        return
    
    posthog.capture(
        distinct_id=user_id,
        event=event_name,
        properties=properties or {}
    )

def identify_user(user_id: str, email: str, properties: dict = None):
    '''Set user properties'''
    if not posthog.api_key:
        return
    
    user_props = {'email': email}
    if properties:
        user_props.update(properties)
    
    posthog.identify(
        distinct_id=user_id,
        properties=user_props
    )

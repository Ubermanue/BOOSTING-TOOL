import requests, json, time, uuid, base64, re

def AutoReact():
    def Reaction(actor_id: str, post_id: str, comment_id: str, react: str, token: str):
        rui = requests.Session()
        feedback_id = str(base64.b64encode(('feedback:{}'.format(comment_id)).encode('utf-8')).decode('utf-8'))
        var = {
            "input": {
                "feedback_referrer": "native_newsfeed",
                "tracking": [None],
                "feedback_id": feedback_id,
                "client_mutation_id": str(uuid.uuid4()),
                "nectar_module": "newsfeed_ufi",
                "feedback_source": "native_newsfeed",
                "feedback_reaction_id": react,
                "actor_id": actor_id,
                "action_timestamp": str(time.time())[:10]
            }
        }
        data = {
            'access_token': token,
            'method': 'post',
            'pretty': False,
            'format': 'json',
            'server_timestamps': True,
            'locale': 'id_ID',
            'fb_api_req_friendly_name': 'ViewerReactionsMutation',
            'fb_api_caller_class': 'graphservice',
            'client_doc_id': '2857784093518205785115255697',
            'variables': json.dumps(var),
            'fb_api_analytics_tags': ["GraphServices"],
            'client_trace_id': str(uuid.uuid4())
        }

        pos = rui.post('https://graph.facebook.com/graphql', data=data).json()
        try:
            if react == '0':
                print(f"「Success」» Removed reaction from {actor_id} on {comment_id}")
                return True
            elif react in str(pos):
                print(f"「Success」» Reacted with » {actor_id} to {comment_id}")
                return True
            else:
                print(f"「Failed」» Reacted with » {actor_id} to {comment_id}")
                return False
        except Exception:
            print('Reaction failed due to an error.')
            return False

    def choose_reaction():
        print("Please choose the reaction you want to use.\n")
        reactions = {
            '1': 'Like',
            '2': 'Love',
            '3': 'Haha',
            '4': 'Wow',
            '5': 'Care',
            '6': 'Sad',
            '7': 'Angry',
            '8': 'Remove Reaction'
        }
        for key, value in reactions.items():
            print(f"     「{key}」 {value}")
        
        rec = input('Choose a reaction: ')
        reaction_ids = {
            '1': '1635855486666999',  # Like
            '2': '1678524932434102',  # Love
            '3': '115940658764963',   # Haha
            '4': '478547315650144',   # Wow
            '5': '613557422527858',   # Care
            '6': '908563459236466',   # Sad
            '7': '444813342392137',   # Angry
            '8': '0'                 # Remove Reaction
        }
        return reaction_ids.get(rec)

    def linktradio(comment_link: str) -> tuple:
        # Extract post ID and comment ID from the Facebook comment link
        match = re.search(r'/posts/(\w+).*?comment_id=(\d+)', comment_link)
        if match:
            return match.group(1), match.group(2)
        print("Invalid comment link or format")
        return None, None

    def get_ids_tokens(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]

    actor_ids = get_ids_tokens('/sdcard/Test/tokaid.txt')
    tokens = get_ids_tokens('/sdcard/Test/toka.txt')

    comment_link = input('Enter the Facebook comment link: ')
    post_id, comment_id = linktradio(comment_link)
    
    if not comment_id:
        return

    react = choose_reaction()
    if react == '0':
        remove_count = int(input("How many reactions do you want to remove? "))
        reactions_removed = 0
        for actor_id, token in zip(actor_ids, tokens):
            if reactions_removed >= remove_count:
                break
            success = Reaction(actor_id=actor_id, post_id=post_id, comment_id=comment_id, react='0', token=token)
            if success:
                reactions_removed += 1
        print(f"All {reactions_removed} reactions have been successfully removed! You're awesome!")
    elif react:
        react_count = int(input("How many reactions do you want to send? "))
        reactions_sent = 0
        for actor_id, token in zip(actor_ids, tokens):
            if reactions_sent >= react_count:
                break
            success = Reaction(actor_id=actor_id, post_id=post_id, comment_id=comment_id, react=react, token=token)
            if success:
                reactions_sent += 1
        print(f"All {reactions_sent} reactions have been successfully sent! You're awesome!")
    else:
        print('Invalid reaction option.')

# Run the AutoReact script
AutoReact()
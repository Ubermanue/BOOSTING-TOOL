import requests
import re

def Video_Extractid(url):
    # Example implementation of extracting media ID from a URL
    # Adjust the regex according to the expected format of the media URL
    match = re.search(r'/(videos|photos)/(\d+)', url)
    return match.group(2) if match else None

def load_data(filepath):
    # Load access tokens from a file
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        return []

def has_reacted(media_id, access_token):
    # Dummy implementation; replace with actual logic to check if the user has reacted
    return False

def perform_reaction_media(url, reaction_type, num_reactions):
    media_id = Video_Extractid(url)  # Function to extract the media ID (photo or video)
    if not media_id:
        print("[ERROR] Invalid URL or unable to extract media ID.")
        return

    access_tokens = load_data('/sdcard/Test/toka.txt')  # Load access tokens
    
    reactions_count = 0

    for access_token in access_tokens:
        if access_token.startswith("EA") or access_token.startswith("EAA"):
            try:
                # Reacting with personal account access token
                if not has_reacted(media_id, access_token):
                    url = f'https://graph.facebook.com/v18.0/{media_id}/reactions'
                    params = {'access_token': access_token, 'type': reaction_type}
                    response = requests.post(url, params=params)

                    if response.status_code == 200:
                        reactions_count += 1
                        print(f"[SUCCESS] Successfully reacted with '{reaction_type}' on media ID '{media_id}'. Response: {response.json()}")
                        if reactions_count >= num_reactions:
                            print(f"Reached the limit of {num_reactions} reactions.")
                            return
                    else:
                        print(f"[ERROR] Failed to post reaction on media ID '{media_id}'. Response: {response.json()}")
            except requests.exceptions.RequestException as error:
                print(f"[EXCEPTION] An error occurred during the request: {error}")
            except Exception as e:
                print(f"[ERROR] An unexpected error occurred: {e}")

    print(f"Total reactions sent: {reactions_count}")

# Example usage
if __name__ == "__main__":
    url = input("Enter the media URL: ")
    reaction_type = input("Enter the reaction type (like, love, wow, etc.): ")
    num_reactions = int(input("Enter the number of reactions to perform: "))
    
    perform_reaction_media(url, reaction_type, num_reactions)
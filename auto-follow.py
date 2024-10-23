import requests

def get_ids_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def get_profile_id(profile_link, access_token):
    # Check if it's a vanity URL or a numeric ID
    if profile_link.isdigit():
        return profile_link  # Already a numeric ID

    url = f'https://graph.facebook.com/v19.0/{profile_link}'
    params = {'access_token': access_token, 'fields': 'id'}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get('id', 'Unknown ID')
    return 'Unknown ID'

def get_profile_username(profile_id, access_token):
    url = f'https://graph.facebook.com/v19.0/{profile_id}'
    params = {'access_token': access_token, 'fields': 'name'}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get('name', 'Unknown Profile')
    return 'Unknown Profile'

def follow_facebook_profile():
    access_tokens = get_ids_tokens('/sdcard/Test/toka.txt')

    profile_link = input('Enter the Facebook profile link: ')
    
    # Use the first token to resolve the profile link to an ID
    profile_id = get_profile_id(profile_link.split('/')[-1], access_tokens[0])
    
    # Ask the user how many followers they want to add
    num_followers = int(input('How many followers do you want to add? '))
    
    def follow_profile(profile_id, access_token):
        try:
            url = f'https://graph.facebook.com/v19.0/{profile_id}/subscribers'
            params = {'access_token': access_token}
            response = requests.post(url, params=params)
            
            if response.status_code == 200:
                return True
            return False
        except requests.exceptions.RequestException:
            return False

    follow_count = 0

    for i, access_token in enumerate(access_tokens):
        if follow_count >= num_followers:
            break  # Stop if we've added the requested number of followers
        
        profile_name = get_profile_username(profile_id, access_token)
        
        if follow_profile(profile_id, access_token):
            print(f"Success: Followed the profile '{profile_name}' with ID {i + 1}")
            follow_count += 1
        else:
            print(f"Failed: Could not follow the profile '{profile_name}' with ID {i + 1}")

    print(f"Successfully followed {follow_count} profiles out of {num_followers} requested.")

def remove_facebook_follower():
    access_tokens = get_ids_tokens('/sdcard/Test/toka.txt')

    profile_link = input('Enter the Facebook profile link to remove: ')
    
    # Use the first token to resolve the profile link to an ID
    profile_id = get_profile_id(profile_link.split('/')[-1], access_tokens[0])

    def remove_follower(profile_id, access_token):
        try:
            url = f'https://graph.facebook.com/v19.0/{profile_id}/subscribers'
            params = {'access_token': access_token}
            response = requests.delete(url, params=params)
            
            if response.status_code == 200:
                return True
            return False
        except requests.exceptions.RequestException:
            return False

    remove_count = 0

    for i, access_token in enumerate(access_tokens):
        profile_name = get_profile_username(profile_id, access_token)
        
        if remove_follower(profile_id, access_token):
            print(f"Success: Removed the follower from profile '{profile_name}' with ID {i + 1}")
            remove_count += 1
        else:
            print(f"Failed: Could not remove the follower from profile '{profile_name}' with ID {i + 1}")

    print(f"Successfully removed {remove_count} followers.")

def main_menu():
    while True:
        print("Menu:")
        print("1. Follow a Facebook profile")
        print("2. Remove a follower from a Facebook profile")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            follow_facebook_profile()
        elif choice == '2':
            remove_facebook_follower()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

# Start the menu
main_menu()

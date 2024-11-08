import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor


class DirectoryBruteforce:
    def __init__(self):
        self.url = None
        self.wordlist = None
        self.projectname = None
        self.Thread_count = None
        self.user_choice = None
        self.seconds = None

    def url_validations(self):
        while True:
            self.url = str(input("Enter the url to fuzz : "))

            try:
                response = requests.get(self.url)
                if response.status_code == 200:
                    break
            except requests.exceptions.ConnectionError as e:
                print(f'Invalid URL {e}')

            except requests.exceptions.InvalidURL as e:
                print(f'Invalid URL {e}')

            except requests.exceptions.MissingSchema as e:
                print(f'Invalid URL {e}')

        self.projectname = str(input("Enter the project title : ")).strip()

    def validating_wordlist(self):
        while True:
            self.wordlist = input("Specify the wordlist : ")
            if os.path.exists(self.wordlist):
                break
            else:
                print("FileNotFound")

    def Thread_Count_func(self):
        while True:
            try:
                self.Thread_count = int(input("Enter the Number of Thread Count (between 0 - 9): "))
                # Check if Thread_count is within the valid range
                if (self.Thread_count >= 0 and self.Thread_count <= 9):
                    break  # Exit the loop if input is valid
                else:
                    print("Invalid Thread Count, it must be between 0 and 9.")

            except ValueError:
                print("Invalid input. Please enter an integer.")

    def attack(self, fuzz):

        adding = str(self.url + fuzz.strip())
        requesting = requests.get(adding)
        try:
            if requesting.status_code == 200:
                print(adding)
                with open(f"200_{self.projectname}{1}.txt", "a") as file:
                    file.write(adding + "\n")
                    print(adding)
            elif requesting.status_code == 403:
                print(adding)
                with open(f"403_{self.projectname}.txt", "a") as file:
                    file.write(adding + "\n")
            elif requesting.status_code == 500:
                print(adding)
                with open(f"500_{self.projectname}.txt", "a") as file:
                    file.write(adding + "\n")
            elif requesting.status_code == 429:
                print("Error 429: Too many requests have been made in a short period of time \n(sleeping for 60sec.")
                time.sleep(60)
                if requesting.status_code == 429:
                    print("The Server Not yet cool down")
                    print("Do you want to 'exit' or 'extend' the time to sleep for further attack")
                    DirectoryBruteforce.trail(self)
                else:
                    pass
            else:
                pass


        except ConnectionError as e:
            print(f"connection error {e}")

    import time

    def trail(self):
        while True:  
            self.user_choice = input("Enter a choice (exit/extend): ").strip().lower() 
            if self.user_choice == 'exit':
                print("Exited")
                break  
            elif self.user_choice == 'extend':
                try:
                    self.seconds = int(input("Enter the number of seconds to sleep: "))
                    print(f"Sleeping for {self.seconds} seconds...")
                    time.sleep(self.seconds)

                except ValueError:
                    print("Please enter a valid integer for seconds.")
            else:
                print("Invalid option. Select from the options: 'exit' or 'extend'.")

    def Thread(self):
#        self.Thread_count = int(input("Enter the thread count (between 0 and 9): "))
        with open(self.wordlist, 'r') as f:
            with ThreadPoolExecutor(max_workers=self.Thread_count) as executor:
                executor.map(self.attack, f)


dictionary = DirectoryBruteforce()
dictionary.url_validations()
dictionary.validating_wordlist()
dictionary.Thread_Count_func()
dictionary.Thread()

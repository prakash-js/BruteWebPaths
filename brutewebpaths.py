import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor


class DirectoryBruteforce:

    def __init__(self):
        self.url = None
        self.wordlist = None
        self.projectname = None
        self.cookie = None
        self.Thread_count = None
        self.user_choice = None
        self.seconds = None
        self.redirection = True  #default = True

    def url_validations(self):
        while True:
            self.url = str(input("Enter the url to fuzz : ")).strip()
            if self.url[-1] != '/':
                self.url += '/'

            try:
                response = requests.get(self.url)
                if response.status_code == 200:
                    break
                elif response.status_code != 200:
                    print(f"The Provided url status code is {response.status_code} ")
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

    def get_cookie(self):
        while True:
            user_choice = str(input("Would you like to add a cookie to the requests (Y/N) : "))
            if user_choice == 'Y':
                getting_cookie = str(input("Enter the cookie : "))
                print(getting_cookie)
                break
            elif user_choice == 'N':
                break

    def Thread_Count_func(self):
        while True:
            try:
                self.Thread_count = int(input("Enter the Number of Thread Count (between 1 - 30): "))
                if (self.Thread_count >= 1 and self.Thread_count <= 30):
                    break
                else:
                    print("Invalid Thread Count, it must be between 0 and 16.")

            except ValueError:
                print("Invalid input. Please enter an integer.")

    def check_list(self, url):
        try:
            response = requests.get(url, timeout=8, allow_redirects=self.redirection)
            if response.history:
                final_redirected_url = response.url 
                output = f"{url} was redirected to {final_redirected_url}"
                print(output)
                with open(f"redirected_{self.projectname}.txt", "a") as redirected_file:
                    redirected_file.write(output)
            elif response.status_code == 200:
                print(url)
                with open(f"200_{self.projectname}.txt", "a") as value:
                    value.write(url + "\n")
            elif response.status_code == 403 or requesting.status_code == 401:
                with open(f"403_{self.projectname}.txt", "a") as value:
                    value.write(url + "\n")
            elif response.status_code == 406:
                with open(f"406_{self.projectname}.txt", "a") as value:
                    value.write(url + "\n")
            elif response.status_code == 500:
                print(adding + "   STATUS CODE : 500   ")
                with open(f"500_{self.projectname}.txt", "a") as value:
                    value.write(url + "\n")
            elif response.status_code == 429:
                print(
                    "Error 429: Too many requests have been made in a short period of time \n(sleeping for 600Sec.")
                time.sleep(600)
        except requests.exceptions.RequestException as e:
            pass

        except requests.exceptions.RequestException as e:
            pass


    def attack(self, fuzz):
        adding = str(self.url + fuzz.strip())
        self.check_list(adding)            

    def Thread(self):
        try:
            with open(self.wordlist, 'r') as f:
                with ThreadPoolExecutor(max_workers=self.Thread_count) as executor:
                    executor.map(self.attack, f)
        except Exception as e:
            print(f"Error occur {e} ")
 


    def layer2(self, fuzz):
        with open(f"200_{self.projectname}.txt", 'r') as file:
            for line in file:
                adding2 = line.strip() + '/' + fuzz.strip()
                self.check_list(adding2)


    def Thread2(self):
        try:
            with open(self.wordlist, 'r') as words:
                with ThreadPoolExecutor(max_workers=self.Thread_count) as executor:
                    executor.map(self.layer2, words)
        except Exception as e:
            print(f"Error as {e}")



bruteforce = DirectoryBruteforce()
#bruteforce.get_cookie() # working on it
bruteforce.url_validations()
bruteforce.validating_wordlist()
bruteforce.Thread_Count_func()
bruteforce.Thread()
bruteforce.Thread2()
 

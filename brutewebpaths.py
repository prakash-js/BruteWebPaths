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
        self.n = 1

    def url_validations(self):
        while True:
            self.url = str(input("Enter the url to fuzz : "))
            if self.url[-1] != '/':
                self.url += '/'

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
                self.Thread_count = int(input("Enter the Number of Thread Count (between 0 - 16): "))
                if (self.Thread_count >= 0 and self.Thread_count <= 16):
                    break
                else:
                    print("Invalid Thread Count, it must be between 0 and 16.")

            except ValueError:
                print("Invalid input. Please enter an integer.")

    def attack(self, fuzz):

        adding = str(self.url + fuzz.strip())
        requesting = requests.get(adding, timeout=8, allow_redirects=False)
        try:
            if requesting.status_code == 200:
                print(adding)
                with open(f"200_{self.projectname}{self.n}.txt", "a") as file:
                    file.write(adding + "\n" )
            elif requesting.status_code == 302 or requesting.status_code == 301:
                print(adding + "  REDIRECTION CODE 302 or 301  ")
                with open(f"300_{self.projectname}.txt", "a") as file:
                    file.write(adding + "\n")
            elif requesting.status_code == 403:
                print(adding + "   STATUS CODE : 403 ")
                with open(f"403_{self.projectname}.txt", "a") as file:
                    file.write(adding + "\n")
            elif requesting.status_code == 500:
                print(adding + "   STATUS CODE : 500   " )
                with open(f"500_{self.projectname}.txt", "a") as file:
                    file.write(adding + "\n")
            elif requesting.status_code == 429:
                print("Error 429: Too many requests have been made in a short period of time \n(sleeping for 600Sec.")
                time.sleep(600)
            else:
                pass
        except ConnectionError as e:
            print(f"connection error {e}")

    def Thread(self):
        try:
            with open(self.wordlist, 'r') as f:
                with ThreadPoolExecutor(max_workers=self.Thread_count) as executor:
                    executor.map(self.attack, f)
        except Exception as e:
            print(f"Error occur {e} ")

    def layer2(self, fuzz, n):
        with open(f"200_{self.projectname}{n}.txt", 'r') as file:
            for line in file:
                url = line.strip() + '/' + fuzz.strip()
                try:
                    response = requests.get(url, timeout=8, allow_redirects=False)
                    if response.status_code == 200:
                        print(url)
                        with open(f"200_{self.projectname}{n + 1}.txt", "a") as value:
                            value.write(url + "\n")
                except requests.exceptions.RequestException as e:
                    pass

    def Thread2(self):
        x = self.n

        while True:
            try:
                with open(f"200_{self.projectname}{self.n}.txt", 'r') as file:
                    y = file.read()
                    if not y:
                        break
            except FileNotFoundError:
                break
            try:
                with open(self.wordlist, 'r') as f:
                    with ThreadPoolExecutor(max_workers=self.Thread_count) as executor:
                        executor.map(lambda fuzz: self.layer2(fuzz, x), f)
            except Exception as e:
                print(f"Error {e}")
            x += 1
            self.n = x


bruteforce = DirectoryBruteforce()
bruteforce.url_validations()
bruteforce.validating_wordlist()
bruteforce.Thread_Count_func()
bruteforce.Thread()
bruteforce.Thread2()

import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from colorama import init,Fore
import argparse




class DirectoryBruteforce:
    init(autoreset=True)

    def __init__(self):
        self.url = None
        self.wordlist = None
        self.projectname = None
        self.Thread_count = None
        self.user_choice = None
    #    self.cookie = None
        self.domain = None
        self.seconds = None
        self.n = 1
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.arguments()


    def arguments(self):
        args = argparse.ArgumentParser()
        args.add_argument("--url", type=str, help="Specify a URL.", required=True)
        args.add_argument("--wordlist", type=str, help="Specify the wordlist path",required=True)
        args.add_argument("--output", type=str, help="Specify the output file name",required=True)
   #     args.add_argument("--cookie", type=str, help="Specify the cookie inside string")

        parsed_args = args.parse_args()

        self.url = parsed_args.url
        self.wordlist = parsed_args.wordlist
        self.projectname = parsed_args.output
   #     self.cookie = rf'{parsed_args.cookie}'



    def Extract_domain(self, domain):
        parsed_url = urlparse(domain)
        return parsed_url.netloc

    def url_validations(self):
        if self.url[-1] != '/':
            self.url += '/'

        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.domain = self.Extract_domain(self.url)
        except requests.exceptions.ConnectionError as e:
            print(f'Invalid URL {e}')



        except requests.exceptions.InvalidURL as e:
            print(f'Invalid URL {e}')

        except requests.exceptions.MissingSchema as e:
            print(f'Invalid URL {e}')




    def validating_wordlist(self):

        if os.path.exists(self.wordlist):
            pass
        else:
            print("FileNotFound")

    def Thread_Count_func(self):
        while True:
            try:
                self.Thread_count = int(input("Enter the Number of Thread Count (between 0 - 36): "))
                if (self.Thread_count >= 0 and self.Thread_count <= 36):
                    break
                else:
                    print("Invalid Thread Count, it must be between 0 and 16.")

            except ValueError:
                print("Invalid input. Please enter an integer.")

    def attack(self, fuzz):
        fuzz = fuzz.strip()
        if fuzz == '/':
            return 0
        if '.' not in fuzz[1::]:
            fuzz = fuzz + '/'
        if '.' in fuzz[::-1] and fuzz[-1] == '/':
            fuzz = fuzz[0:len(fuzz) - 1]

        adding = str(self.url + fuzz)
        requesting = requests.get(adding, timeout=8, allow_redirects=True)
        try:
            if requesting.history:
                final_redirected_url = requesting.url
                output = f"{adding} " + Fore.YELLOW + f"was redirected to {Fore.GREEN + final_redirected_url}"
                print(output)
                domain_out = self.Extract_domain(final_redirected_url)
                if self.domain == domain_out:
                    with open(f"200_{self.projectname}{self.n}.txt", "a") as file:
                        file.write(adding + "\n")
            if requesting.status_code == 200:
                print(adding)
                with open(f"200_{self.projectname}{self.n}.txt", "a") as file:
                    file.write(adding + "\n" )
            elif requesting.status_code == 403 or requesting.status_code == 401:
                with open(f"403_{self.projectname}{self.n}.txt", "a") as file:
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

    def layer2(self, fuzz, n):       #fuzz=wordlist n=file_count
        with open(f"200_{self.projectname}{n}.txt", 'r') as file:
            for line in file:
                fuzz = fuzz.strip()
                if fuzz == '/':
                    return 0
                if '.' not in fuzz[1::]:
                    fuzz = fuzz + '/'
                if '.' in fuzz[::-1] and fuzz[-1] == '/':
                    fuzz = fuzz[0:len(fuzz) - 1]

                url = line.strip() + '/' + fuzz
                try:
                    if self.cookie is not None:
                        response = requests.get(url, timeout=8, headers=self.header, cookies=self.cookie)

                    else:
                        response = requests.get(url, timeout=8,headers = self.header)

                    if response.history:
                        final_redirected_url = response.url
                        output = f"{url} " + Fore.YELLOW + f"was redirected to {Fore.GREEN + final_redirected_url}"
                        print(output)
                        domain_out = self.Extract_domain(final_redirected_url)
                        if self.domain == domain_out:
                            with open(f"200_{self.projectname}{n + 1}.txt", "a") as value:
                                value.write(url + "\n")
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
#bruteforce.get_cookie() # working on it
bruteforce.Thread2()


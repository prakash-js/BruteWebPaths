import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from colorama import init, Fore
import argparse


class DirectoryBruteforce:
    init(autoreset=True)

    def __init__(self):
        self.url = None
        self.wordlist = None
        self.projectname = None
        self.Thread_count = 7
        self.user_choice = None
        self.cookie = None
        self.domain = None
        self.redirection = True
        self.seconds = None
        self.n = 1
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.arguments()

    def arguments(self):
        args = argparse.ArgumentParser(description="Directory Brute-Force Tool")
        args.add_argument("--url", type=str, help="Specify a URL.", required=True)
        args.add_argument("--wordlist", type=str, help="Specify the wordlist path", required=True)
        args.add_argument("--output", type=str, help="Specify the output folder name (unique name is preferred)",
                          required=True)
        args.add_argument("--cookie", type=str, help="Specify the cookie inside string")
        args.add_argument("--redirection", type=str,
                          help="Specify whether redirection should be True or False (default is True)")
        args.add_argument("--thread", type=int, help="Specify the thread count (maximum 36, default is 7)")

        parsed_args = args.parse_args()

        self.url = parsed_args.url
        self.wordlist = parsed_args.wordlist
        self.projectname = parsed_args.output
        self.cookie = parsed_args.cookie
        self.redirection = parsed_args.redirection
        self.Thread_count = parsed_args.thread

        if self.redirection:
            variable = self.redirection.lower()
            if variable == "true":
                self.redirection = True
            elif variable == "false":
                self.redirection = False
            else:
                print("Specify redirection as either True or False")
                exit()

        if self.Thread_count:
            try:
                if (self.Thread_count >= 0 and self.Thread_count <= 36):
                    pass
                else:
                    print("Invalid Thread Count, it must be between 0 and 36.")
                    exit()
            except ValueError:
                print("Invalid input. Please enter an integer.")

        if self.cookie:
            try:
                parts = self.cookie.split(';')
                cookie = {}
                for part in parts:
                    if '=' in part:
                        key, value = part.split('=', 1)
                        cookie[key] = value
                    else:
                        cookie[part] = True
                self.cookie = cookie
                print(self.cookie)

            except ValueError:
                print("Invalid cookie format. Use key=value format.")
                return

        # Create the output folder
        try:
            if os.path.exists(self.projectname):
                print(f"Folder '{self.projectname}' already exists!")
                exit()
            else:
                os.mkdir(self.projectname)
        except Exception as e:
            print(e)

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

    def attack(self, fuzz):
        fuzz = fuzz.strip()
        if fuzz == '/':
            return
        if fuzz.endswith('/'):
            fuzz = fuzz.rstrip('/')
        else:
            pass

        if fuzz.startswith('.'):
            for trail in [fuzz, fuzz + '/']:
                adding = str(self.url + trail)
        elif '.' in fuzz[1:]:
            adding = str(self.url + fuzz)
        else:
            adding = str(self.url + fuzz + '/')

        if self.cookie is None:
            requesting = requests.get(adding, timeout=8, allow_redirects=True)
        if self.cookie is not None:
            requesting = requests.get(adding, timeout=8, allow_redirects=True, cookies=self.cookie)
        try:

            if requesting.history:
                final_redirected_url = requesting.url
                output = f"{adding} " + Fore.YELLOW + f"was redirected to {Fore.GREEN + final_redirected_url}"
                print(output)
                print(final_redirected_url)
                domain_out = self.Extract_domain(final_redirected_url)
                if self.domain == domain_out:
                    if final_redirected_url[-1] == '/':
                        with open(os.path.join(self.projectname, f"200_{self.projectname}{self.n}.txt"), "a") as file:
                            file.write(final_redirected_url + "\n")
                    else:
                        with open(os.path.join(self.projectname, f"302_{self.projectname}{self.n}.txt"), "a") as file:
                            file.write(final_redirected_url + "\n")
            elif requesting.status_code == 200:
                print(adding)
                with open(os.path.join(self.projectname, f"200_{self.projectname}{self.n}.txt"), "a") as file:
                    file.write(adding + "\n")
            elif requesting.status_code == 403 or requesting.status_code == 401:
                with open(os.path.join(self.projectname, f"403_{self.projectname}{self.n}.txt"), "a") as file:
                    file.write(adding + "\n")
            elif requesting.status_code == 500:
                print(adding + Fore.RED + "   STATUS CODE : 500   ")
                with open(os.path.join(self.projectname, f"500_{self.projectname}.txt"), "a") as file:
                    file.write(adding + "\n")
            elif requesting.status_code == 429:
                print(
                    Fore.RED + "Error 429: Too many requests have been made in a short period of time \n(sleeping for 600Sec.")
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

    def layer2(self, fuzz, n):  # fuzz=wordlist n=file_count
        with open(os.path.join(self.projectname, f"200_{self.projectname}{n}.txt"), 'r') as file:  # opening saved urls
            for line in file:
                fuzz = fuzz.strip()

                if fuzz == '/':
                    return
                if fuzz.endswith('/'):
                    fuzz = fuzz.rstrip('/')
                else:
                    pass

                if fuzz.startswith('.'):
                    for trail in [fuzz, fuzz + '/']:
                        url = str(line.strip() + trail)
                elif '.' in fuzz[1:]:
                    url = str(line.strip() + fuzz)
                else:
                    url = str(line.strip() + fuzz + '/')
                try:
                    if self.cookie is None:
                        response = requests.get(url, timeout=8, headers=self.header)

                    if self.cookie is not None:
                        response = requests.get(url, timeout=8, headers=self.header, cookies=self.cookie)

                    if response.history:
                        final_redirected_url = response.url
                        output = f"{url} " + Fore.YELLOW + f"was redirected to {Fore.GREEN + final_redirected_url}"
                        print(output)
                        print(final_redirected_url)
                        domain_out = self.Extract_domain(final_redirected_url)
                        if self.domain == domain_out:
                            if final_redirected_url[-1] == '/':
                                with open(os.path.join(self.projectname, f"200_{self.projectname}{n + 1}.txt"),
                                      "a") as value:
                                    value.write(final_redirected_url + "\n")
                            else:
                                with open(os.path.join(self.projectname, f"302_{self.projectname}{n + 1}.txt"),
                                      "a") as value:
                                    value.write(final_redirected_url + "\n")

                    elif response.status_code == 200:
                        print(url)
                        with open(os.path.join(self.projectname, f"200_{self.projectname}{n + 1}.txt"), "a") as value:
                            value.write(url + "\n")
                    elif response.status_code == 403 or response.status_code == 401:
                        with open(os.path.join(self.projectname, f"403_{self.projectname}{self.n + 1}.txt"),
                                  "a") as value:
                            value.write(url + "\n")
                    elif response.status_code == 500:
                        print(url + Fore.RED + "   STATUS CODE : 500   ")
                        with open(os.path.join(self.projectname, f"500_{self.projectname}{self.n + 1}.txt"),
                                  "a") as value:
                            value.write(url + "\n")
                except requests.exceptions.RequestException as e:
                    pass

    def Thread2(self):
        x = self.n

        while True:
            try:
                with open(os.path.join(self.projectname, f"200_{self.projectname}{self.n}.txt"), 'r') as file:
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
bruteforce.Thread()
bruteforce.Thread2()

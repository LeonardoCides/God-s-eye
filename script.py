import requests
import pyfiglet
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional
from colorama import Fore, Style, init

init(autoreset=True)

class UsernameSherlock:
    def __init__(self, username: str):
        self.username = username
        self.timeout = 7
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        self.targets = {
            "Instagram": "https://www.instagram.com/{}/",
            "GitHub": "https://github.com/{}",
            "Twitter": "https://twitter.com/{}",
            "YouTube": "https://www.youtube.com/@{}",
            "Reddit": "https://www.reddit.com/user/{}",
            "Pinterest": "https://www.pinterest.com/{}/",
            "Dev.to": "https://dev.to/{}",
            "Twitch": "https://www.twitch.tv/{}",
            "Steam": "https://steamcommunity.com/id/{}",
            "TikTok": "https://www.tiktok.com/@{}",
            "Medium": "https://medium.com/@{}",
            "Quora": "https://www.quora.com/profile/{}",
            "Vimeo": "https://vimeo.com/{}"
        }
        self.found_profiles = []

    def _check_platform(self, name: str, url_schema: str) -> Optional[str]:
        target_url = url_schema.format(self.username)
        try:
            response = requests.get(target_url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            if response.status_code == 200:
                return f"{name}: {target_url}"
        except requests.RequestException:
            pass
        return None

    def run(self) -> List[str]:
        with ThreadPoolExecutor(max_workers=15) as executor:
            results = executor.map(lambda p: self._check_platform(*p), self.targets.items())
            self.found_profiles = [r for r in results if r]
        return self.found_profiles

    def save_results(self, filename: str = "results.txt"):
        if not self.found_profiles:
            return
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Report for: {self.username}\n" + "="*30 + "\n")
            f.write("\n".join(self.found_profiles))

def main():
    banner = pyfiglet.figlet_format("OLHO DE DEUS", font="slant")
    print(Fore.CYAN + banner)
    print(f"{Fore.MAGENTA}v1.0.0 - Automated OSINT Tool{Style.RESET_ALL}\n")
    
    target_user = input(f"{Fore.YELLOW}Target Username: {Style.RESET_ALL}").strip()
    if not target_user:
        return

    scanner = UsernameSherlock(target_user)
    print(f"\n{Fore.BLUE}[*] Searching {len(scanner.targets)} platforms...{Style.RESET_ALL}")
    
    results = scanner.run()
    
    if results:
        print(f"\n{Fore.GREEN}[+] Matches Found:{Style.RESET_ALL}")
        for entry in results:
            print(f"  {Fore.WHITE}{entry}")
    else:
        print(f"\n{Fore.RED}[-] No matches found.{Style.RESET_ALL}")
        
    scanner.save_results()
    print(f"\n{Fore.CYAN}[*] Done. Results saved to results.txt{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
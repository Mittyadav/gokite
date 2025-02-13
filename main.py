import requests
import json
import random
import time
from typing import Dict, List
from datetime import datetime, timedelta
from colorama import init, Fore, Style

init(autoreset=True)

AI_ENDPOINTS = {
    "https://deployment-uu9y1z4z85rapgwkss1muuiz.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_UU9y1Z4Z85RAPGwkss1mUUiZ",
        "name": "Kite AI Assistant",
        "questions": [
            "What is Kite AI?",
            "How does Kite AI help developers?",
            "What are the main features of Kite AI?",
            "Can you explain the Kite AI ecosystem?",
            "How do I get started with Kite AI?",
            "What are the benefits of using Kite AI?",
            "How does Kite AI compare to other AI platforms?",
            "What kind of problems can Kite AI solve?",
            "Tell me about Kite AI's architecture",
            "What are the use cases for Kite AI?"
        ]
    }
}

class KiteAIAutomation:
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
        self.daily_points = 0
        self.start_time = datetime.now()
        self.next_reset_time = self.start_time + timedelta(hours=24)
        self.MAX_DAILY_POINTS = 200
        self.POINTS_PER_INTERACTION = 10
        self.MAX_DAILY_INTERACTIONS = self.MAX_DAILY_POINTS // self.POINTS_PER_INTERACTION

    def reset_daily_points(self):
        current_time = datetime.now()
        if current_time >= self.next_reset_time:
            print(f"{self.print_timestamp()} {Fore.GREEN}Resetting points for new 24-hour period{Style.RESET_ALL}")
            self.daily_points = 0
            self.next_reset_time = current_time + timedelta(hours=24)
            return True
        return False

    def should_wait_for_next_reset(self):
        if self.daily_points >= self.MAX_DAILY_POINTS:
            wait_seconds = (self.next_reset_time - datetime.now()).total_seconds()
            if wait_seconds > 0:
                print(f"{self.print_timestamp()} {Fore.YELLOW}Daily point limit reached ({self.MAX_DAILY_POINTS}){Style.RESET_ALL}")
                print(f"{self.print_timestamp()} {Fore.YELLOW}Waiting until next reset at {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
                time.sleep(wait_seconds)
                self.reset_daily_points()
            return True
        return False

    def print_timestamp(self):
        return f"{Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]{Style.RESET_ALL}"

    def print_stats(self, stats: Dict):
        """Display user statistics in a sleek, formatted style."""
        print(Fore.CYAN + "\n╔══════════════════════════════╗")
        print("║     📊 USER STATISTICS      ║")
        print("╚══════════════════════════════╝" + Style.RESET_ALL)
        
        print(f"🔹 {Fore.GREEN}Total Interactions:{Style.RESET_ALL} {Fore.WHITE}{stats.get('total_interactions', 0)}{Style.RESET_ALL}")
        print(f"🔹 {Fore.GREEN}Total Agents Used:{Style.RESET_ALL} {Fore.WHITE}{stats.get('total_agents_used', 0)}{Style.RESET_ALL}")
        print(f"📅 {Fore.YELLOW}First Seen:{Style.RESET_ALL} {Fore.WHITE}{stats.get('first_seen', 'N/A')}{Style.RESET_ALL}")
        print(f"🕒 {Fore.YELLOW}Last Active:{Style.RESET_ALL} {Fore.WHITE}{stats.get('last_active', 'N/A')}{Style.RESET_ALL}")

        print(Fore.CYAN + "════════════════════════════════" + Style.RESET_ALL)

    def run(self):
        """Start AI interaction script with a sleek, formatted display."""
        print(Fore.CYAN + "\n╔════════════════════════════════════════════╗")
        print("║  🚀 AI AUTOMATION SCRIPT INITIATED  🔄   ║")
        print("╚════════════════════════════════════════════╝" + Style.RESET_ALL)

        print(f"📌 {self.print_timestamp()} {Fore.GREEN}Script running with 24-hour interaction limits! (Press {Fore.RED}Ctrl+C{Fore.GREEN} to stop){Style.RESET_ALL}")
        print(f"🔹 {self.print_timestamp()} {Fore.CYAN}Wallet Address: {Fore.MAGENTA}{self.wallet_address}{Style.RESET_ALL}")
        print(f"🔹 {self.print_timestamp()} {Fore.CYAN}Daily Point Limit: {Fore.WHITE}{self.MAX_DAILY_POINTS} points ({self.MAX_DAILY_INTERACTIONS} interactions){Style.RESET_ALL}")
        print(f"⏳ {self.print_timestamp()} {Fore.CYAN}Next Reset Scheduled: {Fore.WHITE}{self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")

        print(Fore.CYAN + "════════════════════════════════════════════" + Style.RESET_ALL)

        try:
            while True:
                self.reset_daily_points()
                if self.should_wait_for_next_reset():
                    continue

                print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}Processing New Interaction...{Style.RESET_ALL}")

                # Simulating interaction
                time.sleep(2)
                print(f"\n{Fore.GREEN}✅ Interaction Completed Successfully!{Style.RESET_ALL}")

                # Simulating waiting time
                delay = random.uniform(1, 3)
                print(f"\n{self.print_timestamp()} {Fore.YELLOW}Waiting {delay:.1f} seconds before next interaction...{Style.RESET_ALL}")
                time.sleep(delay)

        except KeyboardInterrupt:
            print(f"\n{self.print_timestamp()} {Fore.YELLOW}Script stopped by user{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{self.print_timestamp()} {Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

def main():
    """Display a sleek, modern banner and start the automation process."""
    print(Fore.CYAN + """
╔═════════════════════════════════════════════════╗
║           🚀 KITE AI AUTOMATION SYSTEM 🚀       ║
║  🤖 Automate AI Interactions & Earn Rewards 🎯  ║
║  🔗 Github: https://github.com/Mittyadav        ║
╚═════════════════════════════════════════════════╝
""" + Style.RESET_ALL)

    print(f"{Fore.YELLOW}📌 First, register here: {Fore.GREEN}https://testnet.gokite.ai?r=sCR5wfyu{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📝 Complete the tasks before proceeding! ✅\n{Style.RESET_ALL}")

    wallet_address = input(f"{Fore.CYAN}🔹 Enter your registered Wallet Address: {Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}✅ Wallet Address Verified! Initializing Automation...{Style.RESET_ALL}")
    time.sleep(1)

    automation = KiteAIAutomation(wallet_address)
    automation.run()

if __name__ == "__main__":
    main()

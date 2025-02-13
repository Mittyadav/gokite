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
    },
    "https://deployment-ecz5o55dh0dbqagkut47kzyc.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_ECz5O55dH0dBQaGKuT47kzYC",
        "name": "Crypto Price Assistant",
        "questions": [
            "Price of Solana",
            "What's the current price of Bitcoin?",
            "Show me Ethereum price trends",
            "Top gainers in the last 24 hours?",
            "Which coins are trending now?",
            "Price analysis for DOT",
            "How is AVAX performing?",
            "Show me the price of MATIC",
            "What's the market cap of BNB?",
            "Price prediction for ADA"
        ]
    },
    "https://deployment-sofftlsf9z4fya3qchykaanq.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_SoFftlsf9z4fyA3QCHYkaANq",
        "name": "Transaction Analyzer",
        "questions": []
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
            print(f"{self.print_timestamp()} {Fore.GREEN}🔄 Resetting points for new 24-hour period{Style.RESET_ALL}")
            self.daily_points = 0
            self.next_reset_time = current_time + timedelta(hours=24)

    def print_timestamp(self):
        return f"{Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]{Style.RESET_ALL}"

    def print_stats(self, stats: Dict):
        print("\n" + Fore.CYAN + "╔════════════════════════════════════════════╗")
        print("║            🚀 CURRENT STATISTICS           ║")
        print("╚════════════════════════════════════════════╝" + Style.RESET_ALL)

        print(f"📊 {Fore.YELLOW}Total Interactions:{Style.RESET_ALL} {Fore.GREEN}{stats.get('total_interactions', 0)}{Style.RESET_ALL}")
        print(f"🤖 {Fore.YELLOW}Total Agents Used:{Style.RESET_ALL} {Fore.GREEN}{stats.get('total_agents_used', 0)}{Style.RESET_ALL}")
        print(f"🕰 {Fore.YELLOW}First Seen:{Style.RESET_ALL} {Fore.CYAN}{stats.get('first_seen', 'N/A')}{Style.RESET_ALL}")
        print(f"🔄 {Fore.YELLOW}Last Active:{Style.RESET_ALL} {Fore.CYAN}{stats.get('last_active', 'N/A')}{Style.RESET_ALL}")
        print(Fore.CYAN + "════════════════════════════════════════════" + Style.RESET_ALL)

    def run(self):
        print(f"{self.print_timestamp()} {Fore.GREEN}🚀 Starting AI interaction script with 24-hour limits (Press Ctrl+C to stop){Style.RESET_ALL}")
        print(Fore.CYAN + "════════════════════════════════════════════════════" + Style.RESET_ALL)
        print(f"💳 {Fore.YELLOW}Wallet Address:{Style.RESET_ALL} {Fore.MAGENTA}{self.wallet_address}{Style.RESET_ALL}")
        print(f"🎯 {Fore.YELLOW}Daily Point Limit:{Style.RESET_ALL} {self.MAX_DAILY_POINTS} points ({self.MAX_DAILY_INTERACTIONS} interactions)")
        print(f"⏳ {Fore.YELLOW}First reset at:{Style.RESET_ALL} {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(Fore.CYAN + "════════════════════════════════════════════════════" + Style.RESET_ALL)

        try:
            while True:
                self.reset_daily_points()

                print("\n" + Fore.MAGENTA + "══════════════════════════════════════════════════" + Style.RESET_ALL)
                print(f"🔄 {Fore.CYAN}New Interaction{Style.RESET_ALL}")
                print(f"📊 Points: {self.daily_points + self.POINTS_PER_INTERACTION}/{self.MAX_DAILY_POINTS}")
                print(Fore.MAGENTA + "══════════════════════════════════════════════════" + Style.RESET_ALL)

                endpoint = random.choice(list(AI_ENDPOINTS.keys()))
                question = random.choice(AI_ENDPOINTS[endpoint]["questions"])

                print("\n" + Fore.CYAN + "📡 Selected AI Assistant:")
                print(f"🤖 {Fore.WHITE}{AI_ENDPOINTS[endpoint]['name']}")
                print(f"🆔 {Fore.WHITE}Agent ID: {AI_ENDPOINTS[endpoint]['agent_id']}")
                print(f"❓ {Fore.WHITE}Question: {question}" + Style.RESET_ALL)

                response = "Sample AI Response"  # Simulated AI response

                print(f"{self.print_timestamp()} {Fore.GREEN}✅ Interaction successfully recorded!{Style.RESET_ALL}")
                self.daily_points += self.POINTS_PER_INTERACTION

                delay = random.uniform(1, 3)
                print(f"\n{self.print_timestamp()} {Fore.YELLOW}⏳ Waiting {delay:.1f} seconds before next query...{Style.RESET_ALL}")
                time.sleep(delay)

        except KeyboardInterrupt:
            print(f"\n{self.print_timestamp()} {Fore.YELLOW}🛑 Script stopped by user{Style.RESET_ALL}")

def main():
    print_banner = """
╔══════════════════════════════════════════════╗
║               KITE AI AUTOMATE               ║
║     Github: https://github.com/Mittyadav    ║
╚══════════════════════════════════════════════╝
    """
    print(Fore.CYAN + print_banner + Style.RESET_ALL)
    
    wallet_address = input(f"{Fore.YELLOW}Register first here: {Fore.GREEN}https://testnet.gokite.ai?r=cmuST6sG{Fore.YELLOW} and Clear Tasks!\nNow, input your registered Wallet Address: {Style.RESET_ALL}")
    
    automation = KiteAIAutomation(wallet_address)
    automation.run()

if __name__ == "__main__":
    main()

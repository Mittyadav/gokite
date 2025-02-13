import requests
import json
import random
import time
from typing import Dict, List
from datetime import datetime, timedelta
from colorama import init, Fore, Style

# Initialize color formatting
init(autoreset=True)

# AI Endpoints and Questions
AI_ENDPOINTS = {
    "https://deployment-uu9y1z4z85rapgwkss1muuiz.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_UU9y1Z4Z85RAPGwkss1mUUiZ",
        "name": "Kite AI Assistant",
        "questions": [
            "What is Kite AI?", "How does Kite AI help developers?",
            "What are the main features of Kite AI?", "Can you explain the Kite AI ecosystem?",
            "How do I get started with Kite AI?", "What are the benefits of using Kite AI?",
            "How does Kite AI compare to other AI platforms?", "What kind of problems can Kite AI solve?",
            "Tell me about Kite AI's architecture", "What are the use cases for Kite AI?"
        ]
    },
    "https://deployment-ecz5o55dh0dbqagkut47kzyc.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_ECz5O55dH0dBQaGKuT47kzYC",
        "name": "Crypto Price Assistant",
        "questions": [
            "Price of Solana", "What's the current price of Bitcoin?",
            "Show me Ethereum price trends", "Top gainers in the last 24 hours?",
            "Which coins are trending now?", "Price analysis for DOT",
            "How is AVAX performing?", "Show me the price of MATIC",
            "What's the market cap of BNB?", "Price prediction for ADA"
        ]
    },
    "https://deployment-sofftlsf9z4fya3qchykaanq.stag-vxzy.zettablock.com/main": {
        "agent_id": "deployment_SoFftlsf9z4fyA3QCHYkaANq",
        "name": "Transaction Analyzer",
        "questions": []
    }
}


class KiteAIAutomation:
    """Automates AI interactions for earning points"""

    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
        self.daily_points = 0
        self.start_time = datetime.now()
        self.next_reset_time = self.start_time + timedelta(hours=24)
        self.MAX_DAILY_POINTS = 200
        self.POINTS_PER_INTERACTION = 10
        self.MAX_DAILY_INTERACTIONS = self.MAX_DAILY_POINTS // self.POINTS_PER_INTERACTION

    def reset_daily_points(self):
        """Resets daily points if 24-hour period has elapsed"""
        if datetime.now() >= self.next_reset_time:
            print(f"{self.timestamp()} {Fore.GREEN}Resetting daily points!{Style.RESET_ALL}")
            self.daily_points = 0
            self.next_reset_time = datetime.now() + timedelta(hours=24)

    def should_wait_for_next_reset(self):
        """If max points reached, wait for reset time"""
        if self.daily_points >= self.MAX_DAILY_POINTS:
            wait_seconds = (self.next_reset_time - datetime.now()).total_seconds()
            print(f"{self.timestamp()} {Fore.YELLOW}Limit reached! Waiting until {self.next_reset_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
            time.sleep(wait_seconds)
            self.reset_daily_points()

    def timestamp(self):
        """Returns formatted timestamp"""
        return f"{Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"

    def get_recent_transactions(self) -> List[str]:
        """Fetches recent transactions from KiteScan"""
        print(f"{self.timestamp()} {Fore.BLUE}Fetching recent transactions...{Style.RESET_ALL}")
        url = 'https://testnet.kitescan.ai/api/v2/advanced-filters'
        params = {'transaction_types': 'coin_transfer', 'age': '5m'}
        headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0'}

        try:
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            hashes = [item['hash'] for item in data.get('items', [])]
            print(f"{self.timestamp()} {Fore.MAGENTA}Fetched {len(hashes)} transactions!{Style.RESET_ALL}")
            return hashes
        except Exception as e:
            print(f"{self.timestamp()} {Fore.RED}Error fetching transactions: {e}{Style.RESET_ALL}")
            return []

    def send_ai_query(self, endpoint: str, message: str) -> str:
        """Sends AI query and returns response"""
        headers = {'Accept': 'text/event-stream', 'Content-Type': 'application/json'}
        data = {"message": message, "stream": True}

        try:
            response = requests.post(endpoint, headers=headers, json=data, stream=True)
            accumulated_response = ""

            print(f"{Fore.CYAN}AI Response: {Style.RESET_ALL}", end='', flush=True)
            for line in response.iter_lines():
                if line and line.decode('utf-8').startswith('data: '):
                    try:
                        json_str = line.decode('utf-8')[6:]
                        if json_str == '[DONE]': break
                        json_data = json.loads(json_str)
                        content = json_data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                        if content:
                            accumulated_response += content
                            print(Fore.MAGENTA + content + Style.RESET_ALL, end='', flush=True)
                    except json.JSONDecodeError:
                        continue
            print()
            return accumulated_response.strip()
        except Exception as e:
            print(f"{self.timestamp()} {Fore.RED}Error in AI query: {e}{Style.RESET_ALL}")
            return ""

    def run(self):
        """Runs AI automation in a loop"""
        print(f"{self.timestamp()} {Fore.GREEN}Starting AI interaction script! (Press Ctrl+C to stop){Style.RESET_ALL}")

        interaction_count = 0

        try:
            while True:
                self.reset_daily_points()
                self.should_wait_for_next_reset()

                interaction_count += 1
                print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}Interaction #{interaction_count}{Style.RESET_ALL}")

                endpoint = random.choice(list(AI_ENDPOINTS.keys()))
                question = random.choice(AI_ENDPOINTS[endpoint]["questions"])

                print(f"{Fore.CYAN}Selected AI: {AI_ENDPOINTS[endpoint]['name']}")
                print(f"{Fore.CYAN}Agent ID: {AI_ENDPOINTS[endpoint]['agent_id']}")
                print(f"{Fore.CYAN}Question: {question}{Style.RESET_ALL}")

                response = self.send_ai_query(endpoint, question)
                self.daily_points += self.POINTS_PER_INTERACTION

                delay = random.uniform(1, 3)
                print(f"{self.timestamp()} {Fore.YELLOW}Waiting {delay:.1f} seconds before next query...{Style.RESET_ALL}")
                time.sleep(delay)

        except KeyboardInterrupt:
            print(f"\n{self.timestamp()} {Fore.YELLOW}Script stopped by user!{Style.RESET_ALL}")


def main():
    """Main function to start automation"""
    banner = """
╔══════════════════════════════════════════╗
║             KITE AI AUTOMATION           ║
║       Github: https://github.com/Mittyadav║
╚══════════════════════════════════════════╝
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)

    wallet_address = input(f"{Fore.YELLOW}Register here: {Fore.GREEN}https://testnet.gokite.ai?r=cmuST6sG{Fore.YELLOW} and Clear Tasks!\nEnter your Wallet Address: {Style.RESET_ALL}")
    
    automation = KiteAIAutomation(wallet_address)
    automation.run()


if __name__ == "__main__":
    main()

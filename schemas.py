import re
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class PromptModel:
    name: str
    welcome_message: str
    prompt_start: str


@dataclass
class ModelQuery:
    model: str
    messages: List[Dict[str, str]]


@dataclass
class L402:
    token: str
    invoice: str
    proxy_mode: str = "aperture"
    preimage: Optional[str] = None
    paid: bool = False

    @staticmethod
    def from_headers(auth_header, proxy_mode: str = "aperture"):
        if "Www-Authenticate" in auth_header:
            l402 = auth_header["Www-Authenticate"]
            if proxy_mode == "aperture":
                # LightningLabs L402 (LSAT)
                # Extract macaroon value
                macaroon = re.search(r'macaroon="(.*?)"', l402).group(1)
                # Extract invoice value
                invoice = re.search(r'invoice="(.*?)"', l402).group(1)
                return L402(macaroon, invoice, proxy_mode)
            elif proxy_mode == "matador":
                # Kody Matador (https://github.com/Kodylow/matador)
                token = l402.split(" ")[1].split("=")[1].replace(",", "")
                invoice = l402.split(" ")[2].split("=")[1]
                return L402(token, invoice, proxy_mode)
        elif "X-Cashu" in auth_header:
            token = auth_header["X-Cashu"]
            # TODO: To implement
            raise NotImplementedError("X-Cashu not implemented")
        else:
            raise ValueError("No 402 header found")

    def set_paid(self, preimage: str) -> bool:
        if self.check_paid(preimage):
            self.preimage = preimage
            self.paid = True
            return True
        else:
            return False

    def check_paid(self, preimage: str) -> bool:
        # TODO:Control that hash of preimage is equal to payment_hash from the invoice
        return True


@dataclass
class ClientQuery:
    ai_mode: str = "chat"
    model: str = "gpt-3.5-turbo"
    prompt: str = ""
    query: str = ""
    l402: Optional[L402] = None

    def set_l402(self, l402):
        self.l402 = l402

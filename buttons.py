import json
from typing import List, Dict


def get_consent_pd_keyboard() -> Dict:
    """
    Клавиатура для согласия на обработку ПД.
    """
    return {
        "buttons": [
            [
                {
                    "text": "✅ Принимаю условия и даю согласие",
                    "callback_data": "accept_pd"
                }
            ],
            [
                {
                    "text": "❌ Отказаться",
                    "callback_data": "decline_pd"
                }
            ]
        ],
        "is_inline": True
    }
import os
from typing import Dict

import movie_api.config as config


def configure_engine() -> Dict:
    # if os.getenv('TESTING', 'False') in ['True', True, 1]:
    #     return {
    #         'db_url': config.TEST_DB_URL,
    #         'options': {
    #             'echo': True
    #         }
    #     }
    # else:
    return {
        "db_url": config.DB_URL,
        "options": {
            "executemany_mode": "batch",
            "pool_size": 1100,
            "max_overflow": 1000,
            "pool_recycle": 100,
        },
    }

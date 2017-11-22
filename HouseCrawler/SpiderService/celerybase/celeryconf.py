import os
import sys

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../services'))
sys.path.append(os.path.abspath('../..'))

broker_url = "redis://10.30.1.18/2"
result_backend = "redis://10.30.1.18/3"
include = ['spider_service',
            # 'task_service',
            # 'monitor_service'
        ]
task_default_queue = 'NewHouseQueue'

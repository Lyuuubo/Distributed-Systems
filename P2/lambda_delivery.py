import json
import time
import random

def lambda_handler(event, context):
    order = event.get('order')
    print("Simulating delivery for order:", order)
    delay = random.randint(2, 10)
    print(f"Simulating delivery: waiting {delay} seconds.")
    time.sleep(delay)
    print("Order successfully delivered:", order, "!")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Order delivered",
            "order": order
        })
    }

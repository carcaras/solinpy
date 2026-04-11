import time


def confirm_transaction(client, signature: str, timeout: int = 30):
    start = time.time()

    while time.time() - start < timeout:
        status = client.get_transaction_status(signature)

        if status in ["confirmed", "finalized"]:
            return {"status": status, "signature": signature}

        if status == "failed":
            return {"status": "failed", "signature": signature}

        time.sleep(1)

    return {"status": "timeout", "signature": signature}

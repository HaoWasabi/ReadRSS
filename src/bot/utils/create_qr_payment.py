import os

class QRGenerator:
    @staticmethod
    def generator(user_id: str ):
        # "https://api.vietqr.io/image/970422-0347402306-9505cHJ.jpg?accountName=NGUYEN%20KHAC%20HIEU&amount=10000&addInfo=donnet"
        return f"https://img.vietqr.io/image/MB-{os.getenv('BANK_ID')}-{os.getenv('QR_TEMPLATE')}.png?accountName=AIKO&amount=10000&addInfo=T{user_id}T"
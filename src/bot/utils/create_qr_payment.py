import os, random

class QRGenerator:
    @staticmethod
    def generator_qr(qr_id: str , gia: int):
        # "https://api.vietqr.io/image/970422-0347402306-9505cHJ.jpg?accountName=NGUYEN%20KHAC%20HIEU&amount=10000&addInfo=donnet"
        return f"https://img.vietqr.io/image/MB-{os.getenv('BANK_ID')}-{os.getenv('QR_TEMPLATE')}.png?accountName=AIKO&amount={gia}&addInfo=T{qr_id}T"
    
    @staticmethod
    def generator_id():
        s = ''
        for i in range(20):
            s += str(random.randint(0, 9))
        
        return s
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CRED_PATH = os.path.join(BASE_DIR, "serviceAccountKey.json")

if not firebase_admin._apps:
    if not os.path.exists(CRED_PATH):
        raise FileNotFoundError(f"ไม่พบไฟล์บริการ Firebase ที่: {CRED_PATH}")
        
    cred = credentials.Certificate(CRED_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()

class FirestoreDB:
    @staticmethod
    def create_document(collection_name: str, data: dict) -> str:
        data["created_at"] = datetime.now(timezone.utc)
        doc_ref = db.collection(collection_name).document()
        doc_ref.set(data)
        return doc_ref.id

    @staticmethod
    def get_document(collection_name: str, doc_id: str):
        doc = db.collection(collection_name).document(doc_id).get()
        if doc.exists:
            return {"id": doc.id, **doc.to_dict()}
        return None

    @staticmethod
    def find_one_by_field(collection_name: str, field: str, value: str):
        if not value:
            return None
        # บังคับแปลง value เป็น str เพื่อป้องกันปัญหา Type Mismatch
        docs = db.collection(collection_name).where(field, "==", str(value)).limit(1).get()
        if docs:
            doc = docs[0]
            return {"id": doc.id, **doc.to_dict()}
        return None

    @staticmethod
    def update_document(collection_name: str, doc_id: str, data: dict):
        db.collection(collection_name).document(doc_id).update(data)
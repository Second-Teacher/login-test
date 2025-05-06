from firebase_admin import firestore

class UserRepository:
    def __init__(self):
        self.db = firestore.client()
        self.collection = self.db.collection('users')
    
    def exists(self, user_id):
        """사용자 문서 존재 여부 확인"""
        doc = self.collection.document(user_id).get()
        return doc.exists
    
    def create(self, user_id, email):
        """새 사용자 문서 생성"""
        user_data = {
            'email': email,
            'createdAt': firestore.SERVER_TIMESTAMP
        }
        self.collection.document(user_id).set(user_data)
from flask import Blueprint, request, session, redirect, url_for
from firebase_admin import auth
from repositories.user_repository import UserRepository

auth_bp = Blueprint('auth', __name__)
user_repository = UserRepository()

@auth_bp.route('/auth', methods=['POST'])
def authorize():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return "Unauthorized", 401

    token = token[7:]
    
    try:
        # 토큰 검증
        decoded_token = auth.verify_id_token(token, check_revoked=True, clock_skew_seconds=60)
        user_id = decoded_token['uid']
        email = decoded_token.get('email', '')
        
        # 세션에 사용자 정보 저장
        session['user'] = decoded_token
        
        # 사용자 문서 확인/생성
        if not user_repository.exists(user_id):
            user_repository.create(user_id, email)
            print(f"User document created for {user_id}")
        
        return redirect(url_for('dashboard.dashboard'))
    except Exception as e:
        print(f"Authentication error: {e}")
        return "Unauthorized", 401
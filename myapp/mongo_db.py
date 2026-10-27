import os
import json
import logging
from datetime import datetime

logger = logging.getLogger('myapp.mongo')

MONGODB_URI = os.environ.get('MONGODB_URI', '')
DB_NAME = os.environ.get('MONGODB_DB_NAME', 'streamflix_db')

_mongo_client = None
_db = None

def get_mongo_db():
    global _mongo_client, _db
    if _db is not None:
        return _db
    
    if not MONGODB_URI:
        return None
    
    try:
        from pymongo import MongoClient
        _mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2500)
        # Verify connection
        _mongo_client.admin.command('ping')
        _db = _mongo_client[DB_NAME]
        logger.info('Connected to MongoDB successfully.')
        return _db
    except Exception as e:
        logger.warning(f'MongoDB connection error: {e}. Falling back to local JSON store.')
        _db = None
        return None

def save_chat_log(session_id, user_prompt, ai_response, intent='query', metadata=None):
    log_doc = {
        'session_id': session_id,
        'user_prompt': user_prompt,
        'ai_response': ai_response,
        'intent': intent,
        'metadata': metadata or {},
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }

    db = get_mongo_db()
    if db is not None:
        try:
            res = db.chat_logs.insert_one(log_doc)
            return {'success': True, 'storage': 'mongodb', 'id': str(res.inserted_id)}
        except Exception as e:
            logger.error(f'Failed to write chat log to MongoDB: {e}')

    # Local Fallback
    fallback_path = os.path.join(os.path.dirname(__file__), 'mongo_chat_logs_fallback.json')
    try:
        logs = []
        if os.path.exists(fallback_path):
            with open(fallback_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        log_doc['_id'] = f'local_{len(logs)+1}'
        logs.append(log_doc)
        with open(fallback_path, 'w', encoding='utf-8') as f:
            json.dump(logs[-100:], f, indent=2) # Keep last 100
        return {'success': True, 'storage': 'local_fallback', 'id': log_doc['_id']}
    except Exception as e:
        logger.error(f'Failed writing to local fallback: {e}')
        return {'success': False, 'error': str(e)}

def save_feedback(session_id, rating, comment='', user_name='Anonymous'):
    feedback_doc = {
        'session_id': session_id,
        'user_name': user_name,
        'rating': rating,
        'comment': comment,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }

    db = get_mongo_db()
    if db is not None:
        try:
            res = db.feedback.insert_one(feedback_doc)
            return {'success': True, 'storage': 'mongodb', 'id': str(res.inserted_id)}
        except Exception as e:
            logger.error(f'Failed to write feedback to MongoDB: {e}')

    fallback_path = os.path.join(os.path.dirname(__file__), 'mongo_feedback_fallback.json')
    try:
        fb_list = []
        if os.path.exists(fallback_path):
            with open(fallback_path, 'r', encoding='utf-8') as f:
                fb_list = json.load(f)
        feedback_doc['_id'] = f'local_fb_{len(fb_list)+1}'
        fb_list.append(feedback_doc)
        with open(fallback_path, 'w', encoding='utf-8') as f:
            json.dump(fb_list[-100:], f, indent=2)
        return {'success': True, 'storage': 'local_fallback', 'id': feedback_doc['_id']}
    except Exception as e:
        logger.error(f'Failed writing feedback fallback: {e}')
        return {'success': False, 'error': str(e)}

def get_mongo_status():
    db = get_mongo_db()
    if db is not None:
        try:
            count = db.chat_logs.count_documents({})
            return {
                'connected': True,
                'status': 'Online (MongoDB Cloud/Instance)',
                'database': DB_NAME,
                'chat_logs_count': count
            }
        except Exception as e:
            pass
    return {
        'connected': False,
        'status': 'Fallback Active (Local Resilient Document Store)',
        'database': 'local_json_resilient_store',
        'note': 'Configure MONGODB_URI in environment variables to link to MongoDB Atlas'
    }

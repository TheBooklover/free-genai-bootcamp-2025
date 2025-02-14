from flask import request, jsonify, g
from flask_cors import cross_origin
from datetime import datetime
import math
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded

def load(app):
  # Initialize rate limiter
  limiter = Limiter(
    app=app,
    key_func=get_remote_address,  # Limit by IP address
    default_limits=["200 per day", "50 per hour"]  # Default limits
  )
  
  # Add rate limit exceeded error handler
  @app.errorhandler(RateLimitExceeded)
  def handle_rate_limit_exceeded(e):
    app.logger.warning(f'Rate limit exceeded: {str(e)}')
    return jsonify({
      "error": "Too many requests",
      "message": "Please try again later",
      "retry_after": e.description
    }), 429
  
  def validate_study_session_request(data):
    required_fields = ['group_id', 'study_activity_id']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
            
    try:
        int(data['group_id'])
        int(data['study_activity_id'])
    except (ValueError, TypeError):
        return False, "Invalid ID format - must be integers"
        
    return True, None

  @app.route('/api/study-sessions', methods=['POST'])
  @cross_origin()
  @limiter.limit("20 per minute")
  def create_study_session():
    try:
      # Add logging for debugging and monitoring
      app.logger.info('Creating new study session')
      app.logger.debug(f'Request data: {request.get_json()}')
      
      cursor = app.db.cursor()
      
      # Validate request data
      data = request.get_json()
      is_valid, error_message = validate_study_session_request(data)
      if not is_valid:
        app.logger.warning(f'Validation failed: {error_message}')
        return jsonify({"error": error_message}), 400
      
      # Input sanitization for security - convert IDs to integers
      try:
        group_id = int(data['group_id'])
        activity_id = int(data['study_activity_id'])
      except (ValueError, TypeError):
        app.logger.warning('Invalid ID format')
        return jsonify({"error": "Invalid ID format - must be integers"}), 400
      
      # Verify group and activity exist
      cursor.execute('''
        SELECT EXISTS(SELECT 1 FROM groups WHERE id = ?) as group_exists,
               EXISTS(SELECT 1 FROM study_activities WHERE id = ?) as activity_exists
      ''', (group_id, activity_id))
      
      result = cursor.fetchone()
      if not result['group_exists']:
        app.logger.warning(f'Group not found: {group_id}')
        return jsonify({"error": "Group not found"}), 400
      if not result['activity_exists']:
        app.logger.warning(f'Study activity not found: {activity_id}')
        return jsonify({"error": "Study activity not found"}), 400
      
      # Create study session
      cursor.execute('''
        INSERT INTO study_sessions (group_id, study_activity_id, created_at)
        VALUES (?, ?, ?)
      ''', (group_id, activity_id, datetime.now()))
      
      session_id = cursor.lastrowid
      
      # Fetch created session details
      cursor.execute('''
        SELECT 
          ss.id,
          ss.group_id,
          g.name as group_name,
          sa.id as activity_id,
          sa.name as activity_name,
          ss.created_at,
          COUNT(wri.id) as review_items_count
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN word_review_items wri ON wri.study_session_id = ss.id
        WHERE ss.id = ?
        GROUP BY ss.id
      ''', (session_id,))
      
      session = cursor.fetchone()
      app.db.commit()
      
      app.logger.info(f'Successfully created study session: {session_id}')
      
      return jsonify({
        'id': session['id'],
        'group_id': session['group_id'],
        'group_name': session['group_name'],
        'activity_id': session['activity_id'],
        'activity_name': session['activity_name'],
        'start_time': session['created_at'],
        'end_time': session['created_at'],  # For now, just use the same time
        'review_items_count': session['review_items_count']
      }), 200
      
    except Exception as e:
      app.logger.error(f'Error creating study session: {str(e)}')
      app.db.rollback()
      return jsonify({"error": str(e)}), 500

  @app.route('/api/study-sessions', methods=['GET'])
  @cross_origin()
  def get_study_sessions():
    try:
      cursor = app.db.cursor()
      
      # Get pagination parameters
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('per_page', 10, type=int)
      offset = (page - 1) * per_page

      # Get total count
      cursor.execute('''
        SELECT COUNT(*) as count 
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
      ''')
      total_count = cursor.fetchone()['count']

      # Get paginated sessions
      cursor.execute('''
        SELECT 
          ss.id,
          ss.group_id,
          g.name as group_name,
          sa.id as activity_id,
          sa.name as activity_name,
          ss.created_at,
          COUNT(wri.id) as review_items_count
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN word_review_items wri ON wri.study_session_id = ss.id
        GROUP BY ss.id
        ORDER BY ss.created_at DESC
        LIMIT ? OFFSET ?
      ''', (per_page, offset))
      sessions = cursor.fetchall()

      return jsonify({
        'items': [{
          'id': session['id'],
          'group_id': session['group_id'],
          'group_name': session['group_name'],
          'activity_id': session['activity_id'],
          'activity_name': session['activity_name'],
          'start_time': session['created_at'],
          'end_time': session['created_at'],  # For now, just use the same time since we don't track end time
          'review_items_count': session['review_items_count']
        } for session in sessions],
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_count / per_page)
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  @app.route('/api/study-sessions/<id>', methods=['GET'])
  @cross_origin()
  def get_study_session(id):
    try:
      cursor = app.db.cursor()
      
      # Get session details
      cursor.execute('''
        SELECT 
          ss.id,
          ss.group_id,
          g.name as group_name,
          sa.id as activity_id,
          sa.name as activity_name,
          ss.created_at,
          COUNT(wri.id) as review_items_count
        FROM study_sessions ss
        JOIN groups g ON g.id = ss.group_id
        JOIN study_activities sa ON sa.id = ss.study_activity_id
        LEFT JOIN word_review_items wri ON wri.study_session_id = ss.id
        WHERE ss.id = ?
        GROUP BY ss.id
      ''', (id,))
      
      session = cursor.fetchone()
      if not session:
        return jsonify({"error": "Study session not found"}), 404

      # Get pagination parameters
      page = request.args.get('page', 1, type=int)
      per_page = request.args.get('per_page', 10, type=int)
      offset = (page - 1) * per_page

      # Get the words reviewed in this session with their review status
      cursor.execute('''
        SELECT 
          w.*,
          COALESCE(SUM(CASE WHEN wri.correct = 1 THEN 1 ELSE 0 END), 0) as session_correct_count,
          COALESCE(SUM(CASE WHEN wri.correct = 0 THEN 1 ELSE 0 END), 0) as session_wrong_count
        FROM words w
        JOIN word_review_items wri ON wri.word_id = w.id
        WHERE wri.study_session_id = ?
        GROUP BY w.id
        ORDER BY w.kanji
        LIMIT ? OFFSET ?
      ''', (id, per_page, offset))
      
      words = cursor.fetchall()

      # Get total count of words
      cursor.execute('''
        SELECT COUNT(DISTINCT w.id) as count
        FROM words w
        JOIN word_review_items wri ON wri.word_id = w.id
        WHERE wri.study_session_id = ?
      ''', (id,))
      
      total_count = cursor.fetchone()['count']

      return jsonify({
        'session': {
          'id': session['id'],
          'group_id': session['group_id'],
          'group_name': session['group_name'],
          'activity_id': session['activity_id'],
          'activity_name': session['activity_name'],
          'start_time': session['created_at'],
          'end_time': session['created_at'],  # For now, just use the same time
          'review_items_count': session['review_items_count']
        },
        'words': [{
          'id': word['id'],
          'kanji': word['kanji'],
          'romaji': word['romaji'],
          'english': word['english'],
          'correct_count': word['session_correct_count'],
          'wrong_count': word['session_wrong_count']
        } for word in words],
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total_count / per_page)
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  def validate_review_request(data):
    """
    Validates the review submission request data.
    Returns (is_valid, error_message) tuple.
    """
    if not data:
        return False, "Missing request data"
        
    if 'reviews' not in data:
        return False, "Missing reviews array"
        
    if not isinstance(data['reviews'], list):
        return False, "reviews must be an array"
        
    for review in data['reviews']:
        if 'word_id' not in review:
            return False, "Missing word_id in review"
            
        if 'correct' not in review:
            return False, "Missing correct field in review"
            
        if not isinstance(review['correct'], bool):
            return False, "correct field must be a boolean"
            
        try:
            int(review['word_id'])
        except (ValueError, TypeError):
            return False, "word_id must be an integer"
            
    return True, None

  @app.route('/api/study-sessions/<int:session_id>/review', methods=['POST'])
  @cross_origin()
  @limiter.limit("20 per minute")
  def submit_session_review(session_id):
    try:
        cursor = app.db.cursor()
        
        # Validate request data
        data = request.get_json()
        is_valid, error_message = validate_review_request(data)
        if not is_valid:
            return jsonify({"error": error_message}), 400
            
        # Verify session exists
        cursor.execute('''
            SELECT EXISTS(SELECT 1 FROM study_sessions WHERE id = ?) as session_exists
        ''', (session_id,))
        
        if not cursor.fetchone()['session_exists']:
            return jsonify({"error": "Study session not found"}), 404
            
        # Process each review
        reviews_data = []
        for review in data['reviews']:
            # Verify word exists
            cursor.execute('''
                SELECT EXISTS(SELECT 1 FROM words WHERE id = ?) as word_exists
            ''', (review['word_id'],))
            
            if not cursor.fetchone()['word_exists']:
                return jsonify({"error": f"Word {review['word_id']} not found"}), 404
                
            # Insert review
            cursor.execute('''
                INSERT INTO word_review_items (
                    study_session_id,
                    word_id,
                    correct,
                    reviewed_at
                ) VALUES (?, ?, ?, ?)
            ''', (session_id, review['word_id'], review['correct'], datetime.now()))
            
            review_id = cursor.lastrowid
            
            # Get review details
            cursor.execute('''
                SELECT 
                    wri.id,
                    wri.word_id,
                    w.kanji,
                    w.romaji,
                    w.english,
                    wri.correct,
                    wri.reviewed_at
                FROM word_review_items wri
                JOIN words w ON w.id = wri.word_id
                WHERE wri.id = ?
            ''', (review_id,))
            
            review_data = cursor.fetchone()
            reviews_data.append({
                "id": review_data['id'],
                "word_id": review_data['word_id'],
                "kanji": review_data['kanji'],
                "romaji": review_data['romaji'],
                "english": review_data['english'],
                "correct": review_data['correct'],
                "reviewed_at": review_data['reviewed_at']
            })
            
        app.db.commit()
        return jsonify({"reviews": reviews_data}), 200
        
    except Exception as e:
        app.db.rollback()
        return jsonify({"error": str(e)}), 500

  @app.route('/api/study-sessions/reset', methods=['POST'])
  @cross_origin()
  def reset_study_sessions():
    try:
      cursor = app.db.cursor()
      
      # First delete all word review items since they have foreign key constraints
      cursor.execute('DELETE FROM word_review_items')
      
      # Then delete all study sessions
      cursor.execute('DELETE FROM study_sessions')
      
      app.db.commit()
      
      return jsonify({"message": "Study history cleared successfully"}), 200
    except Exception as e:
      return jsonify({"error": str(e)}), 500
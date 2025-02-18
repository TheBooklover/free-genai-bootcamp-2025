from flask import request, jsonify, g
from flask_cors import cross_origin
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3

def load(app):
  limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
  )
  limiter.init_app(app)

  @app.route('/groups', methods=['GET'])
  @cross_origin()
  @limiter.limit("60 per minute")  # Reasonable limit for read operations
  def get_groups():
    try:
      cursor = app.db.cursor()

      # Get the current page number from query parameters (default is 1)
      try:
        page = int(request.args.get('page', 1))
        if page < 1:
          return jsonify({"error": "Page number must be positive"}), 400
      except ValueError:
        return jsonify({"error": "Invalid page number"}), 400

      # Validate sort parameters
      sort_by = request.args.get('sort_by', 'name')
      if sort_by not in ['name', 'words_count']:
        return jsonify({"error": "Invalid sort column"}), 400

      groups_per_page = 10
      offset = (page - 1) * groups_per_page

      # Get sorting parameters from the query string
      order = request.args.get('order', 'asc')  # Default to ascending order

      # Validate sort_by and order
      valid_columns = ['name', 'words_count']
      if sort_by not in valid_columns:
        sort_by = 'name'
      if order not in ['asc', 'desc']:
        order = 'asc'

      # Get search parameter
      search = request.args.get('search', '').strip()
      
      # Base query
      query = '''
          SELECT id, name, words_count
          FROM groups
          WHERE 1=1
      '''
      params = []

      # Add search condition if search parameter is provided
      if search:
          query += ' AND name LIKE ?'
          params.append(f'%{search}%')

      # Add sorting and pagination
      query += f' ORDER BY {sort_by} {order} LIMIT ? OFFSET ?'
      params.extend([groups_per_page, offset])

      cursor.execute(query, params)

      groups = cursor.fetchall()

      # Query the total number of groups
      cursor.execute('SELECT COUNT(*) FROM groups')
      total_groups = cursor.fetchone()[0]
      total_pages = (total_groups + groups_per_page - 1) // groups_per_page

      # Format the response
      groups_data = []
      for group in groups:
        groups_data.append({
          "id": group["id"],
          "group_name": group["name"],
          "word_count": group["words_count"]
        })

      # Return groups and pagination metadata
      return jsonify({
        'groups': groups_data,
        'total_pages': total_pages,
        'current_page': page
      })
    except sqlite3.OperationalError as e:
      app.logger.error(f"Database error in get_groups: {str(e)}")
      return jsonify({"error": "Database error"}), 500
    except Exception as e:
      app.logger.error(f"Error in get_groups: {str(e)}")
      return jsonify({"error": str(e)}), 500

  @app.route('/groups/<int:id>', methods=['GET'])
  @cross_origin()
  def get_group(id):
    try:
      cursor = app.db.cursor()

      # Get group details
      cursor.execute('''
        SELECT id, name, words_count
        FROM groups
        WHERE id = ?
      ''', (id,))
      
      group = cursor.fetchone()
      if not group:
        return jsonify({"error": "Group not found"}), 404

      return jsonify({
        "id": group["id"],
        "group_name": group["name"],
        "word_count": group["words_count"]
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  @app.route('/groups/<int:id>/words', methods=['GET'])
  @cross_origin()
  def get_group_words(id):
    try:
      cursor = app.db.cursor()
      
      # Get pagination parameters
      page = int(request.args.get('page', 1))
      words_per_page = 10
      offset = (page - 1) * words_per_page

      # Get sorting parameters
      sort_by = request.args.get('sort_by', 'kanji')
      order = request.args.get('order', 'asc')

      # Validate sort parameters
      valid_columns = ['kanji', 'romaji', 'english', 'correct_count', 'wrong_count']
      if sort_by not in valid_columns:
        sort_by = 'kanji'
      if order not in ['asc', 'desc']:
        order = 'asc'

      # First, check if the group exists
      cursor.execute('SELECT name FROM groups WHERE id = ?', (id,))
      group = cursor.fetchone()
      if not group:
        return jsonify({"error": "Group not found"}), 404

      # Query to fetch words with pagination and sorting
      cursor.execute(f'''
        SELECT w.*, 
               COALESCE(wr.correct_count, 0) as correct_count,
               COALESCE(wr.wrong_count, 0) as wrong_count
        FROM words w
        JOIN word_groups wg ON w.id = wg.word_id
        LEFT JOIN word_reviews wr ON w.id = wr.word_id
        WHERE wg.group_id = ?
        ORDER BY {sort_by} {order}
        LIMIT ? OFFSET ?
      ''', (id, words_per_page, offset))
      
      words = cursor.fetchall()

      # Get total words count for pagination
      cursor.execute('''
        SELECT COUNT(*) 
        FROM word_groups 
        WHERE group_id = ?
      ''', (id,))
      total_words = cursor.fetchone()[0]
      total_pages = (total_words + words_per_page - 1) // words_per_page

      # Format the response
      words_data = []
      for word in words:
        words_data.append({
          "id": word["id"],
          "quebecois": word["quebecois"],
          "standard_french": word["standard_french"],
          "english": word["english"],
          "pronunciation": word["pronunciation"],
          "usage_notes": word["usage_notes"],
          "correct_count": word["correct_count"],
          "wrong_count": word["wrong_count"]
        })

      return jsonify({
        'words': words_data,
        'total_pages': total_pages,
        'current_page': page
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  @app.route('/groups/<int:id>/words/raw', methods=['GET'])
  @cross_origin()
  def get_group_words_raw(id):
    """Fetch all words for a specific group without pagination or sorting.
    
    This endpoint returns the complete set of words for bulk operations and exports.
    Unlike the paginated /words endpoint, this returns all words at once.
    
    Args:
        id (int): The group ID to fetch words for
        
    Returns:
        JSON response with:
        - words: List of word objects containing:
            - id: Word ID
            - kanji: Japanese kanji
            - romaji: Romanized Japanese
            - english: English translation
            - correct_count: Number of correct reviews
            - wrong_count: Number of incorrect reviews
        - total_count: Total number of words in the group
        
    Error Responses:
        - 404: Group not found
        - 500: Server error
    """
    try:
      cursor = app.db.cursor()

      # First, check if the group exists
      cursor.execute('SELECT name FROM groups WHERE id = ?', (id,))
      group = cursor.fetchone()
      if not group:
        return jsonify({"error": "Group not found"}), 404

      # Query to fetch all words without pagination or sorting
      cursor.execute('''
        SELECT w.id,
               w.quebecois,
               w.standard_french,
               w.english,
               w.pronunciation,
               w.usage_notes,
               COALESCE(wr.correct_count, 0) as correct_count,
               COALESCE(wr.wrong_count, 0) as wrong_count
        FROM words w
        JOIN word_groups wg ON w.id = wg.word_id
        LEFT JOIN word_reviews wr ON w.id = wr.word_id
        WHERE wg.group_id = ?
      ''', (id,))
      
      words = cursor.fetchall()

      # Format the response
      words_data = []
      for word in words:
        words_data.append({
          "id": word["id"],
          "quebecois": word["quebecois"],
          "standard_french": word["standard_french"],
          "english": word["english"],
          "pronunciation": word["pronunciation"],
          "usage_notes": word["usage_notes"],
          "correct_count": word["correct_count"],
          "wrong_count": word["wrong_count"]
        })

      return jsonify({
        'words': words_data,
        'total_count': len(words_data)
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500

  @app.route('/groups/<int:id>/study_sessions', methods=['GET'])
  @cross_origin()
  def get_group_study_sessions(id):
    try:
      cursor = app.db.cursor()
      
      # Get pagination parameters
      page = int(request.args.get('page', 1))
      sessions_per_page = 10
      offset = (page - 1) * sessions_per_page

      # Get sorting parameters
      sort_by = request.args.get('sort_by', 'created_at')
      order = request.args.get('order', 'desc')  # Default to newest first

      # Map frontend sort keys to database columns
      sort_mapping = {
        'startTime': 'created_at',
        'endTime': 'last_activity_time',
        'activityName': 'a.name',
        'groupName': 'g.name',
        'reviewItemsCount': 'review_count'
      }

      # Use mapped sort column or default to created_at
      sort_column = sort_mapping.get(sort_by, 'created_at')

      # Get total count for pagination
      cursor.execute('''
        SELECT COUNT(*)
        FROM study_sessions
        WHERE group_id = ?
      ''', (id,))
      total_sessions = cursor.fetchone()[0]
      total_pages = (total_sessions + sessions_per_page - 1) // sessions_per_page

      # Get study sessions for this group with dynamic calculations
      cursor.execute(f'''
        SELECT 
          s.id,
          s.group_id,
          s.study_activity_id,
          s.created_at as start_time,
          (
            SELECT MAX(created_at)
            FROM word_review_items
            WHERE study_session_id = s.id
          ) as last_activity_time,
          a.name as activity_name,
          g.name as group_name,
          (
            SELECT COUNT(*)
            FROM word_review_items
            WHERE study_session_id = s.id
          ) as review_count
        FROM study_sessions s
        JOIN study_activities a ON s.study_activity_id = a.id
        JOIN groups g ON s.group_id = g.id
        WHERE s.group_id = ?
        ORDER BY {sort_column} {order}
        LIMIT ? OFFSET ?
      ''', (id, sessions_per_page, offset))
      
      sessions = cursor.fetchall()
      sessions_data = []
      
      for session in sessions:
        # If there's no last_activity_time, use start_time + 30 minutes
        end_time = session["last_activity_time"]
        if not end_time:
            end_time = cursor.execute('SELECT datetime(?, "+30 minutes")', (session["start_time"],)).fetchone()[0]
        
        sessions_data.append({
          "id": session["id"],
          "group_id": session["group_id"],
          "group_name": session["group_name"],
          "study_activity_id": session["study_activity_id"],
          "activity_name": session["activity_name"],
          "start_time": session["start_time"],
          "end_time": end_time,
          "review_items_count": session["review_count"]
        })

      return jsonify({
        'study_sessions': sessions_data,
        'total_pages': total_pages,
        'current_page': page
      })
    except Exception as e:
      return jsonify({"error": str(e)}), 500
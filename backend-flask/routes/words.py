from flask import Blueprint, request, jsonify, g
from flask_cors import cross_origin
import json
from typing import Dict, Any
from db import get_db

words_bp = Blueprint('words', __name__)

@words_bp.route('/words', methods=['GET'])
def get_words():
    try:
        # TODO: Implement pagination, sorting, and filtering
        db = get_db()
        cursor = db.cursor()
        
        # Basic query to get all words - will be enhanced later
        cursor.execute('SELECT * FROM words')
        words = cursor.fetchall()
        
        return jsonify({
            'words': words,
            'page': 1,
            'total_pages': 1,
            'total_items': len(words)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@words_bp.route('', methods=['GET'])
@cross_origin()
def get_words_with_pagination():
    """
    Get a paginated list of Québécois French words with optional sorting and filtering.
    
    Query Parameters:
    - page (int): Page number (default: 1)
    - per_page (int): Number of items per page (default: 50, max: 100)
    - sort_by (str): Field to sort by (default: 'quebecois')
    - order (str): Sort direction - 'asc' or 'desc' (default: 'asc')
    - search (str): Search term to filter words (searches quebecois, standard_french, and english)
    - group_id (int): Filter words by group ID
    
    Returns:
        JSON response containing:
        - words: List of word objects
        - total_pages: Total number of pages
        - current_page: Current page number
        - total_words: Total number of words
    """
    try:
        db = g.db
        cursor = db.cursor()

        # Validate and parse pagination parameters
        try:
            page = max(1, int(request.args.get('page', 1)))
            per_page = min(100, max(1, int(request.args.get('per_page', 50))))
        except ValueError:
            return jsonify({"error": "Invalid pagination parameters"}), 400
        
        offset = (page - 1) * per_page

        # Validate sorting parameters
        sort_by = request.args.get('sort_by', 'quebecois')
        order = request.args.get('order', 'asc').lower()

        valid_columns = ['quebecois', 'standard_french', 'english', 'correct_count', 'wrong_count']
        if sort_by not in valid_columns:
            return jsonify({"error": f"Invalid sort_by parameter. Must be one of: {', '.join(valid_columns)}"}), 400
        if order not in ['asc', 'desc']:
            return jsonify({"error": "Invalid order parameter. Must be 'asc' or 'desc'"}), 400

        # Build the base query
        query = '''
            SELECT w.id, w.quebecois, w.standard_french, w.english, 
                w.pronunciation, w.usage_notes,
                COALESCE(r.correct_count, 0) AS correct_count,
                COALESCE(r.wrong_count, 0) AS wrong_count
            FROM words w
            LEFT JOIN word_reviews r ON w.id = r.word_id
        '''
        count_query = 'SELECT COUNT(*) FROM words w'
        where_conditions = []
        params = []

        # Handle search parameter
        search = request.args.get('search', '').strip()
        if search:
            where_conditions.append('''
                (w.quebecois LIKE ? OR w.standard_french LIKE ? OR w.english LIKE ?)
            ''')
            search_param = f'%{search}%'
            params.extend([search_param, search_param, search_param])

        # Handle group filter
        group_id = request.args.get('group_id')
        if group_id:
            try:
                group_id = int(group_id)
                where_conditions.append('''
                    w.id IN (SELECT word_id FROM word_groups WHERE group_id = ?)
                ''')
                params.append(group_id)
            except ValueError:
                return jsonify({"error": "Invalid group_id parameter"}), 400

        # Add WHERE clause if conditions exist
        if where_conditions:
            where_clause = ' WHERE ' + ' AND '.join(where_conditions)
            query += where_clause
            count_query += where_clause

        # Add sorting and pagination
        query += f' ORDER BY {sort_by} {order} LIMIT ? OFFSET ?'
        params.extend([per_page, offset])

        # Execute queries
        cursor.execute(query, params)
        words = cursor.fetchall()

        # Get total count for pagination
        cursor.execute(count_query, params[:-2] if params else [])
        total_words = cursor.fetchone()[0]
        total_pages = (total_words + per_page - 1) // per_page

        # Format response
        words_data = [{
            "id": word["id"],
            "quebecois": word["quebecois"],
            "standard_french": word["standard_french"],
            "english": word["english"],
            "pronunciation": word["pronunciation"],
            "usage_notes": word["usage_notes"],
            "correct_count": word["correct_count"],
            "wrong_count": word["wrong_count"]
        } for word in words]

        return jsonify({
            "words": words_data,
            "total_pages": total_pages,
            "current_page": page,
            "total_words": total_words,
            "per_page": per_page
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@words_bp.route('/<int:word_id>', methods=['GET'])
@cross_origin()
def get_word(word_id):
    """
    Get detailed information about a specific Québécois French word.
    
    Parameters:
    - word_id (int): The ID of the word to retrieve
    
    Returns:
        JSON response containing:
        - word: Word object with all details including associated groups
    """
    try:
        cursor = g.db.cursor()
        
        cursor.execute('''
            SELECT w.id, w.quebecois, w.standard_french, w.english,
                   w.pronunciation, w.usage_notes,
                   COALESCE(r.correct_count, 0) AS correct_count,
                   COALESCE(r.wrong_count, 0) AS wrong_count,
                   GROUP_CONCAT(DISTINCT g.id || '::' || g.name) as groups
            FROM words w
            LEFT JOIN word_reviews r ON w.id = r.word_id
            LEFT JOIN word_groups wg ON w.id = wg.word_id
            LEFT JOIN groups g ON wg.group_id = g.id
            WHERE w.id = ?
            GROUP BY w.id
        ''', (word_id,))
        
        word = cursor.fetchone()
        
        if not word:
            return jsonify({"error": "Word not found"}), 404
        
        # Parse groups
        groups = []
        if word["groups"]:
            groups = [
                {"id": int(group_id), "name": group_name}
                for group_str in word["groups"].split(',')
                for group_id, group_name in [group_str.split('::')]
            ]
        
        return jsonify({
            "word": {
                "id": word["id"],
                "quebecois": word["quebecois"],
                "standard_french": word["standard_french"],
                "english": word["english"],
                "pronunciation": word["pronunciation"],
                "usage_notes": word["usage_notes"],
                "correct_count": word["correct_count"],
                "wrong_count": word["wrong_count"],
                "groups": groups
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
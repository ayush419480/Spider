# Vercel's app.py

from flask import Flask, render_template, request, jsonify
import json
import os
import requests 

app = Flask(__name__)

# =================================================================
# FIX 1: Set the protocol to HTTP. 
# This resolves the SSLEOFError for non-standard ports (30151).
# You MUST replace 'your-bot-project-name.up.railway.app' with your actual bot domain.
# =================================================================
BOT_API_BASE_URL = "http://your-bot-project-name.up.railway.app" # <-- REPLACE THIS!
BOT_API_PORT = "30151" 

@app.route('/')
def index():
    try:
        # Robust path handling for Vercel deployment
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'emotes.json')
        
        with open(file_path, 'r') as f:
            emotes = json.load(f)
        
        # NOTE: This requires 'index.html' to be present in a 'templates' folder.
        return render_template('index.html', emotes=emotes) 
    except FileNotFoundError:
        return jsonify({'message': 'Error: emotes.json or index.html not found'}), 500
    except Exception as e:
        return f"An error occurred in Vercel's index route: {e}", 500


@app.route('/send_emote', methods=['POST'])
def send_emote():
    try:
        data = request.get_json()
        
        # Extract data safely, defaulting to None/empty list
        team_code = data.get('team_code')
        emote_id = data.get('emote_id')
        uids = data.get('uids', [])

        # =================================================================
        # FIX 3: Detailed 400 Bad Request check. 
        # This resolves the "400 Bad Request" error by clarifying the missing field.
        # =================================================================
        missing_fields = []
        if not team_code:
            missing_fields.append("team_code")
        if not emote_id:
            missing_fields.append("emote_id")
        # Ensure uids is a non-empty list
        if not uids or not isinstance(uids, list) or len(uids) == 0:
            missing_fields.append("uids (must be a non-empty list)")

        if missing_fields:
            return jsonify({
                'message': 'Error: Missing required data fields in POST request body.',
                'missing': missing_fields
            }), 400
        # =================================================================

        # Build URL parameters for the Railway Bot API
        params = {
            'emote_id': emote_id,
            'tc': team_code
        }
        # Safely add the UIDs (uid1, uid2, etc.)
        for i, uid in enumerate(uids[:4]): 
            params[f'uid{i+1}'] = uid

        # Final URL for the external bot API call
        api_url = f"{BOT_API_BASE_URL}:{BOT_API_PORT}/join"
        
        # Make the request to the bot running on Railway
        response = requests.get(api_url, params=params, timeout=45) 
        response.raise_for_status() # Check for 4xx/5xx status codes

        # =================================================================
        # FIX 2: Use response.text instead of response.json(). 
        # This resolves the "Expecting value" (JSONDecodeError) crash.
        # =================================================================
        api_response_content = response.text if response.text else "Bot API returned empty content (Success, but No Content)."
        # =================================================================
        
        return jsonify({
            'message': 'Emote request successfully proxied to Bot API.',
            'api_response': api_response_content
        }), 200

    except requests.exceptions.RequestException as e:
        # Catch all requests errors (timeout, connection refused, SSL, etc.)
        return jsonify({
            'message': 'Error communicating with the external Bot API. Check Bot Firewall/Port.',
            'error_details': str(e)
        }), 503 

    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred on Vercel: {e}'}), 500

# Vercel's runtime automatically executes the 'app' object.

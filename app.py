from flask import Flask, jsonify, request, send_from_directory
import json
import os
import time

app = Flask(__name__, static_folder='public', static_url_path='')
DB_FILE = 'db.json'

def read_db():
    """Helper function to read the database file."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump([], f)
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def write_db(data):
    """Helper function to write to the database file."""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def serve_index():
    """Serves the main index.html file."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/items', methods=['GET'])
def get_items():
    """API endpoint to get all items."""
    try:
        items = read_db()
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items', methods=['POST'])
def add_item():
    """API endpoint to add a new item."""
    try:
        items = read_db()
        new_item = {
            'id': int(time.time()),
            'name': request.json['name'],
            'expirationDate': request.json['expirationDate'],
            'quantity': request.json.get('quantity', 1),
            'location': request.json.get('location', 'Pantry'),
            'category': request.json.get('category', 'Misc')
        }
        items.append(new_item)
        write_db(items)
        return jsonify(new_item), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """API endpoint to update an item."""
    try:
        items = read_db()
        for i, item in enumerate(items):
            if item['id'] == item_id:
                items[i]['name'] = request.json.get('name', item['name'])
                items[i]['expirationDate'] = request.json.get('expirationDate', item['expirationDate'])
                items[i]['quantity'] = request.json.get('quantity', item['quantity'])
                items[i]['location'] = request.json.get('location', item['location'])
                items[i]['category'] = request.json.get('category', item['category'])
                write_db(items)
                return jsonify(items[i]), 200
        return jsonify({'message': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """API endpoint to delete an item."""
    try:
        items = read_db()
        original_length = len(items)
        items = [item for item in items if item['id'] != item_id]
        if len(items) == original_length:
            return jsonify({'message': 'Item not found'}), 404
        write_db(items)
        return jsonify({'message': 'Item deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#if __name__ == '__main__':
    app.run(debug=False, port=3000)
#!/usr/bin/env python3
"""SR Private Menu — Backend Server"""

import json, os, uuid, random, string
from flask import Flask, request, jsonify, send_from_directory, session
from werkzeug.utils import secure_filename
from functools import wraps

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, 'data.json')
UPLOADS_DIR = os.path.join(BASE, 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'heic', 'mp4', 'mov', 'webm', 'hevc'}

app = Flask(__name__, static_folder=BASE)
app.secret_key = 'sr-secret-2025-xk9'

# ── Helpers ────────────────────────────────────────────────
def load():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def gen_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def require_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('admin'):
            return jsonify({'error': 'Unauthorized'}), 401
        return fn(*args, **kwargs)
    return wrapper

def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('tier'):
            return jsonify({'error': 'Unauthorized'}), 401
        return fn(*args, **kwargs)
    return wrapper

# ── Static files ───────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(BASE, 'menu.html')

@app.route('/admin')
def admin():
    return send_from_directory(BASE, 'admin.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(BASE, filename)

# ── Public API: verify client identity + code ──────────────
@app.route('/api/verify', methods=['POST'])
def verify():
    body   = request.get_json() or {}
    handle = body.get('handle', '').strip().lower().lstrip('@')
    code   = body.get('code', '').strip().upper()
    data   = load()

    def norm_phone(s): return ''.join(c for c in s if c.isdigit())
    def norm_ig(s):    return s.lower().lstrip('@').strip()

    for client in data['approved_clients']:
        stored = client.get('handle', '')
        is_phone = stored.replace('+','').replace('-','').replace(' ','').replace('(','').replace(')','').isdigit()
        if is_phone:
            match = norm_phone(stored) == norm_phone(body.get('handle',''))
        else:
            match = norm_ig(stored) == norm_ig(body.get('handle',''))

        if match:
            if client.get('code','').upper() == code:
                tier = int(client.get('menu', 1))
                session['tier'] = tier
                return jsonify({'ok': True, 'tier': tier})
            else:
                return jsonify({'error': 'wrong_code'}), 401

    return jsonify({'error': 'not_found'}), 404

# ── Public API: brand config (no prices) ──────────────────
@app.route('/api/config')
def api_config():
    data = load()
    s = data['settings']
    return jsonify({
        'brand_name':  s['brand_name'],
        'tagline':     s['tagline'],
        'ig_handle':   s['ig_handle'],
        'phone':       s['phone'],
        'menu1_name':  s.get('menu1_name', 'Menu 1'),
        'menu2_name':  s.get('menu2_name', 'Menu 2'),
        'menu3_name':  s.get('menu3_name', 'Menu 3'),
    })

# ── Auth API: tier-specific menu ───────────────────────────
@app.route('/api/menu')
@require_auth
def api_menu():
    tier = session.get('tier', 1)
    data = load()
    s    = data['settings']
    def auto_price(base, add):
        """Add dollars to a price string like '$150' → '$250'"""
        if not base:
            return ''
        num = ''.join(c for c in base if c.isdigit() or c == '.')
        try:
            result = float(num) + add
            result = int(result) if result == int(result) else result
            return ('$' if base.strip().startswith('$') else '') + str(result)
        except:
            return base

    price_key = 'price' if tier == 1 else f'price{tier}'

    items = []
    for item in data['menu_items']:
        base  = item.get('price', '')
        if tier == 1:
            price = base
        elif tier == 2:
            price = item.get('price2') or auto_price(base, 100)
        else:
            price = item.get('price3') or auto_price(base, 200)
        items.append({
            'id':          item['id'],
            'category':    item.get('category',''),
            'name':        item.get('name',''),
            'description': item.get('description',''),
            'image':       item.get('image',''),
            'video':       item.get('video',''),
            'status':      item.get('status','available'),
            'price':       price,
        })

    return jsonify({
        'brand_name': s['brand_name'],
        'tagline':    s['tagline'],
        'ig_handle':  s['ig_handle'],
        'phone':      s['phone'],
        'tier':       tier,
        'menu_name':  s.get(f'menu{tier}_name', f'Menu {tier}'),
        'menu_items': items,
    })

# ── Admin: login / logout ──────────────────────────────────
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    body = request.get_json() or {}
    data = load()
    if body.get('password') == data['settings']['admin_password']:
        session['admin'] = True
        return jsonify({'ok': True})
    return jsonify({'error': 'Wrong password'}), 401

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.clear()
    return jsonify({'ok': True})

# ── Admin: settings ────────────────────────────────────────
@app.route('/api/admin/settings', methods=['GET'])
@require_admin
def get_settings():
    return jsonify(load()['settings'])

@app.route('/api/admin/settings', methods=['PUT'])
@require_admin
def update_settings():
    data = load()
    body = request.get_json() or {}
    for k in ['brand_name','tagline','ig_handle','phone','admin_password',
              'menu1_name','menu2_name','menu3_name']:
        if k in body and body[k]:
            data['settings'][k] = body[k]
    save(data)
    return jsonify({'ok': True})

# ── Admin: menu items ──────────────────────────────────────
@app.route('/api/admin/items', methods=['GET'])
@require_admin
def get_items():
    return jsonify(load()['menu_items'])

@app.route('/api/admin/items', methods=['POST'])
@require_admin
def add_item():
    data = load()
    item = request.get_json() or {}
    item['id'] = str(uuid.uuid4())[:8]
    data['menu_items'].append(item)
    save(data)
    return jsonify(item), 201

@app.route('/api/admin/items/<item_id>', methods=['PUT'])
@require_admin
def update_item(item_id):
    data = load()
    body = request.get_json() or {}
    for i, item in enumerate(data['menu_items']):
        if item['id'] == item_id:
            data['menu_items'][i] = {**item, **body, 'id': item_id}
            save(data)
            return jsonify(data['menu_items'][i])
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/admin/items/<item_id>', methods=['DELETE'])
@require_admin
def delete_item(item_id):
    data = load()
    data['menu_items'] = [i for i in data['menu_items'] if i['id'] != item_id]
    save(data)
    return jsonify({'ok': True})

# ── Admin: clients ─────────────────────────────────────────
@app.route('/api/admin/clients', methods=['GET'])
@require_admin
def get_clients():
    return jsonify(load()['approved_clients'])

@app.route('/api/admin/clients', methods=['POST'])
@require_admin
def add_client():
    data     = load()
    body     = request.get_json() or {}
    handle   = body.get('handle', '').strip()
    name     = body.get('name', '').strip()
    lastname = body.get('lastname', '').strip()
    phone    = body.get('phone', '').strip()
    code     = body.get('code', '').strip().upper() or gen_code()
    menu     = int(body.get('menu', 1))
    if not handle and not phone:
        return jsonify({'error': 'Handle or phone required'}), 400
    client = {'id': str(uuid.uuid4())[:8], 'name': name, 'lastname': lastname,
              'handle': handle, 'phone': phone, 'code': code, 'menu': menu}
    data['approved_clients'].append(client)
    save(data)
    return jsonify(client), 201

@app.route('/api/admin/clients/<client_id>', methods=['PUT'])
@require_admin
def update_client(client_id):
    data = load()
    body = request.get_json() or {}
    for i, c in enumerate(data['approved_clients']):
        if c['id'] == client_id:
            if 'name'     in body: data['approved_clients'][i]['name']     = body['name']
            if 'lastname' in body: data['approved_clients'][i]['lastname'] = body['lastname']
            if 'handle'   in body: data['approved_clients'][i]['handle']   = body['handle']
            if 'phone'    in body: data['approved_clients'][i]['phone']    = body['phone']
            if 'code'     in body: data['approved_clients'][i]['code']     = body['code'].upper()
            if 'menu'     in body: data['approved_clients'][i]['menu']     = int(body['menu'])
            save(data)
            return jsonify(data['approved_clients'][i])
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/admin/clients/<client_id>/regen', methods=['POST'])
@require_admin
def regen_code(client_id):
    data = load()
    for i, c in enumerate(data['approved_clients']):
        if c['id'] == client_id:
            new_code = gen_code()
            data['approved_clients'][i]['code'] = new_code
            save(data)
            return jsonify({'code': new_code})
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/admin/clients/<client_id>', methods=['DELETE'])
@require_admin
def delete_client(client_id):
    data = load()
    data['approved_clients'] = [c for c in data['approved_clients'] if c['id'] != client_id]
    save(data)
    return jsonify({'ok': True})

# ── Upload ─────────────────────────────────────────────────
@app.route('/api/admin/upload', methods=['POST'])
@require_admin
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    f = request.files['file']
    ext = f.filename.rsplit('.', 1)[-1].lower() if '.' in f.filename else ''
    if ext not in ALLOWED_EXT:
        return jsonify({'error': 'Invalid file type'}), 400
    filename = str(uuid.uuid4())[:8] + '.' + ext
    f.save(os.path.join(UPLOADS_DIR, filename))
    return jsonify({'url': f'/uploads/{filename}'}), 201

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(UPLOADS_DIR, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    print(f'\n🌿 SR Menu Server running at http://localhost:{port}')
    print(f'   Menu  → http://localhost:{port}/')
    print(f'   Admin → http://localhost:{port}/admin\n')
    app.run(host='0.0.0.0', port=port, debug=False)

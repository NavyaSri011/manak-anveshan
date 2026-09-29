import urllib.request, json

products = [
    'Packaged drinking water',
    'LED street light',
    'Industrial centrifugal pump',
    'Desktop computer',
    'Industrial welding machine'
]

try:
    for p in products:
        req = urllib.request.Request(
            'http://127.0.0.1:8000/api/v1/standards/analyze',
            data=json.dumps({'product_title': p, 'document_text': f'This is a {p}'}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    print(f'\n--- {p} ---')
                    print('Extracted Category:', data['canonical_requirements']['product']['category'])
                    print('Primary Standards:', len(data['primary_standards']))
                    for s in data['primary_standards']:
                        print(f"  - {s['is_number']}: {s['title']}")
                        print(f"    Provenance: {s.get('source_type')} from {s.get('source')}")
                    print('Missing Reqs:', [m['attribute'] for m in data['missing_requirements']])
                else:
                    print(f'\n--- {p} ---')
                    print('Error status:', response.status)
        except Exception as e:
            print(f'\n--- {p} ---')
            print('Request Error:', e)
except Exception as e:
    print('Failed to connect:', e)

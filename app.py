from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from wordcloud import WordCloud
import io
import base64
from PIL import Image

app = Flask(__name__)
CORS(app)  

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/wordcloud', methods=['POST'])
def generate_wordcloud():
    try:
        # Get text from request
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        
        width = data.get('width', 800)
        height = data.get('height', 400)
        background_color = data.get('background_color', 'white')
        colormap = data.get('colormap', 'viridis')
        
        
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color=background_color,
            colormap=colormap,
            max_words=100,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(text)
        
        
        img = wordcloud.to_image()
        
       
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
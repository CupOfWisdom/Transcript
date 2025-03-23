from flask import Flask, request, jsonify
import json
import os
import transcript  # Importa o script de transcrição

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    """Recebe um vídeo, processa e retorna a transcrição"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Salva o arquivo temporariamente
    video_path = "temp_video.mp4"
    file.save(video_path)

    try:
        # Chama a função do transcription.py
        transcription_data = transcript.process_video(video_path)

        # Remove o vídeo temporário
        os.remove(video_path)

        # Retorna o transcription gerado
        return app.response_class(
            response=json.dumps(transcription_data, ensure_ascii=False, indent=4),  # Exibe caracteres corretamente
            status=200,
            mimetype='application/json'
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transcription', methods=['GET'])
def get_transcription():
    """Retorna a última transcrição salva"""
    try:
        with open('transcription.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
        return app.response_class(
            response=json.dumps(data, ensure_ascii=False, indent=4),  # Exibe caracteres corretamente
            status=200,
            mimetype='application/json'
        )
    except FileNotFoundError:
        return jsonify({"error": "No transcription available"}), 404

if __name__ == '__main__':
    app.run(debug=True)

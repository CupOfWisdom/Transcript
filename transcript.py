import whisper
from moviepy.video.io.VideoFileClip import VideoFileClip
import json
import os

def extract_audio(video_path, audio_path="temp_audio.wav"):
    """Extrai o áudio do vídeo e salva como um arquivo WAV"""
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, logger=None)  # Reduz saída no console
    return audio_path

def transcribe_audio(audio_path):
    """Transcreve o áudio utilizando Whisper"""
    model = whisper.load_model("medium")  # ou "small", dependendo da sua necessidade
    result = model.transcribe(audio_path, language="pt", temperature=0.0)
    return result["text"]

def transcribe_audio_with_timestamps(audio_path):
    """Transcreve o áudio utilizando Whisper e captura os timestamps"""
    model = whisper.load_model("medium")  # Escolha o modelo: tiny, base, small, medium, large
    result = model.transcribe(audio_path, language="pt", temperature=0.0, word_timestamps=True)
    
    segments = []
    for segment in result["segments"]:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        segments.append({
            "start": start_time,
            "end": end_time,
            "text": text
        })
    
    return segments

def process_video(video_path, output_json="transcription.json"):
    """Processa um vídeo e salva a transcrição em JSON"""
    audio_path = extract_audio(video_path)
    transcription = transcribe_audio(audio_path)

    transcription_data = {"transcription": transcription}
    
    # Salvar o resultado em um arquivo JSON
    with open(output_json, 'w', encoding="utf-8") as f:
        json.dump(transcription_data, f, ensure_ascii=False, indent=4)

    # Remover arquivos temporários
    os.remove(audio_path)

    return transcription_data

def process_video_with_time(video_path, output_json="transcription.json"):
    """Processa um vídeo e salva a transcrição em JSON"""
    audio_path = extract_audio(video_path)
    transcription = transcribe_audio_with_timestamps(audio_path)

    transcription_data = {"transcription": transcription}
    
    # Salvar o resultado em um arquivo JSON
    with open(output_json, 'w', encoding="utf-8") as f:
        json.dump(transcription_data, f, ensure_ascii=False, indent=4)

    # Remover arquivos temporários
    os.remove(audio_path)

    return transcription_data
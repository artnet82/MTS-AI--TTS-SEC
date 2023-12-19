import requests
import csv
import datetime
import librosa
import sounddevice as sd
import time

server_address = "audiogram.mts.ai:443"
sso_server_url = "https://isso.mts.ru/auth/"
realm_name = "mts"
csv_file = "audio_data.csv"

def process_audio_files():
    while True:
        audio_files = get_audio_files()
        if audio_files:
            with open(csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["File Name", "Content"])
                for audio_file in audio_files:
                    content = process_audio_file(audio_file)
                    writer.writerow([audio_file, content])
                print("CSV write completed.")
        else:
            print("No audio files received from the server.")
        
        time.sleep(60)  # Wait for 60 seconds before checking for new files again

def get_audio_files():
    response = requests.get(f"https://{server_address}/api/audio_files")
    if response.status_code == 200:
        audio_files = response.json()
        return audio_files
    else:
        print("Error getting WAV file list from the server.")
        return []

def process_audio_file(audio_file):
    audio_data, _ = librosa.load(audio_file, sr=None)
    sd.play(audio_data, samplerate=44100)
    sd.wait()
    decibels = librosa.amplitude_to_db(audio_data)
    min_decibels = decibels.min()
    max_decibels = decibels.max()
    bits = audio_data.dtype.itemsize * 8
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"Timestamp": timestamp, "Decibels": decibels, "Bits": bits}
    write_to_csv(data)
    content = f"Processed content of {audio_file}"
    return content

def write_to_csv(data):
    with open(csv_file, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writerow(data)

process_audio_files()

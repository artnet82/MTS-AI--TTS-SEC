import requests
import csv
import datetime
import librosa


server_address = "audiogram.mts.ai:443"


sso_server_url = "https://isso.mts.ru/auth/"
realm_name = "mts"


csv_file = "audio_data.csv"

def process_audio_files():

    audio_files = get_audio_files()

 
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File Name", "Content"])
        for audio_file in audio_files:
            content = process_audio_file(audio_file)
            writer.writerow([audio_file, content])
        print("Запись в CSV завершена.")

def get_audio_files():
  
    response = requests.get(f"https://{server_address}/api/audio_files")
    if response.status_code == 200:
        audio_files = response.json()
        return audio_files
    else:
        print("Ошибка при получении списка файлов WAV с сервера.")
        return []

def process_audio_file(audio_file):

    audio_data, _ = librosa.load(audio_file, sr=None)
    decibels = librosa.amplitude_to_db(audio_data)
    min_decibels = decibels.min()
    max_decibels = decibels.max()
    bits = audio_file.bit_depth

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

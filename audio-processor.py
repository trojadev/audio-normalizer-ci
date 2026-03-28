import os
import random
import subprocess
import json
import sys


def randomize_parameters():
    
    #Randomize pitch between -1 to + 1 octave
    pitch = random.randint(-1200, 1200)

    #Randomoze tempo factor
    tempo_factor = random.uniform(0.2, 1.0)
    #Randomize stretch factor
    stretch_factor = random.uniform(0.2, 1.0)
    #Randomize reverberance, high frequecies damping, pre-delay
    reverberance = random.randint(25, 100)
    hf_damping = random.randint(10, 60)
    pre_delay = random.randint(0, 300)

    #Create effect list with parameters for further use in SoX command run using subprocess module
    effects_list = [
        "pitch", pitch,
        "tempo", tempo_factor,
        "reverb", reverberance, hf_damping, 100, 100, pre_delay, 0,
        "stretch", stretch_factor

    ]

    return [str(e) for e in effects_list if e]


def batch_edit_files(parent_directory):

    processed_files_directory = f"{parent_directory}/processed_files/"
    processed_audio_data_list = []

    for file in os.listdir(parent_directory):
        if os.path.splitext(file)[1].lower() == ".wav":

            # Check if directory for saving processed files exists

            if not os.path.isdir(processed_files_directory):
                os.mkdir(processed_files_directory)

            for i in range(1, 4):

                filepath = f"{parent_directory}/{file}"
                filepath_new = processed_files_directory + \
                    f"{os.path.splitext(file)[0]}_processed_{i}{os.path.splitext(file)[1]}"

                # Normalize audio file and save it to processed files directory

                subprocess.run(["/usr/bin/sox", "-V 0", filepath,
                                filepath_new] + randomize_parameters(), check=True)

                duration = subprocess.check_output(
                    ["/usr/bin/soxi", "-V 0", "-d", f"{filepath}"], text=True).replace("\n", "")
                channels = subprocess.check_output(
                    ["/usr/bin/soxi", "-V 0", "-c", f"{filepath}"], text=True).replace("\n", "")

                processed_audio_data_list.append({"filename:": file,
                                                  "length:": duration,
                                                  "channels:": channels,
                                                  "success:": "success"})

    return processed_audio_data_list


def main():
    directory = "./data"

    try:
        print(f"Current python version: {sys.version}")

        # Normalize audio, retrieve files info and save it in JSON format

        audio_data = batch_edit_files(directory)
        audio_data_json = json.dumps(audio_data, indent=4)
        print(audio_data_json)
        sys.exit(0)

    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()

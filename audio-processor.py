import os
import subprocess
import json
import sys


def normalize_audio_file(filepath):

    parent_directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    filepath_splitted = os.path.splitext(filepath)

    print(filepath)
    print(filepath_splitted)
    processed_files_directory = f"{parent_directory}/processed_files/"

    # Create a save path for a processed file
    filepath_new = processed_files_directory + \
        f"{os.path.basename(filepath_splitted[0])}_normalized{filepath_splitted[1]}"

    try:

        # Check if directory for saving processed files exists

        if not os.path.isdir(processed_files_directory):
            os.mkdir(processed_files_directory)

        # Normalize audio file and save it to processed files directory

        subprocess.run(["/usr/bin/sox", filepath,
                       filepath_new, "norm", "-3"], check=True)

        duration = subprocess.check_output(
            ["/usr/bin/soxi", "-d", filepath], text=True).replace("\n", "")
        channels = subprocess.check_output(
            ["/usr/bin/soxi", "-c", filepath], text=True).replace("\n", "")

        print(f"{filename} normalized!")

        return {
            "filename:": filename,
            "length:": duration,
            "channels:": channels,
            "success:": "success"

        }
    except subprocess.CalledProcessError as e:
        print(f"Error processing file: {e}", file=sys.stderr)


def batch_normalize_files(parent_directory):

    processed_files_directory = f"{parent_directory}/processed_files/"
    processed_audio_data_list = []

    for file in os.listdir(parent_directory):
        if os.path.splitext(file)[1].lower() == ".wav":

            # Check if directory for saving processed files exists

            if not os.path.isdir(processed_files_directory):
                os.mkdir(processed_files_directory)

            filepath = f"{parent_directory}/{file}"
            filepath_new = processed_files_directory + \
                f"{os.path.splitext(file)[0]}_processed{os.path.splitext(file)[1]}"

            # Normalize audio file and save it to processed files directory

            subprocess.run(["/usr/bin/sox", "-V 0", filepath,
                           filepath_new, "norm", "-3"], check=True)

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
    directory = "/data"

    # Below code will be used after I write possibility to either batch process or provide specific file as an argument
    # #Check if any argument was provided
    # if len(sys.argv) == 2:
    #     filepath = sys.argv[1]
    #     if not os.path.exists(filepath):
    #         print(f"Error: File {filepath} does not exist.", file=sys.stderr)
    #         sys.exit(1)
    # elif len(sys.argv) > 2:
    #     print(f"Passed {len(sys.argv) - 1} arguments, but only 1 needed", file=sys.stderr)
    #     sys.exit(1)
    # else:
    #     print("Filepath not specified, please provide one.", file=sys.stderr)
    #     sys.exit(1)

    try:
        print(f"Current python version: {sys.version}")
        # Normalize audio, retrieve files info and save it in JSON format
        audio_data = batch_normalize_files(directory)
        audio_data_json = json.dumps(audio_data, indent=4)
        print(audio_data_json)
        sys.exit(0)

    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()

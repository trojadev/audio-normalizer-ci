import os
import subprocess
import json
import sys

   

def get_file_info(filepath):
    filename = os.path.basename(filepath)
    
    try:
        duration = subprocess.check_output(["/usr/bin/soxi", "-d", filepath], text=True).replace("\n", "")
        
        channels = subprocess.check_output(["/usr/bin/soxi", "-c", filepath], text=True).replace("\n", "")

        # audio_data = {filename : file_length}

        # audio_data_in_json = json.dumps(audio_data)

        # print(audio_data_in_json)

        return {
            "filename:" : filename,
            "length:" : duration,
            "channels:" : channels,
            "success:" : "success"

        }
    except subprocess.CalledProcessError as e:
        print(f"Error processing file using soxi: {e}", file=sys.stderr)
    


def main():

    #Check if any argument was provided
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        if not os.path.exists(filepath):
            print(f"Error: File {filepath} does not exist.", file=sys.stderr)
            sys.exit(1)
    elif len(sys.argv) > 2:
        print(f"Passed {len(sys.argv) - 1} arguments, but only 1 needed", file=sys.stderr)
        sys.exit(1)
    else:
        print("Filepath not specified, please provide one.", file=sys.stderr)
        sys.exit(1)
    
    try:

        #Retrieve file info and save it in JSON format
        audio_data = get_file_info(filepath)
        audio_data_json = json.dumps(audio_data, indent=4)
        print(audio_data_json)
        sys.exit(0)
    
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
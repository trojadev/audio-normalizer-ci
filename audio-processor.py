import os
import subprocess
import json
import sys

def normalize_audio_file(filepath):
    
    parent_directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    filepath_splitted = os.path.splitext(filepath)

    processed_files_directory = f"{parent_directory}/processed_files/"
   
    #Create a save path for a processed file
    filepath_new = processed_files_directory + f"{os.path.basename(filepath_splitted[0])}_normalized{filepath_splitted[1]}"

    
  
###
    
    try:
        
        #Check if directory for saving processed files exists

        if not os.path.isdir(processed_files_directory):
            os.mkdir(processed_files_directory)
        
        #Normalize audio file and save it to processed files directory

        subprocess.run(["/usr/bin/sox", filepath, filepath_new, "norm", "-3"], check=True)

        duration = subprocess.check_output(["/usr/bin/soxi", "-d", filepath], text=True).replace("\n", "")
        channels = subprocess.check_output(["/usr/bin/soxi", "-c", filepath], text=True).replace("\n", "")
       

        print(f"{filename} normalized!")

        return {
            "filename:" : filename,
            "length:" : duration,
            "channels:" : channels,
            "success:" : "success"

        }
    except subprocess.CalledProcessError as e:
        print(f"Error processing file: {e}", file=sys.stderr)



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


        #Normalize audio, retrieve file info and save it in JSON format
        audio_data = normalize_audio_file(filepath)
        audio_data_json = json.dumps(audio_data, indent=4)
        print(audio_data_json)
        sys.exit(0)
    
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
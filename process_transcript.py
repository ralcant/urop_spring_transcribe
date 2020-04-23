import csv
import os
'''
Returns a list of the speaker_labels of each word processed from a given input_folder
and writes to a given `processed` folder with a certain prefix.
'''
def process_csv(filename, 
                transcript_inputs_folder = "./transcripts/inputs/",
                transcript_processed_folder = "./transcripts/processed_inputs/", transcript_processed_prefix = "processed_", lazy_update = True):
    file_path = get_path(transcript_inputs_folder, "", filename, "csv")
    with open(file_path) as csv_file:
        print(f"Reading elements from {file_path}")
        output_path = get_path(transcript_processed_folder, transcript_processed_prefix, filename, "txt")
        if os.path.exists(output_path) and lazy_update:
            print(f"The processed input located at {output_path} already exists and lazy_update = True, so we are skipping this.")
            return
        with open(output_path, 'w+') as out:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            all_speakers = [] #keeps track of the speaker labels in the order they appear
            for row in csv_reader:
                print(".", end="") #just to keep track of where we are
                if line_count > 0: #not counting header
                    phrase = row[3] #format is _,speaker,elapsed_time,CONTENT,video-timestamp-frame number,video-timestamp-elapsed time,video-timestamp-local_time,question
                    for token in extract_from_phrase(phrase):
                        out.write(f'{token}\n')
                        speaker_label = row[1]
                        all_speakers.append(speaker_label) # to keep track of the labels
                line_count += 1
            print(f'\nProcessed {line_count} lines for file {filename}')
        print(f"Just wrote to {filename}.txt")
    return all_speakers
"""
Returns a list of the words/sentences/phrases that we care about in this text. Some options are
- Just return a list of the same text. 
- Return a list of all the words found in the phrase. 
- Return all the complete sentences in the text
Make sure to always return something that can be iterable. Be careful about returning lists with empty strings/useless information
"""
def extract_from_phrase(text):
    # return [text] # uncomment if you want to return the same text
    return text.split(" ") # if you want to return all the words found in a phrase
    # TODO: find a way to return a list
'''
Returns the complete path given a folder, prefix, name and type
Folder must end in "/"
For example, create_path("./audios/", "audio_", "file1", "mp3") returns "./audios/audio_file1.mp3"
'''
def get_path(folder, prefix, name, file_type):
    return "{}{}{}.{}".format(folder, prefix, name, file_type)

if __name__ == "__main__":
    video_name = "p01_s1_vid_parent_annotation_2019-03-06-11-36-09"
    #all_speakers = process_csv(video_name)
    #print(all_speakers)
import csv
import os
import pprint
import math
from collections import namedtuple
from datetime import datetime
import cmudict
ROW = namedtuple('Row', ["place", \
                                "speaker_label", \
                                "elapsed_time", \
                                "content", \
                                "frame_number", \
                                "timestamp_elapsed_time", \
                                "timestamp_local_time", \
                                "question"])
'''
Returns a list of the speaker_labels of each word processed from a given input_folder
and writes to a given `processed` folder with a certain prefix.
'''
def process_csv(filename, num_parts,
                transcript_inputs_folder = "./transcripts/inputs/",
                transcript_processed_folder = "./transcripts/processed_inputs/", transcript_processed_prefix = "processed_", lazy_update = True):
    os.makedirs(f"{transcript_processed_folder}{filename}", exist_ok=True) #creating necessary folder if necessary
    
    file_path = get_path(transcript_inputs_folder, "", filename, "csv")
    get_subpart_path = lambda num_part: get_path(f"{transcript_processed_folder}{filename}/", f"{transcript_processed_prefix}{num_parts}_part_", num_part, "txt")
    # if all(os.path.exists(get_subpart_path(i)) for i in range(1, num_parts+1)) and lazy_update:
    #     print(f"The processed inputs already exist at {file_path} and lazy_update is {lazy_update}, so we are skippping it")
    #     return
    with open(file_path) as csv_file:
        all_speakers = [] #keeps track of the speaker labels in the order they appear
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)  #to skip the header
        all_rows = [ROW._make(row) for row in csv_reader]
        first_timestamp = float(all_rows[0].timestamp_elapsed_time)
        last_timestamp = float(all_rows[-1].timestamp_elapsed_time)
        duration = last_timestamp - first_timestamp + 1 #increase the size of interval. Assuming that
        part_duration = duration/num_parts
        print(f"part_duration = {part_duration} for {num_parts} parts")
        all_info = {i: {
            "words": [],
            "speaker_labels":[]
        } for i in range(1, num_parts+1)} #for every part, it keeps all words and their speaker_labels
        print("Going through each row...")
        for i, row in enumerate(all_rows):
            curr_time = float(row.timestamp_elapsed_time)
            next_time = float(all_rows[i+1].timestamp_elapsed_time) if i < len(all_rows) - 1 else curr_time
            #print(f"for the row #{i}, the curr_time = {curr_time} and end_time = {next_time}")
            for word, word_start_time, word_end_time in get_word_times(row.content, curr_time, next_time):
                #print(f"For the word {word}, the start_time is {word_start_time} and end_time is {word_end_time}")
                index =  math.floor((word_start_time - first_timestamp) / part_duration ) #what line to create it    
                #print(f"index is {index}")
                all_info[index+1]["words"].append(word)
                all_info[index+1]["speaker_labels"].append(row.speaker_label)

    ### writing to the designed txt files ####
    for part in range(1, num_parts+1):
        print(f"Trying to write part # {part}")
        with open(get_subpart_path(part), 'w+') as out:
            for word in all_info[part]["words"]:
                out.write(f'{word}\n')
    print(f'\nProcessed {len(all_rows)} lines for file {filename}')

    return all_info
"""
Returns a list of the words/sentences/phrases that we care about in this text. Some options are
- Just return a list of the same text. 
- Return a list of all the words found in the phrase. 
- Return all the complete sentences in the text
Make sure to always return something that can be iterable. Be careful about returning lists with empty strings/useless information
"""
#def extract_from_phrase(text):
#    # return [text] # uncomment if you want to return the same text
#    return text.split(" ") # if you want to return all the words found in a phrase
    # TODO: find a way to return a list of the "phrases" in text
'''
Returns the complete path given a folder, prefix, name and type
Folder must end in "/"
For example, create_path("./audios/", "audio_", "file1", "mp3") returns "./audios/audio_file1.mp3"
'''
def get_path(folder, prefix, name, file_type):
    return "{}{}{}.{}".format(folder, prefix, name, file_type)
def get_syllables(word):
    d = cmudict.dict()
    return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]
def get_word_times_equally_divided(text, start_time, end_time):
    duration = end_time - start_time
    all_words = text.split(" ")
    time_per_word = duration / len(all_words)
    for i, word in enumerate(all_words):
        start_word = start_time + i*time_per_word
        end_word = start_time + (i+1)*time_per_word
        yield word, start_word, end_word
def get_word_times(text, start_time, end_time):
    # yield sentence, start_time, end_time  #if want to do it text-wise
    # return
    return get_word_times_equally_divided(text, start_time, end_time) # if want to use 
if __name__ == "__main__":
    video_name = "p01_s1_vid_parent_annotation_2019-03-06-11-36-09"
    #all_speakers = process_csv(video_name)
    #print(all_speakers)
    num_parts = 4
    process_csv(video_name, num_parts, lazy_update=False)
    # print(cmudict.words())
    # print("True" in cmudict.words())
    # print(get_syllables("Lets"))
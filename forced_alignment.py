#!/usr/bin/env python
# coding=utf-8
import json 
import os
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from moviepy.editor import AudioFileClip, concatenate_videoclips
from audio_handler import write_audio_of_all_videos
from process_transcript import process_csv
class Transcribe_project:
    def __init__(self,
                video_folder="./videos/",                               
                transcript_inputs_folder = "./transcripts/inputs/",     
                audio_folder = "./audios/", audio_prefix = "audio_",
                transcript_processed_folder = "./transcripts/processed_inputs/", transcript_processed_prefix = "processed_",
                output_folder = "./transcripts/outputs/", output_prefix = "output_"):
        super().__init__()
        self.video_folder = video_folder
        self.transcripts_inputs_folder = transcript_inputs_folder
        self.audio_folder = audio_folder
        self.audio_prefix = audio_prefix
        self.transcript_processed_folder = transcript_processed_folder
        self.transcript_processed_prefix = transcript_processed_prefix
        self.output_folder = output_folder
        self.output_prefix = output_prefix
    """
    Starts the transcription job by steps:
    -  STEP 1 : Processing the videos (combining them and extracting the audio)
    -  STEP 2 : Process the transcript (originally a .csv file) --> write a .text file with all the words
    -  STEP 3 : Use the audio and text file to force allign it and then write a json file with the results
    -  STEP 4 : Use the speaker order from above to insert it in the json file
    """
    def start_transcribe_job(self, filename, lazy_update_audio = True, lazy_update_processed_transcript = True):
        ## STEP 1: Processing the videos (combining them and extracting the audio)
        self.write_audio(filename, lazy_update_audio)
        ## STEP 2: Process the transcript (originally a .csv file) --> write a .text file with all the words
        speaker_labels = self.process_transcript(filename, lazy_update_processed_transcript)
        ## STEP 3: Use the audio and text file to force allign it and then write a json file with the results
        self.transcribe(filename)
        ## STEP 4: Use the speaker order from above to insert it in the json file
        self.add_speaker_labels(filename, speaker_labels)
        return f"\nSuccesfully processed the filename: {filename}\n"
    """
    Combines the videos found in self.video_folder/filename/
    Set lazy_update = True if you already got the audio and don't want to do the process again, as this takes time
    For more details in the implementation, see audio_handler.py
    """
    def write_audio(self, filename, lazy_update):
        write_audio_of_all_videos(filename, self.video_folder, self.audio_folder, self.audio_prefix, lazy_update)
    """
    Process the .csv file found in self.transcripts_inputs_folder/filename.csv by extracting the words 
    in all the sentences. It returns a list of the speaker_labels for every word said. 
    Set lazy_update = Trye if you already got the processed_transcript and you don't want to do it again. 
    For more details in implementation, see process_transcript.py
    """
    def process_transcript(self, filename, lazy_update):
        return process_csv(filename, self.transcripts_inputs_folder, self.transcript_processed_folder, self.transcript_processed_prefix, lazy_update)
    '''
    Does most of the work of forced allignment. It assumes that an audio file was already created by 
    self.write_audio and that there is already a processed transcript after running self.process_transcript
    '''
    def transcribe(self, filename):
        print("Starting task for filename: {}\n".format(filename))
        config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
        task = Task(config_string=config_string)
        task.audio_file_path_absolute = get_path(self.audio_folder, self.audio_prefix, filename, "mp3")
        task.text_file_path_absolute = get_path(self.transcript_processed_folder, self.transcript_processed_prefix, filename, "txt")
        task.sync_map_file_path_absolute = get_path(self.output_folder, self.output_prefix, filename, "json")
        print("Processing task...\n")
        # process Task
        ExecuteTask(task).execute()
        print("Taks processed. Writing output to {}".format(get_path(self.output_folder, self.output_prefix, filename, "json")))
        # output sync map to file
        task.output_sync_map_file()
    """
    When first starting with this file, run this function to create the necessary directories 
    you need for this to work. For more details in what are the meanings of this folders, see the README.
    """
    def make_necessary_folders(self):
        os.makedirs(self.video_folder)
        os.makedirs(self.audio_folder)
        os.makedirs(self.transcript_processed_folder)
        os.makedirs(self.transcripts_inputs_folder)
        os.makedirs(self.output_folder)
    """
    Uses the given speaker_labels to update our output from calling self.transcribe. The result is that
    the output json file contains the label of the speaker for every fragment.
    """
    def add_speaker_labels(self, filename, speaker_labels):
        output_path = get_path(self.output_folder, self.output_prefix, filename, "json")
        with open(output_path, 'r') as f:
            out = json.load(f)
            all_fragments = out["fragments"]
            for i, fragment in enumerate(all_fragments):
                fragment["speaker_label"] = speaker_labels[i]
        with open(output_path, 'w+') as json_to_write:
            json.dump(out, json_to_write, indent=4)

'''
Returns the complete path given a folder, prefix, name and type
Folder must end in "/"
For example, create_path("./audios/", "audio_", "file1", "mp3") returns "./audios/audio_file1.mp3"
'''
def get_path(folder, prefix, name, file_type):
    return "{}{}{}.{}".format(folder, prefix, name, file_type)


if __name__ == "__main__":
    project = Transcribe_project()
    ###### FIRST: IF YOU JUST GOT THIS FILE, please uncomment below (and run) ###########
    #project.make_folders()

    ###### SECOND: comment line above^ and uncomment this below (and run) #################
    #filename = "p01_s2_vid_parent_annotation_2019-03-13-11-16-16"
    #response = project.start_transcribe_job(filename)
    #print(response)

    ###### THIRD: Try to change the filename to other (valid) names and see if it works! ####
    ########### Your output JSON files will be located in /transcripts/outputs/##############
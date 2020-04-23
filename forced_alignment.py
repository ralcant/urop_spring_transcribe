#!/usr/bin/env python
# coding=utf-8
import json 
import os
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from videos_handler import mix_videos
from moviepy.editor import AudioFileClip, concatenate_videoclips
from audio_handler import write_audio_of_all_videos
from process_transcript import process_csv
class Transcribe_project:
    def __init__(self,
                video_folder="./videos/",                               #folders where to put 
                transcript_inputs_folder = "./transcripts/inputs/",     #folders where to put the data
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
    def start_transcribe_job(self, filename):
        ## We will do this in separate steps

        ## STEP 1: Processing the videos (combining them and extracting the audio)
        self.write_audio(filename)
        ## STEP 2: Process the transcript (originally a .csv file) --> write a .text file with all the words
        speaker_labels = self.process_transcript(filename)
        ## STEP 3: Use the audio and text file to force allign it and then write a json file with the results
        self.transcribe(filename)
        ## STEP 4: Use the speaker order from above to insert it in the json file
        self.add_speaker_labels(filename, speaker_labels)

        return f"\nSuccesfully processed the filename: {filename}\n"
    def write_audio(self, filename):
        write_audio_of_all_videos(filename, self.video_folder, self.audio_folder, self.audio_prefix)
    def process_transcript(self, filename):
        return process_csv(filename, self.transcripts_inputs_folder, self.transcript_processed_folder, self.transcript_processed_prefix)
    '''
    output_folder: where to store the folder. Should finish in "/"
    output_prefix: prefix of the name of the filename. For example, if the filename is "ab" and the
                prefix is xy_ then the output name will be "xy_ab"
    '''
    def transcribe(self, filename):
        ######## Before transcribing, we need to do some work ##########
        ################################################################
        # create Task object
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
    def add_speaker_labels(self, filename, speaker_labels):
        output_path = get_path(self.output_folder, self.output_prefix, filename, "json")
        print(os.path.exists(output_path))
        print(output_path)
        with open(output_path, 'r') as f:
            print(type(f))
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
VIDEO_INPUT_FOLDER = "p01_s1_vid__parent_annotation_2019-03-06-11-36-09"
VIDEO_OUTPUT_FOLDER = "videos/"


if __name__ == "__main__":
    #print("mixing videos!... \n")
    #mix_videos(min_clip, max_clip) #all videos
    #print("Finished mixing \n")
    #VIDEO_NAME = "video_from_{}_to_{}".format(min_clip, max_clip)
    #filename = "p01_s1_vid_parent_annotation_2019-03-06-11-36-09"
    filename = "p01_s2_vid_parent_annotation_2019-03-13-11-16-16"
    project = Transcribe_project()
    response = project.start_transcribe_job(filename)
    print(response)
    #PATH_VIDEO_TEST = f"./audios/audio_{video_name}.mp3"  
    #audio_file = AudioFileClip(PATH_VIDEO_TEST)
    #print("File duration : {}".format(audio_file.duration))
    #new_audio_path = "audios/{}.mp3".format(VIDEO_NAME)
    #print("Writing video audio to {}".format(new_audio_path))
    #audio_file.write_audiofile(new_audio_path)
    #transcript = "p01_s1_vid_parent_annotation_2019-03-06-11-36-09"
    #transcribe(video_name)
    #print(len(speaker_labels))
    #add_speaker_labels(speaker_labels, video_name)

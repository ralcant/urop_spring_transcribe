from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, concatenate_videoclips
import os
def extract_number_from_video(filename, termination = ".mp4"):
    #is_parsable = re.search("[[^0-9](\s)+.\s]", filename)
    #print(is_parsable)
    for i in range(len(filename)):
        char = filename[i]
        if char.isdecimal():
            last_decimal_index = len(filename) - len(termination) -1
            num_extracted = filename[i:last_decimal_index + 1]
            if num_extracted.isdecimal():
                return int(num_extracted)
            else:
                raise NameError("The filename {} should be of the form [PREFIX][NUMBER][TERMINATION]".format(filename))
    raise NameError("The filename {} didnt have any decimal digits".format(filename))
def write_audio_of_all_videos(name, video_folder="./videos/", 
                             audio_folder = "./audios/", audio_prefix = "audio_"):
    list_all_clips = []
    root_folder = ''.join([video_folder, name])
    all_elements = os.listdir(root_folder)
    only_mp4 = list(filter(lambda name: name.endswith(".mp4"), all_elements)) #only keeping the videos
    sorted_videos = sorted(only_mp4, key = extract_number_from_video) # ordering with the number, not with the str rep
                                                                      # 'video_2' goes before 'video_10'
    print("Trying to combine all audios!")
    for sub_video in sorted_videos:
        #print("adding video: {}".format(os.path.join(root_folder, sub_video)))
        print(".", end="") #just to keep track of where we are 
        clip_i = AudioFileClip(os.path.join(root_folder, sub_video))
        list_all_clips.append(clip_i)
    clips_combined = concatenate_audioclips(list_all_clips)
    print()
    output_audio = get_path(audio_folder, audio_prefix, name, "mp3")
    print("Clips combined, now writing to {}".format(output_audio))
    clips_combined.write_audiofile(output_audio)
'''
Returns the complete path given a folder, prefix, name and type
Folder must end in "/"
For example, create_path("./audios/", "audio_", "file1", "mp3") returns "./audios/audio_file1.mp3"
'''
def get_path(folder, prefix, name, file_type):
    return "{}{}{}.{}".format(folder, prefix, name, file_type)

if __name__ == "__main__":
    video_name = "p01_s1_vid_parent_annotation_2019-03-06-11-36-09"
    #video_name = "processed"
    write_audio_of_all_videos(video_name)
    #print(os.path.join("./video/abcd", "ahhh/",".mp4"))
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, concatenate_videoclips
import os
"""
Excract the 'number' of a filename. For example
>>> extract_number_from_video("clip-54.mp4") will return 54
>>> extract_number_from_video("_video-3.mp4") will return 
We use this to sort by number the several videos that could exist in a folder 
in the write_audio_of_all_videos function
"""
def extract_number_from_video(filename, termination = ".mp4"):
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
"""
Combines all the videos from video_folder/name/ and stores it as an mp3 audio 
expressed like audio_prefixed followed by the name. For example, if audio_prefix = 'audio_' 
and the name = "cool_videos" then this will write to an mp3 file called 'audio_cool_videos.mp3'
in the audio_folder folder.
"""
def write_audio_of_videos_in_parts(name, num_parts, video_folder="./videos/", 
                             audio_folder = "./audios/", audio_prefix = "audio_", lazy_update= True):
    all_parts_folder = f"{audio_folder}{name}/"
    get_subpart_path = lambda num_part: get_path(all_parts_folder, f"{audio_prefix}{num_parts}_part_", num_part, "mp3")
    os.makedirs(all_parts_folder, exist_ok=True) #creating necessary folder if necessary
    total_audio_path = get_path(all_parts_folder, audio_prefix, name, "mp3")
    if os.path.exists(total_audio_path) and lazy_update:
        print(f"The audio: {total_audio_path} already exists and lazy_update is set to {lazy_update}, so we are skipping this.")
    else:
        print(get_subpart_path(1))
        list_all_clips = []
        all_elements = os.listdir(f"{video_folder}{name}/")
        only_mp4 = list(filter(lambda name: name.endswith(".mp4"), all_elements)) #only keeping the videos
        sorted_videos = sorted(only_mp4, key = extract_number_from_video) # ordering with the number, not with the str rep
                                                                        # 'video_2' goes before 'video_10'        
        print("Trying to combine all audios!")
        for sub_video in sorted_videos:
            print(".", end="") #just to keep track of where we are 
            subclip = AudioFileClip(f"{video_folder}{name}/{sub_video}")
            list_all_clips.append(subclip)
        clips_combined = concatenate_audioclips(list_all_clips)
        print()
        print("Clips combined, now writing to {}".format(total_audio_path))
        clips_combined.write_audiofile(total_audio_path)       
    print(f"\nNow trying to divide the audio in {num_parts} parts \n") #TODO: check if the parts already exist
    divide_audio(total_audio_path, num_parts, all_parts_folder, audio_prefix)
    audio = AudioFileClip(total_audio_path)
    every_part_duration = (audio.duration)/num_parts
    audio.close()
    return every_part_duration
def divide_audio(audio_folder, num_parts, parts_folder, audio_part_prefix):
    audio = AudioFileClip(audio_folder)
    total_duration = audio.duration
    part_duration = total_duration/num_parts
    get_subpart_path = lambda num_part: get_path(parts_folder, f"{audio_part_prefix}{num_parts}_part_", num_part, "mp3")
    for i in range(1,num_parts+1):
        t_start, t_end = part_duration * (i-1), part_duration* i
        #audio = None
        #need to create the object again because subclip updates
        audio_i = audio.coreader().subclip(t_start, t_end) #the coreader() creates a new copy, each one for each piece
        print(f"Trying to write part #{i}\n")
        print(f"audio goes from {t_start}s to {t_end}s\n")
        audio_i.write_audiofile(get_subpart_path(i))
        #audio_i.close()
        print(f"Finished writing part #{i}")
    audio.close()
    print(f"Finish writing all parts in {parts_folder}")
'''
Returns the complete path given a folder, prefix, name and type
Folder must end in "/"
For example, create_path("./audios/", "audio_", "file1", "mp3") returns "./audios/audio_file1.mp3"
'''
def get_path(folder, prefix, name, file_type):
    return "{}{}{}.{}".format(folder, prefix, name, file_type)

if __name__ == "__main__":
    video_name = "p01_s1_vid_parent_annotation_2019-03-06-11-36-09"
    video_name =  "p01_s2_vid_parent_annotation_2019-03-13-11-16-16"
    num_parts = 4
    #write_audio_of_videos_in_parts(video_name, num_parts)
    audio = AudioFileClip(f"./audios/{video_name}/audio_{video_name}.mp3")
    audio_part_1 = AudioFileClip(f"./audios/{video_name}/audio_2_part_1.mp3")
    audio_part_2 = AudioFileClip(f"./audios/{video_name}/audio_2_part_2.mp3")
    print(audio.duration)
    print(audio_part_1.duration)
    print(audio_part_2.duration)
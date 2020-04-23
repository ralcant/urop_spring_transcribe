# urop_spring_transcribe
Computes forced-alignment for processing videos given .csv files with their respective transcript.

## Requirements
1. moviepy (https://zulko.github.io/moviepy/install.html)
2. aeneas (https://www.readbeyond.it/aeneas/docs/libtutorial.html#dependencies)

## Setup
1. Clone the repo by running `git clone https://github.com/ralcant/urop_spring_transcribe.git`
2. `cd urop_spring_transcribe`
3. Go to `forced_alignment.py` and see the bottom part, uncomment the line that says `HELLO, UNCOMMENT ME :)`, and run `python forced_alignment.py`. This will create the directories you need to run this script.
Now, go to the [folder of the videos of 5s](https://drive.google.com/drive/u/1/folders/1EiYlxLbYYj5Ms9Vw6bgfZ_B9YLhS9tfD) 
and download one of the folders (with all videos in it). For starters, you can try the first one, as that one worked well for me (Spoiler alert: not all of them did :( ). 
4. Once it downloads, unzip the folder and place it into the `videos` folder of the repo
5. Now go to the [drive of all the transcripts](https://drive.google.com/drive/u/1/folders/1dYyPtDaEaxvLU7e5XkH9LHHlzmYpEO_m) and download the csv file of THE SAME session you downloaded before.
6. They HAVE to have the same name (the only difference is that one of them is a folder and the other is a .csv file). Are you sure they are t-h-e s-a-m-e? 
7. Totally sure? Okay, fine. Continue.
8. Now we are all setup! (yayyyy)

## Run the code
1. Go to `forced_alignment.py` and comment the `project.make_folders()` line and uncomment the other 3 lines below.
2. Before running, change the value of `filename = ` to the name for the video and .csv you downloaded
3. Run `python forced_alignment.py` and see magic happen in front of your eyes.

## Problems
1. As surprising as this might sound, this has a <i>bug</i>. It worked well for me for the first file but 
after that I get the error 

`numpy.core._exceptions.MemoryError: Unable to allocate array with shape (35430069,) and data type float64`

aaaaand I personally don't know how to fix it, and trust me I've been trying. (insert sad face)

This is why I am coming to you.

## To-do
- [ ] Fix the bug commented above ^ 
- [ ] Try to see if there is a way to avoid downloading all the videos, as this takes a lot of time
- [ ] Try to see if maybe there is something different than `aeneas` that can help us do forced alignment?

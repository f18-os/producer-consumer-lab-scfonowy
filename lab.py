#! /usr/bin/env python3

import cv2
from threading import Thread, Semaphore, Lock
from random import shuffle

# producer/consumer queue class to make the rest of the lab a little nicer :)
# the put/get algorithm is just the standard one on the web (this one from wikipedia!)
class ProducerConsumerQueue():
    def __init__(self, size=10):
        self.queue = []
        self.insertSemaphore = Semaphore(value=0) # semaphore used to handle insertions
        self.removeSemaphore = Semaphore(value=size) # semaphore used to handle removals
        self.lock = Lock()
    
    def put(self, item):
        self.removeSemaphore.acquire()
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.insertSemaphore.release()
    
    def get(self):
        self.insertSemaphore.acquire()
        self.lock.acquire()
        item = self.queue.pop(0)
        self.lock.release()
        self.removeSemaphore.release()

        return item
    
    def empty(self):
        return len(self.queue) == 0

def extract_frames(outputBuffer, clip="clip.mp4"):
    global extractDone
    ### CODE FROM ASSIGNMENT (SLIGHTLY MODIFIED)
    # Initialize frame count 
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(clip)

    # read first image
    success,image = vidcap.read()
    
    
    while success:
        # add the frame to the buffer
        outputBuffer.put(image)
        print("Extracting frame {}".format(count))
       
        success,image = vidcap.read()
        count += 1

    print("Frame extraction complete")
    extractDone = True
    return

def convert_frames(inputBuffer, outputBuffer):
    global extractDone, convertDone
    count = 0
    while not (inputBuffer.empty() and extractDone):
        # get frame from buffer
        frame = inputBuffer.get()

        # convert the image to grayscale
        print('Converting frame {}'.format(count))
        grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # add the frame to the buffer
        outputBuffer.put(grayscaleFrame)
        count += 1
    convertDone = True
    return

def display_frames(inputBuffer):
    global convertDone
    ### CODE FROM ASSIGNMENT (SLIGHTLY MODIFIED)
    # initialize frame count
    count = 0

    # go through each frame in the buffer until the buffer is empty
    while not (inputBuffer.empty() and convertDone):
        # get frame from buffer
        frame = inputBuffer.get()
        print("Displaying frame {}".format(count))        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow("Video", frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()
    return

### main
# different frame buffers
colorFrameBuffer = ProducerConsumerQueue(size=10)
grayscaleFrameBuffer = ProducerConsumerQueue(size=10)

# signals for completion
extractDone = False
convertDone = False

# create threads, but don't start them
extractThread = Thread(target=extract_frames, args=(colorFrameBuffer, ))
convertThread = Thread(target=convert_frames, args=(colorFrameBuffer, grayscaleFrameBuffer, ))
# displayThread = Thread(target=display_frames, args=(colorFrameBuffer, ))

# shuffle the threads randomly enough
threads = [extractThread, convertThread]
shuffle(threads)

# start the threads
for thread in threads:
    thread.start()
display_frames(grayscaleFrameBuffer) # needs to be on main thread in macOS
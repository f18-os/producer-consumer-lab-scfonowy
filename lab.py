#! /usr/bin/env python3

import cv2
from threading import Thread, Semaphore, Lock
from random import shuffle
import time

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
        if self.insertSemaphore.acquire(timeout=3): # extra safeguard
            self.lock.acquire()
            item = self.queue.pop(0)
            self.lock.release()
            self.removeSemaphore.release()

            return item
        
        else:
            return None
    
    def empty(self):
        return len(self.queue) == 0

def extract_frames(outputBuffer, clip="clip.mp4"):
    print("Extraction thread started...")
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
    outputBuffer.put(None)
    return

def convert_frames(inputBuffer, outputBuffer):
    print("Conversion thread started...")
    count = 0

    # get initial frame
    frame = inputBuffer.get()

    while frame is not None:
        # convert the image to grayscale
        print('Converting frame {}'.format(count))
        # took this from the assignment, too! wow!!
        grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # add the frame to the buffer
        outputBuffer.put(grayscaleFrame)
        count += 1

        # get frame from buffer
        frame = inputBuffer.get()

    print ("Frame conversion complete")
    outputBuffer.put(None)
    return

def display_frames(inputBuffer):
    print("Display thread started...")
    ### CODE FROM ASSIGNMENT (SLIGHTLY MODIFIED)
    # initialize frame count
    count = 0

    # get initial frame
    frame = inputBuffer.get()

    # code used to approximate 24 fps from professor's email
    # on course mailing list
    frameInterval_s = 0.042         # inter-frame interval, in seconds

    nextFrameStart = time.time()

    # go through each frame in the buffer until the buffer is empty
    while frame is not None:

        print("Displaying frame {}".format(count))        

        # display the image in a window called "video" 
        cv2.imshow("Video", frame)

        # delay beginning of next frame display (sampled from email)
        delay_s = nextFrameStart - time.time()
        nextFrameStart += frameInterval_s
        delay_ms = int(max(1, 1000 * delay_s))
        print ("delay = %d ms" % delay_ms)
        if cv2.waitKey(delay_ms) and 0xFF == ord("q"):
            break

        count += 1
        
        # get frame from buffer
        frame = inputBuffer.get()

    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()
    return

### main
# different frame buffers
colorFrameBuffer = ProducerConsumerQueue(size=10)
grayscaleFrameBuffer = ProducerConsumerQueue(size=10)

# create threads, but don't start them
extractThread = Thread(target=extract_frames, args=(colorFrameBuffer, ))
convertThread = Thread(target=convert_frames, args=(colorFrameBuffer, grayscaleFrameBuffer, ))
displayThread = Thread(target=display_frames, args=(grayscaleFrameBuffer, ))

# shuffle the threads randomly enough
threads = [extractThread, convertThread, displayThread]
shuffle(threads)

# start the threads
for thread in threads:
    thread.start()
#display_frames(grayscaleFrameBuffer) # needs to be on main thread in macOS

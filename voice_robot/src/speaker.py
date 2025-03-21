#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import vosk
import pyaudio
import json

model = vosk.Model(lang="en-us")


rec = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192)
output_file_path = "recognized_text.txt"



class speaker_node:
    def __init__(self) -> None:
        rospy.init_node("speaker_node", anonymous=True)
        self.pub = rospy.Publisher("/nadeef_command", String, queue_size=1)
    def send(self, command):
        self.pub.publish(command)
        rospy.loginfo("Command: " + command)
    def run(self):
        rospy.loginfo("Speaker node is running")
        while not rospy.is_shutdown():
            
            with open(output_file_path, "w") as output_file:
                print("Listening for speech. Say 'Terminate' to stop.")
    # Start streaming and recognize speech
                while True:
                    data = stream.read(4096)#read in chunks of 4096 bytes
                    if rec.AcceptWaveform(data):#accept waveform of input voice
                # Parse the JSON result and get the recognized text
                        result = json.loads(rec.Result())
                        recognized_text = result['text']
                        self.send(recognized_text)
            # Write recognized text to the file
                        output_file.write(recognized_text + "\n")
                        print(recognized_text)
            
            # Check for the termination keyword
                        if "terminate" in recognized_text.lower():
                            print("Termination keyword detected. Stopping...")
                            break
            # Stop and close the stream
            stream.stop_stream()
            stream.close()

# Terminate the PyAudio object
            p.terminate()
            rospy.sleep(1)

if __name__=='__main__':
    node = speaker_node()
    node.run()
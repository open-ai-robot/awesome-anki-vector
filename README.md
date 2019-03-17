<img src="https://user-images.githubusercontent.com/799578/52912304-8c5aae80-32ea-11e9-8a04-b92ca50a7cb7.jpg" width="480"/>

# Table of contents
- [Table of contents](#table-of-contents)
- [Anki Vector AI++](#anki-vector-ai)
- [Object detection](#object-detection)
    - [Run the code yourself](#run-the-code-yourself)
    - [How it works](#how-it-works)
- [Shoes placed](#shoes-placed)

# Anki Vector AI++
[Anki Vector](https://www.anki.com/en-us/vector) - The Home Robot With Interactive AI Technology.

Well, I bought this little guy at 10 Feb 2019, if you want a robot pet, and you want to do some AI programming on it, then I highly recommend you to get Anki Vector.

I build this project to share my codes and docs.


# Object detection
This program is to enable Vector to detect objects with its camera, and tell us what it found. 

We take a photo from Vector's camera, then post to Google Vision Service, then Google Vision Service returns the object detection result, 
finally, we turn all the label text into a sentence and send to Vector so that Vector can say it out loud.

Here are some demo videos:

1. Vector detected a watch on my desk.

[![image1](https://user-images.githubusercontent.com/799578/52912513-5834bd00-32ed-11e9-82a8-8432cf50c3b6.png)](https://youtu.be/Zee8vcq2-Vc)

2. Vector detected a bear on my phone’s album.

[![image2](https://user-images.githubusercontent.com/799578/52912527-7dc1c680-32ed-11e9-8aaf-f2c16b29750b.png)](https://youtu.be/fjIAyzzA3FM)

3. Vector detected a game controller on my desk.

[![image3](https://user-images.githubusercontent.com/799578/52912537-9df18580-32ed-11e9-8ee5-a1b3db52298a.png)
](https://youtu.be/fzhcvPQBTBY)

4. Vector was exploring on my desk as usual and randomly tell me what it found. 

[![image4](https://user-images.githubusercontent.com/799578/53691347-e5304980-3db6-11e9-8393-78ddd1233295.png)](https://youtu.be/7zd7-YOIkvc)

Well, let's see how to do it.

### Run the code yourself
1. Install [Vector Python SDK](https://developer.anki.com/vector/docs/install-macos.html). You can test the SDK by running any of the example from [anki/vector-python-sdk/examples/tutorials/](https://github.com/anki/vector-python-sdk/tree/master/examples/tutorials) 
2. Set up your Google Vision account. Then follow the [Quickstart](https://cloud.google.com/vision/docs/quickstart-client-libraries) to test the API.
3. Clone this project to local. It requires Python 3.6+.
4. Don forget to set Google Vision environment variable GOOGLE_APPLICATION_CREDENTIALS to the file path of the JSON file that contains your service account key.  e.g. `export GOOGLE_APPLICATION_CREDENTIALS="/Workspace/Vector-vision-62d48ad8da6e.json"`
5. Make sure your computer and Vector in the same WiFi network. Then run `python3 object_detection.py`.
6. If you are lucky, Vector will start the first object detection, it will say "My lord, I found something interesting. Give me 5 seconds."

### How it works
1. Connect to Vector with `enable_camera_feed=True`, because we need the [anki_vector.camera](https://developer.anki.com/vector/docs/generated/anki_vector.camera.html) API.
```python
robot = anki_vector.Robot(anki_vector.util.parse_command_args().serial, enable_camera_feed=True)
```

2. We'll need to show what Vector see on its screen.

```python
def show_camera():
    print('Show camera')
    robot.camera.init_camera_feed()
    robot.vision.enable_display_camera_feed_on_face(True)
```

and close the camera after the detection.

```python    
def close_camera():
    print('Close camera')
    robot.vision.enable_display_camera_feed_on_face(False)
    robot.camera.close_camera_feed()
```
3. We'll save take a photo from Vector's camera and save it later to send to Google Vision.

```python
def save_image(file_name):
    print('Save image')
    robot.camera.latest_image.save(file_name, 'JPEG')
```
4. We post the image to Google Vision and parse the result as a text for Vector.

```python
def detect_labels(path):
    print('Detect labels, image = {}'.format(path))
    # Instantiates a client
    # [START vision_python_migration_client]
    client = vision.ImageAnnotatorClient()
    # [END vision_python_migration_client]

    # Loads the image into memory
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    res_list = []
    for label in labels:
        if label.score > 0.5:
            res_list.append(label.description)

    print('Labels: {}'.format(labels))
    return ', or '.join(res_list)
```
5. Then we send the text to Vector and make it say the result.

```python
def robot_say(text):
    print('Say {}'.format(text))
    robot.say_text(text)
```
6. Finally, we put all the steps together.

```python
def analyze():
    stand_by()
    show_camera()
    robot_say('My lord, I found something interesting. Give me 5 seconds.')
    time.sleep(5)

    robot_say('Prepare to take a photo')
    robot_say('3')
    time.sleep(1)
    robot_say('2')
    time.sleep(1)
    robot_say('1')
    robot_say('Cheers')

    save_image(image_file)
    show_image(image_file)
    time.sleep(1)

    robot_say('Start to analyze the object')
    text = detect_labels(image_file)
    show_image(image_file)
    robot_say('Might be {}'.format(text))

    close_camera()
    robot_say('Over, goodbye!')

```
7. We want Vector randomly active the detection action, so we wait for a random time (about 30 seconds to 5 minutes) for the next detection.

```python
def main():
    while True:
        connect_robot()
        try:
            analyze()
        except Exception as e:
            print('Analyze Exception: {}', e)

        disconnect_robot()
        time.sleep(random.randint(30, 60 * 5))
```

8. When Vector success to active the detection action, you should see logs:

```shell
2019-02-17 21:55:42,113 anki_vector.robot.Robot WARNING  No serial number provided. Automatically selecting 009050ae
Connect to Vector...
2019-02-17 21:55:42,116 anki_vector.connection.Connection INFO     Connecting to 192.168.1.230:443 for Vector-M2K2 using /Users/gaolu.li/.anki_vector/Vector-M2K2-009050ae.cert
2019-02-17 21:55:42,706 anki_vector.connection.Connection INFO     control_granted_response {
}

Show camera
Say My lord, I found something interesting. Give me 5 seconds.
Say Prepare to take a photo
Say 3
Say 2
Say 1
Say Cheers
Save image
Show image = /Workspace/labs/Anki-Vector-AI/resources/latest.jpg
Display image on Vector's face...
Say Start to analyze the object
Detect labels, image = /Workspace/labs/Anki-Vector-AI/resources/latest.jpg
Labels: [mid: "/m/08dz3q"
description: "Auto part"
score: 0.6821197867393494
topicality: 0.6821197867393494
]
Show image = /Workspace/labs/Anki-Vector-AI/resources/latest.jpg
Display image on Vector's face...
Say Might be Auto part
Close camera
Say Over, goodbye!
2019-02-17 21:56:12,460 anki_vector.connection.Connection INFO     control_lost_event {
}

2019-02-17 21:56:12,460 anki_vector.robot.Robot WARNING  say_text cancelled because behavior control was lost
2019-02-17 21:56:12,461 anki_vector.util.VisionComponent INFO     Delaying disable_all_vision_modes until behavior control is granted
2019-02-17 21:56:12,707 anki_vector.connection.Connection INFO     control_granted_response {
}

Vector disconnected

```

You can find the latest photo that Vector uses to detention in `resources/latest.jpg`.


# Shoes placed
This program is to enable Vector to place shoes for us. Vector will place our shoes when we're not at home, so we can leave home without worry about the shoes, especially when we're in a hurry.

This program is in research. I'll share the plan, the design, the docs, the codes here. I highly recommend you make an issue on GitHub so we can talk about it further if you're interesting, any help is welcome!

The design proposal is in this Google doc. https://docs.google.com/document/d/10TQEdbIdcvCW8gNAUvVVSe1YxzFxsQExP_X33M3_Aos/edit?usp=sharing

![image](https://user-images.githubusercontent.com/799578/54486068-ce611b00-48bd-11e9-810e-f278f285005e.png)


Here is a draft demo video I made to give you guys a sense of the program:

[![image](https://user-images.githubusercontent.com/799578/54484263-bbd6e980-489d-11e9-97a5-aa6eaafe8b80.png)](https://youtu.be/Wj_TB6Mr8qA)


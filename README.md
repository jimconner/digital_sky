# Digital Sky

Digital Sky is a LED lighting project. 

<Pretty animated GIF goes here>

Indoor lighting is generally pretty sucky. If it wasn't there wouldn't be a booming market in SAD lamps to help keep the winter blues at bay. 

Outdoor lighting levels are not constant. Sometimes the sun will come out from behind a cloud and bathe you in glorious rays. Sometimes in the evenings the sky looks like it's on fire - all red and gold. When there's a storm brewing the world turns grey and purple.

People want a lot of different things from their indoor lighting depending on what task they're doing. In a home environment warm white is the most popular choice, but in a workshop environment a daylight white gives better colour balance and helps keep people alert. Photography and filming call for very specific colour temperatures, whereas parties and general decoration call for a whole range of different colours and intensities.

The goal of the Digital Sky project is to have one set of lights which can do it all.


A set of YouTube videos describe the project hardware in detail.

Part 0: https://www.youtube.com/watch?v=tIFp80Za02Q

Part 1: https://www.youtube.com/watch?v=aaL2gH_QrJY

Part 2: https://www.youtube.com/watch?v=8ieTPU6f_Ws

Part 3: https://www.youtube.com/watch?v=-cvN6kNjJMA

Part 4: The video that will describe how this software all works :-)

This repository contains the software component to run the Digital Sky lamps.

## The Software
The Digital Sky control software uses jgarff's rpi_ws281x library ( https://github.com/jgarff/rpi_ws281x ) for the low level strip control.
This software is built on the Twisted Matrix Python Asychronous Event-Driven Framework ( https://twistedmatrix.com/trac/ )

The controller software works in a way that is similar music production software (Ableton, garageband, cuebase etc).
All 'animation' plugins are required to have an emit_row() function, which when called will emit the pixel values for an entire strip of RGBW pixels.
Each time the emit_row() function is called, they must emit the next row in their sequence.
Multiple animations may be running at the same time.
The maximum pixel colour value from each animation will be the one which is displayed (i.e. if one animation sets green to 50% and another sets 75% then the result will be 75%)

A similar set of 'strip_animations' are for setting the values for the Warm-White, Natural-White, Daylight-White and Ice-Blue elements on each lamp. As with the RGBW animations, the highest value for each pixel channel will be the one which gets displayed.

(in the future, when I write more code) Filters may be attached to the output of any 'animation' or 'strip_animation' to perform simple operations such as reducing brightness or shifting colour balance. 

The Digital Sky controller software also subscribes to an MQTT message bus and listens out for messages sent by a Snips voice assistant. Snips runs totally locally on the raspberry PI and allows for voice control over the lamps.

This link probably won't work for you because I haven't published the agent yet, but I'm putting it here for myself so that I don't loose it.

https://console.snips.ai/assistant/proj_VXNK6aedOw4/app/skill_o6OlPAP64KP/edit 



## Contributing

Yes please. Contributions welcome through normal git workflow (fork, pull request etc) providing that they are also MIT licensed.  
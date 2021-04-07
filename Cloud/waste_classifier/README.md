## Materials needed

3x LEDs
1x Button
4x Resistors
1x Breadboard

Setup above equipment according to pin layout in `rpi_waste_classifier.py`

Download model from https://nusu-my.sharepoint.com/:u:/r/personal/e0311162_u_nus_edu/Documents/classification%20model/trash-dataset-v3%20TFLite.zip?csf=1&web=1

Unzip and rename folder to `model` and place in the same directory as `rpi_waste_classifier.py`


Requirements
```
pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl

pip3 install lobe
```


Run program with python3

Current drawbacks

- Label for `no item` added, works sometimes


## Dataset used

https://github.com/garythung/trashnet 

`dataset-resized.zip`

The categories cardboard, glass, metal, paper, plastic was placed under `recyclable` label, while trash was placed under `general trash` label. 

There is a much greater set of images that for the `recyclable` label, so by default the model might predict `recyclable` when shown something random.

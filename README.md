# PlantIdentifier
<h2>Creates a PowerPoint presentation from an input sequence of images</h2>
<p>- Each slide of the PowerPoint will contain one image and its matching plant name</p>

<b>Dependencies:</b>
```
tensorflow, python-pptx, PIL, OpenCV, numpy, scikit-learn
```
<h2>Instructions:</h2>
<p>
- Drag all your photos into the <b>id_dir</b> directory (no matter the image format)
- Download this dataset: [label](https://zenodo.org/record/4726653#.ZE5bJC9BxQK) and drag it into the main directory
- Open a terminal window in the main directory, run <b>python main.py true</b> to train the model, then <b>python main.py false</b> to evaluate your images and create the resulting PowerPoint
- All photos will be converted to Portable Pixmap Format, original format moved to <b>wrong_formats</b>
</p>
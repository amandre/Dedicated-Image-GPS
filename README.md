# Dedicated Image GPS
v1.0.0 (beta)

The application is an innovative implementation of the graphical password scheme which uses the user's image to create the sequence of coordinates.
It is based on CD-GPS (Click-Draw GPS) but the additional level of authentication is the personalized image (which needs to be uploaded from the client's device).

### Installation
The application doesn't need any installation procedure because the whole script can be run using main script.
```
python main.py
```

### Used technologies
The application was created in Python v2.7 using mainly Tkinter, PIL and pymongo libraries.

### future improvements
Application needs to store the pieces of the images used for password creation. There is a need to distinguish not only the provided sequences but the images as well.

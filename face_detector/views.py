from email.mime import image
import os
from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import cv2
import urllib
import numpy as np

FACE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_frontalface_default.xml".format(base_path=os.path.abspath(os.path.dirname(__file__)))

def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        image = cv2.imread(path)
    # otherwise, the image does not reside on disk
    else:	
        # if the URL is not None, then download the image
        if url is not None:
            #resp = urllib.urlopen(url)
            resp = urllib.request.urlopen(url)
            data = resp.read()
        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            data = stream.read()
        # convert the image to a NumPy array and then read it into
        # OpenCV format
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image

class FaceDetectionView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        data = {'message':'Hello world'}
        return JsonResponse(data)

    def post(self, request):
        data = {"success": False}

        if request.FILES.get("image", None) is not None:
            image = _grab_image(stream=request.FILES["image"])
        else:
            url = request.POST.get("url", None)
            if url is None:
                data["error"] = "Not Url provided"
                return JsonResponse(data)
                
            image = _grab_image(url=url)

        # convert the image to grayscale, load the face cascade detector,
        # and detect faces in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        rects = detector.detectMultiScale(gray, 1.3, 5)

        # construct a list of bounding boxes from the detection
        rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in rects]
        # update the data dictionary with the faces detected
        data.update({"num_faces": len(rects), "faces": rects, "success": True})
        # return a JSON response
        return JsonResponse(data)

    def put(self, request):
        pass

    def delete(self, request):
        pass
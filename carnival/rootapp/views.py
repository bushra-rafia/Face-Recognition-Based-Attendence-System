from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from .forms import SetcameraForm,UsersForm
from .models import Setcamera,Users,attendance
from django.contrib.auth.decorators import login_required
from datetime import datetime


class Home(TemplateView):
    template_name = 'login.html'

@login_required
def capture(request):
    return render (request,'capture.html')

@login_required
def dashboardView(request):
    return render (request,'dashboard.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            form.cleaned_data.get('username')
            ##messages.success(request, f'Your account has been successfully created!Log in now')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})



@login_required
def user_list(request):
    user = Users.objects.all()
    return render(request, 'user_list.html', {
        'user': user
    })
@login_required
def upload_user(request):
    if request.method == 'POST':
        form = UsersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UsersForm()
    return render(request, 'upload_user.html', {
        'form': form
    })


@login_required
def delete_user(request, pk):
    if request.method == 'POST':
        user = Users.objects.get(pk=pk)
        user.delete()
    return redirect('user_list')


@login_required
def edit_user(request, pk) :
    user = Users.objects.get(pk=pk)
    return render(request,"edit_user.html", {'user': user})


@login_required
def update(request, pk) :
    user = Users.objects.get(pk=pk)
    form = UsersForm(request.POST,request.FILES, instance= user)
    if form.is_valid():
        form.save()
        return redirect('/users/')
    return render(request,"edit_user.html", {'user': user})


@login_required
def attend(request) :
    r =attendance.objects.last()
    a = Users.objects.get(u_id=r.u_id)
    #print(a.img)
    #print(a)
    return render(request, 'attend.html',{'a': a})

@login_required
def cameralist(request):
    camera = Setcamera.objects.all()
    return render(request, 'cameralist.html', {
        'camera': camera
    })
@login_required
def upload_camera(request):
    if request.method == 'POST':
        form = SetcameraForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cameralist')
    else:
        form = SetcameraForm()
    return render(request, 'upload_camera.html', {
        'form': form
    })
@login_required
def delete_camera(request, pk):
    if request.method == 'POST':
        x = Setcamera.objects.get(pk=pk)
        x.delete()
    return redirect('cameralist')

@login_required
def edit_camera(request, pk) :
    x = Setcamera.objects.get(pk=pk)
    return render(request,"edit_camera.html", {'x': x})

@login_required
def update_camera(request, pk) :
    x =Setcamera.objects.get(pk=pk)
    form = SetcameraForm(request.POST,request.FILES, instance= x)
    if form.is_valid():
        form.save()
        return redirect('/cameralist/')
    return render(request,"edit_camera.html", {'x': x})



@login_required
def camera_recognise(request):
    import os
    import cv2
    import requests
    import numpy as np
    import face_recognition
    from os.path import splitext
    x = request.POST['choice']

    # make a list of all the available images
    images = os.listdir('media/user')
    known_face_encodings = []
    known_face_names = []

    for i in os.listdir('media/user'):
        pic = face_recognition.load_image_file('media/user/' + i)
        known_face_encodings.append(face_recognition.face_encodings(pic)[0])
        known_face_names.append(i[:i.rfind('_')])
        if not len(known_face_encodings):
            print(i, "can't be encoded")
            continue

    x = 'rtsp:' + x + '/h264_ulaw.sdp'
    video_capture = cv2.VideoCapture(x)


    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]



        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                root = "Unknown"

                # user_name = splitext(known_face_names[i])[0]
                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)



                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                    root, ext = os.path.splitext(name)
                    # print(root)
                    if (root != "unknown"):
                        now = datetime.now()
                        dt = now.strftime("%d/%m/%Y")
                        tym = now.strftime(" %H:%M:%S")
                        user = attendance(u_id=root,date=dt,time=tym)
                        user.save()


                face_names.append(root)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Release handle to the webcam
            video_capture.release()
            cv2.destroyAllWindows()

@login_required
def user_recognise(request):
    import os
    import cv2
    import requests
    import numpy as np
    import face_recognition
    from os.path import splitext


    # make a list of all the available images
    images = os.listdir('media/user')
    known_face_encodings = []
    known_face_names = []

    for i in os.listdir('media/user'):
        pic = face_recognition.load_image_file('media/user/' + i)
        known_face_encodings.append(face_recognition.face_encodings(pic)[0])
        known_face_names.append(i[:i.rfind('_')])
        if not len(known_face_encodings):
            print(i, "can't be encoded")
            continue



    video_capture = cv2.VideoCapture(0)
    #video_capture = cv2.VideoCapture('rtsp:192.168.0.126:8080/h264_ulaw.sdp')

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                root = "Unknown"

                # user_name = splitext(known_face_names[i])[0]
                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                    root, ext = os.path.splitext(name)
                    # print(root)
                    if (root != "unknown"):
                        now = datetime.now()
                        dt = now.strftime("%d/%m/%Y")
                        tym = now.strftime(" %H:%M:%S")
                        user = attendance(u_id=root,date=dt,time=tym)
                        user.save()

                    """if attendance.objects.filter(u_id=root,date=dt).exists():
                            pass
                        else
                            user.save()"""

                face_names.append(root)


        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Release handle to the webcam
            video_capture.release()
            cv2.destroyAllWindows()



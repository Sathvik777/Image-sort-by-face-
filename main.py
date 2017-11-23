import os
from itertools import permutations

import numpy as np
from os.path import basename
import  http.client, base64, json
from matplotlib import pyplot as plt

import  face_recognition

import api_client

face_encodings_by_filename = {}

face_encodings_by_personID = {}

personid_with_list_of_faceids = {}

images_directory = "cached_images"



def init_face_encodings_from_images():

    for filename in os.listdir(images_directory):
        try:
            add_encoding_by_filename(images_directory + "/" + filename)
        except:
            os.remove(images_directory + "/" + filename)




def add_encoding_by_filename(filename):
    if filename.endswith(".npy"):
        face_encodings_npy = np.load(filename)
        base_filename = basename(filename)
        face_encodings_by_filename[base_filename] = face_encodings_npy


def list_face_ids_matching_current_person():
    #current_person_encodings = face_encodings_by_personID[current_person[0]]
    for personid in face_encodings_by_personID:
        for current_faceid in face_encodings_by_filename:
            list_of_face_ids =[]
            match = face_recognition.compare_faces( face_encodings_by_personID[personid], face_encodings_by_filename[current_faceid], 0.55)
            #print(match)


            if(match[0]):
                face_id_without_npy = int(current_faceid.split('.')[0])

                if (face_id_without_npy == 1509447475):
                    print(personid)

                if personid in personid_with_list_of_faceids:
                    list_of_face_ids = personid_with_list_of_faceids[personid]
                    list_of_face_ids.append(face_id_without_npy)
                    personid_with_list_of_faceids[personid] = list_of_face_ids
                else:
                    list_of_face_ids.append(face_id_without_npy)
                    personid_with_list_of_faceids[personid] = list_of_face_ids

    build_json_body_and_post()




def add_face_encodings_by_personID(personId,filenames):
    #TODO: loop over all files but think about resources

    filename = str(filenames[0])+".npy"
    if filename in face_encodings_by_filename:
        face_encodings_by_personID[personId] = face_encodings_by_filename[filename]


def load_reff_face_encodings():
    data = api_client.get_all_personId()
    for person in data['listOfPersons']:
        add_face_encodings_by_personID(person['person'],person['faceIds'])

    list_face_ids_matching_current_person()



def build_json_body_and_post():
    json_body_list = []
    for current_person in personid_with_list_of_faceids:

        json_element = {
            'personId': current_person,
            'listOfFaces': personid_with_list_of_faceids[current_person]
        }
        json_body_list.append(json_element)

    print(json_body_list)

    #api_client.update_faces_of_every_person(json_body_list)



if __name__ == "__main__":
    init_face_encodings_from_images()

    load_reff_face_encodings()


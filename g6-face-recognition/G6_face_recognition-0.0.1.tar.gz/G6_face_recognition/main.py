from G6_face_recognition.face_matching import *
from G6_face_recognition.encode_face_model import *
from G6_face_recognition.feature_encode import *
import os
import sys
import argparse





def face_model_train(train_db_path, train_encoding_model_path):
    if os.path.exists(train_db_path):
        if os.path.exists(train_encoding_model_path):
            face_names = face_test_model(train_db_path, train_encoding_model_path)
            return face_names
        else:

            return "encoding model path not exist"
    else:

        return "image database path not exist"


def face_model_test(test_encoding_model_path, image_path):
    if os.path.exists(test_encoding_model_path):
        if os.path.exists(image_path):
            face_name = face_recg(test_encoding_model_path, image_path)
            return face_name
        else:

            return "image path not exist"
    else:

        return "image model path not exist"


def face_image_encoding(image_path):
    if os.path.exists(image_path):
        face_image_encoding_result = engroup(image_path)
        return face_image_encoding_result
    else:
        
        return "image path not exist"


def main():
    parser = argparse.ArgumentParser(
        description='CLI - face recognition.')
    parser.add_argument('-trn', '--train_encoding_model_path', type=str, help='train encoding model path')
    parser.add_argument('-td', '--train_db_path', type=str, help='train image database path')
    parser.add_argument('-tn', '--test_encoding_model_path', type=str, help='test encoding model path')
    parser.add_argument('-i', '--image_path', type=str, help='image path')

    if len(sys.argv) < 2:
        print('Specify a key to use')
        sys.exit(1)

    # Optional bash tab completion support
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    args = parser.parse_args()
    if args.train_db_path != None and args.train_encoding_model_path != None:
        face_model_train(args.train_db_path, args.train_encoding_model_path)
    if args.test_encoding_model_path != None and args.image_path != None:
        face_model_test(args.test_encoding_model_path, args.image_path)
    if args.image_path != None:
        face_image_encoding(args.image_path)




if __name__ == "__main__":
    main()


from allosaurus.app import read_recognizer
from allosaurus.download import download_model
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser('Phone recognizer')
    parser.add_argument('--device_id', type=int, default=-1, help='specify cuda device id to use, -1 means no cuda and will use cpu for inference')
    parser.add_argument('--model', type=str, default='latest', help='specify which model to use. default is to use the latest model')
    parser.add_argument('--lang_id', type=str, default='ipa',help='specify which language inventory to use for recognition. default is to use all phone inventory')
    parser.add_argument('-i', '--input', type=str, help='specify your input wav file')

    args = parser.parse_args()

    # download model if not exists
    download_model(args.model)

    # create recognizer
    recognizer = read_recognizer(args)

    # run inference
    phones = recognizer.recognize(args.input, args.lang_id)

    print(phones)
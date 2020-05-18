from pathlib import Path

exe_relate_dir = Path("/content/gdrive/My Drive/Colab_Codes/deep_t2i/exe_relate")
data_dir = Path("/root/data")

tiny_data_dir = Path("../exe_relate/tiny_data")
model_dir = exe_relate_dir/"models"
results_dir = exe_relate_dir/"results"

class Birds():
    '''
    data_dir -
        tmp -
        imgs -
        caps -
        images.txt
        bounding_boxes.txt
        train_test_split.txt
    '''
    img_url = "http://www.vision.caltech.edu/visipedia-data/CUB-200-2011/CUB_200_2011.tgz"
    cap_url = "https://drive.google.com/uc?export=download&id=1O_LtUP9sch09QH3s_EBAgLEctBQ5JBSJ"
    data_dir = data_dir/"birds"
    tiny_data_dir = tiny_data_dir/"birds"
    large_model_dir = model_dir/"large_birds"
    tiny_model_dir = model_dir/"tiny_birds"
    large_results_dir = results_dir/"large_birds"

class AnimeHeads():
    '''
    data_dir -
        tmp -
        imgs
        tags.csv
    '''
    url = "https://drive.google.com/uc?export=download&id=1tpW7ZVNosXsIAWu8-f5EpwtF3ls3pb79"
    data_dir = data_dir/"anime_heads"
    tiny_data_dir = tiny_data_dir/"anime_heads"
    large_model_dir = model_dir/"large_anime_heads"
    tiny_model_dir = model_dir/"tiny_anime_heads"
    large_results_dir = results_dir/"large_anime_heads"
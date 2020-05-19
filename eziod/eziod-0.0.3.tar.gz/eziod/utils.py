import os
import requests
import numpy as np
from sklearn.metrics import auc
import matplotlib.pylab as plt

def download_data(download_url, dst_file):
    down_res = requests.get(url=download_url, stream=True)
    file_size = int(down_res.headers['Content-Length'])
    chunk_size = 5120
    total = 0
    ratio = 0
    with open(dst_file, "wb") as f:
        if chunk_size > file_size:
            f.write(down_res.content)
            ratio = 1
            print(os.path.basename(dst_file) + '[' + '>' * (int(ratio * 60)) + ']{:.0f}%'.format(ratio * 100))
        else:
            for chunk in down_res.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    total += chunk_size
                    if total / file_size > ratio + (1 / 20):
                        ratio = total / file_size
                        print(os.path.basename(dst_file) + '[' + '>' *(int(ratio * 60)) + ']{:.0f}%'.format(ratio *100))
    if ratio < 0.995:
        print(os.path.basename(dst_file) + '[' + '>' * (int(60)) + ']{:.0f}%'.format(100))



def bbox_overlaps(boxes1, boxes2):
    # boxes1 m*4
    # boxes2 n*4
    ious = np.empty((len(boxes1), len(boxes2)))
    for i in range(len(boxes1)):
        x1, y1, x2, y2 = boxes1[i]
        min_x = np.maximum(x1, boxes2[:, 0])
        min_y = np.maximum(y1, boxes2[:, 1])
        max_x = np.minimum(x2, boxes2[:, 2])
        max_y = np.minimum(y2, boxes2[:, 3])
        insert_x = np.maximum(0, max_x - min_x)
        insert_y = np.maximum(0, max_y - min_y)
        ious[i] = (insert_x * insert_y) / ((y2 - y1) * (x2 - x1) + (boxes2[:, 3] - boxes2[:, 1]) * (boxes2[:, 2] - boxes2[:, 0]) - (insert_x * insert_y))
    return ious


# 计算pr值
def caculate_pr(pred, gt_img_infos, iou_threshold = 0.2, num_c = 1):
    TP_FP_list = [[] for _ in range(num_c)]
    npos = [0 for _ in range(num_c)]
    count = [0 for _ in range(num_c)]

    gt = {os.path.basename(i.img_path) : [[j.box for j in i.objs], [j.class_index for j in i.objs]] for i in gt_img_infos}

    for c in range(num_c):
        TP_FP = []
        for k in pred:
            pred_box, pred_conf = pred[k]
            gt_box, gt_cls = gt[k]

            # 真实标签中等于c的
            gt_cls = gt_cls[gt_cls == c]
            gt_box = gt_box[gt_cls == c, :]

            # 预测标签中等于c的
            pred_conf = pred_conf[pred_conf.argmax(1) == c, :][:, c]
            pred_box = pred_box[pred_conf.argmax(1) == c, :]

            # 待预测的目标的个数
            npos[c] += len(gt_cls)

            # 计算真实目标喝预测目标之间的iou
            overlaps = bbox_overlaps(gt_box, pred_box)

            # 真实目标框是否已经被匹配
            dets = np.zeros(len(gt_cls))
            for j in range(len(pred_conf)):
                # 取第j个预测框对全部真实框的iou
                overlap = overlaps[:, j]
                if len(overlap) !=0:
                    # iou最大的真实框的索引
                    max_overlap_index = np.argmax(overlap)
                    # iou最大的值
                    max_overlap = overlap[max_overlap_index]
                    if max_overlap > iou_threshold:
                        if dets[max_overlap_index] == 0:
                            # 表示没有被匹配
                            # TP = 1, FP = 0
                            # 需要使用conf来排序从而画pr图
                            TP_FP.append((pred_conf[j], 1, 0))
                            dets[max_overlap_index] = 1
                            count[c] += 1
                        else:
                            # TP = 0, FP = 1
                            TP_FP.append((pred_conf[j], 0, 1))
                    else:
                        # TP = 0, FP = 1
                        # 没有超过阈值 同样是FP
                        TP_FP.append((pred_conf[j], 0, 1))
                else:
                    # TP = 0, FP = 1
                    # 没有预测到真实框，同样是FP
                    TP_FP.append((pred_conf[j], 0, 1))

        TP_FP_list[c] = TP_FP
    print(count)
    for c in range(num_c):
        # class
        TP_FP_array = np.stack(TP_FP_list[c], 0)
        TP_FP_array = TP_FP_array[np.argsort(-TP_FP_array[:, 0])]

        cum_sum_TP = np.cumsum(TP_FP_array[:, 1])
        cum_sum_FP = np.cumsum(TP_FP_array[:, 2])
        precision = cum_sum_TP / (cum_sum_TP + cum_sum_FP)
        recall = cum_sum_TP / npos[c]

        print('class_{}'.format(c), auc(recall, precision))
        plt.plot(recall, precision, label="class_{}_map_{:.3f}".format(c, auc(recall, precision)))
    plt.show()



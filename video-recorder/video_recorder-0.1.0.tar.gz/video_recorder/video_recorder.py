import cv2

def Video_Recorder(capture_index=0,filename='video.mp4'):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cap=cv2.VideoCapture(0)
    fps=int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')#视频存储的格式
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), \
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(filename, fourcc, fps, size)#视频存储
    status='WAIT'
    print(fps,size)
    frame_count=0
    while True:
        ret,frame=cap.read()
        key=cv2.waitKey(1)
        if status=='WAIT':
            frame=cv2.putText(frame, 'press s to start record', 
                                (0, 50), font, 1.2, (0, 0, 255), 2)
        else:
            out.write(frame)
            frame=cv2.putText(frame, 'recording '+str(frame_count)+'frame,press e to stop', 
                                (0, 50), font, 1.2, (0, 0, 255), 2)
            frame_count+=1
        if key==ord('s') and status=='WAIT':
            out = cv2.VideoWriter(filename, fourcc, fps, size)#视频存储
            status='REC'
            frame_count=0
        if key==ord('e') and status=='REC':
            out.release()
            status='WAIT'
        if key==ord('q') and status=='WAIT':
            break
        if ret is False:
            return None
        else:
            frame=cv2.putText(frame, 'press q to finish program', 
                                (0, 100), font, 1.2, (0, 0, 255), 2)
            cv2.imshow(filename,frame)
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    Video_Recorder()
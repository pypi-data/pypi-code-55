"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
import json
from grpc._channel import _Rendezvous
from ndlapi.api._interfaces.RecognitionService import IRService
from ndlapi.api._pyproto import api_common_pb2 as ac
from ndlapi.api._utils import iterate_over_file_bytes, print_progress


class IVideoService(IRService, object):
    def __init__(self, auth):
        super(IVideoService, self).__init__(auth)
        self.media_types.append('video')

    def _video_send_function(self, video_path):
        for blob_num, blob in enumerate(iterate_over_file_bytes(video_path, self._video_blob_size)):
            data = ac.BytesData(data=blob, pack_num=blob_num)
            request = ac.ProcessingRequest(data=data, file_extension=video_path.split('.')[-1])
            print_progress(send_progress=self._video_blob_size * blob_num + len(blob))
            yield request
        print()

    def process_video(self, video_path):
        processing_ok, result = False, {}
        try:
            response_iterator = self.stub.process_video_stream(self._video_send_function(video_path))

            print("Establishing connection ... This may take a while")

            processing_ok, result = False, {}
            for response in response_iterator:
                if response.code == ac.TicketStatusCode.Queued:
                    print('Your response in queue')

                elif response.code == ac.TicketStatusCode.InProgress:
                    print_progress(units_progress=response.units_progress)

                elif response.code == ac.TicketStatusCode.OK:
                    processing_ok = True
                    for image_res in response.result:
                        result[image_res.num] = json.loads(image_res.result)

                else:
                    self._process_bad_answer(response)

        except _Rendezvous as e:
            self._handle_error(e)

        else:
            print()
            result = self._postprocess_result(result)

        return processing_ok, result

    @property
    def _video_blob_size(self):
        return 16 * 2 ** 10

    @staticmethod
    def _postprocess_result(old_result):
        return old_result

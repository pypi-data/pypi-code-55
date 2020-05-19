import datetime
import os
import re


def write_sheets(frames, method, writer):
    for key in frames:
        for name, frame in frames[key].items():
            frame.to_excel(writer, sheet_name=f"{method} {name}", index=False)


def write_csv(frames, method):
    for key in frames:
        for name, frame in frames[key].items():
            frame.to_csv(os.path.join("out", f"{name}_{method}.csv"), index=False)


def write_topic_structured_csv(frames, method, out_path):
    tracer = {}
    try:
        os.mkdir(os.path.join(out_path, "data_files_for_acd"))
    except OSError:
        pass
    out_path = os.path.join(out_path, "data_files_for_acd")
    for isograd in frames:
        # Gradient / Isotherm:
        for topic in frames[isograd]:
            # Topic
            i = 0
            for name, frame in frames[isograd][topic].items():
                # Frames
                _path = os.path.join(out_path, f"{name}_{method}.csv")
                if tracer.get(topic):
                    tracer[topic].append(_path)
                else:
                    tracer[topic] = [_path]
                frame.to_csv(_path, index=False)
    return tracer

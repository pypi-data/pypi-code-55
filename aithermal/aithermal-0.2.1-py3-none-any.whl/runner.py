import os
import argparse
import aithermal
import pandas as pd
import xlsxwriter
import simplelogging
import oyaml as yaml
from aihelper import aifile, aiyaml


def main():
    log = simplelogging.get_logger(file_name="aithermal.log", console=False)

    def represent_none(self, _):
        return self.represent_scalar("tag:yaml.org,2002:null", "")

    yaml.add_representer(type(None), represent_none)

    parameters = os.path.join(os.getcwd(), "project parameters.yaml")
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="root path")

    try:
        with open(parameters, "r") as stream:
            data_loaded = yaml.safe_load(stream)
    except FileNotFoundError as e:
        data_loaded = aiyaml.write_yaml()
        with open("project parameters.yaml", "w") as outfile:
            yaml.dump(data_loaded, outfile, default_flow_style=False)
        print("Please fill out the project parameters.yaml document")
        log.exception(f"{FileNotFoundError} {e}")
        os.startfile(os.path.join(os.getcwd(), "project parameters.yaml"))
    try:
        _run(*decompress(data_loaded))
    except TypeError as e:
        print("Please double-check your project parameters.yaml document'")
        log.exception(e)
        os.startfile(os.path.join(os.getcwd(), "project parameters.yaml"))


def decompress(data_loaded):
    wavelengths = data_loaded.get("WAVE LENGTHS")
    rms = data_loaded.get("RMS")
    root = data_loaded.get("DIRECTORY")

    directory_listing, method_listing, temperature_listing = aifile.topic_directories(
        root
    )

    return (
        method_listing,
        temperature_listing,
        root,
        wavelengths,
        rms,
    )


def _run(method_listing, temperature_listing, root, wavelengths, rms):

    gradient_temp = temperature_listing.get("gradient", [])
    isotherm_temp = temperature_listing.get("isotherm", [])

    baseline_path = os.path.join(root, "Parameter\\Baseline\\")

    all_frames = aithermal.load_dsc(method_listing, baseline_path, rms, wavelengths)

    tracer = {}
    for method, data in all_frames.items():
        tracer[method] = aithermal.write_topic_structured_csv(data, method, root)
    acd_frame = []
    ms_frame = []
    for method, trace in tracer.items():
        if method == "MS":
            z = pd.DataFrame.from_dict(trace, orient="index").stack()
            r = (
                z.reset_index()
                .set_index("level_0")
                .drop(columns="level_1", errors="ignore")
                .rename(columns={0: "MS File"})
            )
            ms_frame = r
        else:
            acd_frame.append(generate_results_csv_acd(trace, f"{method} File"))

    tracers = pd.concat(acd_frame, axis=1)
    tracers = ms_frame.join(tracers)

    tracers["Gradient"] = ",".join([str(x) for x in gradient_temp])
    tracers["Isotherms"] = ",".join([str(x) for x in isotherm_temp])
    tracers = tracers.reset_index()
    tracers = tracers.rename(columns={"index": "Name"})
    acd_trace_path = os.path.join(root, "ACD Traces")
    try:
        os.mkdir(acd_trace_path)
    except OSError:
        pass

    tracers.to_csv(os.path.join(acd_trace_path, "ACD Trace.csv"), index=False, sep=";")

    acd_frame.append(ms_frame)
    for this_frame in acd_frame:
        this_frame["Gradient"] = ",".join([str(x) for x in gradient_temp])
        this_frame["Isotherms"] = ",".join([str(x) for x in isotherm_temp])
        this_frame = this_frame.reset_index()
        this_frame = this_frame.rename(columns={"index": "Name", "level_0": "Name"})
        method = this_frame.columns[1].split(" ")[0]
        this_frame["Method"] = method
        this_frame.to_csv(
            os.path.join(acd_trace_path, f"{method} Trace.csv"), index=False, sep=";"
        )


def generate_results_csv_acd(frame, prefix):
    return pd.DataFrame.from_dict(frame, orient="index").add_prefix(f"{prefix} ")


if __name__ == "__main__":
    main()

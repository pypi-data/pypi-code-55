import json
import os
import requests
# import secrets
import sys
import subprocess
import platform
from datetime import datetime
import shlex
import time
import zipfile

from typing import Any, Dict, List, Optional, cast
from certora_cli.certoraTester import compareResultsWithExpected, get_errors, has_violations, get_violations  # type: ignore

MAX_FILE_SIZE = 10 * 1024 * 1024
config_path = "%s/%s" % (os.getcwd().replace("\\", "/"), ".certora_config")
ZipFileName = "sample.zip"
CompressingProgress = "  - compressing  ({}/{})\r"
Response = requests.models.Response

# bash colors
bashGreenColor = "\033[32m"
bashRedColor = "\033[31m"
bashColorEnd = "\033[0m"

# error messages
TimeoutMsgPrefix = bashRedColor + "Request timed out." + bashColorEnd
ErrorMsgPrefix = bashRedColor + "An error occurred:" + bashColorEnd
ErrorStatusPrefix = bashRedColor + "Error Status:" + bashColorEnd
ConnectionErrorPrefix = bashRedColor + "Connection error:" + bashColorEnd
VaasErrorPrefix = bashRedColor + "Server reported an error:" + bashColorEnd
ServerErrorPrefix = bashRedColor + "Server Error" + bashColorEnd
verificationErrorMsgPrefix = bashRedColor + "Prover found violations:" + bashColorEnd

# completion messages
completeCompress = bashGreenColor + "Finished compressing" + bashColorEnd
completeSubmit = bashGreenColor + "Job submitted to server" + bashColorEnd
noVerificationErrors = bashGreenColor + "No errors found by Prover!" + bashColorEnd

common_solidity_options = ["--optimize", "--optimize-runs"]
legal_run_args = ["--settings", "--cache", "--output", "--output_folder",
                  "--link", "--address", "--path", "--packages_path", "--packages", "--solc",
                  "--solc_args", "--verify", "--assert", "--dont_fetch_sources",
                  "--iscygwin", "--varmap", "--build", "--jar", "--debug", "--help",
                  "--cloud", "--staging", "--local", "--key"]
legal_run_args += common_solidity_options
legal_build_args = ["--cache", "--output", "--output_folder", "--link",
                    "--address", "--path", "--packages_path", "--packages", "--solc",
                    "--solc_args", "--verify", "--assert", "--dont_fetch_sources",
                    "--iscygwin", "--varmap", "--debug", "--help"]
legal_build_args += common_solidity_options

def check_legal_args(args: List[str], legal_args: List[str]) -> None:
    for arg in args:
        if arg.startswith("--") and arg not in legal_args:
            print("Error: argument is illegal {}".format(arg))
            sys.exit(1)

def getUrl(env: str) -> str:
    if env == "local":
        url = 'http://127.0.0.1:5000'
    elif env == "staging":
        url = 'https://vaas-stg.certora.com'
    else:
        url = 'https://prover.certora.com'
    return url

def getKey(args: Dict[str, str]) -> str:
    if "key" in args:
        return args["key"]
    return os.environ['CERTORAKEY']

def getBranch(args: Dict[str, str]) -> str:
    branch = args["branch"] if "branch" in args else ""
    if branch == "" or branch is None:
        return "master"

    return branch

def outputErrorResponse(response: Response) -> None:
    print(ErrorStatusPrefix, response.status_code)
    if response.status_code == 500:
        print(ServerErrorPrefix)
        print("Please, contact Certora on https://www.certora.com")
        return
    try:
        errorResponse = response.json()
        # print(errorResponse)
        if "errorString" in errorResponse:
            print(VaasErrorPrefix, errorResponse["errorString"])
        elif "message" in errorResponse:
            print(VaasErrorPrefix, errorResponse["message"])
    except Exception:
        print(ErrorMsgPrefix)
        print(response.text)

def checkExecException(jsonResponse: Dict[str, Any], statusUrl: str) -> None:
    # When there is an exception while running the job
    if "execException" in jsonResponse:
        exceptionResponse = jsonResponse["execException"]
        if exceptionResponse is not None:
            try:
                errorMsg = exceptionResponse["message"]
                print(ErrorMsgPrefix, errorMsg)
                print("For further details visit", statusUrl)
            except Exception:
                print(ErrorMsgPrefix, "Server returned an error with no message:")
                print(exceptionResponse)
                print("Please contact Certora on https://www.certora.com")
            raise

def parseJson(response: Response) -> Dict[str, Any]:
    try:
        jsonResponse = response.json()
    except ValueError:
        print(ErrorMsgPrefix, "Could not parse JSON response")
        print(response.text)  # Should we print the whole response here?
        return {}
    return jsonResponse

def pollOutput(url: str, statusUrl: str, nextIndex: int = 0, lim: int = 60) -> None:
    r = requests.get(url, timeout=lim)
    if (r.status_code != requests.codes.ok):
        outputErrorResponse(r)
        # raise requests.exceptions.RequestException
        raise Exception('No additional output is available')

    jsonResponse = parseJson(r)
    if not jsonResponse:  # Error parsing json
        print(ErrorMsgPrefix, "Failed to parse response. For more info visit", statusUrl)
        return
    checkExecException(jsonResponse, statusUrl)  # look for execution exceptions
    try:
        allOutput = jsonResponse["allOutput"]
    except Exception:
        print(ErrorMsgPrefix, "No output is available.")
        print("For further details visit", statusUrl)
        return

    for i in range(nextIndex, len(allOutput)):
        print(allOutput[i]["line"], flush=True)

    if not jsonResponse["finished"]:  # TODO: recheck if this condition is good enough for base case
        time.sleep(0.5)
        pollOutput(url, statusUrl, len(allOutput))

def lookForPath(path: str) -> Optional[str]:
    try:
        r = requests.get(path, timeout=10)
        if (r.status_code == requests.codes.ok):
            # read
            return r.json()
        else:
            return None
    except (requests.exceptions.Timeout, requests.exceptions.RequestException, ConnectionError):
        printConnError()
        return None

def lookForIndex(indexPath: str, statusUrl: str) -> None:
    try:
        r = requests.get(indexPath, timeout=20)
        if (r.status_code == requests.codes.ok):
            print("Output URL:", indexPath)
        elif (r.status_code == 500):
            print(ErrorMsgPrefix, "Failed to fetch index.html. For further details visit", statusUrl)
            return
        else:
            print(ErrorMsgPrefix, "index.html was not created.")
            print("For further details visit", statusUrl)  # indexPath.replace("index","FinalResults")

    except (requests.exceptions.Timeout, requests.exceptions.RequestException, ConnectionError):
        printConnError()

def printConnError() -> None:
    print(
        ConnectionErrorPrefix,
        "Server is currently unavailable. Please try again later.")
    print("For further information, please contact Certora on https://www.certora.com",
          flush=True)

def getTotalFiles(dir: str) -> int:
    try:
        total_files = sum(len(files) for _, _, files in os.walk(dir))
        return total_files
    except OSError:
        print(ErrorMsgPrefix, "Could not traverse", dir)
        return -1

def verificationRequest(url: str, authData: Dict[str, Any]) -> Optional[Response]:
    verifyUrl = url + "/cli/verify"
    additional_headers = {'content-encoding': 'gzip'}
    try:
        r = requests.post(verifyUrl, data=authData, files={'any_files': (ZipFileName, open(ZipFileName, 'rb'))},
                          headers=additional_headers, timeout=60)
        return r
    except requests.exceptions.Timeout:
        # set up for a retry?
        print(TimeoutMsgPrefix, "Please, contact Certora on https://www.certora.com", flush=True)
    except requests.exceptions.RequestException:
        # catastrophic error. Do we have to catch this?
        printConnError()
    except ConnectionError:
        printConnError()
    return None

def compressFiles(*fileNames: Any) -> bool:
    zipObj = zipfile.ZipFile(ZipFileName, 'w', zipfile.ZIP_DEFLATED)

    total_files = 0
    for fileName in fileNames:
        # print(fileName)
        if os.path.isdir(fileName):
            total_dir_files = getTotalFiles(fileName)
            if total_dir_files == 0:
                print(ErrorMsgPrefix, "Provided directory - '{}' is empty.".format(fileName))
                return False
            elif total_dir_files > 0:
                total_files += total_dir_files
        elif os.path.isfile(fileName):
            total_files += 1
        else:
            print(ErrorMsgPrefix, "Provided file - '{}' does not exist.".format(fileName))
            return False
    if total_files < 1:
        if len(fileNames) == 0:
            print(ErrorMsgPrefix, "No file was provided. Please, contact Certora on https://www.certora.com")
        else:
            print(ErrorMsgPrefix, "Provided file(s) - {} do(es) not exist.".format(", ".join(fileNames)))
        return False

    i = 0

    for fileName in fileNames:
        if os.path.isdir(fileName):
            try:
                # traverse a directory
                for root, _, files in os.walk(fileName):
                    for f in files:
                        f_name = sanitize_path(os.path.join(root, f))
                        zipObj.write(f_name)
                        i += 1
                        print(CompressingProgress.format(i, total_files), flush=True, end="")
                print("", flush=True)
            except OSError:
                print(ErrorMsgPrefix, "Could not compress a directory -", fileName)
                return False
        else:  # zip file
            try:
                zipObj.write(fileName)
                i += 1
                print(CompressingProgress.format(i, total_files), flush=True, end="")
            except OSError:
                print(ErrorMsgPrefix, "Could not compress", fileName)
                return False

    zipObj.close()
    return True

# verify on a local/staging/remote server
def cliVerify(args: Dict[str, str], compareToExpected: bool = True) -> bool:
    CERTORA_CONFIG = ".certora_config"
    CERTORA_BUILD = ".certora_build.json"
    CERTORA_VERIFY = ".certora_verify.json"

    env = args["env"] if "env" in args else ""
    url = getUrl(env)

    certoraKey = getKey(args)
    # runName = "run_" + secrets.token_hex(5)  # since 3.6
    runName = "run_" + os.urandom(5).hex()

    authData = {
        "certoraKey": certoraKey,
        "runName": runName
    }

    if env == "staging":
        authData["branch"] = getBranch(args)

    if "settings" in args:
        authData["settings"] = args["settings"]

    print("Compressing the files...", flush=True)
    # remove previous zip file
    if os.path.exists(ZipFileName):
        os.remove(ZipFileName)

    # create new zip file
    if not compressFiles(CERTORA_BUILD, CERTORA_VERIFY, CERTORA_CONFIG):
        return False

    if os.path.getsize(ZipFileName) > MAX_FILE_SIZE:
        print(ErrorMsgPrefix, "Max 10MB file size exceeded.", flush=True)
        return False
    print(completeCompress, flush=True)
    print()
    print("Uploading files...", flush=True)

    resp = verificationRequest(url, authData)  # send post request to /cli/vertify

    if resp is None:  # on error
        return False

    if (resp.status_code != requests.codes.ok):
        respStatus = resp.status_code
        if respStatus == 403:
            print("You have no permission. Please, make sure you entered a valid key.")
            return False

        outputErrorResponse(resp)
    else:
        jsonResponse = parseJson(resp)
        if not jsonResponse:
            return False

        try:
            if not jsonResponse["success"]:  # on exception
                print(ErrorMsgPrefix, jsonResponse["errorString"], flush=True)
                return False

            anonymousKey = jsonResponse["anonymousKey"]
            userRunName = jsonResponse["name"]
        except Exception:  # (Json) ValueError
            print(ErrorMsgPrefix, "Unexpected Json response")
            print("Please, contact Certora on https://www.certora.com", flush=True)
            return False

        print(completeSubmit, flush=True)
        print()
        indexPath = url + "/users/" + userRunName + "/index.html?anonymousKey=" + anonymousKey
        print("Preparing output:", indexPath, flush=True)

        print("Output:", flush=True)
        outputUrl = url + "/job/" + userRunName + "?anonymousKey=" + anonymousKey
        statusUrl = outputUrl.replace("job", "jobNice")

        try:
            pollOutput(outputUrl, statusUrl)
            lookForIndex(indexPath, statusUrl)
        except requests.exceptions.Timeout:
            # set up for a retry?
            # pollOutput(outputUrl)
            print(TimeoutMsgPrefix, "You can follow up on the status:", statusUrl)
            print("In case of an error, please contact Certora on https://www.certora.com", flush=True)
            return False
        except requests.exceptions.RequestException:
            # catastrophic error.
            printConnError()
            return False
            # raise SystemExit(e)
        except ConnectionError:
            print("You were disconnected from server, but your request is still being processed.")
            print("You can follow up on the status:", statusUrl)
            print("When the job is completed without errors, the results will be presented in", indexPath)
            return False
        except Exception:
            return False

    if compareToExpected:
        outputPath = url + "/users/" + userRunName + "/output.json?anonymousKey=" + anonymousKey
        actual = lookForPath(outputPath)
        if actual is None:
            return False
        actualResults = cast(dict, actual)
        expectedFilename = "expected.json"
        basedOnExpected = os.path.exists(expectedFilename)
        if basedOnExpected:
            with open(expectedFilename) as expectedFile:
                expected = json.load(expectedFile)
                result = compareResultsWithExpected("test", actualResults["rules"], expected["rules"], {}, {})

            if get_errors():
                print(verificationErrorMsgPrefix, get_errors())
            if has_violations():
                print(verificationErrorMsgPrefix)
                get_violations()
        else:
            errors = []
            result = True

            for rule in actualResults["rules"].keys():
                ruleResult = actualResults["rules"][rule]
                if isinstance(ruleResult, str) and ruleResult != 'SUCCESS':
                    errors.append(rule)
                    result = False
                elif isinstance(ruleResult, dict):
                    nesting = ruleResult
                    for method in nesting.keys():
                        if method != 'SUCCESS' and len(nesting[method]) > 0:
                            errors.append(rule + ": " + ','.join(nesting[method]))
                            result = False
            if not result:
                print(verificationErrorMsgPrefix + "\n", ',\n'.join(errors))

        if result:
            if basedOnExpected:
                print(noVerificationErrors, "(based on expected.json)")
            else:
                print(noVerificationErrors)
            return True
        else:
            return False
    else:
        return True


DEFAULT_CONF = "default.conf"
MANDATORY_CONTRACTS = "contracts"
OPTION_OUTPUT = "output"
OPTION_OUTPUT_FOLDER = "output_folder"
OPTION_OUTPUT_VERIFY = "output_verify"
OPTION_PATH = "path"
OPTION_PACKAGES_PATH = "packages_path"
OPTION_PACKAGES = "packages"
OPTION_SOLC_MAP = "solc_map"
OPTION_SOLC = "solc"
OPTION_LINK = "link"
OPTION_ADDRESS = "address"
OPTION_VERIFY = "verify"
OPTION_ASSERT = "assert"
OPTION_CACHE = "cache"
OPTION_LINK_CANDIDATES = "linkCandidates"
OPTION_SOLC_ARGS = "solc_args"
ENVVAR_CERTORA = "CERTORA"

def fatal_error(s: str, DEBUG: bool = False) -> None:
    print(s)
    if DEBUG:
        raise Exception(s)
    sys.exit(1)

def debug_print_(s: str, DEBUG: bool = False) -> None:
    if DEBUG:
        print(s)

def is_windows() -> bool:
    return platform.system() == 'Windows'

def get_file_name(file: str) -> str:
    return ''.join(file.split("/")[-1])

def get_file_basename(file: str) -> str:
    return ''.join(file.split("/")[-1].split(".")[0:-1])

def get_file_extension(file: str) -> str:
    return file.split("/")[-1].split(".")[-1]

def safe_create_dir(path: str) -> None:
    try:
        os.mkdir(path)
    except OSError:
        debug_print_("Failed to create directory %s: %s" % (path, sys.exc_info()))
        pass

def print_failed_to_run(cmd: str) -> None:
    print()
    print("Failed to run %s" % (cmd, ))
    if (is_windows() and cmd.find('solc') != -1 and cmd.find('exe') == -1):
        print("did you forget the .exe extension for solcXX.exe??")
    print()

def run_cmd(cmd: str, name: str, config_path: str, input: bytes = None) -> None:
    debug_print_("Running cmd %s" % (cmd,))

    stdout_name = "%s/%s.stdout" % (config_path, name)
    stderr_name = "%s/%s.stderr" % (config_path, name)
    debug_print_("stdout, stderr = %s,%s" % (stdout_name, stderr_name))

    with open(stdout_name, 'w+') as stdout:
        with open(stderr_name, 'w+') as stderr:
            try:
                args = prepare_call_args(cmd)
                exitcode = subprocess.run(args, stdout=stdout, stderr=stderr, input=input).returncode
                if exitcode:
                    print("Failed to run %s" % cmd)
                    with open(stderr_name, 'r') as stderr_read:
                        for line in stderr_read:
                            print(line)
                    sys.exit(1)
                else:
                    debug_print_("Exitcode %d" % (exitcode,))
            except Exception:
                print_failed_to_run(cmd)
                raise

def run_cmd_slim(cmd: str, name: str) -> None:
    try:
        exitcode = subprocess.call(shlex.split(cmd))
        if exitcode:
            print("Failed to run %s, got exitcode %d" % (cmd, exitcode))
            sys.exit(1)
        else:
            debug_print_("Exitcode %d" % (exitcode,))
    except Exception:
        print_failed_to_run(cmd)
        raise

def current_conf_to_file(parsed_options: Dict[str, Any], files: List[str], fileToContractName: Dict[str, str]) -> None:
    out = {}

    def simple_set(option: str) -> None:
        if option in parsed_options:
            out[option] = parsed_options[option]

    simple_set(OPTION_CACHE)
    simple_set(OPTION_OUTPUT)
    simple_set(OPTION_OUTPUT_FOLDER)
    simple_set(OPTION_OUTPUT_VERIFY)
    simple_set(OPTION_PACKAGES_PATH)
    simple_set(OPTION_SOLC)
    simple_set(OPTION_SOLC_MAP)
    simple_set(OPTION_PATH)
    simple_set(OPTION_SOLC_ARGS)

    if OPTION_LINK in parsed_options:
        out[OPTION_LINK] = {}
        for link in parsed_options[OPTION_LINK]:
            k, f_v = link.split(":", 2)
            f, v = f_v.split("=", 2)

            if k in out[OPTION_LINK]:
                out[OPTION_LINK][k][f] = v
            else:
                out[OPTION_LINK][k] = {f: v}

    if OPTION_PACKAGES in parsed_options:
        out[OPTION_PACKAGES] = {}
        for package_entry in parsed_options[OPTION_PACKAGES].split(" "):
            package, package_path = package_entry.split("=", 2)
            out[OPTION_PACKAGES][package] = package_path

    if OPTION_ADDRESS in parsed_options:
        out[OPTION_ADDRESS] = {}
        for manual_address_entry in parsed_options[OPTION_ADDRESS]:
            out[OPTION_ADDRESS][manual_address_entry] = parsed_options[OPTION_ADDRESS][manual_address_entry]

    if OPTION_VERIFY in parsed_options:
        out[OPTION_VERIFY] = {}
        for verquery_entry in parsed_options[OPTION_VERIFY]:
            contract, spec = verquery_entry.split(":", 2)
            if contract in out[OPTION_VERIFY]:
                out[OPTION_VERIFY][contract].append(spec)
            else:
                out[OPTION_VERIFY][contract] = [spec]

    if OPTION_ASSERT in parsed_options:
        out[OPTION_ASSERT] = parsed_options[OPTION_ASSERT]

    # TODO: Add OPTION_LINK_CANDIDATES handling from comamnd line to conf

    # finally... files:
    out[MANDATORY_CONTRACTS] = []
    for file in files:
        out[MANDATORY_CONTRACTS].append("%s:%s" % (file, fileToContractName[file]))

    safe_create_dir(".last_confs")
    out_file_name = ".last_confs/last_conf_%s.conf" % (datetime.now().strftime("%d_%m_%Y__%H_%M_%S"))
    with open(out_file_name, 'w+') as out_file:
        json.dump(out, out_file, indent=4, sort_keys=True)

def handle_file_list(file_list: List[str], files: List[str], fileToContractName: Dict[str, str]) -> None:
    for arg in file_list:
        if arg.startswith("--"):
            break

        if is_windows():
            path_normalized_file = arg.replace("\\", "/")
        else:
            path_normalized_file = arg

        if ":" in path_normalized_file:
            contract_path = path_normalized_file.split(":")[0]
            contract_name = path_normalized_file.split(":")[1]
            files.append(contract_path)
            fileToContractName[contract_path] = contract_name
        else:
            files.append(path_normalized_file)
            fileToContractName[path_normalized_file] = get_file_basename(path_normalized_file)

# features: read from conf. write last to last_conf and to conf_date..
def read_from_conf(conf_file_name: str, parsed_options: Dict[str, Any], files: List[str],
                   fileToContractName: Dict[str, str]) -> None:
    with open(conf_file_name, "r") as conf_file:
        json_obj = json.load(conf_file)
        if MANDATORY_CONTRACTS not in json_obj:
            raise Exception("Configuration file %s must specify contract files in \"contracts\"" % (conf_file_name))

        handle_file_list(json_obj[MANDATORY_CONTRACTS], files, fileToContractName)

        if OPTION_SOLC in json_obj:
            parsed_options[OPTION_SOLC] = json_obj[OPTION_SOLC]

        if OPTION_SOLC_ARGS in json_obj:
            parsed_options[OPTION_SOLC_ARGS] = json_obj[OPTION_SOLC_ARGS]

        if OPTION_LINK in json_obj:
            flattened_links = []
            for linked in json_obj[OPTION_LINK]:
                for field in json_obj[OPTION_LINK][linked]:
                    flattened_links.append("%s:%s=%s" % (linked, field, json_obj[OPTION_LINK][linked][field]))

            parsed_options[OPTION_LINK] = flattened_links

        if OPTION_ADDRESS in json_obj:
            parsed_options[OPTION_ADDRESS] = {}
            for entry in json_obj[OPTION_ADDRESS]:
                parsed_options[OPTION_ADDRESS][entry] = json_obj[OPTION_ADDRESS][entry]

        if OPTION_PACKAGES in json_obj:
            flattened_packages = []
            for package in json_obj[OPTION_PACKAGES]:
                package_loc = json_obj[OPTION_PACKAGES][package]
                if package_loc.find("$PWD") != -1:
                    package_loc = package_loc.replace("$PWD", os.getcwd().replace("\\", "/"))
                flattened_packages.append("%s=%s" % (package, package_loc))
            parsed_options[OPTION_PACKAGES] = ' '.join(flattened_packages)

        if OPTION_VERIFY in json_obj:
            flattened_verification_queries = []
            for contract_verquery in json_obj[OPTION_VERIFY]:
                for specfile in json_obj[OPTION_VERIFY][contract_verquery]:
                    flattened_verification_queries.append("%s:%s" % (contract_verquery, specfile))
            parsed_options[OPTION_VERIFY] = flattened_verification_queries

        if OPTION_ASSERT in json_obj:
            parsed_options[OPTION_ASSERT] = json_obj[OPTION_ASSERT]

        if OPTION_LINK_CANDIDATES in json_obj:
            parsed_options[OPTION_LINK_CANDIDATES] = json_obj[OPTION_LINK_CANDIDATES]

        if OPTION_CACHE in json_obj:
            parsed_options[OPTION_CACHE] = json_obj[OPTION_CACHE]

        if OPTION_PATH in json_obj:
            parsed_options[OPTION_PATH] = json_obj[OPTION_PATH].replace("$PWD", os.getcwd().replace("\\", "/"))


"""
 Hack to avoid problems with the parameter of --solc_args (problem is that the
 parameter looks like an option).

 Changes its parameter object (a list) in place.

 What this actually does:
   look for the argument "--solc_args"
   prepend the argument that immediately follows "--solc_args" with a space, so
   it is not recognized as an option by the argument parsing logic.

 source of inspiration:
   https://stackoverflow.com/questions/16174992/cant-get-argparse-to-read-quoted-string-with-dashes-in-it
"""
def nestedOptionHack(args: List[str]) -> None:
    for i in range(len(args)):
        debug_print_(args[i])
        if (args[i] == '--' + OPTION_SOLC_ARGS):
            try:
                # TODO: throw a warning if args[i+1] matches one of the options of this script
                args[i + 1] = ' ' + args[i + 1]
            except Exception:
                print("Error: '-solc_args' needs a parameter, thus cannot be the last argument")
                sys.exit()

def sanitize_path(pathString: str) -> str:
    return pathString.replace("\\", "/")

def prepare_call_args(cmd: str) -> List[str]:
    split = shlex.split(cmd)
    if (split[0].endswith('.py')):
        # sys.executable returns a full path to the current running python, so it's good for running our own scripts
        certora_root = get_certora_root_directory()
        args = [sys.executable] + [sanitize_path(os.path.join(certora_root, split[0]))] + split[1:]
    else:
        args = split
    return args

def get_certora_root_directory() -> str:
    return os.getenv(ENVVAR_CERTORA, os.getcwd())

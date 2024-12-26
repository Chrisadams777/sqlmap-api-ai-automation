#!/usr/bin/env python
"""
Copyright (c) 2006-2024 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

from __future__ import print_function

try:
    import sys
    import requests  # HTTP requests
    import urllib  # URL encoding
    import base64  # Base64 encoding

    sys.dont_write_bytecode = True

    try:
        __import__("lib.utils.versioncheck")  # must be the first non-standard import
    except ImportError:
        sys.exit("[!] Wrong installation detected (missing modules). Visit 'https://github.com/sqlmapproject/sqlmap/#installation' for further details")

    import bdb
    import glob
    import inspect
    import json
    import logging
    import os
    import re
    import shutil
    import tempfile
    import threading
    import time
    import traceback
    import warnings

    # Handle deprecations
    if "--deprecations" not in sys.argv:
        warnings.filterwarnings(action="ignore", category=DeprecationWarning)
    else:
        warnings.resetwarnings()
        warnings.filterwarnings(action="ignore", message="'crypt'", category=DeprecationWarning)
        warnings.simplefilter("ignore", category=ImportWarning)
        if sys.version_info >= (3, 0):
            warnings.simplefilter("ignore", category=ResourceWarning)

    warnings.filterwarnings(action="ignore", message="Python 2 is no longer supported")
    warnings.filterwarnings(action="ignore", message=".*was already imported", category=UserWarning)
    warnings.filterwarnings(action="ignore", message=".*using a very old release", category=UserWarning)
    warnings.filterwarnings(action="ignore", message=".*default buffer size will be used", category=RuntimeWarning)
    warnings.filterwarnings(action="ignore", category=UserWarning, module="psycopg2")

    # Importing custom sqlmap libraries
    from lib.core.data import logger
    from lib.core.common import banner, checkPipedInput, checkSums, createGithubIssue, dataToStdout
    from lib.core.common import extractRegexResult, filterNone, getDaysFromLastUpdate, getFileItems, getSafeExString
    from lib.core.common import maskSensitiveData, openFile, setPaths, weAreFrozen, setColor, unhandledExceptionMessage
    from lib.core.convert import getUnicode
    from lib.core.compat import LooseVersion
    from lib.core.data import cmdLineOptions, conf, kb
    from lib.core.datatype import OrderedSet
    from lib.core.enums import MKSTEMP_PREFIX
    from lib.core.exception import SqlmapBaseException, SqlmapShellQuitException, SqlmapSilentQuitException, SqlmapUserQuitException
    from lib.core.option import init, initOptions
    from lib.core.patch import dirtyPatches, resolveCrossReferences
    from lib.core.settings import GIT_PAGE, IS_WIN, LAST_UPDATE_NAGGING_DAYS, LEGAL_DISCLAIMER, THREAD_FINALIZATION_TIMEOUT, UNICODE_ENCODING, VERSION
    from lib.parse.cmdline import cmdLineParser
    from lib.utils.crawler import crawl
    from lib.controller.controller import start

except KeyboardInterrupt:
    errMsg = "user aborted"
    if "logger" in globals():
        logger.critical(errMsg)
        raise SystemExit
    else:
        import time
        sys.exit("\r[%s] [CRITICAL] %s" % (time.strftime("%X"), errMsg))

# --- WAF Detection and Adaptive Tamper Application ---
WAF_SIGNATURES = {
    "Cloudflare": {
        "headers": ["Server: cloudflare"],
        "error_message": "Cloudflare",
        "recommended_tampers": ["space2comment", "between", "randomcase"]
    },
    "AWS Shield": {
        "headers": ["x-amz-cf-id"],
        "error_message": "403 Forbidden",
        "recommended_tampers": ["charencode", "appendnullbyte"]
    },
    "F5 BIG-IP": {
        "headers": ["X-WA-Info"],
        "error_message": "Access Denied",
        "recommended_tampers": ["between", "equaltolike"]
    }
}

def load_tamper_history():
    if os.path.exists("tamper_history.json"):
        with open("tamper_history.json", "r") as f:
            return json.load(f)
    return defaultdict(list)

def save_tamper_history(history):
    with open("tamper_history.json", "w") as f:
        json.dump(history, f)

def apply_adaptive_tamper(waf_detected, response):
    history = load_tamper_history()
    applied_tampers = []

    if waf_detected:
        print(f"[INFO] WAF detected: {waf_detected}. Applying recommended tampers.")
        for tamper in WAF_SIGNATURES[waf_detected]["recommended_tampers"]:
            applied_tampers.append(tamper)
            print(f"[INFO] Applying tamper: {tamper}")
            # Example: response = apply_tamper(tamper, response)

        if response_is_successful(response):  # Define response_is_successful based on actual SQLmap criteria
            history[waf_detected].extend(applied_tampers)
            save_tamper_history(history)
        else:
            print(f"[WARNING] Default tampers ineffective for WAF {waf_detected}, iterating for optimal combination.")

    return applied_tampers

def detect_waf(response_headers, response_body):
    for waf_name, waf_info in WAF_SIGNATURES.items():
        if any(header in response_headers for header in waf_info["headers"]) or waf_info["error_message"] in response_body:
            return waf_name
    return None

# Rest of the existing code
def modulePath():
    try:
        _ = sys.executable if weAreFrozen() else __file__
    except NameError:
        _ = inspect.getsourcefile(modulePath)
    return getUnicode(os.path.dirname(os.path.realpath(_)), encoding=sys.getfilesystemencoding() or UNICODE_ENCODING)

def checkEnvironment():
    try:
        os.path.isdir(modulePath())
    except UnicodeEncodeError:
        errMsg = "Your system does not properly handle non-ASCII paths. Please move the sqlmap's directory to another location"
        logger.critical(errMsg)
        raise SystemExit

    if LooseVersion(VERSION) < LooseVersion("1.0"):
        errMsg = "Your runtime environment (e.g., PYTHONPATH) is broken. Ensure you're not running newer versions of sqlmap with older runtime scripts."
        logger.critical(errMsg)
        raise SystemExit

def main():
    try:
        dirtyPatches()
        resolveCrossReferences()
        checkEnvironment()
        setPaths(modulePath())
        banner()
        args = cmdLineParser()
        cmdLineOptions.update(args.__dict__ if hasattr(args, "__dict__") else args)
        initOptions(cmdLineOptions)

        if checkPipedInput():
            conf.batch = True

        if conf.get("api"):
            from lib.utils.api import StdDbOut, setRestAPILog
            sys.stdout = StdDbOut(conf.taskid, messagetype="stdout")
            sys.stderr = StdDbOut(conf.taskid, messagetype="stderr")
            setRestAPILog()

        conf.showTime = True
        dataToStdout("[!] legal disclaimer: %s\n\n" % LEGAL_DISCLAIMER, forceOutput=True)
        dataToStdout("[*] starting @ %s\n\n" % time.strftime("%X /%Y-%m-%d/"), forceOutput=True)

        init()

        if not conf.updateAll:
            if conf.smokeTest:
                from lib.core.testing import smokeTest
                os._exitcode = 1 - (smokeTest() or 0)
            elif conf.vulnTest:
                from lib.core.testing import vulnTest
                os._exitcode = 1 - (vulnTest() or 0)
            else:
                start()

    except SqlmapUserQuitException:
        if not conf.batch:
            errMsg = "user quit"
            logger.error(errMsg)

    except (SqlmapSilentQuitException, bdb.BdbQuit):
        pass

    except SqlmapShellQuitException:
        cmdLineOptions.sqlmapShell = False

    except SqlmapBaseException as ex:
        errMsg = getSafeExString(ex)
        logger.critical(errMsg)
        os._exitcode = 1
        raise SystemExit

    except KeyboardInterrupt:
        print()
        logger.critical("user aborted")

    except EOFError:
        print()
        logger.critical("exit")

    except Exception as ex:
        exc_msg = unhandledExceptionMessage()
        if exc_msg:
            logger.critical(exc_msg)
        else:
            logger.critical(getSafeExString(ex))
        logger.error(traceback.format_exc(), exc_info=True)

    finally:
        os._exit(0)

if __name__ == "__main__":
    main()

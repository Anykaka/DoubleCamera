__error_table = {
    0: "OK",
    1: "Any",
    2: "Timeout",
    3: "Illegal Argument",
    4: "Illegal Data Format",
    5: "Illegal Request",
    6: "Illegal Response",
    7: "Illegal State",
    8: "Illegal Type",
    9: "Index Out Of Bounds",
    10: "No Such Element",
    11: "No Such Field",
    12: "No Such Method",
    13: "Null Pointer",
    14: "Unsupported Version",
    15: "Unsupported Operation",
    40400: "Shooting fail",
    40401: "Camera Not Ready",
    40402: "Already Running Polling Api",
    40403: "Still Capturing Not Finished",
    41003: "Some content could not be deleted",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    406: "Not Acceptable",
    413: "Request Entity Too Large",
    414: "Request-URI Too Long",
    501: "Not Implemented",
    503: "Service Unavailable",
}


def err_table(err_number):
    if err_number in __error_table:
        return __error_table[err_number]
    else:
        return "out of err_table, no mean"


if __name__ == '__main__':
    print(err_table(503))


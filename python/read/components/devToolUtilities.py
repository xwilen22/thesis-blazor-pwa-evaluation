def get_stack_trace_by_timer_id(timerId, profileJson):
    for function in profileJson:
        try:
            retrievedTimerId = function["args"]["data"]["timerId"]
            if retrievedTimerId == timerId:
                stackTrace = function["args"]["data"]["stackTrace"]
                return stackTrace
        except KeyError:
            continue
    return []
import time


def convert_clock_2_times(time_str: str) -> int:
    clock = time_str.split(":")
    h = int(clock[0])
    m = int(clock[1])
    s = float(clock[2])

    times = h * 60 * 60 * 1000 + m * 60 * 1000 + s * 1000
    times = int(times)
    print(times)
    return times


# def get_time_stamp():
#     ct = time.time()
#     local_time = time.localtime(ct)
#     data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
#     data_ms = (ct - int(ct)) * 1000
#     time_stamp = "%s.%03d" % (data_head, data_ms)
#     print(time_stamp)
#     stamp = ("".join(time_stamp.split()[0].split("-")) + "".join(time_stamp.split()[1].split(":"))).replace('.', '')
#     print(stamp)


def get_curr_datetime_ms_str() -> str:
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y%m%d%H%M%S", local_time)
    data_ms = (ct - int(ct)) * 1000
    curr_datetime_ms_str = "%s%03d" % (data_head, data_ms)
    return curr_datetime_ms_str


def get_curr_millisecond() -> int:
    return int(time.time() * 1000)


if __name__ == "__main__":
    get_curr_datetime_ms_str()

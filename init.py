import json
import datetime

level_dict = {
    "empty": 0,
    "info": 1,
    "warning": 2,
    "WARNING": 2,
    "error": 3,
    "notice": 4
}

code_dict = {
    "empty": 0,
    "H10": 1,  # app crashed
    "H12": 2,  # request timeout
    "H13": 3,  # connection close without response
    "R14": 4,  # Memory quota exceeded
    "R15": 5  # Memory quota vastly exceeded
}

method_dict = {"empty": 0, "GET": 1, "POST": 2, "PUT": 3, "DELETE": 4}

logs_arr = []

prediction_arr = []

rowcount = 0
zamanlar = []
zamanfarklari = []


def millis(start_time):
    dt = datetime.datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 +
          dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms


with open('data.jsonl') as f:
    for line in f:
        output = json.loads(line)
        jdate = output['timestamp'].split('+')[0]
        timestamp = datetime.datetime.strptime(jdate, '%Y-%m-%dT%H:%M:%S.%f')

        log_arr = []

        try:
            log_level = output['level']
            if log_level is not None:
                log_arr.append(level_dict[log_level])
            else:
                log_arr.append(level_dict['empty'])
        except:
            log_arr.append(level_dict['empty'])

        log_arr.append(millis(timestamp))

        try:
            log_method = output['method']
            log_arr.append(method_dict[log_method])
        except:
            log_arr.append(method_dict['empty'])

        try:
            log_code = output['code']
            log_arr.append(code_dict[log_code])
        except:
            log_arr.append(code_dict['empty'])

        try:
            log_status = output['status']
            log_arr.append(log_status)
        except:
            log_arr.append(0)

        try:
            log_service = output['service'].split('ms')[0]
            log_arr.append(log_service)
        except:
            log_arr.append(0)

        if rowcount - 1 >= 0:
            log = logs_arr[rowcount - 1]
            log_timestamp = log[1]
            current_timestamp = millis(timestamp)
            if log_timestamp >= current_timestamp:
                diff = log_timestamp - current_timestamp
                log_arr.append(diff)
            elif current_timestamp > log_timestamp:
                diff = current_timestamp - log_timestamp
                log_arr.append(diff)
        else:
            log_arr.append(0)

        
        if log_arr[3] is not 0:
            print(log_arr)
            logs_arr.append(log_arr)
            rowcount += 1
        zamanlar.append(timestamp)


print(len(logs_arr))
'''
fark=0
def cal_average(num):
    sum_num = 0
    for t in num:
        sum_num = sum_num + t

    avg = sum_num / len(num)
    return avg

for x in range(rowcount):
    if x > 0:
        if zamanlar[x-1] > zamanlar[x]:
            fark=zamanlar[x-1] - zamanlar[x]
        elif zamanlar[x] > zamanlar[x-1]:
            fark = zamanlar[x] - zamanlar[x-1]
        zamanfarklari.append(fark.microseconds)
        print(fark.microseconds)

print("En yuksek deger:",max(zamanfarklari))
print("Ortalama degeri:",cal_average(zamanfarklari))
'''

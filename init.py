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

# 0 level_dict,  1 timestamp, 2 method_dict, 3 code_dict, 4 log_status, 5 log_service, 6 diff
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

        if log_arr[4] is not 0:
            #print(log_arr)
            logs_arr.append(log_arr)
            rowcount += 1
        zamanlar.append(timestamp)


print(len(logs_arr))




ratio = 0.0
timeout_count = 0
success_response_count = 0
connection_closed_count = 0
memory_quota_exceeded_count = 0
error_count = 0

for i in range(len(logs_arr)):
    tempLog = logs_arr[i]
    if tempLog[3] == 0: # 😎
        success_response_count += 1
        if success_response_count > 20:
            timeout_count = 0
            connection_closed_count = 0
            memory_quota_exceeded_count = 0
            error_count = 0
        elif success_response_count > 10:
            ratio = 0.0
            if timeout_count > 2:
                timeout_count -= 3
            if connection_closed_count > 2:
                connection_closed_count -= 3
            if memory_quota_exceeded_count > 2:
                memory_quota_exceeded_count -= 3
            if error_count > 3:
                error_count -= 3
        elif success_response_count > 5:
            ratio /= 2
            if timeout_count > 1:
                timeout_count -= 2
            if connection_closed_count > 1:
                connection_closed_count -= 2
            if memory_quota_exceeded_count > 1:
                memory_quota_exceeded_count -= 2
            if error_count > 1:
                error_count -= 2
        else:
            if timeout_count > 0:
                timeout_count -= 1
            if connection_closed_count > 0:
                connection_closed_count -= 1
            if memory_quota_exceeded_count > 0:
                memory_quota_exceeded_count -= 1
            if error_count > 0:
                error_count -= 1
            if ratio > 0:
                ratio -= 0.1
        prediction_arr.append(ratio)
    elif tempLog[3] == 1: # app crashed :( ⚰️
        timeout_count = 0
        connection_closed_count = 0
        success_response_count = 0
        memory_quota_exceeded_count = 0
        error_count = 0
        ratio = 0.0
        #print(1)
        prediction_arr.append(1.0)
    else:
        if tempLog[3] == 2: # request timeout :| 🥴
            timeout_count +=1
            if timeout_count > 10: 
                ratio = ratio + 1.0
                success_response_count = 0
            elif timeout_count > 7: 
                ratio = ratio + 0.8
                success_response_count = 0
            elif  timeout_count > 5:
                success_response_count = 0
                ratio = ratio + 0.5
            elif  timeout_count > 3:
                ratio = ratio + 0.3
                if success_response_count > 2:
                    success_response_count -= 3
            elif  timeout_count > 1:
                ratio = ratio + 0.1
                if success_response_count > 0:
                    success_response_count -= 1
        elif tempLog[3] == 3: # connection close without response 🤯
            connection_closed_count +=1
            if connection_closed_count > 10: 
                ratio = ratio + 1.0
                success_response_count = 0
            elif connection_closed_count > 7: 
                ratio = ratio + 0.9
                success_response_count = 0
            elif  connection_closed_count > 5:
                ratio = ratio + 0.7
                success_response_count = 0
            elif  connection_closed_count > 3:
                ratio = ratio + 0.4
                success_response_count = 0
            elif  connection_closed_count >= 1:
                ratio = ratio + 0.1
                if success_response_count > 1:
                    success_response_count -= 2
                elif success_response_count == 1:
                    success_response_count = 0
        elif tempLog[3] == 4 or tempLog[3] == 5: # memory quota exceeded 🤮
            memory_quota_exceeded_count +=1
            if memory_quota_exceeded_count > 8: 
                ratio = ratio + 1.0
                success_response_count = 0
            elif  memory_quota_exceeded_count > 5:
                ratio = ratio + 0.8
                success_response_count = 0
            elif  memory_quota_exceeded_count > 3:
                ratio = ratio + 0.5
                success_response_count = 0
            elif  memory_quota_exceeded_count >= 1:
                ratio = ratio + 0.2
                if success_response_count > 0:
                    success_response_count -= 1
        else:
            if tempLog[0] == 3: #😡
                error_count += 1
                if error_count > 20:
                    ratio = ratio + 0.7
                    success_response_count = 0
                elif error_count > 10:
                    ratio = ratio + 0.4
                    if success_response_count > 2:
                        success_response_count -= 3
                elif  error_count > 5:
                    ratio = ratio + 0.1
                    if success_response_count > 0:
                        success_response_count -= 1
        prediction_arr.append(ratio)
    #print(prediction_arr[i])
print('prediction_arr length ',len(prediction_arr))

'''

# 0 level_dict,  1 timestamp, 2 method_dict, 3 code_dict, 4 log_status, 5 log_service, 6 diff

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

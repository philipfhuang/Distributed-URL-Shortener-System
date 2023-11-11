import redis
import os

master = redis.Redis(host='redis-primary', port=6379)

#try:
#    log = open("appendonlylog", "a+")
#except Exception:
#    print("could not open log file")

stream_name = 'log_stream'
group_name = 'log_group'
data_dir = '/app/data'
os.makedirs(data_dir, exist_ok=True)

try:
    master.xgroup_create(stream_name, group_name, id='0', mkstream=True)
except redis.exceptions.ResponseError as e:
    if "BUSYGROUP Consumer Group name already exists" in str(e):
        print("Consumer group already exists.")
    else:
        raise e


def process_messages():
    print('running')
    while True:
        try:
            messages = master.xreadgroup(group_name, 'log_consumer', {stream_name: '>'}, count=100, block=1000)
            with open(os.path.join(data_dir, 'appendonlylog'), 'a+') as log:    
                for stream, stream_message in messages:
                    for message in stream_message:
                        msg_id, data = message
                        short_url = data['short_url']
                        long_url = data['long_url']

                        log.write(f"inserted pair short: {short_url}    long: {long_url}")
                        log.flush()

                        master.xack(stream_name, group_name, msg_id)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    process_messages()

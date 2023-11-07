from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

def convert_to_json(output, node):
    lines = output.split('\n')

    if len(lines) < 2:
        return []

    header = lines[0]
    columns = header.split()

    docker_info = []

    for line in lines[1:]:
        datas = line.split()
        result_dict["NODE ID"] = node
        result_dict = {columns[i]: datas[i] for i in range(len(columns))}
        docker_info.append(result_dict)

    return docker_info

@app.route('/get_docker_nodes')
def get_docker_nodes():
    nodes_info = []
    ips = ["10.128.1.42", "10.128.2.42", "10.128.3.42", "10.182.4.42"]
    for ip in ips:
        output = subprocess.check_output(f"ssh {ip} 'docker ps -a'", shell=True, stderr=subprocess.STDOUT, text=True)
        node = subprocess.check_output(f"ssh {ip} 'hostname'", shell=True, stderr=subprocess.STDOUT, text=True)
        node_info = convert_to_json(output, node)
        nodes_info.extend(node_info)
    return jsonify(nodes_info)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

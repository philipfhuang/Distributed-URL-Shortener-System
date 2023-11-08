from flask import Flask, render_template, jsonify
import json
import subprocess

app = Flask(__name__)

@app.route('/get_docker_nodes')
def get_docker_nodes():
    nodes_info = []
    ips = ["10.128.1.42", "10.128.2.42", "10.128.3.42", "10.128.4.42"]
    for ip in ips:
        try:
            output = subprocess.check_output(f"ssh {ip} 'docker ps -a --format json --no-trunc'", shell=True, stderr=subprocess.STDOUT, text=True, timeout=5)
            node = subprocess.check_output(f"ssh {ip} 'hostname'", shell=True, stderr=subprocess.STDOUT, text=True, timeout=5)
        except subprocess.TimeoutExpired:
            return jsonify([{
                "Node": ip,
                "Info": "TIMEOUT",
            }])
        outputs = output.split('\n')
        node_info = [json.loads(output) for output in outputs if output != '']
        node_infos = {
            "Node": node.strip(),
            "Info": node_info,
        }
        nodes_info.append(node_infos)
    return jsonify(nodes_info)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')

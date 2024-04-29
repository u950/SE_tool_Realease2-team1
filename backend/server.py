from flask import Flask, jsonify, request
from flask_cors import CORS     # to handle cross-origin resources sharing
import os
import subprocess    #for executing the git clone command
import shutil
from main import CodeSnippetExtractor
from Dependency_extract import DependencyExtractor





app = Flask(__name__)
CORS(app)    #this will enable cors for alla routes

dependencies_json = []

@app.route('/')
def home():
    return jsonify("hell0")


@app.route('/download_repo', methods=['POST'])   # API END POINT 
def download_repo():
    try:
        #extract the data sent from the frontend
        repo_url = request.form['repo_url']
        repo_name = request.form.get('repo_name', '')   # default top empty string if not provided
        github_token = request.form.get('github_token', '')

        #determine the repository's name if not provided
        if not repo_name:
            repo_full_name = repo_url.split('/')[-2] + '/' + repo_url.split('/')[-1].replace('.git', '')
            repo_name = repo_full_name.split('/')[-1]

            #prepare the directory where the repository will be cloned
            repo_path = os.path.join(os.getcwd(), repo_name)
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
            os.makedirs(repo_path)

            #construct the git clone command
            if github_token:
                clone_command = f'git clone https://x-access-token:{github_token}@github.com/{repo_url.split("/")[-2]}/{repo_url.split("/")[-1]} "{repo_path}"'
            else:
                clone_command = f'git clone https://github.com/{repo_url.split("/")[-2]}/{repo_url.split("/")[-1]} "{repo_path}"'
            
            #execute the git clone command
            result = subprocess.run(clone_command, shell=True, check=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode !=0:
                return jsonify({"error": result.stderr}),500

            #check the result of the git clone command
            if result.returncode == 0:
                files_list = os.listdir(repo_path)
                return jsonify({"message" :f"Repository '{repo_name}' cloned successfully.", "repo_name":repo_name, "files":files_list})
                
            else:
                return jsonify({"error": "Failed to clone repository"}),500
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
    
    
@app.route('/get_dependencies', methods=['POST'])
def dependecies_function():
    data= request.json
    directory = data.get('directory')
    if not directory:
        return jsonify({"error": "Directory not provided"}),400
    try:
        analyse = DependencyExtractor(directory)
        analyse.run_extraction()
        dependencies_json = analyse.return_dependencies()
        print(dependencies_json)
        return dependencies_json
    except Exception as e:
        print("error loading dependency : ",e)




@app.route('/node_clicked', methods=['POST'])
def node_clicked():
    try:
        clicked_node = request.json
        
        # Process the clicked node data here
        clicked_node_id = clicked_node[0]['id']
        
        print("clicked on :",clicked_node_id)
        # Return a response if needed
        return jsonify({"message": "Node data received successfully ","show":clicked_node})
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
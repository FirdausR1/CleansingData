import re
import pandas as pd
import sqlite3
from flask import Flask , jsonify , url_for ,render_template,redirect
from flask import request
import re
from data_cleansing import cleansing_data
from flasgger import Swagger,swag_from, LazyJSONEncoder, LazyString
from data_reading_and_writing import create_table, insert_to_table, read_table







app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

title = str(LazyString(lambda: 'API Documentation for Data Processing dan Modelling'))
version = str(LazyString(lambda: '1.0.0'))
description = str(LazyString(lambda : 'Dokumnetasi API untuk Data Processing dan Modelling'))
host = LazyString(lambda: request.host)

# create swagger_template

swagger_template = {'info':{'title': title,
                            'version': version,
                            'description': description 
                            },
                    'host': host
                    }

swagger_config = {
    "headers": [],
    "specs": [{"endpoint":"docs", "route": '/docs.json'}],
    "static_url_path": "/flasgger_static",
    "swagger_ui":True,
    "specs_route":"/docs/"
}

swagger = Swagger(app,
                  # template = swagger_template,
                  config = swagger_config
                 )
@app.route('/')
def index():
    return render_template('index_2.html')

@app.route('/proses', methods=['POST'])
def proses():
   
    if request.method == 'POST':
        go_to_page = request.form['pilihan']
        if go_to_page == "Input_Text":
            return redirect(url_for("input_text_processing"))
        elif go_to_page == "2":
            return redirect(url_for("input_file_processing"))
        elif go_to_page == "3":
            return redirect(url_for("read_database"))
        else:
            return render_template("index_2.html")



@app.route('/text-processing',methods=['GET', 'POST'])
def input_text_processing():
    if request.method == 'POST':
        previous_text=request.form['inputText']
        cleaned_text=cleansing_data(previous_text)
        json_response={'previous_text': previous_text,
                       'cleaned_text': cleaned_text
                      }
        json_response=jsonify(json_response)
        return json_response
    else:
        return render_template("input_processing.html")
    
    
@app.route('/file-processing',methods=['GET', 'POST'])
def input_file_processing():
    if request.method == 'POST':
        input_file = request.files['inputFile']
        df = pd.read_csv(input_file, encoding='latin1')
        if("Tweet" in df.columns):
            list_of_tweets = df['Tweet'] #yang dari CSV
            list_of_cleaned_tweet = df['Tweet'].apply(lambda x: cleansing_data(x)) #ini yang hasil cleaning-an

            create_table()
            for previous_text, cleaned_text in zip(list_of_tweets, list_of_cleaned_tweet): # disini di-looping barengan
                insert_to_table(value_1=previous_text, value_2=cleaned_text)
            
            json_response={'list_of_tweets': list_of_tweets[0],
                           'list_of_cleaned_tweet': list_of_cleaned_tweet[0]
                          }
            json_response=jsonify(json_response)
            return json_response
        else:
            json_response={'ERROR_WARNING': "NO COLUMNS 'Tweet' APPEAR ON THE UPLOADED FILE"}
            json_response = jsonify(json_response)
            return json_response
    else:
        return render_template("file_processing.html")

@app.route('/read-database',methods=['GET', 'POST'])
def read_database():
    if request.method == "POST":
        showed_index=request.form['inputIndex']
        showed_keywords = request.form['inputKeywords']
        if len(showed_index)>0:
            print("AAAAAAAAAA")
            result_from_reading_database = read_table(target_index=showed_index)
            previous_text=result_from_reading_database[0].decode('latin1')
            cleaned_text=result_from_reading_database[1].decode('latin1')
            json_response={'Index': showed_index,
                           'Previous_text': previous_text,
                           'Cleaned_text': cleaned_text
                          }
            json_response = jsonify(json_response)
            return json_response
        elif len(showed_keywords)>0:
            print("BBBBBBBBB")
            results = read_table(target_keywords=showed_keywords)
            json_response={'showed_keywords': showed_keywords,
                           'previous_text': results[0][0].decode('latin1'),
                           'cleaned_text': results[0][1].decode('latin1')
                          }
            json_response = jsonify(json_response)
            return json_response
        else:
            print("CCCCCCCC")
            json_response={'ERROR_WARNING': "INDEX OR KEYWORDS IS NONE"}
            json_response = jsonify(json_response)
            return json_response
    else:
        return render_template("read_database.html")
'''
@swag_from("docs/file_processing.yml", methods=['POST'])
@app.route('/file-processing',methods=['POST'])
def file_processing():
            if 'upload_file' not in request.files:
                return 'Tidak ada file yang diunggah'
    
            file = request.files['upload_file']
    
    
            if file.filename == '':
                return 'Nama file kosong'
    
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
        
       
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
                return 'File berhasil diunggah'
            else:
                return 'Tipe file tidak diizinkan'
    
        


@swag_from("docs/read_index_data.yml", methods=['POST'])
@app.route('/read-index-data',methods=['POST'])
def read_index_data():
    index = request.form.get('index')
    result = read_table(target_index=int(index),
                         table_name='new_cleaning1')
    response_data = jsonify({"tweets":result})
    return response_data
    
'''
if __name__ == '__main__':
    app.run(debug=True)

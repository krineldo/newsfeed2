# newsfeed2

1: Install kafka, zookeeper and mongodb <br><br>
2: Make sure you run all the above services are running <br><br>
3: Install all the packages in imports using pip install if they fail to install automatically, in files mongoDb.py, producer.py, consumer.py <br>

4: Run files with this order: mongoDb.py, consumer.py, producer.py, network1.py, plotting.py (Inside PyhtonProject3)<br>
(We run these 5 files with Pycharm separately. The consumer has to be running before you run the producer.)<br><br>
5: Open VScode. Inside the project folder delete venv folder<br><br>
6: run commands to create venv and install requirements: <br><br>
python3 -m venv venv<br>
source venv/bin/activate<br>
pip install -r requirements.txt<br><br>

7: run with command: <br>
flask run

8: Open browser at http://127.0.0.1:5000/ . After signing up(POST) you can view articles(GET) with your preffered topics<br><br>
9: If you want to change the preffered topics, click the button update keywords(UPDATE)<br><br>
10: If you want to view and delete users(DELETE), log out if you haven't already and log in as admin@admin.com with password: admin1234<br><br> 



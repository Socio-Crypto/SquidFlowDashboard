# build_files.sh
pip install -r requirements.txt
python3.9 manage.py collectstatic
# pip uninstall textblob
# pip uninstall nltk
# python3.9 manage.py get_user_threads_based_date
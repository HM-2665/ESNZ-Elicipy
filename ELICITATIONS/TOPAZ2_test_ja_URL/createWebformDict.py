# Add login page requesting password
password_protected = False
encrypted = False

# select 'github', 'local' or 'local_github'
datarepo = 'local'

# Github repository for answers, used only when datarepo='github' or 'local_github'
RepositoryData = 'HM-2665/ESNZ-Elicipy'

# this can be 'seed' or 'target'
quest_type = 'seed'  # ※ target用のフォームの場合は 'target' にしてください

absolute_indexing = True
label_flag = True

pctls = [5, 50, 95]

confirmation_email = False

# if confirmation email is True and datarepo is 'local' or 'local_github'
# fill the following fields, if 'github' add to streamlit secrets
# SENDER_ADDRESS = ""
# SENDER_PASSWORD = ""
# SENDER_NAME = ""
# SMTP_SERVER_ADDRESS = ""
# PORT = 587
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

# メール送信機能の有効化
confirmation_email = False

# 送信元（メールサーバー）の設定
# SENDER_ADDRESS = "haruko-mishina@wjecnet.onmicrosoft.com"
# SENDER_PASSWORD = "LGgeekom37"
# SENDER_NAME = "事務局"
# SMTP_SERVER_ADDRESS = "[suspicious link removed]"
# PORT = 587
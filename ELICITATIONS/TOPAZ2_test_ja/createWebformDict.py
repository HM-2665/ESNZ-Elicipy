# Add login page requesting password
password_protected = False
encrypted = False

# select 'github', 'local' or 'local_github'
# datarepo = 'local'
datarepo = 'local_github'

# Github repository for answers, used only when datarepo='github'
# or 'local_github'
RepositoryData = 'test_answers'

# Parameters used only when datarepo='local' or 'local_github'
# user = ''
# github_token = ''

# this can be 'seed' or 'target'
quest_type = 'seed'

#group_list = [
#    'SG1 (Clermont)', 'SG2 (Quito)', 'SG3 (Geol.)', 'SG4 (MathMod)',
#    'SG5 (Junior)', 'SG6 (Senior)'
#]

# target_list = [2,3]
# seed_list = [1,2]
absolute_indexing = True

label_flag = True

pctls = [5, 50, 95]
# companion_document = ""
# supplementary_documents = [""]

confirmation_email = False

# if confirmation email is True and datarepo is 'local' or 'local_github'
# fill the following fields, if 'github' add to streamlit
# secrets

# SENDER_ADDRESS
# SENDER_PASSWORD
# SENDER_NAME
# SMTP_SERVER_ADDRESS
# PORT

# 差出人・送信元アカウント情報
# SENDER_NAME = "TOPAZ2 Elicitation Team"           # 差出人表示名
# SENDER_ADDRESS = "haruko-mishina@wjecnet.onmicrosoft.com"          # 送信元メールアドレス
# SENDER_PASSWORD = "GeekomLG37"              # パスワード（※アプリパスワード等）

# SMTPサーバー情報
# SMTP_SERVER_ADDRESS = "smtp.office365.com"        # SMTPサーバー名
# PORT = 587                                        # ポート番号（通常は587）


datarepo = 'local_github'
RepositoryData = "ESNZ-Elicipy"       # ご自身のGitHubリポジトリ名
github_token = "ghp_xxxxxxxxxxxx"     # GitHubのPersonal Access Token
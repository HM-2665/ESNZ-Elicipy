import os
import sys
from streamlit.web import cli as stcli


def run_streamlit():
  # 自分自身のファイル位置から streamlit_app.py の絶対パスを取得
  app_path = os.path.join(os.path.dirname(__file__), "streamlit_app.py")
  sys.argv = ["streamlit", "run", app_path] + sys.argv[1:]
  sys.exit(stcli.main())
import sys,os 

class BuildDir:
    """基準パスを取得し必要なパスを構成する"""

    def __init__(self):
        self.base_dir =  os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.dirname(self.base_dir)
        # frozen の場合は _internal/seed ディレクトリを使用
        self.static = os.path.join(self.base_dir, "static")
        self.templates = os.path.join(self.base_dir, "templates")
        self.database_uri = "sqlite:///test.db"
        
        

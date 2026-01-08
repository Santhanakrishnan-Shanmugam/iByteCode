import dataset

def getDB():
    return dataset.connect(
        "mysql+pymysql://root:12345@localhost/Learn"
    )

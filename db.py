import pymysql
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('db.cfg')

conn = pymysql.connect(
    host=config.get('db', 'host'), 
    port=config.getint('db', 'port'), 
    user=config.get('db', 'user'), 
    passwd=config.get('db', 'password'), 
    db=config.get('db', 'db'))

cur = conn.cursor()

def insertRecord(stats):
    query = """
    INSERT INTO repos 
    (user, name, url, git_url, watchers, forks, created, updated, commits, language, license)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    cur.execute(query, (
        stats['user'],
        stats['name'],
        stats['url'],
        stats['git_url'],
        str(stats['watchers']),
        str(stats['forks']),
        stats['created'].strftime('%Y-%m-%d %H:%M:%S'),
        stats['updated'].strftime('%Y-%m-%d %H:%M:%S'),
        str(stats['commits']),
        stats['language'],
        stats['license'])
    )

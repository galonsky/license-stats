import pymysql
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.cfg')

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
    (user, name, url, git_url, watchers, forks, created, updated, commits, language, license, license_type, collaborators, issues)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

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
        stats['license'],
        stats['license_type'],
        str(stats['collaborators']),
        str(stats['issues'])
    ))


def insertError(url, error):
    query = 'INSERT INTO repos (url, error) VALUES (%s, %s);'
    cur.execute(query, (url, error))


def getLicenses():
    query = 'SELECT id, license FROM repos WHERE license IS NOT NULL;';
    cur.execute(query)
    return cur.fetchall()


def updateType(id, licenseType):
    query = 'UPDATE repos SET license_type = %s WHERE id = %s'
    cur.execute(query, (licenseType, str(id)))


def getNoIssues():
    query = 'SELECT id, user, name FROM repos WHERE collaborators IS NULL AND issues IS NULL AND error IS NULL;'
    cur.execute(query)
    return cur.fetchall()


def getNoCollaborators():
    query = 'SELECT id, user, name FROM repos WHERE collaborators = 0 AND error IS NULL;'
    cur.execute(query)
    return cur.fetchall()


def updateNoIssue(id, issues, collabs):
    query = 'UPDATE repos SET issues = %s, collaborators = %s WHERE id = %s;'
    cur.execute(query, (issues, collabs, id))


def updateNoCollab(id, collabs):
    query = 'UPDATE repos SET collaborators = %s WHERE id = %s;'
    cur.execute(query, (collabs, id))

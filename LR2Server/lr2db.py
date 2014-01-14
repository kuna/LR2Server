import sqlite3
import os
import codecs, sys

dbList = {}
gradeList = {}
songCnt = 0
gradeCnt = 0

scoreList = {}
scoreCnt = 0

def loadDB(src):
	print "-------------------------------"
	print "Trying to open %s ..." % src
	print "-------------------------------"

	global songCnt
	global dbList
	global gradeList
	global gradeCnt

	conn = sqlite3.connect(src)
	cur = conn.cursor()

	#c = cur.execute("SELECT * FROM song ORDER BY parent")
	c = cur.execute("SELECT * FROM song")
	songCnt = 0

	for row in c:
		bmspath = os.path.split(row[7])[0]
		if (dbList.has_key(bmspath)):
			dbList[bmspath].append(row)
		else:
			dbList[bmspath] = [row]
			#try:
			#	print "hash %s, name %s" % (row[0], row[1].decode("utf-8").encode("shift_jis").decode("mbcs"))
			#except Exception, e:
			#	print "hash %s, name %s" % (row[0], row[1].decode("utf-8").encode("cp949").decode("mbcs"))

		songCnt += 1

	c = cur.execute("SELECT * FROM grade")
	gradeCnt = 0

	for row in c:
		gradeList[row[1]] = row[3][32:]
		gradeCnt += 1

	c.close()

	print "total sabun count: %d, total bms count: %d" % (songCnt, len(dbList.items()))


def loadScoreDB(src):
	print "-------------------------------"
	print "Trying to open %s ..." % src
	print "-------------------------------"

	global scoreList
	global scoreCnt

	conn = sqlite3.connect(src)
	cur = conn.cursor()

	c = cur.execute("SELECT * FROM score")
	scoreCnt = 0

	for row in c:
		scoreList[row[0]] = row
		scoreCnt += 1

	c.close();

	print "loaded score db"
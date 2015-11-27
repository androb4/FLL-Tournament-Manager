import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import thread
import time
import math
import xlrd

import match_schedule


class MatchListUploadHandler(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        book = xlrd.open_workbook(file_contents=fileinfo['body'])
        sheet = book.sheet_by_index(0)

        for t in range(2, len(sheet.row_values(1))):
            match_schedule.tableNames.append(sheet.row_values(1)[t])

        for r in range(2, sheet.nrows):
            match = match_schedule.Match()
            for t in range(2, len(sheet.row_values(r))):
                if sheet.row_values(r)[t] is not "":
                    match.matchNumber = int(sheet.row_values(r)[0])
                    match.teams.append(int(sheet.row_values(r)[t]))
                    match.tables.append(match_schedule.tableNames[t-2])
            match_schedule.matchList.append(match)

        for m in range(0, len(match_schedule.matchList)):
            print "Match" + str(match_schedule.matchList[m].matchNumber),
            for t in range(0, len(match_schedule.matchList[m].teams)):
                print " " + match_schedule.matchList[m].tables[t] + " " + str(match_schedule.matchList[m].teams[t]),
            print

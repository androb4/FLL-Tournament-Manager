import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import thread
import time
import math
import xlrd
import copy

import match_schedule

class AudioSource:
    DISPLAY_AUDIENCE, MATCH_CONTROL = range(2)

audioSource = AudioSource.DISPLAY_AUDIENCE

class MatchListUploadHandler(tornado.web.RequestHandler):
    def post(self):
        match_schedule.matchList = []
        fileinfo = self.request.files['filearg'][0]
        book = xlrd.open_workbook(file_contents=fileinfo['body'])
        sheet = book.sheet_by_index(0)

        for t in range(2, len(sheet.row_values(1))):
            match_schedule.tableNames.append(sheet.row_values(1)[t])

        for r in range(2, sheet.nrows):
            match = copy.deepcopy(match_schedule.Match)
            for t in range(2, len(sheet.row_values(r))):
                if sheet.row_values(r)[t] is not "":
                    match['matchNumber'] = int(sheet.row_values(r)[0])
                    match['matchTime'] = sheet.row_values(r)[1]
                    match['teams'].append(int(sheet.row_values(r)[t]))
                    match['tables'].append(match_schedule.tableNames[t-2])
            match_schedule.matchList.append(match)

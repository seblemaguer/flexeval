# Import Libraries
import random
import string

from flask import Blueprint, send_from_directory, abort

import core.utils as utils

class Assets():

    def __init__(self):
        self.table = {}
        utils.app.add_url_rule('/assets/<path:lpath>','assets',self.get)
        utils.app.add_url_rule('/assets:obfuscation/<key>','assets:secure',self.retrieve)
        utils.reserved_name.append("assets")

    def obfuscate(self,url):
        base = 'assets/'
        key = ''.join((random.choice(string.ascii_lowercase) for i in range(256)))
        print(url)
        self.table[key] = url[len(base):]
        return '/assets:obfuscation/'+key

    def retrieve(self,key):
        try:
            lpath = self.table[key]
            del self.table[key]
            return self.get(lpath),200,{"Cache-Control": "no-cache"}
        except Exception as e:
            abort(410)

    def get(self,lpath):

        try:
            lpath = lpath.split("/")

            file = lpath[len(lpath)-1]
            lpath = lpath[:len(lpath)-1]

            path = ""

            assert not(file == "." or file == ".." or file == "~" or file == "__pycache__")

            for _path in lpath:
                assert not(_path == "." or _path == ".." or _path == "~" or _path == "__pycache__")

                path = path + "/" + _path

            try:
                try:
                    return send_from_directory(utils.NAME_REP_CONFIG+"/systems/public"+path,file)
                except Exception as e:
                    return send_from_directory(utils.NAME_REP_CONFIG+"/assets"+path,file)
            except Exception as e:
                return send_from_directory(utils.ROOT+"/core/assets"+path, file)

        except Exception as e:
            abort(404)

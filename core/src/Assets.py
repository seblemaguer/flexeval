# Import Libraries
import random
import string

from flask import Blueprint, send_from_directory, abort

import core.utils as utils

class Assets():

    def __init__(self,prefix):
        self.prefix = prefix
        self.table = {}
        utils.app.add_url_rule(self.prefix+'/<path:lpath>','assets',self.get)
        utils.app.add_url_rule(self.prefix+':obfuscation/<key>','assets:secure',self.retrieve)

    def obfuscate(self,url):
        base = self.prefix+'/'
        key = ''.join((random.choice(string.ascii_lowercase) for i in range(256)))

        self.table[key] = url[len(base):]
        return self.prefix+':obfuscation/'+key

    def retrieve(self,key):
        lpath = self.table[key]
        del self.table[key]
        return self.get(lpath)

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

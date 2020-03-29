# Import Libraries
import random
import string

from flask import Blueprint, send_from_directory, abort

import core.utils as utils

class Assets():

    def __init__(self):
        self.table = {}
        utils.app.add_url_rule('/assets/<path:lpath>','assets',self.get)
        utils.app.add_url_rule('/oassets/<key>','assets:secure',self.retrieve)
        utils.reserved_name.append("assets")
        utils.reserved_name.append("ossets")

    def obfuscate(self,url):
        key = ''.join((random.choice(string.ascii_lowercase) for i in range(20)))

        url_block = url.split(".")
        if(len(url_block) > 0):
            key = key + "." + url_block[len(url_block) - 1]

        self.table[key] = url
        return utils.make_url('/oassets/'+key)

    def retrieve(self,key):
        try:
            lpath = self.table[key]
            #del self.table[key]
            return self.get(lpath)
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

# coding: utf8
# license : CeCILL-C

from flask import abort,current_app,send_from_directory

from flexeval.core import ProviderFactory

class AssetsProviderError(Exception):
    pass

class UnknowSourceError(AssetsProviderError):

    def __init__(self,path,_from):
        self.path = path
        self._from = _from

def decode(path):
    try:
        repositories = path.split("/")
        file = repositories[len(repositories)-1]
        repositories = repositories[:len(repositories)-1]

        assert not(file == "." or file == ".." or file == "~" or file == "__pycache__")

        for repository in repositories:
            assert not(repository == "." or repository == ".." or repository == "~" or repository == "__pycache__")

        return repositories,file

    except Exception as e:
        abort(403)

def generate_path(repositories):

    path = ""
    for repository in repositories:
        path = path + "/" + repository

    return path


class AssetsProvider():

    def __init__(self,url_prefix):
        self.url_prefix = url_prefix
        current_app.add_url_rule(self.url_prefix+'/<path:path>',self.__class__.__name__+':assets:'+url_prefix,self.get_content)
        ProviderFactory().set("assets",self)
        print(" * AssetsProvider:"+self.__class__.__name__+" loaded and bound to: "+self.url_prefix)


    def local_url(self,path,_from=None):

        if not(path[0] == "/"):
            path = "/"+path

        if _from is None:
            return self.url_instance(path)
        elif _from == "flexeval":
            return self.url_flexeval(path)
        elif _from[:3] == "mod":
            return self.url_mod(_from[4:],path)
        else:
            raise UnknowSourceError(path,_from)

    def url_flexeval(self,path):
        return self.url_prefix+"/flexeval"+path

    def url_mod(self,name_mod,path):
        return self.url_prefix+"/flexeval/mods/"+name_mod+path

    def url_instance(self,path):
        return self.url_prefix+path

    def get_content(self,path):

        repositories,file = decode(path)

        try:
            try:
                return send_from_directory(current_app.config["FLEXEVAL_INSTANCE_DIR"]+"/assets/"+generate_path(repositories),file)
            except Exception as e:
                if repositories[0] == "flexeval":
                    try:
                        return send_from_directory(current_app.config["FLEXEVAL_DIR"]+"/assets/"+generate_path(repositories[1:]),file)
                    except Exception as e:
                        if repositories[1] == "mods":
                            return send_from_directory(current_app.config["FLEXEVAL_DIR"]+"/mods/"+repositories[2]+"/assets/"+generate_path(repositories[3:]),file)
                        else:
                            abort(404)
                else:
                    abort(404)
        except Exception as e:
            abort(404)

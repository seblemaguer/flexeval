# Import Libraries
import os
import importlib

from flask import Blueprint,request,redirect,session, abort

from core.utils import config, render_template, safe_copy_rep, ROOT, NAME_REP_CONFIG, app

# Initialize
bp = Blueprint('admin', __name__)
tiles = []

def secure_mod():

    if "admin_password" in request.form:
        session["admin_password"] = request.form["admin_password"]

    if "admin_password" in session:
        if not(session["admin_password"] == config["admin"]["password"]):
            abort(403)
    else:
        abort(403)

# Enable admin/mod
for admin_mod_name in os.listdir(ROOT+"/core/admin/mods"):
    try:
        lib_imported = importlib.import_module("core.admin.mods."+admin_mod_name)
        lib_imported.bp.before_request(secure_mod)
        safe_copy_rep(ROOT+"/core/admin/mods/"+admin_mod_name+"/templates",NAME_REP_CONFIG+"/.tmp/templates/admin/"+admin_mod_name)
        app.register_blueprint(lib_imported.bp,url_prefix='/admin/'+admin_mod_name) # Register Blueprint
        tiles.append({"title":lib_imported.TITLE,"description":lib_imported.DESCRIPTION,"link":"./"+admin_mod_name})

    except Exception as e:
        print("ADMIN MOD : "+admin_mod_name+" can't be initialized.")
        print("MSG ERROR: "+str(e))


# Enable the authentification
@bp.before_request
def secure():

    if "admin_password" in request.form:
        session["admin_password"] = request.form["admin_password"]

    if "admin_password" in session:
        if not(session["admin_password"] == config["admin"]["password"]):
            del session["admin_password"]
            abort(403)
    else:
        return render_template("admin/auth.tpl")

# Routes
@bp.route('/',methods=["GET","POST"])
def panel():
    return render_template("admin/panel.tpl",tiles=tiles)

@bp.route('/deco',methods=["GET","POST"])
def deco():
    del session["admin_password"]
    return redirect("./")

# Import Libraries
from flask import Blueprint,request,redirect,session,abort
from flask_mail import Mail,Message

from core.mods.auth_by_invitation.model.User import User as mUser
from core.src.providers.AuthProvider import LoginAuthProvider
from core.utils import db,config,get_provider,set_provider,render_template,app,public_url, make_url
from core.src.Module import AdminModule


mail = Mail()
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'infooveriq@gmail.com'  # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = 'infooveriq@gmail.com' # enter your email here
app.config['MAIL_PASSWORD'] = 'password' # enter your password here

with AdminModule('auth_by_invitation:admin',__name__,title="Member",description="Send invitation to people to join your website. ") as ap:

    # Routes
    @ap.route('/')
    def panel():
        return render_template("auth_by_invitation/admin/panel.tpl")

    @ap.route('/email-param')
    def emailparam():
        config={}

        falseCredential = False
        if request.args.get("falseCredential") is not None:
            falseCredential = True

        config['MAIL_SERVER'] = app.config['MAIL_SERVER']
        config['MAIL_PORT'] = app.config['MAIL_PORT']
        config['MAIL_USE_TLS'] = app.config['MAIL_USE_TLS']
        config['MAIL_USERNAME'] = app.config['MAIL_USERNAME']
        config['MAIL_PASSWORD'] = app.config['MAIL_PASSWORD']

        return render_template("auth_by_invitation/admin/config.tpl",config=config,falseCredential=falseCredential)


    @ap.route('/email-param/register', methods=["POST"])
    def emailparam_register():
        app.config['MAIL_SERVER'] = request.form['MAIL_SERVER']
        app.config['MAIL_PORT'] = request.form['MAIL_PORT']
        app.config['MAIL_USE_TLS'] = request.form['MAIL_USE_TLS']
        app.config['MAIL_USERNAME'] = request.form['MAIL_USERNAME']
        app.config['MAIL_DEFAULT_SENDER'] = request.form['MAIL_USERNAME']
        app.config['MAIL_PASSWORD'] = request.form['MAIL_PASSWORD']

        mail.init_app(app)

        return redirect(make_url("/admin/auth_by_invitation"))

    @ap.route('/invite')
    def send():
        return render_template("auth_by_invitation/admin/send.tpl",public_url=public_url)

    @ap.route('/invite-register',methods=["POST"])
    def inviteregister():
        try:
            emails = request.form["emails"].split(",")
            message = "<html><body><p>"+request.form["message"].replace("\n","</p><p>")+"</p>"
            title_message = request.form["title_message"]
            for email in emails:
                bdd_mistake = False
                try:
                    user = mUser(email)
                    message = message + "<p><a href='" + public_url +'/?token='+str(user.token) + "'>"+public_url+"/?token=.... </a></p></body></html>"
                    print(message)
                    db.session.add(user)
                    db.session.commit()

                except Exception as e:
                    print(e)
                    bdd_mistake = True

                if not(bdd_mistake):
                    msg = Message(title_message,recipients=[email])
                    msg.html = message
                    mail.send(msg)

            return redirect('./pending-invitation')


        except Exception as e:
            print(e)
            return redirect('./email-param?falseCredential')

    @ap.route('/pending-invitation')
    def pendinginvitation():
        users = mUser.query.all()
        return render_template("auth_by_invitation/admin/pending.tpl",public_url=public_url,users=users)

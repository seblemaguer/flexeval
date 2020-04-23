# coding: utf8
import json

from flask import current_app

from perceval.utils import AppSingleton
from .Provider import Provider


class LegalTerms(metaclass=AppSingleton):

    def __init__(self):

        self.legal_terms = {"EULA":None,"GDPR":None}
        self.is_GDPR_Compliant = False

        print(" * Legal information are collected from the following file:"+current_app.config["PERCEVAL_INSTANCE_DIR"]+'/legal.json')

        try:
            with open(current_app.config["PERCEVAL_INSTANCE_DIR"]+'/legal.json',encoding='utf-8') as config:
                self.legal_terms = json.load(config)
        except FileNotFoundError as e:
            print("   WARNING: The legal file is missing")
        except Exception as e:
            print("   WARNING: Error in the legal file")
            print("   Details: "+str(e))

        self.minimal_GDPR_Compliance()

        if not(self.is_GDPR_Compliant):
            print("   [LEGAL ISSUE] For any data collection from this website, please fix the warning(s), to ensure GDPR compliance.")

        current_app.add_url_rule('/legal_terms','legal_terms',self.page)

    def minimal_GDPR_Compliance(self):
        if not(self.legal_terms["GDPR"] is None):
            GDPR = self.legal_terms["GDPR"]
            self.is_GDPR_Compliant = True

            if GDPR["data_controller"]["identity"] is None:
                print("   WARNING: Missing data_controller:identity in your legal file.")
                self.is_GDPR_Compliant = False

            if GDPR["data_controller"]["contact"]["email"] is None and GDPR["data_controller"]["contact"]["other"] is None:
                print("   WARNING: Missing data_controller:contact:email and  data_controller:contact:other in your legal file.")
                print("    -> Complete at least one of the two fields.")
                self.is_GDPR_Compliant = False

            if GDPR["data_collection"]["purpose"] is None:
                print("   WARNING: Missing data_collection:purpose in your legal file.")
                self.is_GDPR_Compliant = False

            if GDPR["data_conservation"]["duration"] is None and GDPR["data_conservation"]["criterions_duration"] is None:
                print("   WARNING: Missing data_conservation:duration and data_conservation:criterions_duration in your legal file.")
                print("    -> Complete at least one of the two fields.")
                self.is_GDPR_Compliant = False

            if GDPR["data_protection_officer"]["identity"] is None:
                print("   WARNING: Missing data_protection_officer:identity in your legal file.")
                self.is_GDPR_Compliant = False

            if GDPR["data_protection_officer"]["contact"]["email"] is None and GDPR["data_protection_officer"]["contact"]["phone_number"] is None and GDPR["data_protection_officer"]["contact"]["other"] is None:
                print("   WARNING: Missing data_protection_officer:contact:email and data_protection_officer:contact:phone_number and data_protection_officer:contact:other in your legal file.")
                print("    -> Complete at least one of the three fields.")
                self.is_GDPR_Compliant = False



    def page(self):
        from .Module import Module
        from .Config import Config

        EULA  = self.legal_terms["EULA"]
        GDPR = self.legal_terms["GDPR"]

        return Module.render_template(Provider().get("templates").get("/legal.tpl","perceval"),parameters={"EULA":EULA,"GDPR":GDPR},args={"len":len})

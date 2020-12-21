# coding: utf8
# license : CeCILL-C

# Global
import os
import logging

# Yaml
from yaml import load, dump

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Flask
from flask import current_app
from flask import session as flask_session

# Flexeval
from flexeval.utils import AppSingleton, make_global_url, redirect
from flexeval.core import ProviderFactory, Module, Config


LEGAL_CONFIGURATION_BASENAME = "legal"


class LegalTermNotCheckError(Exception):
    pass


class LegalTerms(metaclass=AppSingleton):
    def __init__(self, next_url=None):
        self._logger = logging.getLogger(self.__class__.__name__)

        self.legal_terms = {"GCU": None, "GDPR": None}
        self.is_GDPR_Compliant = False
        self.next_url = next_url

        self._logger.info(
            " * Legal information are collected from the following file:"
            + current_app.config["FLEXEVAL_INSTANCE_DIR"]
            + "%s.yaml" % LEGAL_CONFIGURATION_BASENAME
        )

        try:
            with open(
                os.path.join(
                    current_app.config["FLEXEVAL_INSTANCE_DIR"],
                    "%s.yaml" % LEGAL_CONFIGURATION_BASENAME,
                ),
                encoding="utf-8",
            ) as config_stream:
                self.legal_terms = load(config_stream, Loader=Loader)
        except FileNotFoundError as e:
            self._logger.warning("The legal file is missing")
        except Exception as e:
            self._logger.warning("Error in the legal file")
            self._logger.warning("Details: " + str(e))

        self.minimal_GDPR_Compliance()

        if not (self.is_GDPR_Compliant):
            self._logger.error(
                "[LEGAL ISSUE] For any data collection from this website, please fix the warning(s), to ensure GDPR compliance."
            )

        current_app.add_url_rule("/legal_terms", "legal_terms", self.page)
        current_app.add_url_rule(
            "/legal_terms/ok",
            "validate_legal_terms",
            self.validate_legal_terms,
            methods=["POST"],
        )

    def minimal_GDPR_Compliance(self):
        if not (self.legal_terms["GDPR"] is None):
            GDPR = self.legal_terms["GDPR"]
            self.is_GDPR_Compliant = True

            if GDPR["data_controller"]["identity"] is None:
                self._logger.warning(
                    "Missing data_controller:identity in your legal file."
                )
                self.is_GDPR_Compliant = False

            if (
                GDPR["data_controller"]["contact"]["email"] is None
                and GDPR["data_controller"]["contact"]["other"] is None
            ):
                self._logger.warning(
                    "Missing data_controller:contact:email and  data_controller:contact:other in your legal file."
                )
                self._logger.warning("Complete at least one of the two fields.")
                self.is_GDPR_Compliant = False

            if GDPR["data_collection"]["purpose"] is None:
                self._logger.warning("Missing data_collection:purpose in your legal file.")
                self.is_GDPR_Compliant = False

            if (
                GDPR["data_conservation"]["duration"] is None
                and GDPR["data_conservation"]["criterions_duration"] is None
            ):
                self._logger.warning(
                    "Missing data_conservation:duration and data_conservation:criterions_duration in your legal file."
                )
                self._logger.warning("-> Complete at least one of the two fields.")
                self.is_GDPR_Compliant = False

            if GDPR["data_protection_officer"]["identity"] is None:
                self._logger.warning(
                    "Missing data_protection_officer:identity in your legal file."
                )
                self.is_GDPR_Compliant = False

            if (
                GDPR["data_protection_officer"]["contact"]["email"] is None
                and GDPR["data_protection_officer"]["contact"]["phone_number"] is None
                and GDPR["data_protection_officer"]["contact"]["other"] is None
            ):
                self._logger.warning(
                    "Missing data_protection_officer:contact:email and data_protection_officer:contact:phone_number and data_protection_officer:contact:other in your legal file."
                )
                self._logger.warning("-> Complete at least one of the three fields.")
                self.is_GDPR_Compliant = False

    def page(self):
        return self.page_with_validation_required(self.next_url)

    def page_with_validation_required(self, validate_next_local_url=None):

        GCU = self.legal_terms["GCU"]
        GDPR = self.legal_terms["GDPR"]

        parameters = {"GCU": GCU, "GDPR": GDPR}

        if validate_next_local_url is not None:
            parameters["validate"] = True
            self.session["validate_next_local_url"] = validate_next_local_url

        return Module.render_template(
            ProviderFactory().get("templates").get("/legal.tpl"),
            parameters=parameters,
            args={"len": len},
        )

    def validate_legal_terms(self):
        self.session["validate_by_user"] = True
        return redirect(self.session["validate_next_local_url"])

    def user_has_validate(self):
        if "validate_by_user" in self.session:
            pass
        else:
            raise LegalTermNotCheckError()

    @property
    def session(self):
        if "legalterms" not in flask_session.keys():
            flask_session["legalterms"] = {}

        return flask_session["legalterms"]

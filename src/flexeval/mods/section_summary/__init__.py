# coding: utf8

import logging

# Flexeval
from flexeval.core import campaign_instance
from flexeval.mods.test import test_manager

logger = logging.getLogger()

with campaign_instance.register_stage_module(__name__) as sm:

    @sm.route("/", methods=["GET"])
    @sm.valid_connection_required
    def main():
        """Entry point for the Test

        This function prepare the template and defines some key helper
        internal functions to generate the information required during
        the save stage. These functions are:
          - get_syssamples which provides the list of selected samples per *given system*
          - save_field_name which *has to be called* to get the field value (score, preference selection...)
            during the saving

        """

        # Get the current Stage and the corresponding test
        summary_stage = sm.current_stage
        next_urls: dict[str, str] = summary_stage.next_local_urls

        # Get the user
        user = sm.auth_provider.user

        stages = campaign_instance.get_stage_graph().list_stages()
        list_test_sections = []
        section_information = dict()
        for k, stage in stages.items():
            if stage.get_module_name() == "test":
                # Force the registering of the test
                if not test_manager.has(stage.name):
                    test = test_manager.register(stage.name, stage)
                else:
                    test = test_manager.get(stage.name)

                # Retrieve the information
                max_steps = int(stage["nb_steps"])  # TODO: add a default if ("nb_steps" in stage) else 0
                cur_step = test.nb_steps_complete_by(user)

                # Generate the required parameters for the template
                section_information[stage.name] = {
                    "label": stage["label"] if "label" in stage else stage.name,
                    "url": next_urls[stage.name],
                    "cur_step": cur_step,
                    "max_steps": max_steps,
                }
                list_test_sections.append(stage.name)
            else:
                logger.debug(f"ignore {k} because {stage.get_module_name()}")

        parameters = {"list_test_sections": list_test_sections, "section_information": section_information}

        # Complete the parameters with additional config
        for k in summary_stage.keys():
            if (k not in parameters) and (k.lower() != "template"):
                parameters[k] = summary_stage.get(k)

        return sm.render_template(path_template=summary_stage.template, parameters=parameters)

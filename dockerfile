FROM odoo:14.0

USER root

# Define python library here
RUN pip3 install pyjwt
RUN pip3 install requests-cache

USER odoo
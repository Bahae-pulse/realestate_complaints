FROM odoo:17.0

USER root

# Create necessary directories and set permissions
RUN mkdir -p /var/lib/odoo/.local/share/Odoo/filestore && \
    chown -R odoo:odoo /var/lib/odoo/.local/share/Odoo

RUN mkdir -p /var/lib/odoo/.local/share/Odoo/sessions && \
    chown -R odoo:odoo /var/lib/odoo/.local/share/Odoo/sessions

USER odoo

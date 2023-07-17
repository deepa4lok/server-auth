# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Keycloak auth integration",
    "summary": "Integrate Keycloak into your SSO",
    "version": "14.0.1.0.3",
    'category': 'Tools',
    "website": "https://github.com/OCA/server-auth",
    'author': 'Camptocamp, Odoo Community Association (OCA), The Open Source Company (TOSC)',
    "license": "AGPL-3",
    "depends": [
        "auth_oauth",
    ],
    "data": [
        "security/ir.model.access.csv",
        'data/auth_oauth_provider.xml',
        'wizard/keycloak_sync_wiz.xml',
        'wizard/keycloak_create_wiz.xml',
        'views/auth_oauth_views.xml',
        'views/res_users_views.xml',
    ],
}

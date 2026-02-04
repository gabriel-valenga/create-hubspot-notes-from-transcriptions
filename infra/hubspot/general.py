from utils.aws.ssm.parameter_store import parameter_store

HUBSPOT_CRM_API_BASE_URL = 'https://api.hubapi.com/crm/v3/objects/'
HUBSPOT_INTEGRATION_PRIVATE_APP_KEY = parameter_store.get_parameter('HUBSPOT_INTEGRATION_PRIVATE_APP_KEY')
HUBSPOT_CRM_API_HEADERS = {
    'Authorization': f'Bearer {HUBSPOT_INTEGRATION_PRIVATE_APP_KEY}',
    'Content-Type': 'application/json'
}
HUBSPOT_INTEGRATION_OWNER_ID = parameter_store.get_parameter('HUBSPOT_INTEGRATION_OWNER_ID')
HUBSPOT_ASSOCIATION_TYPE_NOTE_TO_CONTACT = '202'

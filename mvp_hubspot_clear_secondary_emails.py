import os
import requests
import time

from infra.hubspot.contacts import HubspotContacts

BASE_URL = "https://api.hubapi.com"
TOKEN = os.getenv("HUBSPOT_INTEGRATION_PRIVATE_APP_KEY")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def search_contacts_with_secondary(after=None):
    body = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "hs_additional_emails",
                        "operator": "HAS_PROPERTY"
                    }
                ]
            }
        ],
        "properties": ["email", "hs_additional_emails"],
        "limit": 100
    }

    if after:
        body["after"] = after

    response = requests.post(
        f"{BASE_URL}/crm/v3/objects/contacts/search",
        headers=HEADERS,
        json=body
    )

    response.raise_for_status()
    return response.json()


def batch_clear_secondary(contact_ids):
    updates = [
        {
            "id": cid,
            "properties": {
                "hs_additional_emails": ""
            }
        }
        for cid in contact_ids
    ]

    for i in range(0, len(updates), 100):
        chunk = updates[i:i+100]

        response = requests.post(
            f"{BASE_URL}/crm/v3/objects/contacts/batch/update",
            headers=HEADERS,
            json={"inputs": chunk}
        )

        response.raise_for_status()
        print(f"Cleaned {len(chunk)} contacts")


def main():
    after = None
    total_processed = 0

    while True:
        data = search_contacts_with_secondary(after)
        results = data.get("results", [])

        if not results:
            break

        contact_ids = [
            contact["id"]
            for contact in results
            if contact["properties"].get("hs_additional_emails")
        ]

        if contact_ids:
            batch_clear_secondary(contact_ids)
            total_processed += len(contact_ids)

        paging = data.get("paging")
        if paging and "next" in paging:
            after = paging["next"]["after"]
            time.sleep(0.2)  # handling rate limits
        else:
            break

    print(f"Number of processed contacts: {total_processed}")


def test_create_contact():
    hubspot_contacts = HubspotContacts()
    email='testad@test1.com'
    hubspot_contacts.create_hubspot_contact(email=email)


if __name__ == "__main__":
    main()
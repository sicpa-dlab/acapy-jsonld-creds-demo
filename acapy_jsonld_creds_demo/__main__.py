"""Run the demo."""

from datetime import date
import json
import os
import time
import uuid

from acapy_client import Client
from acapy_client.api.connection import create_invitation, receive_invitation
from acapy_client.api.credentials import get_w3c_credentials
from acapy_client.api.issue_credential_v20 import (
    issue_credential_automated as issue_credential_v20_automated,
)
from acapy_client.api.present_proof_v20 import (
    send_request_free as send_proof_request,
    get_records as get_proof_records,
)
from acapy_client.api.wallet import create_did
from acapy_client.models import (
    CreateInvitationRequest,
    ReceiveInvitationRequest,
    V20CredSendRequest,
    DIDCreate,
    DIDCreateMethod,
    LDProofVCDetail,
    V20CredFilter,
    W3CCredentialsListRequest,
    V20PresSendRequestRequest,
)
from acapy_client.models.did import DID
from acapy_client.models.dif_options import DIFOptions
from acapy_client.models.dif_proof_request import DIFProofRequest
from acapy_client.models.presentation_definition import PresentationDefinition
from acapy_client.models.v20_pres_request_by_format import V20PresRequestByFormat


HOLDER_URL = os.environ.get("HOLDER", "http://localhost:3001")
ISSUER_URL = os.environ.get("ISSUER", "http://localhost:3003")


def describe(description: str, api):
    def _describe(**kwargs):
        print(description)
        request = api._get_kwargs(**kwargs)
        print("Request:", json.dumps(request, indent=2))
        result = api.sync_detailed(**kwargs)
        if not result.parsed:
            raise Exception("Request failed: {}".format(repr(result)))
        print("Response:", json.dumps(result.parsed.to_dict(), indent=2))
        return result.parsed

    return _describe


def main():
    """Run steps."""
    holder = Client(base_url=HOLDER_URL)
    issuer = Client(base_url=ISSUER_URL)

    # Establish Connection {{{
    holder_conn_record = describe("Create new invitation in holder", create_invitation)(
        client=holder, json_body=CreateInvitationRequest(), auto_accept="true"
    )

    issuer_conn_record = describe("Receive invitation in issuer", receive_invitation)(
        client=issuer,
        json_body=ReceiveInvitationRequest.from_dict(
            holder_conn_record.invitation.to_dict()
        ),
    )
    # }}}

    # Prepare signing and subject DIDs {{{
    did_info: DID = describe("Create new DID for issuing", create_did)(
        client=issuer, json_body=DIDCreate(method=DIDCreateMethod.KEY)
    ).result
    subject_did: DID = describe("Create new DID for use as credential subject", create_did)(
        client=holder, json_body=DIDCreate(method=DIDCreateMethod.KEY)
    ).result
    # }}}

    print("Pausing to allow connection to finish...")
    time.sleep(1)

    # Issue Credential v2 {{{
    describe("Issue Credential v2 to holder", issue_credential_v20_automated)(
        client=issuer,
        json_body=V20CredSendRequest(
            connection_id=issuer_conn_record.connection_id,
            auto_remove=False,
            comment="nothing",
            filter_=V20CredFilter(
                ld_proof=LDProofVCDetail.from_dict(
                    {
                        "credential": {
                            "@context": [
                                "https://www.w3.org/2018/credentials/v1",
                                "https://w3id.org/citizenship/v1",
                            ],
                            "type": [
                                "VerifiableCredential",
                                "PermanentResidentCard"
                            ],
                            "issuer": {
                                "id": did_info.did,
                                "name": "Issuer"
                            },
                            "issuanceDate": str(date.today()),
                            "credentialSubject": {
                                "id": subject_did.did,
                                "familyName": "Smith",
                                "givenName": "Bob",
                                "birthDate": "2020-01-01",
                                "type": [
                                    "PermanentResident",
                                    "Person"
                                ]
                            },
                            "proof": {
                                "type": "CAdESRSASignature2020",
                                "created": "2021-07-08T10:55:33Z",
                                "verificationMethod": "did:sov:staging:BJX4adKceDv9D4qmztEN3F#MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAziPjJZebqdAhKZI0zUqd7439PGAlGY/MEIYl/hd0f3paG6UNcnQr74mzkOsJblSTcfzWCPefqWDQ1L/jQ0Iz1gR47I5l+sW7bBRivs1iWON6bcRXuitmVXFJPTl+R6x5vcEcOYlrKq0Fo9fEgbHb5i7Hjl0nWSOLcFsFkgSXfgmv3eI4uYlQyqs6qyICpApcWrijjIRlBlhsbv6Oz0Z8yi0v8FvgEy7Dq40yIoY3IWEGB8GNgi/E3lnLSRsGvzTWT5SXuurSzxrArh2okcNwtAt9DRF3VtMBO701zC2rfI65VyoIKX4QvctGiLSNOSYajDJ9Jg6GjnlE/US0Z6hyDwIDAQAB",
                                "proofPurpose": "myAssertionMethod",
                                "cades": "-----BEGIN PKCS7-----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-----END PKCS7-----"
                            }
                        },
                        "options": {
                            "proofType": "Ed25519Signature2018",
                        },
                    }
                )
            ),
        ),
    )
    # }}}

    print("Pausing to allow credential exchange to occur...")
    time.sleep(2)
    describe("Holder retrieve and display JSON-LD credentials", get_w3c_credentials)(
        client=holder, json_body=W3CCredentialsListRequest()
    )

    # Request Proof v2 {{{
    field_id = str(uuid.uuid4())
    describe("Request proof v2 from holder", send_proof_request)(
        client=issuer,
        json_body=V20PresSendRequestRequest(
            connection_id=issuer_conn_record.connection_id,
            presentation_request=V20PresRequestByFormat(
                dif=DIFProofRequest(
                    presentation_definition=PresentationDefinition.from_dict(
                        {
                            "format": {
                                "ldp_vp": {"proof_type": ["Ed25519Signature2018"]}
                            },
                            "input_descriptors": [
                                {
                                    "id": "input_1",
                                    "name": "Verify Person",
                                    "schema": [
                                        {
                                            "uri": "https://www.w3.org/2018/credentials#VerifiableCredential"
                                        }
                                    ],
                                    "constraints": {
                                        "fields": [
                                            {
                                                "id": field_id,
                                                "path": [
                                                    "$.issuer.id"
                                                ],
                                                "filter": {
                                                    "const": did_info.did
                                                }
                                            }
                                        ],
                                        "is_holder": [
                                            {
                                                "field_id": [field_id],
                                                "directive": "required"
                                            }
                                        ]
                                    }
                                }
                            ]
                        },
                    ),
                    options=DIFOptions(
                        challenge=str(uuid.uuid4()), domain="test-degree"
                    ),
                ),
            ),
        )
    )
    print("Pausing to allow presentation exchange to occur...")
    time.sleep(2)
    describe("List presentations on verifier", get_proof_records)(client=issuer)
    # }}}


if __name__ == "__main__":
    main()

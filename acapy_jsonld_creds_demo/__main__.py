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

    # Prepare signing DID {{{
    did_info = describe("Create new DID for issuing", create_did)(
        client=issuer, json_body=DIDCreate(method=DIDCreateMethod.KEY)
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
                                "https://www.w3.org/2018/credentials/examples/v1",
                            ],
                            "type": [
                                "VerifiableCredential",
                                "UniversityDegreeCredential",
                            ],
                            "issuer": did_info.did,
                            "issuanceDate": str(date.today()),
                            "credentialSubject": {
                                "degree": {
                                    "type": "BachelorDegree",
                                    "name": "Bachelor of Science and Arts",
                                }
                            },
                        },
                        "options": {"proofType": "Ed25519Signature2018"},
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
    describe("Request proof v2 from holder", send_proof_request)(
        client=issuer,
        json_body=V20PresSendRequestRequest(
            connection_id=issuer_conn_record.connection_id,
            presentation_request=V20PresRequestByFormat(
                dif=DIFProofRequest(
                    presentation_definition=PresentationDefinition.from_dict(
                        {
                            "id": "32f54163-7166-48f1-93d8-ff217bdb0654",
                            "format": {
                                "ldp_vp": {"proof_type": ["Ed25519Signature2018"]}
                            },
                            "input_descriptors": [
                                {
                                    "id": "degree_input_1",
                                    "name": "Degree",
                                    "schema": [
                                        {
                                            "uri": "https://www.w3.org/2018/credentials#VerifiableCredential"  # noqa: E501
                                        },
                                        {
                                            "uri": "https://www.w3.org/2018/credentials/examples/v1#UniversityDegreeCredential",  # noqa: E501
                                        },
                                    ],
                                    "constraints": {
                                        "fields": [
                                            {
                                                "path": ["$.issuer"],
                                                "filter": {"const": did_info.did},
                                            },
                                        ],
                                    },
                                }
                            ],
                        }
                    ),
                    options=DIFOptions(
                        challenge=str(uuid.uuid4()), domain="test-degree"
                    ),
                )
            ),
        ),
    )
    print("Pausing to allow presentation exchange to occur...")
    time.sleep(2)
    describe("List presentations on verifier", get_proof_records)(client=issuer)
    # }}}


if __name__ == "__main__":
    main()
